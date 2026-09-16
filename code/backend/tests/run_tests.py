"""
Test Runner using standard Python unittest and httpx AsyncClient.
"""

import unittest
import asyncio
import json
import sys
import os
from unittest.mock import patch, MagicMock

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from app.main import app
from app.modules.rag_assistant.schemas import (
    SubQueryItem,
    SubQueryResult,
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

class TestRAGPipeline(unittest.TestCase):

    def test_01_decomposer_subqueries_and_intents(self):
        """SPEC-RAG-01: Kiểm tra Decomposer bẻ câu hỏi thành sub-queries và gán Intent chính xác."""
        complex_query = "Cát vệ sinh Cature giá bao nhiêu, phí ship thế nào và shop có bán mèo con không?"
        mock_json = {
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

        with patch.object(decomposer_service.llm, "generate_json", return_value=mock_json):
            result = asyncio.run(decomposer_service.decompose(complex_query))
            self.assertIsInstance(result, DecomposerOutputSchema)
            self.assertTrue(result.is_complex)
            self.assertEqual(len(result.sub_queries), 3)
            self.assertEqual(result.sub_queries[0].intent, "SQL_PRODUCT")
            self.assertEqual(result.sub_queries[1].intent, "VECTOR_KNOWLEDGE")
            self.assertEqual(result.sub_queries[2].intent, "OUT_OF_DOMAIN")

    def test_02_sql_product_catalog_retrieval(self):
        """SPEC-RAG-02: Kiểm tra SQL Product Worker truy vấn đúng giá và tồn kho sản phẩm."""
        mock_db = MagicMock()
        mock_product = MagicMock()
        mock_product.sku = "CAT-CATURE-6L"
        mock_product.name = "Cát vệ sinh Cature Tofu 6L"
        mock_product.price = 145000.0
        mock_product.sale_price = None
        mock_product.stock_quantity = 25
        mock_product.status = "IN_STOCK"
        mock_product.attributes = {"volume": "6L", "scent": "Original"}

        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [mock_product]

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
        self.assertEqual(result.sub_query_id, 1)
        self.assertEqual(result.target_source, "SQL_PRODUCT")
        self.assertIn("Cát vệ sinh Cature Tofu 6L", result.retrieved_content)
        self.assertIn("145,000đ", result.retrieved_content)
        self.assertIn("Tồn kho: 25", result.retrieved_content)

    def test_03_pgvector_hnsw_retrieval(self):
        """SPEC-RAG-03: Kiểm tra Vector Worker truy vấn pgvector HNSW trên Supabase (Không dùng score threshold)."""
        mock_db = MagicMock()
        mock_db.execute.return_value.fetchall.return_value = [
            (
                "chunk-1",
                "Chinh_sach_van_chuyen.pdf",
                "Miễn phí vận chuyển nội thành cho đơn hàng từ 500.000đ trở lên.",
                {"page": 2, "policy_code": "PET-CS-003"}
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

            result = VectorKnowledgeRetriever.retrieve(sq, mock_db, top_k=1)
            self.assertEqual(result.sub_query_id, 2)
            self.assertEqual(result.target_source, "VECTOR_KNOWLEDGE")
            self.assertEqual(len(result.citations), 1)
            self.assertEqual(result.citations[0].document_name, "Chinh_sach_van_chuyen.pdf")
            self.assertIn("500.000đ", result.retrieved_content)

    def test_04_out_of_domain_fallback_handling(self):
        """SPEC-RAG-04: Kiểm tra xử lý Out-of-Domain sinh thông báo ngoài phạm vi + đề xuất kết nối CSKH."""
        sq = SubQueryItem(
            id=3,
            query="Shop có dịch vụ phẫu thuật tiêm phòng thú y tại nhà không",
            intent="OUT_OF_DOMAIN",
            target_source="NONE"
        )

        result = OutOfDomainHandler.handle(sq)
        self.assertEqual(result.sub_query_id, 3)
        self.assertEqual(result.intent, "OUT_OF_DOMAIN")
        self.assertIn("OUT OF DOMAIN", result.retrieved_content)
        self.assertIn("PetHome chuyên cung cấp thức ăn, phụ kiện", result.retrieved_content)
        self.assertIn("Nhân viên CSKH", result.retrieved_content)

    def test_05_parallel_retrieval_service(self):
        """Kiểm tra ParallelRetrievalService điều phối song song."""
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
                query="Shop có bán voi con không",
                intent="OUT_OF_DOMAIN",
                target_source="NONE"
            )
        ]

        with patch.object(SQLProductRetriever, "retrieve") as mock_sql:
            mock_sql.return_value = SubQueryResult(
                sub_query_id=1,
                intent="SQL_PRODUCT",
                target_source="SQL_PRODUCT",
                query="Giá cát",
                retrieved_content="Cát Cature: 145.000đ",
                citations=[]
            )

            aggregated = asyncio.run(parallel_retrieval_service.execute_parallel(sub_queries, "Query tổng hợp"))
            self.assertIsInstance(aggregated, AggregatedContext)
            self.assertEqual(len(aggregated.sub_query_results), 2)
            self.assertIn("Cát Cature: 145.000đ", aggregated.merged_context_text)
            self.assertIn("OUT OF DOMAIN", aggregated.merged_context_text)

    def test_06_sse_chat_stream_endpoint(self):
        """SPEC-RAG-05: Kiểm tra Endpoint /api/chat/stream trả về text/event-stream và token chunk."""
        conv_id = "10000000-0000-0000-0000-000000000001"
        
        async def mock_stream_pipeline(conversation_id, user_message):
            yield {"event": "token", "data": {"token": "Chào bạn! "}}
            yield {"event": "token", "data": {"token": "PetHome xin hỗ trợ bạn."}}
            yield {"event": "done", "data": {"full_text": "Chào bạn! PetHome xin hỗ trợ bạn.", "citations": []}}


        async def run_client():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                with patch.object(rag_pipeline_service, "stream_chat_pipeline", side_effect=mock_stream_pipeline):
                    response = await ac.post(
                        "/api/chat/stream",
                        json={"conversation_id": conv_id, "message": "Xin chào shop"}
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertIn("text/event-stream", response.headers["content-type"])
                    body = response.text
                    self.assertIn("event: token", body)
                    self.assertIn("Chào bạn!", body)
                    self.assertIn("event: done", body)

        asyncio.run(run_client())

    def test_07_rag_health_check_endpoint(self):
        """Kiểm tra Endpoint /api/chat/health."""
        async def run_client():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.get("/api/chat/health")
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertEqual(data["status"], "online")
                self.assertEqual(data["module"], "RAG Assistant KH-06")

        asyncio.run(run_client())

if __name__ == "__main__":
    unittest.main()
