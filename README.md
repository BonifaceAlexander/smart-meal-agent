# smart-meal-agent (v2) — AI Meal Recommender & Ordering Assistant

## What’s included
- FastAPI backend (`app/`) with orchestrator, MCP mock adapter, and vector-index placeholder.
- Streamlit demo UI (`app/ui.py`)
- Dockerfile & docker-compose for local dev
- GitHub Actions CI skeleton
- `requirements.txt` and simple DB init script
- `README` with run instructions

## Quick start (dev)
1. Create a Python venv and install deps:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
3. In another terminal start Streamlit demo:
   ```bash
   streamlit run app/ui.py --server.port 8501
   ```
4. Open http://localhost:8501 for the demo UI.

## Docker (optional)
```bash
docker compose up --build
```

## Notes
- This v2 scaffold includes a **mock MCP adapter** for testing order flows without a real provider.
- The vector index is a placeholder to show where to integrate Chroma/pgvector/FAISS.
- Replace `OPENAI_API_KEY` with your key if you want to enable LangChain LLM calls.

