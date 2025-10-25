import asyncio
import io
import torch
import numpy as np
from TTS.api import TTS
from pathlib import Path
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor
import time
import wave

from app.utils.gts_manager import parse_emotion_text
from app.utils.hashing import get_hash

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = BASE_DIR / "data/samples"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

class TTSEngine:
    def __init__(self, model_name: str, use_cuda: bool = True, workers: int = 4) -> None:
        start = time.time()
        self.device = "cuda" if use_cuda and torch.cuda.is_available() else "cpu"
        self.tts = TTS(model_name=model_name, progress_bar=False)
        self.tts.to(self.device)
        
        self.executor = ThreadPoolExecutor(max_workers=workers)
        self.samples_dir = SAMPLES_DIR
        self.output_dir = OUTPUT_DIR
        
        print(f"🚀 Инициализация TTS [{self.device}]... ✅ ({round(time.time() - start, 2)}s)")
        
    def _generate_fragment(self, text: str, emotion: str, hashing: bool) -> Path:
        fragment_key = f"{emotion}-{text}"
        output_name = get_hash(fragment_key) if hashing else fragment_key
        output_path = self.output_dir / f"{output_name}.wav"

        if output_path.exists():
            print(f"⚡ Уже есть в кэше: {output_path.name}")
            return output_path

        sample = self.samples_dir / f"{emotion}_sample.wav"
        return self._tts_with_fallback(text, sample, output_path)
    
    def _tts_with_fallback(self, text: str, sample_wav: Path, output_path: Path) -> Path:
        try:
            start = time.time()
            self.tts.tts_to_file(
                text=text,
                speaker_wav=str(sample_wav),
                file_path=str(output_path),
                language="ru"
            )
            print(f"🎧 [{self.device}] → {output_path.name} ({round(time.time() - start, 2)}s)")
            return output_path

        except Exception as e:
            if self.device == "cuda":
                print(f"⚠ Ошибка CUDA: {e} → переключаюсь на CPU")
                self.device = "cpu"
                self.tts = TTS(model_name=self.tts.model_name, progress_bar=False)
                self.tts.to("cpu")
                return self._tts_with_fallback(text, sample_wav, output_path)
            raise
    
    async def generate_fragment_async(self, text: str, emotion: str, hashing: bool) -> Path:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self._generate_fragment, text, emotion, hashing)
    
    def generate_audiofile(self, text: str, hashing: bool = True, output_name: str = ""):
        text_hash = get_hash(text)
        final_path = self.output_dir / (output_name or f"{text_hash}.wav")

        if hashing and final_path.exists():
            print(f"⚡ Финальный файл уже есть → {final_path.name}")
            return final_path

        fragments = parse_emotion_text(text)
        print(f"🔍 Фрагментов: {len(fragments)}")

        if len(fragments) == 1:
            emotion, frag_text = fragments[0]
            print(f"🎤 Один фрагмент → генерирую сразу: {emotion}")
            return self._tts_with_fallback(frag_text, self.samples_dir / f"{emotion}_sample.wav", final_path)

        audio_segments = [
            AudioSegment.from_wav(self._generate_fragment(frag_text, emotion, hashing))
            for emotion, frag_text in fragments
        ]

        combined = audio_segments[0]
        for segment in audio_segments[1:]:
            combined += segment
            
        combined.export(final_path, format="wav")
        print(f"✅ Собрано → {final_path.name}")
        return final_path
            
    async def generate_stream(self, text: str, format: str = "wav"):
        """
        Асинхронная потоковая генерация речи — отдаёт байты аудио по фрагментам.
        Можно использовать с StreamingResponse (FastAPI), WebSocket, yield в HTTP.
        """
        fragments = parse_emotion_text(text)
        print(f"🔄 Stream TTS — найдено {len(fragments)} фрагментов")
        
        sample_rate = self.tts.synthesizer.output_sample_rate # type: ignore
        print(f"📡 Частота дискретизации модели: {sample_rate}")
        
        buffer = io.BytesIO()
        wav_writer = wave.open(buffer, "wb")
        wav_writer.setnchannels(1)
        wav_writer.setsampwidth(2)  # 16-bit PCM
        wav_writer.setframerate(sample_rate) # type: ignore
        
        header_sent = False

        for emotion, fragment_text in fragments:
            print(f"🎙️ Stream-фрагмент: [{emotion}] → \"{fragment_text}\"")
            sample_path = self.samples_dir / f"{emotion}_sample.wav"
            
            audio = self.tts.tts(
                text=fragment_text,
                speaker_wav=str(sample_path),
                language="ru"
            )

            if isinstance(audio, list):
                audio = np.array(audio, dtype=np.float32)

            if audio.dtype != np.int16:
                audio = (audio * 32767).clip(-32768, 32767).astype(np.int16)
                
            wav_writer.writeframes(audio.tobytes())
            
            if not header_sent:
                wav_writer.close()
                buffer.seek(0)
                data = buffer.read()
                print(f"📤 Отправлен заголовок + 1-й фрагмент ({len(data)} bytes)")
                yield data
                header_sent = True

            else:
                print(f"📤 Отправлен следующий RAW-фрагмент ({len(audio.tobytes())} bytes)")
                yield audio.tobytes()

