"""
RAG Lab Config & Data Loader Module
Path: code/backend/rag_lab/config.py
"""

import os
import sys
import json
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

sys.stdout.reconfigure(encoding='utf-8')

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("RAG_Lab")

# Determine Paths
RAG_LAB_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(RAG_LAB_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(BACKEND_DIR))
ENV_PATH = os.path.join(PROJECT_ROOT, "code", ".env")

if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    load_dotenv()

# Gemini API Key Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")
if not GEMINI_API_KEY:
    logger.warning("⚠️ No GEMINI_API_KEY found in environment variables!")

# Import Google GenAI SDK (google.genai)
_GENAI_CLIENT = None
try:
    from google import genai
    if GEMINI_API_KEY:
        _GENAI_CLIENT = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    logger.error(f"Error loading google.genai: {e}")

def generate_llm_response(prompt: str, model_name: str = "gemini-3.1-flash-lite") -> str:
    """Helper to generate text using Gemini API (gemini-3.1-flash-lite)."""
    if _GENAI_CLIENT is not None:
        models_to_try = [model_name, "gemini-3.5-flash-lite", "gemini-3.6-flash", "gemini-2.5-flash-lite"]
        for m in models_to_try:
            try:
                res = _GENAI_CLIENT.models.generate_content(model=m, contents=prompt)
                if res and hasattr(res, 'text') and res.text:
                    return res.text
            except Exception as e:
                logger.debug(f"Model {m} failed: {e}")
                continue
    # Legacy fallback if client is None
    try:
        import google.generativeai as genai_legacy
        genai_legacy.configure(api_key=GEMINI_API_KEY)
        m = genai_legacy.GenerativeModel("gemini-1.5-flash")
        res = m.generate_content(prompt)
        return res.text if res else ""
    except Exception as e:
        logger.error(f"LLM Generation Error: {e}")
        return ""



# Data File Paths
PRODUCTS_FILE = os.path.join(PROJECT_ROOT, "docs", "rag", "processed", "products_relational.json")
PREPARED_CHUNKS_FILE = os.path.join(PROJECT_ROOT, "docs", "rag", "processed", "knowledge_chunks_prepared.json")
EMBEDDED_CHUNKS_FILE = os.path.join(PROJECT_ROOT, "docs", "rag", "processed", "embedded_chunks.json")

# Global Cache
_PRODUCTS = None
_CHUNKS = None
_EMBEDDED_CHUNKS = None
_EMBEDDER = None
_SUPABASE_CONN_STR = None

def get_supabase_db_url() -> str:
    global _SUPABASE_CONN_STR
    if _SUPABASE_CONN_STR is None:
        db_url = os.getenv("DATABASE_URL", "")
        if db_url.startswith("postgresql+psycopg2://"):
            db_url = db_url.replace("postgresql+psycopg2://", "postgres://")
        _SUPABASE_CONN_STR = db_url
    return _SUPABASE_CONN_STR

def query_supabase_products() -> List[Dict[str, Any]]:
    """Query products directly from Supabase PostgreSQL database table."""
    conn_str = get_supabase_db_url()
    if not conn_str:
        return []
    try:
        import psycopg2
        conn = psycopg2.connect(conn_str, connect_timeout=5)
        cur = conn.cursor()
        cur.execute("SELECT sku, name, category, pet_type, price, stock_quantity, status, attributes, description FROM products")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        products = []
        for r in rows:
            products.append({
                "sku": r[0],
                "name": r[1],
                "category": r[2],
                "pet_type": r[3],
                "price": float(r[4]) if r[4] is not None else 0,
                "stock_quantity": r[5],
                "status": r[6],
                "attributes": r[7] if r[7] is not None else {},
                "description": r[8] if r[8] is not None else ""
            })
        return products
    except Exception as e:
        logger.warning(f"⚠️ Supabase PostgreSQL query failed, using fallback JSON: {e}")
        return []

def load_products() -> List[Dict[str, Any]]:
    global _PRODUCTS
    if _PRODUCTS is None:
        # Try loading directly from Supabase DB first
        _PRODUCTS = query_supabase_products()
        if not _PRODUCTS:
            if os.path.exists(PRODUCTS_FILE):
                with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
                    _PRODUCTS = json.load(f)
            else:
                _PRODUCTS = []
    return _PRODUCTS

def get_embedder():
    global _EMBEDDER
    if _EMBEDDER is None:
        sys.path.append(os.path.join(BACKEND_DIR, "app", "modules", "rag_assistant"))
        try:
            from embedder import VietnameseEmbedder
            _EMBEDDER = VietnameseEmbedder("dangvantuan/vietnamese-embedding")
        except Exception as e:
            logger.error(f"Failed to load VietnameseEmbedder: {e}")
            _EMBEDDER = None
    return _EMBEDDER

def load_embedded_chunks() -> List[Dict[str, Any]]:
    global _EMBEDDED_CHUNKS
    if _EMBEDDED_CHUNKS is None:
        if os.path.exists(EMBEDDED_CHUNKS_FILE):
            with open(EMBEDDED_CHUNKS_FILE, "r", encoding="utf-8") as f:
                _EMBEDDED_CHUNKS = json.load(f)
        else:
            logger.info("Generating embedded chunks from prepared chunks...")
            if os.path.exists(PREPARED_CHUNKS_FILE):
                with open(PREPARED_CHUNKS_FILE, "r", encoding="utf-8") as f:
                    chunks = json.load(f)
                embedder = get_embedder()
                if embedder:
                    _EMBEDDED_CHUNKS = embedder.embed_chunks(chunks)
                    with open(EMBEDDED_CHUNKS_FILE, "w", encoding="utf-8") as f:
                        json.dump(_EMBEDDED_CHUNKS, f, ensure_ascii=False, indent=2)
                else:
                    _EMBEDDED_CHUNKS = chunks
            else:
                _EMBEDDED_CHUNKS = []
    return _EMBEDDED_CHUNKS

def vector_search(query_text: str, top_k: int = 3, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
    """
    Performs cosine similarity vector search over embedded chunks.
    Returns list of dicts: {'rank', 'score', 'document_name', 'content', 'metadata'}.
    """
    embedded_chunks = load_embedded_chunks()
    embedder = get_embedder()
    if not embedded_chunks or not embedder:
        return []

    q_vec = embedder.embed_text(query_text)
    doc_vectors = np.array([c["embedding"] for c in embedded_chunks])
    
    sims = cosine_similarity([q_vec], doc_vectors)[0]
    top_indices = np.argsort(sims)[::-1][:top_k]

    results = []
    for rank, idx in enumerate(top_indices, 1):
        score = float(sims[idx])
        if score >= score_threshold:
            chunk = embedded_chunks[idx]
            results.append({
                "rank": rank,
                "score": score,
                "document_name": chunk.get("document_name"),
                "content": chunk.get("content"),
                "metadata": chunk.get("metadata")
            })
    return results
