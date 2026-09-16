"""
Comprehensive Test Suite for RAG Assistant Module (KH-06 Architecture).
Tests Decomposer, SQL Product Retriever, Vector Knowledge Retriever (pgvector HNSW),
OutOfDomain Handler, Pipeline Orchestrator, and FastAPI SSE Stream Endpoint.
"""

import pytest
import asyncio
import json
from unittest.mock import patch, MagicMock
import httpx

from app.main import app
from app.modules.rag_assistant.schemas import (
    SubQueryItem,
    DecomposerOutputSchema,
    CitationItem,
    AggregatedContext
)
from app.modules.rag_assistant.decomposer import decomposer_service
from app.modules.rag_assistant.retrievers import (
    SQLProductRetriever,
    VectorKnowledgeRetriever,
    OutOfDomainHandler,
    parallel_retrieval_service
)
from app.modules.rag_assistant.pipeline import rag_pipeline_service
from app.common.models import Product, KnowledgeChunk

client = httpx.Client(transport=httpx.ASGITransport(app=app), base_url="http://test")

# ==============================================================================
# 1. TEST GATE 1: DECOMPOSER SUB-QUERIES & INTENTS (SPEC-RAG-01)
# ==============================================================================
@pytest.mark.asyncio
async def test_decomposer_subqueries_and_intents():
    """Kiểm tra Decomposer bẻ câu hỏi thành sub-queries và gán Intent chính xác."""
    complex_query = "Cát vệ sinh Cature giá bao nhiêu, phí ship thế nào và shop có bán mèo con không?"
    
    mock_decomposer_json = {
        "standalone_query": complex_query,
        "reasoning": "Query contains product price, shipping policy, and out-of-domain live animal inquiry.",
        "is_complex": True,
        "sub_queries": [
            {
                "id": 1,
                "query": "Giá cát vệ sinh Cature",
                "intent": "SQL_PRODUCT",
                "target_source": "SQL_PRODUCT",
                "product_search_keyword": "Cature",
                "pet_type": "CAT",
                "category": "Vệ sinh"
            },
            {
                "id": 2,
                "query": "Chính sách và phí vận chuyển giao hàng",
                "intent": "VECTOR_KNOWLEDGE",
                "target_source": "VECTOR_KNOWLEDGE",
                "product_search_keyword": None,
                "pet_type": None,
                "category": None
            },
            {
                "id": 3,
                "query": "Shop có bán mèo con không",
                "intent": "OUT_OF_DOMAIN",
                "target_source": "NONE",
                "product_search_keyword": None,
                "pet_type": "CAT",
                "category": None
            }
        ]
    }

    with patch.object(decomposer_service.llm, "generate_json", return_value=mock_decomposer_json):
        result = await decomposer_service.decompose(complex_query)

        assert isinstance(result, DecomposerOutputSchema)
        assert result.is_complex is True
        assert len(result.sub_queries) == 3
        
        # Kiểm tra Sub-query 1: SQL_PRODUCT
        assert result.sub_queries[0].intent == "SQL_PRODUCT"
        assert result.sub_queries[0].target_source == "SQL_PRODUCT"
        assert result.sub_queries[0].product_search_keyword == "Cature"

        # Kiểm tra Sub-query 2: VECTOR_KNOWLEDGE
        assert result.sub_queries[1].intent == "VECTOR_KNOWLEDGE"
        assert result.sub_queries[1].target_source == "VECTOR_KNOWLEDGE"

        # Kiểm tra Sub-query 3: OUT_OF_DOMAIN
        assert result.sub_queries[2].intent == "OUT_OF_DOMAIN"
        assert result.sub_queries[2].target_source == "NONE"


# ==============================================================================
# 2. TEST GATE 2: SQL PRODUCT CATALOG LOOKUP (SPEC-RAG-02)
# ==============================================================================
def test_sql_product_catalog_retrieval():
    """Kiểm tra SQL Product Worker truy vấn đúng giá và tồn kho sản phẩm."""
    mock_db = MagicMock()
    mock_product = MagicMock()
    mock_product.sku = "CAT-CATURE-6L"
    mock_product.name = "Cát vệ sinh Cature Tofu 6L"
    mock_product.price = 145000.0
    mock_product.sale_price = None
    mock_product.stock_quantity = 25
    mock_product.status = "IN_STOCK"
    mock_product.attributes = {"volume": "6L", "scent": "Original"}

    mock_db.query.return_value.filter.return_value.limit.return_value.all.return_value = [mock_product]

    sq = SubQueryItem(
        id=1,
        query="Cát Cature giá bao nhiêu",
        intent="SQL_PRODUCT",
        target_source="SQL_PRODUCT",
        product_search_keyword="Cature",
        pet_type="CAT",
        category="Vệ sinh"
    )

    result = SQLProductRetriever.retrieve(sq, mock_db)
    assert result.sub_query_id == 1
    assert result.target_source == "SQL_PRODUCT"
    assert "Cát vệ sinh Cature Tofu 6L" in result.retrieved_content
    assert "145,000đ" in result.retrieved_content
    assert "Tồn kho: 25" in result.retrieved_content


