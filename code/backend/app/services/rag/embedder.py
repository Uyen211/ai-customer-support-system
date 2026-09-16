"""
Module Vector Embedding tiếng Việt sử dụng mô hình 768 chiều.
Kiểm tra an toàn độ dài token trước khi thực hiện embedding.
"""

import logging
from typing import List
from sentence_transformers import SentenceTransformer
from app.core.config import settings

logger = logging.getLogger(__name__)

class VietnameseEmbedder:
    """Singleton Embedder phục vụ chuyển đổi text sang vector 768 chiều."""
    
    def __init__(self, model_name: str = settings.EMBEDDING_MODEL_NAME):
        logger.info(f"Đang khởi tạo VietnameseEmbedder với model: {model_name}")
        self.model_name = model_name
        # Tự động tải hoặc load model từ local cache
        self.model = SentenceTransformer(model_name)
        # Giới hạn độ dài tối đa an toàn của sequence
        self.max_seq_length = getattr(self.model, "max_seq_length", 256)

    def encode(self, text: str) -> List[float]:
        """
        Encode một đoạn văn bản thành vector embedding 768 chiều.
        Kiểm tra độ dài token trước khi đưa vào mô hình để tránh lỗi tràn ngữ cảnh.
        """
        if not text or not text.strip():
            return [0.0] * 768

        clean_text = text.strip()
        
        # Kiểm tra và cắt tỉa an toàn độ dài từ/token nếu văn bản quá dài
        words = clean_text.split()
        if len(words) > self.max_seq_length:
            logger.warning(f"Văn bản vượt quá ngưỡng an toàn ({len(words)} từ > {self.max_seq_length}). Đang tự động cắt tỉa.")
            clean_text = " ".join(words[:self.max_seq_length])

        vector = self.model.encode(clean_text, normalize_embeddings=True)
        return vector.tolist()

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Encode danh sách văn bản theo lô."""
        if not texts:
            return []
        
        trimmed_texts = []
        for t in texts:
            words = t.strip().split()
            if len(words) > self.max_seq_length:
                trimmed_texts.append(" ".join(words[:self.max_seq_length]))
            else:
                trimmed_texts.append(t.strip())

        vectors = self.model.encode(trimmed_texts, normalize_embeddings=True)
        return vectors.tolist()
