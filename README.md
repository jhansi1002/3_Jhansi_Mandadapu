# Medication Reminder Chatbot (Label-Aware)

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