# ==============================================================================
# 3. TEST GATE 3: VECTOR PGVECTOR RETRIEVAL (NO SCORE THRESHOLD) (SPEC-RAG-03)
# ==============================================================================
def test_pgvector_hnsw_retrieval():
    """Kiểm tra Vector Worker truy vấn pgvector HNSW trên Supabase không bị chặn bởi score threshold."""
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchall.return_value = [
        (
            "chunk-1",
            "Chinh_sach_van_chuyen.pdf",
            "Miễn phí vận chuyển nội thành cho đơn hàng từ 500.000đ trở lên.",
            {"page": 2, "policy_code": "PET-CS-003"}
        ),
        (
            "chunk-2",
            "Chinh_sach_van_chuyen.pdf",
            "Thời gian giao hàng tiêu chuẩn từ 1-2 ngày làm việc.",
            {"page": 3, "policy_code": "PET-CS-003"}
        )
    ]

    sq = SubQueryItem(
        id=2,
        query="Chính sách phí ship giao hàng",
        intent="VECTOR_KNOWLEDGE",
        target_source="VECTOR_KNOWLEDGE"
    )

    with patch("app.modules.rag_assistant.retrievers.get_embedder") as mock_embedder_func:
        mock_embedder = MagicMock()
        mock_embedder.embed_text.return_value = [0.1] * 768
        mock_embedder_func.return_value = mock_embedder

        result = VectorKnowledgeRetriever.retrieve(sq, mock_db, top_k=2)

        assert result.sub_query_id == 2
        assert result.target_source == "VECTOR_KNOWLEDGE"
        assert len(result.citations) == 2
        assert result.citations[0].document_name == "Chinh_sach_van_chuyen.pdf"
        assert "500.000đ" in result.retrieved_content


# ==============================================================================
# 4. TEST GATE 4: OUT OF DOMAIN FALLBACK PER SUB-QUERY (SPEC-RAG-04)
# ==============================================================================
def test_out_of_domain_fallback_handling():
    """Kiểm tra xử lý Out-of-Domain sinh thông báo ngoài phạm vi + đề xuất kết nối CSKH."""
    sq = SubQueryItem(
        id=3,
        query="Shop có dịch vụ phẫu thuật tiêm phòng thú y tại nhà không",
        intent="OUT_OF_DOMAIN",
        target_source="NONE"
    )

    result = OutOfDomainHandler.handle(sq)
    assert result.sub_query_id == 3
    assert result.intent == "OUT_OF_DOMAIN"
    assert "OUT OF DOMAIN" in result.retrieved_content
    assert "PetHome chuyên cung cấp thức ăn, phụ kiện" in result.retrieved_content
    assert "Nhân viên CSKH" in result.retrieved_content


# ==============================================================================
# 5. TEST GATE 5: PARALLEL RETRIEVAL EXECUTION
# ==============================================================================
@pytest.mark.asyncio
async def test_parallel_retrieval_service():
    """Kiểm tra ParallelRetrievalService điều phối đồng thời các sub-query workers."""
    sub_queries = [
        SubQueryItem(
            id=1,
            query="Giá cát Cature",
            intent="SQL_PRODUCT",
            target_source="SQL_PRODUCT",
            product_search_keyword="Cature"
        ),
        SubQueryItem(
            id=2,
            query="Chính sách đổi trả trong mấy ngày",
            intent="VECTOR_KNOWLEDGE",
            target_source="VECTOR_KNOWLEDGE"
        ),
        SubQueryItem(
            id=3,
            query="Shop có bán voi con không",
            intent="OUT_OF_DOMAIN",
            target_source="NONE"
        )
    ]

    with patch.object(SQLProductRetriever, "retrieve") as mock_sql, \
         patch.object(VectorKnowledgeRetriever, "retrieve") as mock_vec:
        
        mock_sql.return_value = MagicMock(sub_query_id=1, intent="SQL_PRODUCT", query="Giá cát", retrieved_content="Cát Cature: 145.000đ", citations=[])
        mock_vec.return_value = MagicMock(sub_query_id=2, intent="VECTOR_KNOWLEDGE", query="Đổi trả", retrieved_content="Đổi trả trong 7 ngày", citations=[CitationItem(document_name="ChinhSachDoiTra.pdf", metadata={}, content_snippet="Đổi trả trong 7 ngày")])

        aggregated = await parallel_retrieval_service.execute_parallel(sub_queries, "Query tổng hợp")

        assert isinstance(aggregated, AggregatedContext)
        assert len(aggregated.sub_query_results) == 3
        assert len(aggregated.all_citations) == 1
        assert "Cát Cature: 145.000đ" in aggregated.merged_context_text
        assert "Đổi trả trong 7 ngày" in aggregated.merged_context_text
        assert "OUT OF DOMAIN" in aggregated.merged_context_text


# ==============================================================================
# 6. TEST GATE 6: SSE CHAT STREAM ENDPOINT (SPEC-RAG-05)
# ==============================================================================
def test_sse_chat_stream_endpoint():
    """Kiểm tra Endpoint /api/chat/stream trả về text/event-stream và chunk token."""
    conv_id = "10000000-0000-0000-0000-000000000001"
    
    async def mock_stream_pipeline(conv_id, msg):
        yield {"event": "token", "data": {"token": "Chào bạn! "}}
        yield {"event": "token", "data": {"token": "PetHome xin hỗ trợ bạn."}}
        yield {"event": "done", "data": {"full_text": "Chào bạn! PetHome xin hỗ trợ bạn.", "citations": []}}

    with patch.object(rag_pipeline_service, "stream_chat_pipeline", side_effect=mock_stream_pipeline):
        response = client.post(
            "/api/chat/stream",
            json={"conversation_id": conv_id, "message": "Xin chào shop"}
        )
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]
        body = response.text
        assert "event: token" in body
        assert "Chào bạn!" in body
        assert "event: done" in body

def test_rag_health_check_endpoint():
    """Kiểm tra Endpoint /api/chat/health."""
    response = client.get("/api/chat/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["module"] == "RAG Assistant KH-06"
