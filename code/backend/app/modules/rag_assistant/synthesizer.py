"""
Module MultiContextSynthesizer cho RAG Assistant (Kiến trúc KH-06 Nâng cấp).
Tổng hợp đa ngữ cảnh và sinh câu trả lời streaming token-by-token.
"""

import logging
from typing import AsyncGenerator
from app.core.llm import llm_service
from app.modules.rag_assistant.prompts import MULTI_CONTEXT_SYNTHESIZER_PROMPT_KH06
from app.modules.rag_assistant.schemas import AggregatedContext

logger = logging.getLogger(__name__)

class MultiContextSynthesizerService:
    def __init__(self):
        self.llm = llm_service

    async def stream_synthesize(self, aggregated_context: AggregatedContext) -> AsyncGenerator[str, None]:
        """
        Nạp aggregated_contexts và standalone_query vào Prompt 2, stream câu trả lời về cho Client.
        """
        prompt = (
            MULTI_CONTEXT_SYNTHESIZER_PROMPT_KH06
            .replace("{aggregated_contexts}", aggregated_context.merged_context_text)
            .replace("{standalone_query}", aggregated_context.standalone_query)
        )


        logger.info(f"Bắt đầu stream tổng hợp câu trả lời cho query: '{aggregated_context.standalone_query}'")
        async for token in self.llm.stream_text(prompt):
            yield token

synthesizer_service = MultiContextSynthesizerService()
