"""
Parallel Retrieval Workers cho RAG Assistant (Kiến trúc KH-06 Nâng cấp).
Bao gồm: SQLProductRetriever, VectorKnowledgeRetriever (Supabase pgvector HNSW),
OutOfDomainHandler và ParallelRetrievalService.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, text

from app.core.database import SessionLocal
from app.core.config import settings
from app.common.models import Product, KnowledgeChunk
from app.modules.rag_assistant.embedder import VietnameseEmbedder
from app.modules.rag_assistant.schemas import (
    SubQueryItem,
    SubQueryResult,
    CitationItem,
    AggregatedContext
)

logger = logging.getLogger(__name__)

# Khởi tạo singleton embedder (768 dimensions)
_embedder_instance = None

def get_embedder() -> VietnameseEmbedder:
    global _embedder_instance
    if _embedder_instance is None:
        _embedder_instance = VietnameseEmbedder(model_name=settings.EMBEDDING_MODEL_NAME)
    return _embedder_instance

class SQLProductRetriever:
    """Tra cứu thông tin sản phẩm và tồn kho real-time từ CSDL quan hệ."""
    
    @staticmethod
    def retrieve(sub_query: SubQueryItem, db: Session) -> SubQueryResult:
        logger.info(f"[SQL Worker] Tra cứu sản phẩm cho sub-query #{sub_query.id}: '{sub_query.query}'")
        try:
            query_builder = db.query(Product)
            
            # Lọc theo từ khóa tên hoặc sku
            if sub_query.product_search_keyword:
                kw = f"%{sub_query.product_search_keyword.strip()}%"
                query_builder = query_builder.filter(
                    or_(
                        Product.name.ilike(kw),
                        Product.sku.ilike(kw),
                        Product.description.ilike(kw)
                    )
                )
            
            # Lọc theo loại thú cưng
            if sub_query.pet_type:
                query_builder = query_builder.filter(
                    or_(
                        Product.pet_type == sub_query.pet_type,
                        Product.pet_type == "ALL"
                    )
                )
                
            # Lọc theo danh mục
            if sub_query.category:
                query_builder = query_builder.filter(Product.category.ilike(f"%{sub_query.category}%"))

            products = query_builder.limit(5).all()

            if not products:
                # Tìm kiếm nới lỏng nếu không tìm thấy
                if sub_query.product_search_keyword:
                    words = sub_query.product_search_keyword.strip().split()
                    if len(words) > 1:
                        kw_first = f"%{words[0]}%"
                        products = db.query(Product).filter(Product.name.ilike(kw_first)).limit(3).all()

            if not products:
                retrieved_text = f"Không tìm thấy sản phẩm phù hợp với từ khóa '{sub_query.product_search_keyword or sub_query.query}' trong kho hàng hiện tại."
            else:
                lines = ["Tìm thấy các sản phẩm phù hợp trong CSDL Kho hàng:"]
                for p in products:
                    price_str = f"{int(p.price):,}đ"
                    sale_str = f" (Giá KM: {int(p.sale_price):,}đ)" if p.sale_price else ""
                    stock_str = f"Tồn kho: {p.stock_quantity} ({p.status})"
                    attr_str = f" - Thuộc tính: {p.attributes}" if p.attributes else ""
                    lines.append(f"- **{p.name}** [Mã SKU: {p.sku}] - Giá: {price_str}{sale_str} - {stock_str}{attr_str}")
                retrieved_text = "\n".join(lines)

            return SubQueryResult(
                sub_query_id=sub_query.id,
                intent=sub_query.intent,
                target_source="SQL_PRODUCT",
                query=sub_query.query,
                retrieved_content=retrieved_text,
                citations=[]
            )
        except Exception as e:
            logger.error(f"[SQL Worker] Lỗi truy vấn DB: {e}")
            return SubQueryResult(
                sub_query_id=sub_query.id,
                intent=sub_query.intent,
                target_source="SQL_PRODUCT",
                query=sub_query.query,
                retrieved_content=f"Lỗi tra cứu CSDL Sản phẩm: {str(e)}",
                citations=[]
            )

class VectorKnowledgeRetriever:
    """Tra cứu Vector pgvector HNSW trên Supabase PostgreSQL (Không dùng score threshold)."""
    
    @staticmethod
    def retrieve(sub_query: SubQueryItem, db: Session, top_k: int = 3) -> SubQueryResult:
        logger.info(f"[Vector Worker] Tra cứu pgvector cho sub-query #{sub_query.id}: '{sub_query.query}'")
        try:
            embedder = get_embedder()
            query_vector = embedder.embed_text(sub_query.query)
            
            if not query_vector:
                return SubQueryResult(
                    sub_query_id=sub_query.id,
                    intent=sub_query.intent,
                    target_source="VECTOR_KNOWLEDGE",
                    query=sub_query.query,
                    retrieved_content="Không thể tạo vector cho câu hỏi rỗng.",
                    citations=[]
                )

            # Truy vấn pgvector Cosine Distance trên Supabase
            # Sử dụng cú pháp native hoặc raw SQL với HNSW index
            vector_str = f"[{','.join(str(x) for x in query_vector)}]"
            sql_query = text("""
                SELECT id, document_name, content, metadata
                FROM knowledge_chunks
                ORDER BY embedding <=> (:query_vector)::vector
                LIMIT :limit_k;
            """)
            
            result = db.execute(sql_query, {"query_vector": vector_str, "limit_k": top_k}).fetchall()

            if not result:
                retrieved_text = "Không tìm thấy đoạn trích tài liệu chính sách/hướng dẫn phù hợp trong cơ sở tri thức."
                citations = []
            else:
                lines = ["Tìm thấy các đoạn trích tài liệu & chính sách liên quan:"]
                citations = []
                for row in result:
                    doc_name = row[1]
                    content = row[2]
                    metadata = row[3] or {}
                    lines.append(f"--- [Tài liệu: {doc_name}] ---\n{content}\n")
                    citations.append(CitationItem(
                        document_name=doc_name,
                        metadata=metadata,
                        content_snippet=content[:200] + "..." if len(content) > 200 else content
                    ))
                retrieved_text = "\n".join(lines)

            return SubQueryResult(
                sub_query_id=sub_query.id,
                intent=sub_query.intent,
                target_source="VECTOR_KNOWLEDGE",
                query=sub_query.query,
                retrieved_content=retrieved_text,
                citations=citations
            )
        except Exception as e:
            logger.error(f"[Vector Worker] Lỗi truy vấn pgvector: {e}")
            return SubQueryResult(
                sub_query_id=sub_query.id,
                intent=sub_query.intent,
                target_source="VECTOR_KNOWLEDGE",
                query=sub_query.query,
                retrieved_content=f"Lỗi tra cứu CSDL Vector: {str(e)}",
                citations=[]
            )

class OutOfDomainHandler:
    """Xử lý các câu hỏi nằm ngoài phạm vi hoạt động của cửa hàng đồ dùng thú cưng."""
    
    @staticmethod
    def handle(sub_query: SubQueryItem) -> SubQueryResult:
        logger.info(f"[OOD Handler] Xử lý câu hỏi ngoài phạm vi #{sub_query.id}: '{sub_query.query}'")
        retrieved_text = (
            f"LƯU Ý NGHIỆP VỤ (OUT OF DOMAIN): Câu hỏi '{sub_query.query}' nằm ngoài phạm vi kinh doanh của PetHome "
            "(PetHome chuyên cung cấp thức ăn, phụ kiện, cát vệ sinh và đồ dùng thú cưng; không bán động vật/thú sống "
            "và không cung cấp dịch vụ thú y/phẫu thuật điều trị). "
            "HÃY giải thích lịch sự điều này cho khách hàng và chủ động hỏi xem khách hàng có muốn kết nối với Nhân viên CSKH để được hỗ trợ chuyên sâu không."
        )
        return SubQueryResult(
            sub_query_id=sub_query.id,
            intent="OUT_OF_DOMAIN",
            target_source="NONE",
            query=sub_query.query,
            retrieved_content=retrieved_text,
            citations=[]
        )

class ChitchatHandler:
    @staticmethod
    def handle(sub_query: SubQueryItem) -> SubQueryResult:
        return SubQueryResult(
            sub_query_id=sub_query.id,
            intent="GREETING_CHITCHAT",
            target_source="NONE",
            query=sub_query.query,
            retrieved_content="Đây là lời chào hỏi / xã giao. Hãy gửi lời chào nồng nhiệt và sẵn sàng hỗ trợ khách hàng mua sắm hoặc giải đáp chính sách.",
            citations=[]
        )

class HumanAgentHandler:
    @staticmethod
    def handle(sub_query: SubQueryItem) -> SubQueryResult:
        return SubQueryResult(
            sub_query_id=sub_query.id,
            intent="HUMAN_AGENT_REQUEST",
            target_source="NONE",
            query=sub_query.query,
            retrieved_content="Khách hàng yêu cầu gặp tư vấn viên trực tiếp. Hãy thông báo hệ thống đang chuyển tiếp và mời khách hàng chờ trong giây lát.",
            citations=[]
        )

class ParallelRetrievalService:
    """Bộ điều phối thực thi song song tất cả các Sub-queries."""

    async def execute_parallel(self, sub_queries: List[SubQueryItem], standalone_query: str) -> AggregatedContext:
        loop = asyncio.get_running_loop()
        tasks = []

        for sq in sub_queries:
            if sq.intent == "SQL_PRODUCT" or sq.target_source == "SQL_PRODUCT":
                tasks.append(loop.run_in_executor(None, self._run_sql_worker, sq))
            elif sq.intent == "VECTOR_KNOWLEDGE" or sq.target_source == "VECTOR_KNOWLEDGE":
                tasks.append(loop.run_in_executor(None, self._run_vector_worker, sq))
            elif sq.intent == "OUT_OF_DOMAIN":
                tasks.append(asyncio.to_thread(OutOfDomainHandler.handle, sq))
            elif sq.intent == "GREETING_CHITCHAT":
                tasks.append(asyncio.to_thread(ChitchatHandler.handle, sq))
            elif sq.intent == "HUMAN_AGENT_REQUEST":
                tasks.append(asyncio.to_thread(HumanAgentHandler.handle, sq))
            else:
                # Mặc định gọi vector worker
                tasks.append(loop.run_in_executor(None, self._run_vector_worker, sq))

        logger.info(f"Bắt đầu thực thi song song {len(tasks)} sub-query tasks...")
        results = await asyncio.gather(*tasks, return_exceptions=False)
        
        # Gom ngữ cảnh
        merged_blocks = []
        all_citations = []

        for res in results:
            merged_blocks.append(f"=== [SUB-QUERY #{res.sub_query_id} (Intent: {res.intent})]: '{res.query}' ===\n{res.retrieved_content}\n")
            if res.citations:
                all_citations.extend(res.citations)

        aggregated = AggregatedContext(
            standalone_query=standalone_query,
            sub_query_results=results,
            merged_context_text="\n".join(merged_blocks),
            all_citations=all_citations
        )
        logger.info(f"Hoàn thành gom ngữ cảnh: {len(all_citations)} trích dẫn thu thập được.")
        return aggregated

    def _run_sql_worker(self, sq: SubQueryItem) -> SubQueryResult:
        db: Session = SessionLocal()
        try:
            return SQLProductRetriever.retrieve(sq, db)
        finally:
            db.close()

    def _run_vector_worker(self, sq: SubQueryItem) -> SubQueryResult:
        db: Session = SessionLocal()
        try:
            return VectorKnowledgeRetriever.retrieve(sq, db, top_k=settings.RAG_TOP_K)
        finally:
            db.close()

parallel_retrieval_service = ParallelRetrievalService()
