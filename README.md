# Medication Reminder Chatbot (Label-Aware)

<<<<<<< HEAD
Mini app scaffold that does:

- Ingest openFDA drug label JSONs into a local Chroma vector store
- Provide a retrieval-augmented `ask_drug(question)` function
- Provide reminder generation (sample JSON plan per drug/dosage)
- Run a small FastAPI server with a simple web UI for chat and reminders

Quick start

1. Create a virtual env and install deps (Windows):

   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt

   Or use the helper batch: `run_app.bat` to create venv, install deps and launch the app.

2. Ingest sample labels:

   python scripts/ingest_openfda.py --drugs aspirin ibuprofen acetaminophen --outdir data/labels

3. Start the app:

   uvicorn src.main:app --reload --port 8000

Open http://localhost:8000 in your browser.

Notes

- If you have an OpenAI key and want nicer LLM responses, set `OPENAI_API_KEY` in your environment. The app will fall back to returning retrieved passages if no key is present.
- This is a minimal scaffold meant to be extended. See `/src` for the core modules.
=======
## Problem Statement
Patients and caregivers often struggle to understand drug usage instructions, warnings, and dosage details from complex medication labels. This project aims to build an AI-powered chatbot that answers questions over drug labels and generates a simple medication reminder plan.

## Solution Overview
We propose a Retrieval-Augmented Generation (RAG) based chatbot that retrieves relevant information from official drug labels and provides accurate answers along with a structured medication reminder plan.

## Domain
Healthcare – Medication Safety and Adherence

## Tech Stack
- Python
- LangChain
- ChromaDB (Vector Database)
- FastAPI (Optional for API exposure)

## Dataset
- openFDA Drug Label Dataset  
  https://open.fda.gov/apis/drug/label/download/

## Expected Outcome
- A function `ask_drug(question)` that answers queries over drug labels
- A sample JSON-based medication reminder plan per drug and dosage

## Team
This project is developed as part of an AI Hackathon by a team of final-year students.
>>>>>>> 2f4745003aea09338b1223ee0311670b2dccbf3d
