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

from app.db.session import SessionLocal
from app.core.config import settings
from app.models.product import Product
from app.models.knowledge_chunk import KnowledgeChunk
from app.services.rag.embedder import VietnameseEmbedder
from app.schemas.rag import (
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
    """Tra cứu thông tin sản phẩm, thuộc tính JSONB và tồn kho real-time từ CSDL quan hệ."""
    
    @staticmethod
    def retrieve(sub_query: SubQueryItem, db: Session) -> SubQueryResult:
        logger.info(f"[SQL Worker] Tra cứu sản phẩm cho sub-query #{sub_query.id}: '{sub_query.query}'")
        try:
            query_builder = db.query(Product)
            
            # Lọc theo từ khóa (Tên, SKU, Mô tả, Danh mục, hoặc thuộc tính JSONB)
            if sub_query.product_search_keyword:
                kw = f"%{sub_query.product_search_keyword.strip()}%"
                query_builder = query_builder.filter(
                    or_(
                        Product.name.ilike(kw),
                        Product.sku.ilike(kw),
                        Product.description.ilike(kw),
                        Product.category.ilike(kw),
                        text("CAST(attributes AS TEXT) ILIKE :kw").bindparams(kw=kw)
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

            # Lọc theo Thương hiệu (JSONB attributes->>'brand')
            if sub_query.brand:
                brand_kw = f"%{sub_query.brand.strip()}%"
                query_builder = query_builder.filter(
                    text("attributes->>'brand' ILIKE :brand_kw").bindparams(brand_kw=brand_kw)
                )

            # Lọc theo Kích thước (JSONB attributes->>'size')
            if sub_query.size:
                size_kw = f"%{sub_query.size.strip()}%"
                query_builder = query_builder.filter(
                    text("attributes->>'size' ILIKE :size_kw").bindparams(size_kw=size_kw)
                )

            # Lọc theo Trọng lượng / Thể tích (JSONB attributes)
            if sub_query.weight_volume:
                wv_kw = f"%{sub_query.weight_volume.strip()}%"
                query_builder = query_builder.filter(
                    text("CAST(attributes AS TEXT) ILIKE :wv_kw").bindparams(wv_kw=wv_kw)
                )

            # Lọc theo khoảng giá (price / sale_price)
            if sub_query.price_max is not None:
                query_builder = query_builder.filter(
                    or_(
                        Product.sale_price <= sub_query.price_max,
                        Product.price <= sub_query.price_max
                    )
                )
            if sub_query.price_min is not None:
                query_builder = query_builder.filter(Product.price >= sub_query.price_min)

            # Lọc theo tình trạng còn hàng
            if sub_query.in_stock_only:
                query_builder = query_builder.filter(Product.stock_quantity > 0, Product.status == "IN_STOCK")

            products = query_builder.limit(5).all()

            if not products:
                # Tìm kiếm nới lỏng nếu không tìm thấy
                if sub_query.product_search_keyword:
                    words = sub_query.product_search_keyword.strip().split()
                    if len(words) > 1:
                        kw_first = f"%{words[0]}%"
                        products = db.query(Product).filter(
                            or_(
                                Product.name.ilike(kw_first),
                                text("CAST(attributes AS TEXT) ILIKE :kw_first").bindparams(kw_first=kw_first)
                            )
                        ).limit(3).all()

            if not products:
                retrieved_text = f"Không tìm thấy sản phẩm phù hợp với từ khóa '{sub_query.product_search_keyword or sub_query.query}' trong kho hàng hiện tại."
            else:
                lines = ["Tìm thấy các sản phẩm phù hợp trong CSDL Kho hàng:"]
                for p in products:
                    price_str = f"{int(p.price):,}đ"
                    sale_str = f" (Giá KM: {int(p.sale_price):,}đ)" if p.sale_price else ""
                    stock_str = f"Tồn kho: {p.stock_quantity} ({p.status})"
                    
                    # Format thông tin thuộc tính chi tiết từ JSONB
                    attr_details = []
                    if p.attributes and isinstance(p.attributes, dict):
                        for k, v in p.attributes.items():
                            attr_details.append(f"{k}: {v}")
                    attr_formatted = f" | Thuộc tính: [{', '.join(attr_details)}]" if attr_details else ""
                    desc_formatted = f" | Mô tả: {p.description}" if p.description else ""

                    lines.append(f"- **{p.name}** [Mã SKU: {p.sku}] - Giá: {price_str}{sale_str} - {stock_str}{attr_formatted}{desc_formatted}")
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
            logger.error(f"Lỗi SQL Product Retrieval: {e}")
            return SubQueryResult(
                sub_query_id=sub_query.id,
                intent=sub_query.intent,
                target_source="SQL_PRODUCT",
                query=sub_query.query,
                retrieved_content="Không thể kiểm tra tồn kho và giá sản phẩm lúc này do lỗi hệ thống.",
                citations=[]
            )

class VectorKnowledgeRetriever:
    """Tra cứu tri thức tài liệu, chính sách từ Supabase PostgreSQL pgvector HNSW Index."""
    
    @staticmethod
    def retrieve(sub_query: SubQueryItem, db: Session, top_k: int = settings.RAG_TOP_K) -> SubQueryResult:
        logger.info(f"[Vector Worker] Tra cứu Vector pgvector cho sub-query #{sub_query.id}: '{sub_query.query}'")
        try:
            embedder = get_embedder()
            query_vector = embedder.encode(sub_query.query)

            # Supabase pgvector HNSW Cosine Distance search (Không dùng score threshold theo KH-06)
            sql_query = text("""
                SELECT 
                    id,
                    document_name,
                    content,
                    metadata,
                    1 - (embedding <=> :vector) AS similarity
                FROM knowledge_chunks
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> :vector ASC
                LIMIT :limit;
            """).bindparams(
                vector=str(query_vector),
                limit=top_k
            )

            results = db.execute(sql_query).fetchall()

            if not results:
                return SubQueryResult(
                    sub_query_id=sub_query.id,
                    intent=sub_query.intent,
                    target_source="VECTOR_KNOWLEDGE",
                    query=sub_query.query,
                    retrieved_content="Không tìm thấy tài liệu chính sách phù hợp trong cơ sở tri thức.",
                    citations=[]
                )

            citations = []
            content_blocks = []

            for row in results:
                chunk_id, doc_name, content, meta, sim = row
                content_blocks.append(f"[Tài liệu: {doc_name}]\n{content}")
                citations.append(
                    CitationItem(
                        document_name=doc_name or "Tài liệu PetHome",
                        metadata=meta if isinstance(meta, dict) else {},
                        content_snippet=content[:200] + "..." if len(content) > 200 else content
                    )
                )

            merged_text = "\n\n".join(content_blocks)

            return SubQueryResult(
                sub_query_id=sub_query.id,
                intent=sub_query.intent,
                target_source="VECTOR_KNOWLEDGE",
                query=sub_query.query,
                retrieved_content=merged_text,
                citations=citations
            )

        except Exception as e:
            logger.error(f"Lỗi Vector pgvector Retrieval: {e}")
            return SubQueryResult(
                sub_query_id=sub_query.id,
                intent=sub_query.intent,
                target_source="VECTOR_KNOWLEDGE",
                query=sub_query.query,
                retrieved_content="Không thể tra cứu cơ sở tri thức lúc này do lỗi kết nối vector database.",
                citations=[]
            )

class OutOfDomainHandler:
    """Xử lý các câu hỏi ngoài phạm vi nghiệp vụ và tạo phản hồi lịch sự + mời CSKH."""

    @staticmethod
    def handle(sub_query: SubQueryItem) -> SubQueryResult:
        logger.info(f"[OOD Handler] Xử lý sub-query ngoài phạm vi #{sub_query.id}: '{sub_query.query}'")
        
        explanation = (
            f"Về câu hỏi '{sub_query.query}': Cửa hàng PetHome chuyên cung cấp thức ăn, phụ kiện, dụng cụ chăm sóc "
            f"cho thú cưng (chó, mèo, chim, thú nhỏ), hiện không hỗ trợ dịch vụ hoặc sản phẩm này. "
            f"Nếu quý khách cần hỗ trợ thêm thông tin chi tiết, quý khách có muốn kết nối trực tiếp với nhân viên tư vấn không ạ?"
        )

        return SubQueryResult(
            sub_query_id=sub_query.id,
            intent=sub_query.intent,
            target_source="NONE",
            query=sub_query.query,
            retrieved_content=explanation,
            citations=[]
        )

class ParallelRetrievalService:
    """Service điều phối chạy song song các Retrieval Workers cho danh sách Sub-queries."""

    async def retrieve_all(self, sub_queries: List[SubQueryItem]) -> AggregatedContext:
        loop = asyncio.get_running_loop()
        tasks = []

        for sq in sub_queries:
            if sq.target_source == "SQL_PRODUCT":
                tasks.append(self._run_sql_worker(sq, loop))
            elif sq.target_source == "VECTOR_KNOWLEDGE":
                tasks.append(self._run_vector_worker(sq, loop))
            else: # OUT_OF_DOMAIN, GREETING, HUMAN_AGENT
                tasks.append(self._run_ood_worker(sq))

        results: List[SubQueryResult] = await asyncio.gather(*tasks)

        # Gom ngữ cảnh
        context_blocks = []
        all_citations = []

        for res in results:
            context_blocks.append(
                f"=== SUB-QUESTION {res.sub_query_id}: {res.query} (Nguồn: {res.target_source}, Intent: {res.intent}) ===\n"
                f"{res.retrieved_content}\n"
            )
            all_citations.extend(res.citations)

        return AggregatedContext(
            standalone_query="",
            sub_query_results=results,
            merged_context_text="\n".join(context_blocks),
            all_citations=all_citations
        )

    async def _run_sql_worker(self, sub_query: SubQueryItem, loop: asyncio.AbstractEventLoop) -> SubQueryResult:
        def _sync_work():
            db = SessionLocal()
            try:
                return SQLProductRetriever.retrieve(sub_query, db)
            finally:
                db.close()
        return await loop.run_in_executor(None, _sync_work)

    async def _run_vector_worker(self, sub_query: SubQueryItem, loop: asyncio.AbstractEventLoop) -> SubQueryResult:
        def _sync_work():
            db = SessionLocal()
            try:
                return VectorKnowledgeRetriever.retrieve(sub_query, db)
            finally:
                db.close()
        return await loop.run_in_executor(None, _sync_work)

    async def _run_ood_worker(self, sub_query: SubQueryItem) -> SubQueryResult:
        return OutOfDomainHandler.handle(sub_query)

parallel_retrieval_service = ParallelRetrievalService()
