import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from gradio_client import Client
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

embedder = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index(os.path.join(DATA_DIR, "vinebot.index"))

with open(os.path.join(DATA_DIR, "vinebot_docs.pkl"), "rb") as f:
    docs = pickle.load(f)


client = Client("exzort/Vinebot-Mistral-Private-Space")


# Context retrieval using FAISS

def retrieve_context(query, top_k=3):

    query_vec = embedder.encode([query])
    distances, indices = index.search(query_vec, top_k)
    retrieved = [docs[i] for i in indices[0]]
    return "\n".join(retrieved)



def generate_answer(query, context=None):

    if context is None:
        context = retrieve_context(query)

    prompt = f"""
You are VineBot, an AI assistant trained on the Blessed Vineyard Ministry Manual.
Use the context below to answer truthfully and concisely.
Do NOT add new dialogue, user questions, or repeat the question.

Context:
{context}

Question:
{query}

Final Answer:
"""

    try:
        result = client.predict(
            message=prompt,
            api_name="/predict"
        )

        cleaned = re.sub(r"(?i)\b(User:|Question:|Q:|Answer:|Final Answer:)\b", "", result).strip()

        # Prevent the model from echoing the prompt or question text exactly
        cleaned = cleaned.replace(query, "").strip()

        return cleaned or result.strip()

    except Exception as e:
        return f"⚠️ Error generating response: {str(e)}"
