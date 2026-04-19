# ============================================================
# VERSION 1 — ingest.py
# SMELLS PRESENT:
#   [S1] Long Method       — ingest_documents() does everything
#   [S2] Magic Numbers     — 1000, 200, hardcoded inline
#   [S3] Hardcoded Config  — paths and model names in code
#   [S4] Duplicate Code    — PDF and TXT loading are near-identical
#   [S5] No Abstraction    — no classes, no interfaces
# ============================================================

import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()


def ingest_documents():
    # [S1] LONG METHOD — loading, splitting, embedding, saving all in one function
    # [S3] HARDCODED CONFIG — paths written directly, not from config/env

    all_docs = []

    # [S4] DUPLICATE CODE — PDF loading block
    pdf_folder = "knowledge_base/central_schemes"  # [S3] hardcoded path
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(pdf_folder, filename)
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            all_docs.extend(docs)
            print(f"Loaded PDF: {filename}")

    # [S4] DUPLICATE CODE — TXT loading block (same structure, different loader)
    txt_folder = "knowledge_base/legal_docs"  # [S3] hardcoded path
    for filename in os.listdir(txt_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(txt_folder, filename)
            loader = TextLoader(filepath, encoding="utf-8")
            docs = loader.load()
            all_docs.extend(docs)
            print(f"Loaded TXT: {filename}")

    # [S4] DUPLICATE CODE — another PDF folder (state_docs), same pattern repeated
    state_folder = "knowledge_base/state_docs"  # [S3] hardcoded
    for filename in os.listdir(state_folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(state_folder, filename)
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            all_docs.extend(docs)
            print(f"Loaded State PDF: {filename}")

    # [S4] DUPLICATE CODE — budget folder, same pattern again
    budget_folder = "knowledge_base/budget"  # [S3] hardcoded
    for filename in os.listdir(budget_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(budget_folder, filename)
            loader = TextLoader(filepath, encoding="utf-8")
            docs = loader.load()
            all_docs.extend(docs)
            print(f"Loaded Budget TXT: {filename}")

    print(f"Total documents loaded: {len(all_docs)}")

    # [S2] MAGIC NUMBERS — 1000 and 200 with no explanation
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,    # [S2] magic number
        chunk_overlap=200   # [S2] magic number
    )
    chunks = splitter.split_documents(all_docs)
    print(f"Total chunks: {len(chunks)}")

    # [S3] HARDCODED CONFIG — model name written inline
    embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
    vector_store = FAISS.from_documents(chunks, embeddings)
   
    # [S3] HARDCODED CONFIG — save path inline
    vector_store.save_local("backend/data/vector_store")
    print("FAISS index saved.")


if __name__ == "__main__":
    ingest_documents()
