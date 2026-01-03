import os
from typing import List
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import json
from pathlib import Path

# This module provides a small wrapper around Chroma to store label passages and a
# helper `ask_drug` that returns retrieved passages or uses an LLM if an OpenAI key is present.

class DrugRetriever:
    def __init__(self, data_dir: str = "data/labels", persist_directory: str = None):
        self.data_dir = Path(data_dir)
        # allow overriding via env var CHROMA_PERSIST_DIR
        self.persist_directory = persist_directory or os.getenv("CHROMA_PERSIST_DIR", "./chromadb")
        self._client = None
        self._store = None
        try:
            # prefer sentence-transformers pre-trained miniLM model
            self._emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        except Exception:
            # fallback to model name only if the package mapping differs
            self._emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        if self.data_dir.exists():
            self._ensure_store()

    def _load_documents(self) -> List[Document]:
        docs = []
        if not self.data_dir.exists():
            return docs
        for p in self.data_dir.glob("*.json"):
            with open(p, "r", encoding="utf-8") as f:
                j = json.load(f)
            text = j.get("text", "")
            meta = {"drug": j.get("drug_name"), "source": str(p)}
            docs.append(Document(page_content=text, metadata=meta))
        return docs

    def _ensure_store(self):
        docs = self._load_documents()
        if not docs:
            return
        self._store = Chroma.from_documents(docs, self._emb, persist_directory=self.persist_directory)

    def rebuild(self):
        # call after adding documents
        self._ensure_store()

    def _retrieve(self, query: str, k: int = 3):
        if not self._store:
            return []
        results = self._store.similarity_search(query, k=k)
        return results

    def ask_drug(self, question: str, top_k: int = 3) -> str:
        # Use OpenAI LLM only if API key is present and a Chroma store exists.
        openai_key = os.getenv("OPENAI_API_KEY")
        passages = self._retrieve(question, k=top_k)
        if not passages:
            return "No indexed labels found. Run the ingestion script to index sample labels and call POST /api/rebuild_index."
        if openai_key and self._store:
            try:
                from langchain.chat_models import ChatOpenAI
                from langchain.chains import RetrievalQA
                llm = ChatOpenAI(temperature=0, openai_api_key=openai_key)
                qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=self._store.as_retriever())
                resp = qa.run(question)
                return resp
            except Exception:
                # fall back to returning passages
                pass
        # Default: return the top_k passages concatenated
        out = "\n\n".join([f"Source: {p.metadata.get('source')}\n\n{p.page_content}" for p in passages])
        return out
