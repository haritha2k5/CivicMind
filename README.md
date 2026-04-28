# CivicMind — RAG-Powered Civic Intelligence Platform

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

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- A Gemini API key from [aistudio.google.com](https://aistudio.google.com)

---

### Step 1 — Clone and configure

```bash
cd civicmind

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
# From the civicmind/ root folder
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

## Running 

```bash
cd civicmind
pip install -r requirements.txt
python -m backend.ingest          # build index
uvicorn backend.main:app --reload --port 8000
```

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
