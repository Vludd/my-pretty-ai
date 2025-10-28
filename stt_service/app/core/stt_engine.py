import time
import torch
import whisper

class STTEngine:
    def __init__(self, model: str = "base", use_cuda: bool = True) -> None:
        self.model_name = model
        self.device = "cuda" if use_cuda and torch.cuda.is_available() else "cpu"
        
        print("CUDA available:", torch.cuda.is_available())
        print("Using GPU:", torch.cuda.get_device_name(0)) if torch.cuda.is_available() and use_cuda else print("Using CPU")
        
        self.model = whisper.load_model(self.model_name)
        self.model = self.model.to(self.device)
        
    def transcribe(self, audio_path: str):
        start = time.time()
        result = self.model.transcribe(audio_path)
        
        sentences = result["text"]
        print(f"Recognized text: {sentences} ({round(time.time() - start, 2)}s)")
        return sentences
