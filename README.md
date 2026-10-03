# NovaMart AI Customer Support Agent

## Purpose
Deterministic pipeline for Support AI, featuring Policy Engine, Decider, and Guardrails.

## Configuration
Copy `.env.example` to `.env` and set `LLM_API_KEY` to use real models.
If unset, falls back to deterministic mock logic.

## Usage
```
python server.py --cli
python server.py --port 8080
```

## Testing
```
python -m pytest -q
```
