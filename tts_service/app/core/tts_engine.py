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
from app.types import TTSDevice

from app.utils.logger import logger

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = BASE_DIR / "data/samples"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

class TTSEngine:
    def __init__(self, model_name: str, device: TTSDevice = TTSDevice.CUDA, workers: int = 4) -> None:
        start = time.time()
        self.device = TTSDevice.CUDA.value if device == TTSDevice.CUDA and torch.cuda.is_available() else TTSDevice.CPU.value
        self.tts = TTS(model_name=model_name, progress_bar=False)
        self.executor = ThreadPoolExecutor(max_workers=workers)
        self.samples_dir = SAMPLES_DIR
        self.output_dir = OUTPUT_DIR
        
        self.tts.to(self.device)
        
        logger.info(f"✓ TTS Initialization finished. Using [{self.device}] ({round(time.time() - start, 2)}s)")
        
    def _generate_fragment(self, text: str, emotion: str, hashing: bool) -> Path:
        fragment_key = f"{emotion}-{text}"
        output_name = get_hash(fragment_key) if hashing else fragment_key
        output_path = self.output_dir / f"{output_name}.wav"

        if output_path.exists():
            logger.warning(f"Exists in cache: {output_path.name}")
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
            logger.info(f"✓ Generated audio [{self.device}]: {output_path.name} ({round(time.time() - start, 2)}s)")
            return output_path

        except Exception as e:
            if self.device == "cuda":
                logger.error(f"⚠ CUDA Error: {e} switching to CPU...")
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
            logger.info(f"Final file is already exists -> {final_path.name}")
            return final_path

        fragments = parse_emotion_text(text)
        logger.debug(f"Fragments: {len(fragments)}")

        if len(fragments) == 1:
            emotion, frag_text = fragments[0]
            logger.debug(f"One fragment, generating immediately: {emotion}")
            return self._tts_with_fallback(frag_text, self.samples_dir / f"{emotion}_sample.wav", final_path)

        audio_segments = [
            AudioSegment.from_wav(self._generate_fragment(frag_text, emotion, hashing))
            for emotion, frag_text in fragments
        ]

        combined = audio_segments[0]
        for segment in audio_segments[1:]:
            combined += segment
            
        combined.export(final_path, format="wav")
        logger.info(f"✓ Collected! {final_path.name}")
        return final_path
            
    async def generate_stream(self, text: str, format: str = "wav"):
        """
        Asynchronous speech generation that streams audio bytes in chunks.
        Can be used with StreamingResponse (FastAPI), WebSocket or HTTP yield.
        """
        fragments = parse_emotion_text(text)
        logger.debug(f"Stream TTS: founded {len(fragments)} fragments")
        
        sample_rate = self.tts.synthesizer.output_sample_rate # type: ignore
        logger.debug(f"Sample rate of model: {sample_rate}")
        
        buffer = io.BytesIO()
        wav_writer = wave.open(buffer, "wb")
        wav_writer.setnchannels(1)
        wav_writer.setsampwidth(2)  # 16-bit PCM
        wav_writer.setframerate(sample_rate) # type: ignore
        
        header_sent = False

        for emotion, fragment_text in fragments:
            logger.debug(f"Stream-fragment: [{emotion}] -> \"{fragment_text}\"")
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
                logger.debug(f"Sent header and initial audio chunk ({len(data)} bytes)")
                yield data
                header_sent = True

            else:
                logger.debug(f"Sent next RAW-fragment ({len(audio.tobytes())} bytes)")
                yield audio.tobytes()

