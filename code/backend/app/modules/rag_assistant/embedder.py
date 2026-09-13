"""
Module VietnameseEmbedder cho RAG Assistant.
Sử dụng mô hình 'dangvantuan/vietnamese-embedding' (768 chiều).
"""

import os
import logging
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class VietnameseEmbedder:
    def __init__(self, model_name: str = "dangvantuan/vietnamese-embedding"):
        self.model_name = model_name
        logger.info(f"Đang nạp mô hình Embedding: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.model.max_seq_length = 256
        logger.info(f"Nạp mô hình {model_name} thành công (max_seq_length=256)!")

    def embed_text(self, text: str) -> List[float]:
        """Tạo vector embedding (768 dimensions) cho 1 chuỗi văn bản."""
        if not text or not text.strip():
            return []
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Nhận danh sách các Child Chunks, tính toán embedding cho nội dung của từng chunk,
        và trả về danh sách chunks mới chứa trường 'embedding'.
        """
        logger.info(f"Đang tiến hành embedding cho {len(chunks)} chunks...")
        contents = [c.get("content", "") for c in chunks]
        embeddings = self.model.encode(contents, batch_size=16, show_progress_bar=True, convert_to_numpy=True)
        
        embedded_chunks = []
        for chunk, emb in zip(chunks, embeddings):
            chunk_copy = dict(chunk)
            chunk_copy["embedding"] = emb.tolist()
            embedded_chunks.append(chunk_copy)
            
        logger.info(f"Hoàn tất embedding {len(embedded_chunks)} chunks!")
        return embedded_chunks
