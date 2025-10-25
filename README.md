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
  - `tts_service/` — module for voice and audio generation.

- **Fully customizable**: you can add your own tasks, prompts and expand the functionality. (IN DEV)

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Vludd/my-pretty-ai.git
cd my-pretty-ai
```

2. Set dependencies for backend:
```bash
cd backend
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

4. Set dependencies for frontend:
```bash
cd ../frontend
npm install                 # or pnpm install
```

---

## RUN:

1. Backend:
```bash
cd backend
python run.py               # Start on 8000 port by default
```

2. TTS Service:
```bash
cd tts_service
python run.py               # Start on 8100 port by default
```

3. Frontend:
```bash
cd frontend
npm run dev                 # Start on 5173 port by default
```

---

## Project Outline
```bash
.
├── backend/                # API Core
├── frontend/               # Web-interface
├── tts_service/            # Voiceover and audio generation
├── LICENSE
├── README.md
├── docker-compose.yml      # Soon
└── makefile                # Soon
```

---

## License
The project is distributed under the mit License. For more information, see the LICENSE file.

---

## Planned features:
```bash

```
