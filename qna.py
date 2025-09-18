# qna.py
import os
import requests
from typing import Dict, Any

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
MODEL = os.getenv('OLLAMA_MODEL', 'llama2')

class QnAEngine:
    def __init__(self):
        self.indexed_doc = None

    def index_document(self, extracted: Dict[str, Any]):
        self.indexed_doc = extracted

    def is_indexed(self):
        return self.indexed_doc is not None

    def answer_query(self, query: str) -> str:
        if not self.indexed_doc:
            raise RuntimeError("No document indexed")
        doc_text = self.indexed_doc.get('text','')[:5000]
        prompt = (
            "You are an assistant that answers questions about a company's financial statements. "
            "Use the provided document content to answer. If the answer cannot be found, say you don't know.\n\n"
            f"DOCUMENT:\n{doc_text}\n\nQUESTION: {query}\n\nAnswer concisely and cite the line or table when possible."
        )
        try:
            resp = requests.post(f"{OLLAMA_URL}/api/completions", json={
                "model": MODEL,
                "prompt": prompt,
                "max_tokens": 512,
            }, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            if 'choices' in data and len(data['choices'])>0:
                return data['choices'][0].get('message', data['choices'][0]).get('content', '') if isinstance(data['choices'][0].get('message',None), dict) else data['choices'][0].get('text', '')
            return data.get('text', str(data))
        except Exception as e:
            return f"Error calling Ollama: {e}"
