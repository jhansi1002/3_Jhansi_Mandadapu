@echo off
REM Create venv and install dependencies if missing, then run the app (Windows)
if not exist .venv (
  python -m venv .venv
  call .venv\Scripts\activate
  pip install -r requirements.txt
) else (
  call .venv\Scripts\activate
)
uvicorn src.main:app --reload --port 8000
pause