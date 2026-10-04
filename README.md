# Web Navigator AI (MVP)

Free, local-first browser research assistant using Ollama, FastAPI, Playwright and React.

## Requirements
- Windows 10/11, Python 3.10+, Node.js LTS, Ollama
- Recommended: 16 GB RAM. A smaller Ollama model may be needed on lower-memory machines.

## Setup
1. Install Ollama from https://ollama.com and run `ollama pull qwen2.5:3b`.
2. Open terminal in `backend`: `py -m venv .venv`, activate it, then `pip install -r requirements.txt`.
3. Run `python -m playwright install chromium`.
4. Start backend: `uvicorn main:app --reload` (from backend folder).
5. In another terminal, enter `frontend`, run `npm install` then `npm run dev`.
6. Open the local Vite URL shown in terminal.

## Scope and safety
This is a functional starter MVP, not a guarantee of universal website compatibility. Search result layouts vary and may block automation. It performs read-only browsing; it does not log in, buy, submit forms, or bypass access controls. Use only public pages and respect site terms and robots policies.

## Troubleshooting
- `ollama list` verifies model installation.
- `http://localhost:8000/health` checks backend.
- If the model is too slow, pull a smaller model and set `OLLAMA_MODEL` accordingly.
