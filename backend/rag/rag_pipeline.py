# ============================================================
# VERSION 1 — rag/rag_pipeline.py
# SMELLS PRESENT:
#   [S6]  God Class       — RAGPipeline does querying, loading,
#                           routing, letter generation, scheme
#                           matching — ALL in one class
#   [S7]  Tight Coupling  — directly imports FAISS and Gemini
#   [S8]  Long Method     — query_policy(), query_grievance(),
#                           query_scheme() all huge methods
#   [S9]  No Interface    — no abstraction, concrete classes only
#   [S10] Duplicate Logic — embedding call repeated in every method
# ============================================================

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RAGPipeline:
    # [S6] GOD CLASS — handles ALL module logic in one class

    def __init__(self):
        # [S7] TIGHT COUPLING — directly instantiates Gemini and FAISS
        # [S3] HARDCODED CONFIG — model names inline
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # [S3] hardcoded
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.3  # [S2] magic number
        )
        # [S7] TIGHT COUPLING — directly loads FAISS
        self.vector_store = FAISS.load_local(
            os.path.join(BASE_DIR, "data", "vector_store"),  # [S3] hardcoded path
            self.embeddings,
            allow_dangerous_deserialization=True
        )

    def query_policy(self, question: str) -> str:
        # [S8] LONG METHOD — does retrieval, prompt building, chain creation, invocation
        # [S10] DUPLICATE LOGIC — retriever setup repeated in every method

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
        return result["result"]

    def query_grievance(self, issue: str) -> dict:
        # [S8] LONG METHOD — 4 steps jammed into one method
        # [S10] DUPLICATE LOGIC — retriever created again (same as query_policy)
        # [S6] GOD CLASS — grievance logic should not be in RAGPipeline

        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 5}  # [S2] magic number repeated
        )

        # Step 1: identify department — direct LLM call
        dept_prompt = f"""
        Given this citizen grievance: "{issue}"
        Identify the most appropriate Indian government department to handle it.
        Reply with only the department name.
        """
        dept_response = self.llm.invoke(dept_prompt)
        department = dept_response.content

        # Step 2: get document checklist via RAG
        doc_query = f"What documents are required for grievance related to {department}?"
        retriever_result = retriever.invoke(doc_query)
        docs_context = "\n".join([d.page_content for d in retriever_result])

        checklist_prompt = f"""
        Based on this context: {docs_context}
        List the documents a citizen needs to file a complaint with {department}.
        """
        checklist_response = self.llm.invoke(checklist_prompt)
        checklist = checklist_response.content

        # Step 3: generate complaint letter — all inline, no separation
        letter_prompt = f"""
        Write a formal complaint letter to {department} regarding: "{issue}"
        Include placeholders for citizen name, address, and date.
        Format it professionally.
        """
        letter_response = self.llm.invoke(letter_prompt)
        letter = letter_response.content

        # Step 4: next steps
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
        # [S8] LONG METHOD — profile serialisation, retrieval, reasoning all inline
        # [S10] DUPLICATE LOGIC — retriever created AGAIN (3rd time)
        # [S6] GOD CLASS — scheme matching has nothing to do with RAG pipeline

        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 8}  # [S2] magic number
        )

        # Serialise profile inline — no helper method
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

        Based on the profile, list every welfare scheme this citizen is eligible for.
        For each scheme mention:
        1. Scheme name
        2. Why they are eligible
        3. How to apply

        Be specific and accurate.
        """

        response = self.llm.invoke(reasoning_prompt)
        return response.content
backend/rag/rag_pipeline.py

