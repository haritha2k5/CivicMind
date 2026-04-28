import os
import time  
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()


def ingest_documents(extra_folders=[]):
    all_docs = []

    pdf_folder = "knowledge_base/central_schemes"
    try:
        for filename in os.listdir(pdf_folder):
            if filename.endswith(".pdf"):
                filepath = os.path.join(pdf_folder, filename)
                loader = PyPDFLoader(filepath)
                docs = loader.load()
                all_docs.extend(docs)
                print(f"Loaded PDF: {filename}")
    except:  
        print("Error loading PDFs")

    txt_folder = "knowledge_base/legal_docs"
    try:
        for filename in os.listdir(txt_folder):
            if filename.endswith(".txt"):
                filepath = os.path.join(txt_folder, filename)
                loader = TextLoader(filepath, encoding="utf-8")
                docs = loader.load()
                all_docs.extend(docs)
                print(f"Loaded TXT: {filename}")
    except:  
        print("Error loading TXTs")

    state_folder = "knowledge_base/state_docs"
    try:
        for filename in os.listdir(state_folder):
            if filename.endswith(".pdf"):
                filepath = os.path.join(state_folder, filename)
                loader = PyPDFLoader(filepath)
                docs = loader.load()
                all_docs.extend(docs)
                print(f"Loaded State PDF: {filename}")
    except:
        print("Error loading state docs")

    budget_folder = "knowledge_base/budget"
    try:
        for filename in os.listdir(budget_folder):
            if filename.endswith(".txt"):
                filepath = os.path.join(budget_folder, filename)
                loader = TextLoader(filepath, encoding="utf-8")
                docs = loader.load()
                all_docs.extend(docs)
                print(f"Loaded Budget TXT: {filename}")
    except: 
        print("Error loading budget docs")

    print(f"Total documents loaded: {len(all_docs)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(all_docs)
    print(f"Total chunks: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local("backend/data/vector_store")
    print("FAISS index saved.")


if __name__ == "__main__":
    ingest_documents()
