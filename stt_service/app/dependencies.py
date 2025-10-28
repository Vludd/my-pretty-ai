from app.core.stt_engine import STTEngine

import app.config as cfg

stt = STTEngine(cfg.STT_MODEL, use_cuda=cfg.STT_USE_CUDA)
