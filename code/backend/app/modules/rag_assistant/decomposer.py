"""
Module Decomposer cho RAG Assistant (Kiến trúc KH-06 Nâng cấp).
Giải quyết đồng tham chiếu, bẻ câu hỏi và gán Intent/Target Source độc lập per sub-query.
"""

import logging
from typing import List, Dict, Any, Optional
from app.core.llm import llm_service
from app.modules.rag_assistant.prompts import MERGED_DECOMPOSER_PROMPT_KH06
from app.modules.rag_assistant.schemas import DecomposerOutputSchema, SubQueryItem

logger = logging.getLogger(__name__)

class QueryDecomposerService:
    def __init__(self):
        self.llm = llm_service

    async def decompose(self, user_query: str, chat_history: Optional[List[Dict[str, Any]]] = None) -> DecomposerOutputSchema:
        """
        Tiếp nhận câu hỏi và lịch sử chat, gọi LLM phân tích, trả về DecomposerOutputSchema.
        """
        # Định dạng chat_history
        history_str = "None"
        if chat_history:
            formatted_history = []
            for msg in chat_history[-6:]:
                role = msg.get("sender_type", "USER")
                content = msg.get("content", "")
                formatted_history.append(f"{role}: {content}")
            history_str = "\n".join(formatted_history)

        prompt = (
            MERGED_DECOMPOSER_PROMPT_KH06
            .replace("{chat_history}", history_str)
            .replace("{user_query}", user_query)
        )


        logger.info(f"Bắt đầu phân tích Decomposer cho query: '{user_query}'")
        raw_json = await self.llm.generate_json(prompt)
        
        try:
            # Validate qua Pydantic
            decomposer_output = DecomposerOutputSchema(**raw_json)
            logger.info(f"Phân tích thành công: is_complex={decomposer_output.is_complex}, {len(decomposer_output.sub_queries)} sub-queries")
            return decomposer_output
        except Exception as e:
            logger.error(f"Lỗi validate DecomposerOutputSchema: {e}. Raw JSON: {raw_json}")
            # Fallback tạo 1 subquery an toàn
            return DecomposerOutputSchema(
                standalone_query=user_query,
                reasoning="Fallback due to schema validation error",
                is_complex=False,
                sub_queries=[
                    SubQueryItem(
                        id=1,
                        query=user_query,
                        intent="VECTOR_KNOWLEDGE",
                        target_source="VECTOR_KNOWLEDGE"
                    )
                ]
            )

decomposer_service = QueryDecomposerService()
