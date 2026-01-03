from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from .retrieval import DrugRetriever
from .reminders import ReminderManager

app = FastAPI(title="MediBot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=str(BASE / "web")), name="static")

# Initialize components (simple singletons for this mini app)
DATA_DIR = BASE / "data"
RETRIEVER = DrugRetriever(data_dir=str(DATA_DIR / "labels"))
REMINDERS = ReminderManager(data_path=str(DATA_DIR / "reminders.json"))


@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse(str(BASE / "web" / "index.html"))


@app.post("/api/chat")
async def chat(payload: dict):
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Missing 'question' in body")
    answer = RETRIEVER.ask_drug(question)
    return JSONResponse({"answer": answer})


@app.post("/api/reminders")
async def create_reminder(payload: dict):
    # expected: drug_name, dosage_mg, frequency_per_day, start_date (ISO), end_date (ISO optional)
    reminder = REMINDERS.create_reminder(payload)
    return JSONResponse(reminder)


@app.get("/api/reminders")
async def list_reminders():
    return JSONResponse(REMINDERS.list_reminders())


@app.get("/api/generate_plan")
async def generate_plan(drug_name: str, dosage_mg: float = 100.0, frequency_per_day: int = 2):
    plan = REMINDERS.generate_reminder_plan(drug_name, dosage_mg, frequency_per_day)
    return JSONResponse(plan)


@app.post("/api/rebuild_index")
async def rebuild_index():
    try:
        RETRIEVER.rebuild()
        return JSONResponse({"status":"ok","message":"Index rebuild requested"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
