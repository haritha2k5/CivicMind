# ============================================================
# VERSION 1 — backend/main.py
# SMELLS PRESENT:
#   [A1] Business logic inside controller (no service layer used)
#   [A2] Layers exist but are not respected — controller calls
#        RAGPipeline directly, bypassing service layer
#   [A3] Direct dependency between layers
#   [S11] God Object — pipeline instance shared globally
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.rag.rag_pipeline import RAGPipeline  # [A2] controller → RAG directly

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # [S3] hardcoded wildcard
    allow_methods=["*"],
    allow_headers=["*"],
)

# [S11] Global mutable state — pipeline created at module level
pipeline = RAGPipeline()


# ── Request models ──────────────────────────────────────────

class PolicyRequest(BaseModel):
    question: str


class GrievanceRequest(BaseModel):
    issue: str


class SchemeRequest(BaseModel):
    age: int
    gender: str
    annual_income: float
    caste_category: str
    state: str
    occupation: str


# ── Endpoints ───────────────────────────────────────────────

@app.post("/policy-pulse")
def policy_pulse(req: PolicyRequest):
    # [A1] BUSINESS LOGIC IN CONTROLLER — validation, formatting done here
    if not req.question.strip():
        return {"error": "Question cannot be empty"}  # [A1] validation in controller

    # [A2] SKIPS SERVICE LAYER — calls RAG directly from controller
    result = pipeline.query_policy(req.question)
    return {"answer": result}


@app.post("/grievance")
def grievance(req: GrievanceRequest):
    # [A1] BUSINESS LOGIC IN CONTROLLER
    if len(req.issue) < 10:  # [A1] input validation in controller
        return {"error": "Please describe your issue in more detail"}

    # [A2] SKIPS SERVICE LAYER
    result = pipeline.query_grievance(req.issue)
    return result


@app.post("/scheme-match")
def scheme_match(req: SchemeRequest):
    # [A1] PROFILE BUILDING IN CONTROLLER — belongs in service layer
    profile = {
        "age": req.age,
        "gender": req.gender,
        "annual_income": req.annual_income,
        "caste_category": req.caste_category,
        "state": req.state,
        "occupation": req.occupation
    }

    # [A2] SKIPS SERVICE LAYER
    result = pipeline.query_scheme_match(profile)
    return {"schemes": result}
