# ============================================================
# VERSION 1 — rag/rag_pipeline.py
# CODE SMELLS (Structural):
#   [S6]  God Class       — RAGPipeline handles everything
#   [S7]  Tight Coupling  — directly imports FAISS + LLM
#   [S8]  Long Method     — all query methods are huge
#   [S9]  No Interface    — no abstraction at all
#   [S10] Duplicate Logic — retriever created in every method
#
# CODE SMELLS (SonarCloud-detectable):
#   [S11] Broad Exception  — bare except in __init__
#   [S12] Unused variable  — 'response_time' computed but unused
#   [S13] Too many returns — multiple return paths
#   [S14] Hard-coded creds — API key fallback hardcoded
# ============================================================

import os
import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RAGPipeline:
    # [S6] GOD CLASS — does querying, routing, letter writing, scheme matching

    def __init__(self):
        try:
            # [S7] TIGHT COUPLING — directly instantiates concrete classes
            self.embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2"  # [S3] hardcoded
            )
            self.llm = ChatGroq(
                model="llama-3.1-8b-instant",   # [S3] hardcoded model
                groq_api_key=os.getenv("GROQ_API_KEY") or "fallback-key",  # [S14] hardcoded fallback
                temperature=0.3  # [S2] magic number
            )
            self.vector_store = FAISS.load_local(
                os.path.join(BASE_DIR, "data", "vector_store"),  # [S3] hardcoded
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        except:  # [S11] BROAD EXCEPTION — masks all errors
            print("Failed to initialise RAGPipeline")

    def query_policy(self, question: str) -> str:
        # [S8] LONG METHOD
        # [S10] DUPLICATE — retriever created here and in every other method

        start_time = time.time()  # [S12] computed but never used

        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 5}  # [S2] magic number
        )

        prompt_template = """
        You are a helpful assistant that explains Indian government schemes.
        Use the context below to answer the question clearly and simply.

        Context: {context}
        Question: {question}

        Answer in plain language:
        """

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt}
        )

        result = chain.invoke({"query": question})
        response_time = time.time() - start_time  # [S12] UNUSED VARIABLE
        return result["result"]

    def query_grievance(self, issue: str) -> dict:
        # [S8] LONG METHOD — 4 steps jammed into one method
        # [S10] DUPLICATE — retriever created AGAIN
        # [S6] GOD CLASS — grievance logic in RAGPipeline

        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 5}  # [S2] magic number repeated
        )

        dept_prompt = f"""
        Given this citizen grievance: "{issue}"
        Identify the most appropriate Indian government department.
        Reply with only the department name.
        """
        dept_response = self.llm.invoke(dept_prompt)
        department = dept_response.content

        doc_query = f"What documents are required for grievance related to {department}?"
        retriever_result = retriever.invoke(doc_query)
        docs_context = "\n".join([d.page_content for d in retriever_result])

        checklist_prompt = f"""
        Based on this context: {docs_context}
        List the documents needed to file a complaint with {department}.
        """
        checklist_response = self.llm.invoke(checklist_prompt)
        checklist = checklist_response.content

        letter_prompt = f"""
        Write a formal complaint letter to {department} regarding: "{issue}"
        Include placeholders for citizen name, address, and date.
        """
        letter_response = self.llm.invoke(letter_prompt)
        letter = letter_response.content

        steps_prompt = f"""
        What are the next steps after filing a complaint with {department}?
        Give a short 3-step guide.
        """
        steps_response = self.llm.invoke(steps_prompt)
        steps = steps_response.content

        return {
            "department": department,
            "documents_required": checklist,
            "complaint_letter": letter,
            "next_steps": steps
        }

    def query_scheme_match(self, profile: dict) -> str:
        # [S8] LONG METHOD
        # [S10] DUPLICATE — retriever created a 3rd time
        # [S6] GOD CLASS — scheme matching unrelated to RAG pipeline

        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 8}  # [S2] magic number, different from above
        )

        # [S3] inline string building — no helper method
        profile_text = (
            f"Age: {profile.get('age')}, "
            f"Gender: {profile.get('gender')}, "
            f"Income: {profile.get('annual_income')}, "
            f"Caste: {profile.get('caste_category')}, "
            f"State: {profile.get('state')}, "
            f"Occupation: {profile.get('occupation')}"
        )

        retrieval_query = f"welfare schemes eligible for: {profile_text}"
        retrieved_docs = retriever.invoke(retrieval_query)
        context = "\n".join([d.page_content for d in retrieved_docs])

        reasoning_prompt = f"""
        Citizen Profile: {profile_text}

        Available Schemes Information:
        {context}

        List every welfare scheme this citizen is eligible for.
        For each scheme mention:
        1. Scheme name
        2. Why they are eligible
        3. How to apply
        """

        response = self.llm.invoke(reasoning_prompt)
        return response.content
