# MyPrettyAI

**MyPrettyAI** — is an offline AI service that allows you to interact with a powerful LLM, recognize speech and voice text using TTS. The project is completely autonomous and does not require an Internet connection for basic functionality.

---

## Basic features

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

## Installation

### Attention! The developer does not guarantee the stable operation of all microservices without meeting the minimum system requirements

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

## RUN:

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

## Project Outline
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

## License
The project is distributed under the mit License. For more information, see the LICENSE file.

---

## Planned features:
```bash
- Voice chat mode
- Setting and running services with Docker-compose
- Cloud AI API integrations
- Performance Manager: automatic switch performance profiles from demanding to less demanding solutions while maintaining agility and ease of maintenance
```
