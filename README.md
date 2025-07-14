# Reddit Persona Analyzer

This project scrapes a Reddit user's recent activity and generates a user persona using a local LLM (Ollama) or a dummy fallback.

---

## Project Structure

- `reddit_scraper.py`   -> Scrapes Reddit comments and posts
- `persona_builder.py`  -> Builds persona using Ollama or dummy fallback
- `main.py`             -> Entry point to run the pipeline
- `persona_final.txt`   -> ✅ Manually saved final persona (from Ollama)
- `<username>_persona.txt` -> Auto-generated on each run (may change)
- `.env` (optional)     -> Store OpenAI key if used in future (not required now)

---

## LLM Usage

- **Primary Model**: `llama3` via [Ollama](https://ollama.com)
- **Fallback**: Dummy persona generator (keyword-based)
- **OpenAI GPT Support**: Implemented but not used due to quota restrictions

---

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt

2. run main.py
   ``` python
   python main.py