import json, httpx
from config import OLLAMA_URL, MODEL

SYSTEM = """You are a browser-task planner. Convert the user's request into a JSON object:
{"goal":"short goal","steps":[{"action":"search","query":"..."},
{"action":"open_result","index":0},{"action":"extract","fields":["title","price","url"]}]}
Allowed actions: search, open_result, extract, summarize. Keep plan to at most 6 steps.
Return JSON only. Never propose login, payment, purchases, posting, deleting, or submitting forms."""

async def plan_task(prompt: str):
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(f"{OLLAMA_URL}/api/generate", json={
                "model": MODEL, "stream": False,
                "prompt": SYSTEM + "\nUser request: " + prompt + "\nJSON:"
            })
            r.raise_for_status()
            raw = r.json().get("response", "")
        start, end = raw.find("{"), raw.rfind("}")
        if start < 0 or end < start: raise ValueError("Model did not return JSON")
        data = json.loads(raw[start:end+1])
        if not isinstance(data.get("steps"), list): raise ValueError("Invalid plan")
        return data
    except Exception:
        # Deterministic fallback keeps the MVP usable if the local model is unavailable.
        return {"goal": prompt, "steps":[{"action":"search","query":prompt},{"action":"extract","fields":["title","url"]}]}
