# CivicMind — RAG-Powered Civic Intelligence Platform

> **AI Course + Software Patterns Lab Project**
> MSc Integrated Software Systems · PSG College of Technology · 2024–25

---

## What is CivicMind?

CivicMind is a three-module AI platform built on Retrieval-Augmented Generation (RAG)
that connects Indian citizens to welfare information in plain language.

| Module | What it does |
|---|---|
| **PolicyPulse** | Answers questions about 50+ government schemes, RTI Act, CPGRAMS, budget |
| **GrievanceGPT** | Routes complaints, lists required documents, auto-generates complaint letters |
| **SchemeMatch AI** | Matches a citizen profile to every eligible welfare scheme |

---

## Project Structure

```
civicmind/
├── civicmind_v1/          ← VERSION 1: Intentional code smells (Software Patterns Lab)
│   ├── backend/
│   │   ├── ingest.py      ← Smells: Long Method, Magic Numbers, Duplicate Code
│   │   ├── rag/
│   │   │   └── rag_pipeline.py  ← Smell: God Class, Tight Coupling
│   │   └── main.py        ← Smell: Business logic in controller
│   └── knowledge_base/
│
├── civicmind_v2/          ← VERSION 2: Clean refactored implementation
│   ├── backend/
│   │   ├── config.py      ← All magic numbers centralised
│   │   ├── ingest.py      ← Clean: 4 focused functions
│   │   ├── controllers/   ← Thin HTTP layer only
│   │   ├── services/      ← Business logic lives here
│   │   ├── rag/
│   │   │   ├── factory/   ← Factory Pattern (LLM creation)
│   │   │   ├── pipeline/  ← Adapter Pattern (Gemini wrapper)
│   │   │   └── strategies/← Strategy + Template Method Patterns
│   │   └── data/          ← Singleton Pattern (FAISS instance)
│   ├── frontend/          ← React + Tailwind, 3 module pages
│   └── knowledge_base/
```

---

## Design Patterns Summary (Version 2)

| Pattern | Where | Purpose |
|---|---|---|
| **Factory** | `rag/factory/llm_factory.py` | Centralise LLM + embedding creation |
| **Singleton** | `data/vector_store_singleton.py` | Load FAISS index only once |
| **Adapter** | `rag/pipeline/llm_adapter.py` | Wrap Gemini behind a standard interface |
| **Strategy** | `rag/strategies/rag_strategy.py` | Different RAG behaviour per module |
| **Template Method** | `GrievanceStrategy` inside strategy file | Fixed 4-step grievance workflow |

---

## Code Smells in Version 1 (for Lab Report)

| Smell | File | Lines |
|---|---|---|
| Long Method | `ingest.py` | `ingest_documents()` — 60+ lines |
| Magic Numbers | `ingest.py`, `rag_pipeline.py` | `1000`, `200`, `5`, `8`, `0.3` |
| Duplicate Code | `ingest.py` | 4 near-identical folder loading blocks |
| Hardcoded Config | Both files | Paths and model names inline |
| God Class | `rag_pipeline.py` | `RAGPipeline` handles everything |
| Tight Coupling | `rag_pipeline.py` | Direct FAISS + Gemini instantiation |
| Business logic in controller | `main.py` | Validation + profile building in routes |
| Layer bypass | `main.py` | Controller calls RAG directly, skips service |

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- A Gemini API key from [aistudio.google.com](https://aistudio.google.com)

---

### Step 1 — Clone and configure

```bash
# Work inside whichever version you want to run (v1 or v2)
cd civicmind_v2

# Add your Gemini API key to .env
# Edit .env and replace: GEMINI_API_KEY=your_gemini_api_key_here
```

---

### Step 2 — Install Python dependencies

```bash
pip install -r requirements.txt
```

---

### Step 3 — Add knowledge base documents

Drop your PDF or TXT files into any of these folders:
```
knowledge_base/central_schemes/   ← government scheme PDFs
knowledge_base/legal_docs/        ← RTI Act, CPGRAMS TXT files
knowledge_base/state_docs/        ← state-level policy PDFs
knowledge_base/budget/            ← budget announcement TXTs
```
Sample files are already included to test with.

---

### Step 4 — Run ingestion (build FAISS index)

```bash
# From the civicmind_v2/ root folder
python -m backend.ingest
```

You should see:
```
Loading from: knowledge_base/central_schemes
  Loaded: pm_kisan.txt
...
Total chunks created: 12
FAISS index saved to: backend/data/vector_store
Ingestion complete.
```

---

### Step 5 — Start the backend

```bash
uvicorn backend.main:app --reload --port 8000
```

API will be live at: [http://localhost:8000](http://localhost:8000)
Swagger docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Step 6 — Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend at: [http://localhost:5173](http://localhost:5173)

---

## API Reference

### POST /policy-pulse
```json
{ "question": "What is PM-KISAN and how do I apply?" }
```

### POST /grievance
```json
{ "issue": "My ration card application was rejected 3 months ago and I have received no response." }
```

### POST /scheme-match
```json
{
  "age": 35,
  "gender": "Female",
  "annual_income": 80000,
  "caste_category": "SC",
  "state": "Tamil Nadu",
  "occupation": "Farmer"
}
```

---

## Example Queries to Test

**PolicyPulse:**
- "What is Ayushman Bharat and who is eligible?"
- "How do I file an RTI application?"
- "What are the benefits of PM Ujjwala Yojana?"

**GrievanceGPT:**
- "My electricity connection was cut without notice 2 weeks ago"
- "I applied for a caste certificate 6 months ago and got no response"

**SchemeMatch AI:**
- Profile: Age 28, Female, Income ₹60,000, OBC, Tamil Nadu, Farmer

---

## Running Version 1 (Smelly)

```bash
cd civicmind_v1
pip install -r requirements.txt
python -m backend.ingest          # build index
uvicorn backend.main:app --reload --port 8000
```

Same frontend works for both versions.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js (Vite) + CSS |
| API | FastAPI (Python) |
| RAG Chain | LangChain |
| Vector Store | FAISS (local) |
| Embedding Model | Gemini `models/embedding-001` via LangChain |
| LLM | Gemini 1.5 Pro via LangChain |
