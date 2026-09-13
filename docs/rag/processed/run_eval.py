"""
Wrapper script để chạy RAG Embedding & Evaluation từ thư mục docs/rag/processed/
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
RAG_MODULE_DIR = os.path.join(BASE_DIR, "code", "backend", "app", "modules", "rag_assistant")

sys.path.append(RAG_MODULE_DIR)

from run_rag_eval import run_evaluation

if __name__ == "__main__":
    run_evaluation()
