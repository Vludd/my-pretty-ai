<h1 align="center">MyPrettyAI</h1>
<h3 align="center">Your digital friend who works locally and offline</h3>

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-cc0000?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Microservices-FF6F00?style=for-the-badge&logo=google-cloud&logoColor=white" />
  <img src="https://img.shields.io/badge/LLM-AI%20Model-6E5494?style=for-the-badge&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/AsyncIO-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</p>

## ▸｜About MyPrettyAI
It's an offline AI service that allows you to interact with a powerful LLM, recognize speech and voice text using TTS. The project is completely autonomous and does not require an Internet connection for basic functionality.

---

## ▸｜Basic features

- **Offline LLM**: support for local models for text generation and communication. (So far only LLM Qwen3/4B)
- **Speech recognition (STT)**: Converting voice commands into text. (IN DEV)
- **Speech synthesis (TTS)**: voice acting locally.
- **Modular architecture**:
  - `backend/` — API and server logic.
  - `frontend/` — interface for interacting with the service.
  - `llm_service/` — LLM Engine module
  - `tts_service/` — module for voice and audio generation.
  - `stt_service/` — audio text recognition module.

- **Fully customizable**: you can add your own tasks, prompts and expand the functionality. (IN DEV)

---

## ▸｜System Requirements

| Component | Minimum | Recommended |
|------------|----------|-------------|
| **CPU** | 4-core processor (AMD Ryzen 3 / Intel i5 8th gen or newer) | 8-core or more (AMD Ryzen 7 / Intel i7) |
| **RAM** | 8 GB | 16–32 GB (for smooth LLM, TTS/STT processing) |
| **Storage** | 10 GB free space (models, cache, logs) | 20 GB free space (large models, cache, logs) |
| **GPU** | Optional (CPU mode supported, but slower) | NVIDIA RTX 3060 / RX 6600 or better (≥ 6 GB VRAM, CUDA 12+) |
| **OS** | Windows 10/11, Linux (tested on Arch Linux) | Windows 10/11, Linux (x86_64, CUDA 12+ supported) |

### Dependencies
*(No need to install this locally when deploying project via Docker!)*

- **Python:** 3.11 or higher
- **Node.js:** 22 or higher (for frontend)
- **ffmpeg:** required for TTS/STT audio processing
- **Redis:** used for caching and job queues
- **Docker:** recommended for containerized deployment

<h4 align="center" style="color:tomato;">⚠️ Stable operation is not guaranteed below the minimum requirements.</h4>

---

## ▸｜Installation Locally

1. Clone the repository:
```bash
git clone https://github.com/Vludd/my-pretty-ai.git
cd my-pretty-ai
```

2. Set dependencies for llm_service:
```bash
cd llm_service
python -m venv venv
source venv/bin/activate    # Linux / Mac
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

3. Set dependencies for tts_service:
```bash
cd ../tts_service
python -m venv venv
source venv/bin/activate    # Linux / Mac
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

4. Set dependencies for stt_service:
```bash
cd ../stt_service
python -m venv venv
source venv/bin/activate    # Linux / Mac
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

5. Set dependencies for backend:
```bash
cd ../backend
python -m venv venv
source venv/bin/activate    # Linux / Mac
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

6. Set dependencies for frontend:
```bash
cd ../frontend
npm install                 # or pnpm install
```

---

## ▸｜Run:

1. LLM Service:
```bash
cd llm_service              # From the root of the project
python run.py               # Start on 8001 port by default
```

2. TTS Service:
```bash
cd tts_service              # From the root of the project
python run.py               # Start on 8002 port by default
```

3. STT Service:
```bash
cd stt_service              # From the root of the project
python run.py               # Start on 8003 port by default
```

4. Backend:
```bash
cd backend                  # From the root of the project
python run.py               # Start on 8000 port by default
```

5. Frontend:
```bash
cd frontend                 # From the root of the project
npm run dev                 # Start on 5173 port by default
```

---

## ▸｜Project Outline
```bash
.
├── backend/                # API Core
├── frontend/               # Web-interface
├── llm_service/            # LLM Engine
├── stt_service/            # Audio text recognition service
├── tts_service/            # Voiceover and audio generation
├── docker-compose.dev.yml  # Soon
├── docker-compose.yml      # Soon
├── LICENSE
├── makefile                # Soon
└── README.md
```

---

## ▸｜License
The project is distributed under the mit License. For more information, see the LICENSE file.

---

## ▸｜Planned features:
```bash
- Voice chat mode
- Setting and running services with Docker-compose
- Cloud AI API integrations
- Performance Manager: automatic switch performance profiles from demanding to less demanding solutions while maintaining agility and ease of maintenance
```
