# ============================================================
# VERSION 1 — ingest.py
# CODE SMELLS (Structural — for lab report):
#   [S1] Long Method       — ingest_documents() does everything
#   [S2] Magic Numbers     — 1000, 200 hardcoded inline
#   [S3] Hardcoded Config  — paths and model names in code
#   [S4] Duplicate Code    — PDF and TXT loading near-identical
#   [S5] No Abstraction    — no classes, no interfaces
#
# CODE SMELLS (SonarCloud-detectable):
#   [S6] Broad Exception   — bare except: catches everything
#   [S7] Unused variable   — 'time' imported but never used
#   [S8] Print statements  — using print instead of logging
#   [S9] Mutable default   — list passed as default argument
# ============================================================

import os
import time  # [S7] UNUSED IMPORT
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()


# [S9] MUTABLE DEFAULT ARGUMENT
def ingest_documents(extra_folders=[]):
    # [S1] LONG METHOD
    # [S3] HARDCODED CONFIG
    all_docs = []

    # [S4] DUPLICATE CODE block 1 — PDF
    pdf_folder = "knowledge_base/central_schemes"
    try:
        for filename in os.listdir(pdf_folder):
            if filename.endswith(".pdf"):
                filepath = os.path.join(pdf_folder, filename)
                loader = PyPDFLoader(filepath)
                docs = loader.load()
                all_docs.extend(docs)
                print(f"Loaded PDF: {filename}")
    except:  # [S6] BROAD EXCEPTION
        print("Error loading PDFs")

    # [S4] DUPLICATE CODE block 2 — TXT
    txt_folder = "knowledge_base/legal_docs"
    try:
        for filename in os.listdir(txt_folder):
            if filename.endswith(".txt"):
                filepath = os.path.join(txt_folder, filename)
                loader = TextLoader(filepath, encoding="utf-8")
                docs = loader.load()
                all_docs.extend(docs)
                print(f"Loaded TXT: {filename}")
    except:  # [S6] BROAD EXCEPTION
        print("Error loading TXTs")

    # [S4] DUPLICATE CODE block 3 — state PDFs
    state_folder = "knowledge_base/state_docs"
    try:
        for filename in os.listdir(state_folder):
            if filename.endswith(".pdf"):
                filepath = os.path.join(state_folder, filename)
                loader = PyPDFLoader(filepath)
                docs = loader.load()
                all_docs.extend(docs)
                print(f"Loaded State PDF: {filename}")
    except:  # [S6] BROAD EXCEPTION
        print("Error loading state docs")

    # [S4] DUPLICATE CODE block 4 — budget TXTs
    budget_folder = "knowledge_base/budget"
    try:
        for filename in os.listdir(budget_folder):
            if filename.endswith(".txt"):
                filepath = os.path.join(budget_folder, filename)
                loader = TextLoader(filepath, encoding="utf-8")
                docs = loader.load()
                all_docs.extend(docs)
                print(f"Loaded Budget TXT: {filename}")
    except:  # [S6] BROAD EXCEPTION
        print("Error loading budget docs")

    print(f"Total documents loaded: {len(all_docs)}")

    # [S2] MAGIC NUMBERS
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(all_docs)
    print(f"Total chunks: {len(chunks)}")

    # [S3] HARDCODED model name
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vector_store = FAISS.from_documents(chunks, embeddings)
    # [S3] HARDCODED CONFIG — save path inline
    vector_store.save_local("backend/data/vector_store")
    print("FAISS index saved.")


if __name__ == "__main__":
    ingest_documents()
