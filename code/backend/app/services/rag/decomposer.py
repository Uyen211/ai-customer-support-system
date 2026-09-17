"""
Bộ bẻ câu hỏi (Query Decomposer) và Định tuyến Ý định (Intent Router) tích hợp cho RAG KH-06.
"""

import json
import logging
from typing import List, Dict, Any, Optional
from app.core.llm import get_llm_service
from app.schemas.rag import DecomposerOutputSchema, SubQueryItem
from app.services.rag.prompts import MERGED_DECOMPOSER_PROMPT_KH06

logger = logging.getLogger(__name__)

class QueryDecomposerService:
    """Service chịu trách nhiệm giải quyết đại từ, phân tách sub-queries và gắn nhãn intent."""

    def __init__(self):
        self.llm = get_llm_service()

    async def decompose(self, query: str, chat_history: Optional[List[Dict[str, str]]] = None) -> DecomposerOutputSchema:
        logger.info(f"Đang bẻ câu hỏi và phân intent cho: '{query}'")
        
        history_str = "None"
        if chat_history and len(chat_history) > 0:
            history_lines = []
            for msg in chat_history[-6:]:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                history_lines.append(f"{role.upper()}: {content}")
            history_str = "\n".join(history_lines)

        prompt = MERGED_DECOMPOSER_PROMPT_KH06.format(
            chat_history=history_str,
            user_query=query
        )

        try:
            # Gọi LLM sinh phản hồi JSON
            json_response = await self.llm.generate_json(prompt)
            
            # Parse vào Pydantic Schema
            output = DecomposerOutputSchema(**json_response)
            
            # Đảm bảo luôn có ít nhất 1 sub-query
            if not output.sub_queries:
                output.sub_queries = [
                    SubQueryItem(
                        id=1,
                        query=output.standalone_query or query,
                        intent="VECTOR_KNOWLEDGE",
                        target_source="VECTOR_KNOWLEDGE"
                    )
                ]
            
            logger.info(f"Kết quả Decomposer: {len(output.sub_queries)} sub-queries, is_complex={output.is_complex}")
            return output

        except Exception as e:
            logger.error(f"Lỗi trong quá trình Decomposer: {e}. Sử dụng fallback.")
            return DecomposerOutputSchema(
                standalone_query=query,
                reasoning="Fallback do lỗi phân tích LLM",
                is_complex=False,
                sub_queries=[
                    SubQueryItem(
                        id=1,
                        query=query,
                        intent="VECTOR_KNOWLEDGE",
                        target_source="VECTOR_KNOWLEDGE"
                    )
                ]
            )

decomposer_service = QueryDecomposerService()
