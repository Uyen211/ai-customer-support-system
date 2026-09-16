"""
LLM Client Service hỗ trợ Google Gemini (gemini-2.5-flash-lite, gemini-1.5-flash)
sử dụng thư viện chính thức google.genai với Structured Output JSON và Streaming SSE.
"""

import os
import json
import logging
import re
from typing import AsyncGenerator, Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

def get_api_key() -> str:
    """Lấy API Key từ config theo thứ tự ưu tiên."""
    return (
        settings.GEMINI_API_KEY
        or settings.GOOGLE_API_KEY
        or settings.OPENAI_API_KEY
        or os.getenv("GEMINI_API_KEY", "")
        or os.getenv("GOOGLE_API_KEY", "")
        or os.getenv("OPENAI_API_KEY", "")
    )

def extract_json_from_text(text: str) -> Dict[str, Any]:
    """Trích xuất JSON từ phản hồi LLM an toàn."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    text = text.strip()
    
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)
        
    return json.loads(text)

class GeminiLLMService:
    def __init__(self):
        self.api_key = get_api_key()
        self.model_name = settings.LLM_MODEL or "gemini-2.5-flash-lite"
        self._genai_client = None
        self._init_client()

    def _init_client(self):
        if not self.api_key:
            logger.warning("Chưa cấu hình GEMINI_API_KEY hoặc OPENAI_API_KEY. LLM sẽ chạy chế độ Mock/Fallback.")
            return

        try:
            from google import genai
            self._genai_client = genai.Client(api_key=self.api_key)
            logger.info(f"Khởi tạo google.genai Client thành công với model: {self.model_name}")
        except Exception as e:
            try:
                import google.generativeai as legacy_genai
                legacy_genai.configure(api_key=self.api_key)
                self._genai_client = legacy_genai
                logger.info(f"Khởi tạo legacy google.generativeai thành công với model: {self.model_name}")
            except Exception as legacy_err:
                logger.error(f"Lỗi khởi tạo Google GenAI client: {e}, legacy: {legacy_err}")

    async def generate_json(self, prompt: str) -> Dict[str, Any]:
        """Gọi LLM và trả về JSON object."""
        if not self.api_key or not self._genai_client:
            logger.warning("Không có API Key, sử dụng Fallback JSON Decomposer.")
            return self._fallback_decompose(prompt)

        try:
            # Kiểm tra nếu là google.genai Client
            if hasattr(self._genai_client, "models"):
                from google.genai import types
                response = self._genai_client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(response_mime_type="application/json")
                )
                return extract_json_from_text(response.text)
            else:
                # Legacy GenerativeModel
                model = self._genai_client.GenerativeModel(
                    model_name=self.model_name,
                    generation_config={"response_mime_type": "application/json"}
                )
                response = model.generate_content(prompt)
                return extract_json_from_text(response.text)
        except Exception as e:
            logger.error(f"Lỗi gọi Gemini generate_json: {e}. Sử dụng Fallback parser.")
            return self._fallback_decompose(prompt)

    async def stream_text(self, prompt: str) -> AsyncGenerator[str, None]:
        """Gọi LLM và stream từng token text."""
        if not self.api_key or not self._genai_client:
            logger.warning("Không có API Key, streaming Fallback message.")
            for chunk in self._fallback_stream(prompt):
                yield chunk
            return

        try:
            if hasattr(self._genai_client, "models"):
                response = self._genai_client.models.generate_content_stream(
                    model=self.model_name,
                    contents=prompt
                )
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
            else:
                model = self._genai_client.GenerativeModel(model_name=self.model_name)
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
        except Exception as e:
            logger.error(f"Lỗi gọi Gemini stream_text: {e}. Streaming fallback error.")
            yield f"Dạ em xin lỗi, hệ thống AI tạm thời gặp gián đoạn ({str(e)}). Vui lòng thử lại sau giây lát ạ!"

    def _fallback_decompose(self, prompt: str) -> Dict[str, Any]:
        """Quy tắc heuristic bóc tách fallback khi không có API Key."""
        match = re.search(r"<user_query>\s*(.*?)\s*</user_query>", prompt, re.DOTALL)
        query = match.group(1).strip() if match else prompt

        sub_queries = []
        is_ood = any(w in query.lower() for w in ["mua chó", "mua mèo", "bán chó", "bán mèo", "heo", "bò", "tiêm phòng", "khám bệnh", "voi"])
        has_product = any(w in query.lower() for w in ["giá", "bao nhiêu", "tiền", "còn hàng", "cát", "pate", "hạt", "royal", "cature"])
        has_policy = any(w in query.lower() for w in ["đổi trả", "ship", "vận chuyển", "freeship", "thanh toán", "bảo hành"])

        if is_ood and (has_product or has_policy):
            sub_queries.append({
                "id": 1,
                "query": query,
                "intent": "SQL_PRODUCT" if has_product else "VECTOR_KNOWLEDGE",
                "target_source": "SQL_PRODUCT" if has_product else "VECTOR_KNOWLEDGE",
                "product_search_keyword": "Cature" if "cature" in query.lower() else None,
                "pet_type": "CAT" if "mèo" in query.lower() else "DOG" if "chó" in query.lower() else None,
                "category": "Vệ sinh" if "cát" in query.lower() else "Thức ăn" if "pate" in query.lower() or "hạt" in query.lower() else None
            })
            sub_queries.append({
                "id": 2,
                "query": "Câu hỏi ngoài phạm vi kinh doanh",
                "intent": "OUT_OF_DOMAIN",
                "target_source": "NONE",
                "product_search_keyword": None,
                "pet_type": None,
                "category": None
            })
            return {
                "standalone_query": query,
                "reasoning": "Heuristic decomposed into product/policy and out-of-domain sub-queries",
                "is_complex": True,
                "sub_queries": sub_queries
            }
        elif is_ood:
            return {
                "standalone_query": query,
                "reasoning": "Heuristic classified query as out of domain",
                "is_complex": False,
                "sub_queries": [{
                    "id": 1,
                    "query": query,
                    "intent": "OUT_OF_DOMAIN",
                    "target_source": "NONE",
                    "product_search_keyword": None,
                    "pet_type": None,
                    "category": None
                }]
            }
        elif has_product and has_policy:
            return {
                "standalone_query": query,
                "reasoning": "Heuristic decomposed into product and policy sub-queries",
                "is_complex": True,
                "sub_queries": [
                    {
                        "id": 1,
                        "query": f"Thông tin giá và tồn kho cho {query}",
                        "intent": "SQL_PRODUCT",
                        "target_source": "SQL_PRODUCT",
                        "product_search_keyword": "Cature" if "cature" in query.lower() else "Royal Canin" if "royal" in query.lower() else None,
                        "pet_type": "CAT" if "mèo" in query.lower() else "DOG" if "chó" in query.lower() else None,
                        "category": "Vệ sinh" if "cát" in query.lower() else "Thức ăn" if "hạt" in query.lower() or "pate" in query.lower() else None
                    },
                    {
                        "id": 2,
                        "query": f"Chính sách liên quan trong {query}",
                        "intent": "VECTOR_KNOWLEDGE",
                        "target_source": "VECTOR_KNOWLEDGE",
                        "product_search_keyword": None,
                        "pet_type": None,
                        "category": None
                    }
                ]
            }
        else:
            intent = "SQL_PRODUCT" if has_product else "VECTOR_KNOWLEDGE"
            return {
                "standalone_query": query,
                "reasoning": f"Single atomic query classified as {intent}",
                "is_complex": False,
                "sub_queries": [{
                    "id": 1,
                    "query": query,
                    "intent": intent,
                    "target_source": intent,
                    "product_search_keyword": None,
                    "pet_type": "CAT" if "mèo" in query.lower() else "DOG" if "chó" in query.lower() else None,
                    "category": "Vệ sinh" if "cát" in query.lower() else "Thức ăn" if "hạt" in query.lower() or "pate" in query.lower() else None
                }]
            }

    def _fallback_stream(self, prompt: str):
        """Fallback stream khi không có LLM connection."""
        yield "Dạ chào bạn! PetHome xin được hỗ trợ bạn:\n\n"
        yield "- Cửa hàng chuyên cung cấp thức ăn, cát vệ sinh và phụ kiện thú cưng chính hãng.\n"
        yield "- Đơn hàng từ 500.000đ được miễn phí vận chuyển nội thành.\n"
        yield "- Nếu bạn cần tư vấn thêm, nhân viên CSKH sẵn sàng hỗ trợ bạn ngay ạ!"

llm_service = GeminiLLMService()
