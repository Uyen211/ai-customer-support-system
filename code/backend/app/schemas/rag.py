"""
Schemas và DTOs cho RAG Assistant (Kiến trúc KH-06 Nâng cấp).
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any

class SubQueryItem(BaseModel):
    id: int = Field(..., description="ID định danh duy nhất của sub-query")
    query: str = Field(..., description="Chuỗi câu hỏi nhỏ nguyên tử đã giải quyết đại từ")
    intent: Literal["SQL_PRODUCT", "VECTOR_KNOWLEDGE", "OUT_OF_DOMAIN", "GREETING_CHITCHAT", "HUMAN_AGENT_REQUEST"] = Field(
        ..., description="Phân loại ý định của sub-query"
    )
    target_source: Literal["SQL_PRODUCT", "VECTOR_KNOWLEDGE", "NONE"] = Field(
        default="NONE", description="Nguồn dữ liệu cần tra cứu"
    )
    product_search_keyword: Optional[str] = Field(None, description="Từ khóa tên sản phẩm hoặc thuộc tính (nếu là SQL_PRODUCT)")
    pet_type: Optional[str] = Field(None, description="Loại thú cưng: DOG, CAT, BIRD, SMALL_PET")
    category: Optional[str] = Field(None, description="Danh mục sản phẩm: Thức ăn, Vệ sinh, Đồ chơi, Phụ kiện, Chăm sóc")
    brand: Optional[str] = Field(None, description="Thương hiệu sản phẩm: Royal Canin, PetKit, Kong, Bio Pet, Cature...")
    size: Optional[str] = Field(None, description="Kích thước/Size: S, M, L, XL...")
    weight_volume: Optional[str] = Field(None, description="Trọng lượng hoặc thể tích: 2kg, 10L, 500ml...")
    price_max: Optional[float] = Field(None, description="Mức giá tối đa yêu cầu (VNĐ)")
    price_min: Optional[float] = Field(None, description="Mức giá tối thiểu yêu cầu (VNĐ)")
    in_stock_only: Optional[bool] = Field(None, description="Chỉ lọc sản phẩm còn hàng trong kho")


class DecomposerOutputSchema(BaseModel):
    standalone_query: str = Field(..., description="Câu hỏi tổng đã giải quyết đồng tham chiếu")
    reasoning: str = Field(..., description="Lý do phân loại và bẻ câu hỏi")
    is_complex: bool = Field(default=False, description="True nếu câu hỏi chứa nhiều hơn 1 sub-query")
    sub_queries: List[SubQueryItem] = Field(default_factory=list, description="Danh sách các sub-queries")

class CitationItem(BaseModel):
    document_name: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    content_snippet: str

class SubQueryResult(BaseModel):
    sub_query_id: int
    intent: str
    target_source: str
    query: str
    retrieved_content: str
    citations: List[CitationItem] = Field(default_factory=list)

class AggregatedContext(BaseModel):
    standalone_query: str
    sub_query_results: List[SubQueryResult] = Field(default_factory=list)
    merged_context_text: str = ""
    all_citations: List[CitationItem] = Field(default_factory=list)

class ChatStreamRequest(BaseModel):
    conversation_id: str
    message: str

class ChatMessageResponse(BaseModel):
    id: str
    conversation_id: str
    sender_type: str
    content: str
    citations: Optional[List[Dict[str, Any]]] = None
