"""
Bộ tổng hợp đa ngữ cảnh (Multi-Context Synthesizer) & SSE Stream Generator.
"""

import logging
from typing import AsyncGenerator, Dict, Any, Optional, List
from app.core.llm import get_llm_service
from app.schemas.rag import AggregatedContext
from app.services.rag.prompts import MULTI_CONTEXT_SYNTHESIZER_PROMPT_KH06

logger = logging.getLogger(__name__)

class MultiContextSynthesizerService:
    """Service tạo câu trả lời tổng hợp và stream token về client."""

    def __init__(self):
        self.llm = get_llm_service()

    async def generate_response_stream(
        self,
        aggregated_context: AggregatedContext,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> AsyncGenerator[str, None]:
        logger.info(f"Đang sinh câu trả lời tổng hợp cho query: '{aggregated_context.standalone_query}'")

        history_str = "None"
        if chat_history and len(chat_history) > 0:
            history_lines = []
            for msg in chat_history[-6:]:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                history_lines.append(f"{role.upper()}: {content}")
            history_str = "\n".join(history_lines)

        prompt = MULTI_CONTEXT_SYNTHESIZER_PROMPT_KH06.format(
            aggregated_contexts=aggregated_context.merged_context_text,
            chat_history=history_str,
            user_query=aggregated_context.standalone_query
        )

        # Stream từng token từ LLM
        async for token in self.llm.generate_stream(prompt):
            yield token

synthesizer_service = MultiContextSynthesizerService()
