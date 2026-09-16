"""
RAG Retrievers Implementation Module (KH-01 to KH-08)
Path: code/backend/rag_lab/retrievers.py

NOTE: All strategies execute UP TO the completion of the RETRIEVAL step ONLY.
They DO NOT send retrieved contexts to an LLM for final generation.
"""

import sys
import time
import json
import re
from typing import List, Dict, Any

sys.stdout.reconfigure(encoding='utf-8')

from config import (
    generate_llm_response,
    load_products,
    vector_search,
    load_embedded_chunks
)

def parse_json_from_llm(text: str) -> Dict[str, Any]:
    """Helper to parse JSON output from Gemini response, stripping markdown backticks."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    try:
        return json.loads(text)
    except Exception as e:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
        return {}

def sql_product_search(keyword: str = None, category: str = None, pet_type: str = None) -> List[Dict[str, Any]]:
    """Helper simulating SQL search on products table (Supabase PostgreSQL or fallback JSON) with token-based matching."""
    products = load_products()
    matched = []
    
    if keyword:
        clean_kw = re.sub(r'^(cho mình hỏi|mình muốn|tìm|muốn mua|có bán|shop|tất cả|cần mua|giá|cho|xem)\s+', '', str(keyword), flags=re.IGNORECASE)
        clean_kw = clean_kw.strip(' "?!.,')
    else:
        clean_kw = None

    for p in products:
        if pet_type and str(pet_type).upper() not in ["ALL", "TẤT CẢ", "NONE", "NULL", "ANY"]:
            if p.get("pet_type") and p.get("pet_type").upper() != str(pet_type).upper() and p.get("pet_type").upper() != "ALL":
                continue
        if category and str(category) not in ["Tất cả", "ALL", "None", "Null", "Any"]:
            if p.get("category", "").lower() != str(category).lower():
                continue
                
        if clean_kw and clean_kw.strip():
            target_str = f"{p.get('name', '')} {p.get('sku', '')} {p.get('attributes', {}).get('brand', '')} {p.get('description', '')}".lower()
            kw_lower = clean_kw.lower().strip()
            
            if kw_lower in target_str:
                matched.append(p)
                continue
                
            stop_words = {"cho", "mèo", "chó", "bán", "giá", "bao", "nhiêu", "sẵn", "hàng", "không", "muốn", "mua", "dùng", "loại", "đó", "shop", "có", "nào", "gì", "thì"}
            tokens = [w for w in re.findall(r'\w+', kw_lower) if len(w) >= 2 and w not in stop_words]
            
            if tokens and all(t in target_str for t in tokens):
                matched.append(p)
                continue
            elif len(tokens) >= 2 and sum(1 for t in tokens if t in target_str) >= len(tokens) - 1:
                matched.append(p)
                continue
            else:
                continue
        else:
            matched.append(p)
            
    return matched

def build_final_context_str(sql_items: List[Dict[str, Any]], vector_chunks: List[Dict[str, Any]]) -> str:
    """Builds the exact context text string to be injected into {context} for LLM Generation."""
    parts = []
    
    if sql_items:
        # Deduplicate sql items by sku
        seen_skus = set()
        dedup_sql = []
        for item in sql_items:
            sku = item.get("sku")
            if sku not in seen_skus:
                seen_skus.add(sku)
                dedup_sql.append(item)
                
        parts.append("=== DỮ LIỆU SẢN PHẨM REAL-TIME (TỪ CSDL SUPABASE POSTGRESQL) ===")
        for p in dedup_sql:
            sku = p.get("sku", "N/A")
            name = p.get("name", "N/A")
            cat = p.get("category", "N/A")
            price = p.get("price", 0)
            stock = p.get("stock_quantity", 0)
            status = p.get("status", "N/A")
            parts.append(f"- SKU: {sku} | Tên: {name} | Danh mục: {cat} | Giá: {price:,.0f} VNĐ | Tồn kho: {stock} ({status})")
            
    if vector_chunks:
        # Deduplicate vector chunks
        seen_contents = set()
        dedup_vector = []
        for c in vector_chunks:
            cnt = c.get("content", "").strip()
            if cnt not in seen_contents:
                seen_contents.add(cnt)
                dedup_vector.append(c)
                
        parts.append("=== TRI THỨC VĂN BẢN TRÍCH XUẤT (TỪ VECTOR DATABASE) ===")
        for idx, c in enumerate(dedup_vector, 1):
            doc = c.get("document_name", "N/A")
            score = c.get("score", c.get("rrf_score", 0.0))
            content = c.get("content", "").strip()
            parts.append(f"[{idx}] (Doc: {doc}, Score: {score:.4f}):\n{content}")
            
    if not parts:
        return "(Không có dữ liệu context được trích xuất - Hệ thống nhận diện câu hỏi ngoài phạm vi hoặc ngắt luồng)"
        
    return "\n\n".join(parts)


# ============================================================================
# KH-01: Naive RAG (Baseline)
# ============================================================================
def retrieve_kh01(query: str, chat_history: List[Dict] = None) -> Dict[str, Any]:
    start_time = time.perf_counter()
    chunks = vector_search(query, top_k=3, score_threshold=0.0)
    latency_ms = (time.perf_counter() - start_time) * 1000
    
    llm_output = "N/A (Chạy trực tiếp Vector Search, không qua LLM Tiền xử lý)"
    raw_db_records = {"sql_items": [], "vector_chunks": chunks}
    final_context_prompt = build_final_context_str([], chunks)
    
    return {
        "plan_code": "KH-01",
        "plan_name": "Naive RAG (Baseline)",
        "query_used": query,
        "llm_output": llm_output,
        "raw_db_records": raw_db_records,
        "final_context_prompt": final_context_prompt,
        "retrieved_chunks": chunks,
        "latency_ms": round(latency_ms, 2)
    }

# ============================================================================
# KH-02: RAG + Score Thresholding (Threshold >= 0.65)
# ============================================================================
def retrieve_kh02(query: str, chat_history: List[Dict] = None) -> Dict[str, Any]:
    start_time = time.perf_counter()
    chunks = vector_search(query, top_k=3, score_threshold=0.65)
    max_score = chunks[0]["score"] if chunks else 0.0
    fallback_triggered = len(chunks) == 0
    latency_ms = (time.perf_counter() - start_time) * 1000
    
    llm_output = "N/A (Chạy trực tiếp Vector Search + Lọc Score >= 0.65, không qua LLM Tiền xử lý)"
    raw_db_records = {"sql_items": [], "vector_chunks": chunks}
    final_context_prompt = build_final_context_str([], chunks)
    
    return {
        "plan_code": "KH-02",
        "plan_name": "RAG + Score Thresholding (>=0.65)",
        "query_used": query,
        "max_score": round(max_score, 4),
        "fallback_triggered": fallback_triggered,
        "llm_output": llm_output,
        "raw_db_records": raw_db_records,
        "final_context_prompt": final_context_prompt,
        "retrieved_chunks": chunks,
        "latency_ms": round(latency_ms, 2)
    }

# ============================================================================
# KH-03: RAG + Contextual Query Rewriter
# ============================================================================
def retrieve_kh03(query: str, chat_history: List[Dict] = None) -> Dict[str, Any]:
    start_time = time.perf_counter()
    history_str = json.dumps(chat_history or [], ensure_ascii=False)
    prompt = f"""# ROLE & TASK
You are the Query Optimization Agent for PetHome. Analyze <chat_history> and <user_query>, resolve all coreferences/pronouns ("nó", "loại này", "cái đó"), and output a single, self-contained, dense search query in Vietnamese.

# CRITICAL CONSTRAINTS:
1. Output ONLY the raw search query string (e.g., "Cát vệ sinh PetKit Cat Litter 10L cho mèo con 2 tháng vón cục").
2. DO NOT include polite greetings, intro text ("Dưới đây là...", "Cho mình hỏi..."), options, quotes, or markdown wraps.

# CONVERSATION CONTEXT
<chat_history>
{history_str}
</chat_history>

# CURRENT INPUT
<user_query>
{query}
</user_query>
"""
    res_text = generate_llm_response(prompt)
    rewritten_query = res_text.strip().strip('"\'`') if res_text else query
    lines = [l.strip() for l in rewritten_query.split('\n') if l.strip() and not l.strip().startswith(('Dưới đây', 'Chào', 'Cho mình', 'Bạn có thể', '1.', '2.', '*'))]
    if lines:
        rewritten_query = lines[0].strip('"\'`')

    chunks = vector_search(rewritten_query, top_k=3, score_threshold=0.65)
    max_score = chunks[0]["score"] if chunks else 0.0
    fallback_triggered = len(chunks) == 0
    latency_ms = (time.perf_counter() - start_time) * 1000

    llm_output = res_text.strip() if res_text else "N/A"
    raw_db_records = {"sql_items": [], "vector_chunks": chunks}
    final_context_prompt = build_final_context_str([], chunks)

    return {
        "plan_code": "KH-03",
        "plan_name": "RAG + Contextual Query Rewriter",
        "original_query": query,
        "rewritten_query": rewritten_query,
        "max_score": round(max_score, 4),
        "fallback_triggered": fallback_triggered,
        "llm_output": llm_output,
        "raw_db_records": raw_db_records,
        "final_context_prompt": final_context_prompt,
        "retrieved_chunks": chunks,
        "latency_ms": round(latency_ms, 2)
    }

# ============================================================================
# KH-04: RAG + Intent Guardrail Router
# ============================================================================
def retrieve_kh04(query: str, chat_history: List[Dict] = None) -> Dict[str, Any]:
    start_time = time.perf_counter()
    history_str = json.dumps(chat_history or [], ensure_ascii=False)
    
    prompt = f"""# ROLE & TASK
You are the Multi-Task Pre-processor for PetHome Việt Nam. Perform TWO operations in a SINGLE pass:
1. COREFERENCE RESOLUTION: Rewrite <user_query> using <chat_history> into a self-contained dense search query in Vietnamese.
2. INTENT CLASSIFICATION: Categorize query into exactly one intent class based on domain scope.

# DOMAIN BOUNDARY SCOPE
1. STORE TYPE: Pet Supplies & Equipment Store (Food, litter, accessories, grooming tools. NO live animals sold).
2. SUPPORTED POLICIES: CSKH & Transfer, Returns & Refunds, Shipping, Payment.
3. SUPPORTED PRODUCT CATEGORIES: Thức ăn, Vệ sinh, Đồ chơi, Phụ kiện, Chăm sóc.
4. SUPPORTED PET TYPES: Dogs (Chó), Cats (Mèo), Birds (Chim), Small Pets (Thỏ, Hamster).
   - UNSUPPORTED: Livestock or wild animals (Bò, Ngựa, Trâu, Heo, Voi...).

# INTENT CLASSES
- GREETING_CHITCHAT: Greetings, thanks, farewells, compliments.
- OUT_OF_DOMAIN: Inquiries outside pet supplies (human clothes, weather) OR unsupported animals (Bò, Ngựa).
- HUMAN_AGENT_REQUEST: Explicit requests for human staff, severe complaints.
- PRODUCT_POLICY_QUERY: Questions about supported pet supplies, prices, stock, shipping, returns, payment, or care advice.

# INPUT
<chat_history>
{history_str}
</chat_history>

<user_query>
{query}
</user_query>

# OUTPUT FORMAT (STRICT JSON ONLY)
{{
  "standalone_query": "Clean dense search query without conversational fluff",
  "intent": "GREETING_CHITCHAT" | "OUT_OF_DOMAIN" | "HUMAN_AGENT_REQUEST" | "PRODUCT_POLICY_QUERY",
  "reasoning": "Brief sentence explaining decision"
}}
"""
    res_text = generate_llm_response(prompt)
    data = parse_json_from_llm(res_text)
    
    intent = data.get("intent", "PRODUCT_POLICY_QUERY")
    standalone_query = data.get("standalone_query", query)
    reasoning = data.get("reasoning", "")
    
    chunks = []
    fallback_triggered = False
    
    if intent == "PRODUCT_POLICY_QUERY":
        chunks = vector_search(standalone_query, top_k=3, score_threshold=0.65)
        fallback_triggered = len(chunks) == 0
        
    latency_ms = (time.perf_counter() - start_time) * 1000

    llm_output = res_text.strip() if res_text else "N/A"
    raw_db_records = {"sql_items": [], "vector_chunks": chunks}
    final_context_prompt = build_final_context_str([], chunks)

    return {
        "plan_code": "KH-04",
        "plan_name": "RAG + Intent Guardrail Router",
        "original_query": query,
        "intent": intent,
        "reasoning": reasoning,
        "standalone_query": standalone_query,
        "fallback_triggered": fallback_triggered,
        "llm_output": llm_output,
        "raw_db_records": raw_db_records,
        "final_context_prompt": final_context_prompt,
        "retrieved_chunks": chunks,
        "latency_ms": round(latency_ms, 2)
    }

# ============================================================================
# KH-05: Hybrid RAG + Direct SQL Catalog Lookup
# ============================================================================
def retrieve_kh05(query: str, chat_history: List[Dict] = None) -> Dict[str, Any]:
    start_time = time.perf_counter()
    history_str = json.dumps(chat_history or [], ensure_ascii=False)
    
    prompt = f"""# ROLE & TASK
You are the Multi-Task Hybrid Router for PetHome. Perform THREE operations in a SINGLE pass:
1. COREFERENCE RESOLUTION: Rewrite <user_query> using <chat_history> into a clean, dense search query.
2. INTENT CLASSIFICATION: Categorize query intent (GREETING_CHITCHAT, OUT_OF_DOMAIN, HUMAN_AGENT_REQUEST, PRODUCT_POLICY_QUERY).
3. SOURCE ROUTING & SQL PARAMETER EXTRACTION: `SQL_ONLY`, `VECTOR_ONLY`, `HYBRID_BOTH`, `OUT_OF_DOMAIN`.
   `product_search_keyword`: Extract clean product brand / SKU / title search keyword (e.g. "Royal Canin Indoor 2kg", "PetKit Cat Litter 10L", "PetKit 6L", "Bio Pet Shampoo 500ml"). Set null if pure policy question.

# INPUT
<chat_history>
{history_str}
</chat_history>

<user_query>
{query}
</user_query>

# OUTPUT FORMAT (STRICT JSON ONLY)
{{
  "standalone_query": "Clean dense search query without conversational fluff",
  "intent": "GREETING_CHITCHAT" | "OUT_OF_DOMAIN" | "HUMAN_AGENT_REQUEST" | "PRODUCT_POLICY_QUERY",
  "reasoning": "Brief sentence",
  "query_type": "SQL_ONLY" | "VECTOR_ONLY" | "HYBRID_BOTH" | "OUT_OF_DOMAIN",
  "product_search_keyword": "Clean product brand/title search keyword (or null)",
  "pet_type": "CAT" | "DOG" | "BIRD" | null,
  "category": "Thức ăn" | "Vệ sinh" | "Đồ chơi" | "Phụ kiện" | "Chăm sóc" | null
}}
"""
    res_text = generate_llm_response(prompt)
    data = parse_json_from_llm(res_text)
    
    intent = data.get("intent", "PRODUCT_POLICY_QUERY")
    query_type = data.get("query_type", "HYBRID_BOTH")
    standalone_query = data.get("standalone_query", query)
    kw = data.get("product_search_keyword")
    p_type = data.get("pet_type")
    cat = data.get("category")
    
    sql_results = []
    vector_results = []
    
    if query_type in ["SQL_ONLY", "HYBRID_BOTH"]:
        search_term = kw or standalone_query
        sql_results = sql_product_search(keyword=search_term, category=cat, pet_type=p_type)
        
    if query_type in ["VECTOR_ONLY", "HYBRID_BOTH"]:
        vector_results = vector_search(standalone_query, top_k=3, score_threshold=0.65)
        
    latency_ms = (time.perf_counter() - start_time) * 1000

    llm_output = res_text.strip() if res_text else "N/A"
    raw_db_records = {"sql_items": sql_results, "vector_chunks": vector_results}
    final_context_prompt = build_final_context_str(sql_results, vector_results)

    return {
        "plan_code": "KH-05",
        "plan_name": "Hybrid RAG + Direct SQL Catalog Lookup",
        "intent": intent,
        "query_type": query_type,
        "standalone_query": standalone_query,
        "sql_params": {"keyword": kw, "pet_type": p_type, "category": cat},
        "llm_output": llm_output,
        "raw_db_records": raw_db_records,
        "final_context_prompt": final_context_prompt,
        "retrieved_sql_products": sql_results,
        "retrieved_vector_chunks": vector_results,
        "latency_ms": round(latency_ms, 2)
    }

# ============================================================================
# KH-06: Hybrid RAG + Sub-query Decomposition
# ============================================================================
def retrieve_kh06(query: str, chat_history: List[Dict] = None) -> Dict[str, Any]:
    start_time = time.perf_counter()
    history_str = json.dumps(chat_history or [], ensure_ascii=False)
    
    prompt = f"""# ROLE & TASK
You are the Multi-Task Decomposer for PetHome. Analyze <chat_history> and <user_query>:
1. COREFERENCE RESOLUTION: Resolve all pronouns into explicit entities.
2. INTENT CLASSIFICATION: Categorize query intent (GREETING_CHITCHAT, OUT_OF_DOMAIN, HUMAN_AGENT_REQUEST, PRODUCT_POLICY_QUERY).
3. SUB-QUERY DECOMPOSITION: If query contains multiple distinct sub-questions (e.g. price/product AND shipping AND return policy), decompose into 2-3 focused atomic search queries with target source labels (`SQL_PRODUCT` vs `VECTOR_KNOWLEDGE`).

# CRITICAL CONSTRAINTS FOR SUB-QUERIES:
Each sub-query string in `sub_queries` MUST be a clean search query with core search terms (e.g. "Máy cho ăn tự động PetKit 6L", "Phí ship giao Cần Thơ", "Thời hạn đổi mới máy lỗi nguồn"), NOT polite conversational sentences.

# INPUT
<chat_history>
{history_str}
</chat_history>

<user_query>
{query}
</user_query>

# OUTPUT FORMAT (STRICT JSON ONLY)
{{
  "standalone_query": "Clean main search query",
  "intent": "GREETING_CHITCHAT" | "OUT_OF_DOMAIN" | "HUMAN_AGENT_REQUEST" | "PRODUCT_POLICY_QUERY",
  "reasoning": "Brief sentence",
  "is_complex": true,
  "sub_queries": [
    {{
      "id": 1,
      "query": "Clean atomic search query string",
      "target_source": "SQL_PRODUCT" | "VECTOR_KNOWLEDGE",
      "product_search_keyword": "Product keyword e.g. PetKit 6L or null",
      "pet_type": "CAT" | "DOG" | "BIRD" | null,
      "category": "Thức ăn" | "Vệ sinh" | "Đồ chơi" | "Phụ kiện" | "Chăm sóc" | null
    }}
  ]
}}
"""
    res_text = generate_llm_response(prompt)
    data = parse_json_from_llm(res_text)
    
    sub_queries = data.get("sub_queries", [])
    if not sub_queries:
        sub_queries = [{
            "id": 1,
            "query": data.get("standalone_query", query),
            "target_source": "VECTOR_KNOWLEDGE",
            "product_search_keyword": None,
            "pet_type": None,
            "category": None
        }]
        
    aggregated_retrievals = []
    all_sql_items = []
    all_vector_chunks = []
    
    for sq in sub_queries:
        sq_text = sq.get("query", query)
        target = sq.get("target_source", "VECTOR_KNOWLEDGE")
        if target == "SQL_PRODUCT":
            kw = sq.get("product_search_keyword") or sq_text
            p_type = sq.get("pet_type")
            cat = sq.get("category")
            p_res = sql_product_search(keyword=kw, category=cat, pet_type=p_type)
            all_sql_items.extend(p_res)
            aggregated_retrievals.append({
                "sub_query": sq_text,
                "target_source": "SQL_PRODUCT",
                "retrieved_products": p_res
            })
        else:
            c_res = vector_search(sq_text, top_k=3, score_threshold=0.60)
            all_vector_chunks.extend(c_res)
            aggregated_retrievals.append({
                "sub_query": sq_text,
                "target_source": "VECTOR_KNOWLEDGE",
                "retrieved_chunks": c_res
            })
            
    latency_ms = (time.perf_counter() - start_time) * 1000

    llm_output = res_text.strip() if res_text else "N/A"
    raw_db_records = {"sql_items": all_sql_items, "vector_chunks": all_vector_chunks}
    final_context_prompt = build_final_context_str(all_sql_items, all_vector_chunks)

    return {
        "plan_code": "KH-06",
        "plan_name": "Hybrid RAG + Sub-query Decomposition",
        "intent": data.get("intent", "PRODUCT_POLICY_QUERY"),
        "standalone_query": data.get("standalone_query", query),
        "is_complex": data.get("is_complex", len(sub_queries) > 1),
        "aggregated_retrievals": aggregated_retrievals,
        "llm_output": llm_output,
        "raw_db_records": raw_db_records,
        "final_context_prompt": final_context_prompt,
        "latency_ms": round(latency_ms, 2)
    }

# ============================================================================
# KH-07: Hybrid Search (Vector + BM25) + Re-ranker
# ============================================================================
def retrieve_kh07(query: str, chat_history: List[Dict] = None) -> Dict[str, Any]:
    start_time = time.perf_counter()
    history_str = json.dumps(chat_history or [], ensure_ascii=False)
    rw_prompt = f"""# ROLE & TASK
Query Optimizer for Hybrid Vector + BM25 Search. Analyze <chat_history> and <user_query>, resolve pronouns, and output ONLY a single clean dense search query in Vietnamese.

# CRITICAL CONSTRAINTS:
1. Output ONLY the raw search query string (e.g. "Cát vệ sinh PetKit Cat Litter 10L cho mèo con vón cục").
2. Absolute NO conversational intro text ("Dưới đây là..."), NO list of options, NO markdown wraps.

# INPUT
History: {history_str}
Query: {query}
"""
    rw_response = generate_llm_response(rw_prompt)
    standalone_query = rw_response.strip().strip('"\'`') if rw_response else query
    lines = [l.strip() for l in standalone_query.split('\n') if l.strip() and not l.strip().startswith(('Dưới đây', 'Chào', 'Cho mình', 'Bạn có thể', '1.', '2.', '*'))]
    if lines:
        standalone_query = lines[0].strip('"\'`')
    
    vector_candidates = vector_search(standalone_query, top_k=20, score_threshold=0.0)
    embedded_chunks = load_embedded_chunks()
    words = [w.lower() for w in re.findall(r'\w+', standalone_query.lower()) if len(w) >= 2]
    
    bm25_candidates = []
    for chunk in embedded_chunks:
        content_lower = chunk.get("content", "").lower()
        score = sum(content_lower.count(w) for w in words)
        if score > 0:
            bm25_candidates.append({"chunk": chunk, "bm25_score": score})
            
    bm25_candidates.sort(key=lambda x: x["bm25_score"], reverse=True)
    bm25_candidates = bm25_candidates[:20]

    rrf_scores = {}
    chunk_map = {}
    k = 60
    for rank, item in enumerate(vector_candidates, 1):
        c_id = item["document_name"] + "_" + str(hash(item["content"][:50]))
        chunk_map[c_id] = item
        rrf_scores[c_id] = rrf_scores.get(c_id, 0.0) + (1.0 / (k + rank))
        
    for rank, item in enumerate(bm25_candidates, 1):
        chunk = item["chunk"]
        c_id = chunk.get("document_name", "") + "_" + str(hash(chunk.get("content", "")[:50]))
        if c_id not in chunk_map:
            chunk_map[c_id] = {
                "document_name": chunk.get("document_name"),
                "content": chunk.get("content"),
                "metadata": chunk.get("metadata"),
                "score": 0.5
            }
        rrf_scores[c_id] = rrf_scores.get(c_id, 0.0) + (1.0 / (k + rank))
        
    sorted_cids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
    
    reranked = []
    for rank, c_id in enumerate(sorted_cids[:3], 1):
        item = chunk_map[c_id]
        item["rrf_rank"] = rank
        item["rrf_score"] = round(rrf_scores[c_id], 4)
        reranked.append(item)
        
    latency_ms = (time.perf_counter() - start_time) * 1000

    llm_output = rw_response.strip() if rw_response else "N/A"
    raw_db_records = {"sql_items": [], "vector_chunks": reranked}
    final_context_prompt = build_final_context_str([], reranked)

    return {
        "plan_code": "KH-07",
        "plan_name": "Hybrid Search (Vector + BM25) + Re-ranker",
        "standalone_query": standalone_query,
        "reranked_chunks": reranked,
        "llm_output": llm_output,
        "raw_db_records": raw_db_records,
        "final_context_prompt": final_context_prompt,
        "latency_ms": round(latency_ms, 2)
    }

# ============================================================================
# KH-08: Multi-Agent ReAct Architecture
# ============================================================================
def retrieve_kh08(query: str, chat_history: List[Dict] = None) -> Dict[str, Any]:
    start_time = time.perf_counter()
    history_str = json.dumps(chat_history or [], ensure_ascii=False)
    
    system_prompt = f"""# ROLE & TASK
You are the ReAct Master Planner Agent for PetHome Việt Nam - Chuỗi cửa hàng Đồ dùng Thú cưng. Your objective is to analyze customer queries, formulate a step-by-step reasoning trajectory (Thought), select and invoke appropriate Tools (Action), analyze execution results (Observation), and repeat until all facts are gathered.

# DOMAIN SCOPE & STORE INFORMATION
1. STORE TYPE: Pet Supplies & Equipment Store (Food, litter, accessories, grooming tools. NO live animals).
2. OFFICIAL POLICIES: CSKH & Transfer, Returns & Refunds, Shipping, Payment.
3. VECTOR KNOWLEDGE BASE: Policies AND Unstructured Product Chunks.
4. SQL PRODUCT CATALOG (Relational): Name, SKU, category, pet_type, price, sale_price, stock_quantity.
5. OFFICIAL PAYMENT & CHANNELS: Vietcombank STK 0123456789 | Owner: Công ty TNHH Thú Cưng PetHome Việt Nam. Zalo OA (Hotline: 0988.123.456) and Fanpage Facebook.

# AVAILABLE TOOLS
1. `tool_sql_product_catalog`: parameters {{"product_keyword": string|null, "category": string|null, "pet_type": string|null}}
2. `tool_vector_knowledge_search`: parameters {{"query_text": string, "knowledge_type": "POLICY_DOCS"|"PRODUCT_KNOWLEDGE"|"ALL"|null}}
3. `tool_official_security_payment`: parameters {{"request_type": "BANK_ACCOUNT_INFO"|"OFFICIAL_CHANNELS_INFO"}}
4. `tool_human_agent_transfer`: parameters {{"issue_category": string, "priority": "P1"|"P2"|"P3", "reason_summary": string}}

# REACT REASONING FORMAT
Thought: <reasoning step>
Action: <one of tool_sql_product_catalog, tool_vector_knowledge_search, tool_official_security_payment, tool_human_agent_transfer>
Action Input: <JSON payload for tool>

(When all facts are gathered)
Thought: I have gathered all necessary information.
Final Action: FINISH
Final Payload: Structured summary of all retrieved data facts.

# USER CONTEXT
<chat_history>
{history_str}
</chat_history>

<user_query>
{query}
</user_query>
"""
    react_steps = []
    collected_observations = []
    all_sql_items = []
    all_vector_chunks = []
    
    current_prompt = system_prompt
    max_turns = 3
    
    for turn in range(1, max_turns + 1):
        text = generate_llm_response(current_prompt)
        
        if "Final Action: FINISH" in text or "FINISH" in text:
            react_steps.append({"turn": turn, "agent_output": text})
            break
            
        action_match = re.search(r"Action:\s*(\w+)", text)
        input_match = re.search(r"Action Input:\s*(\{.*?\})", text, re.DOTALL)
        
        if action_match:
            action_tool = action_match.group(1).strip()
            action_input = parse_json_from_llm(input_match.group(1)) if input_match else {}
            
            observation = {}
            if action_tool == "tool_sql_product_catalog":
                kw = action_input.get("product_keyword")
                cat = action_input.get("category")
                pt = action_input.get("pet_type")
                p_res = sql_product_search(keyword=kw, category=cat, pet_type=pt)
                all_sql_items.extend(p_res)
                observation = {"products": p_res}
            elif action_tool == "tool_vector_knowledge_search":
                q_txt = action_input.get("query_text", query)
                c_res = vector_search(q_txt, top_k=3, score_threshold=0.60)
                all_vector_chunks.extend(c_res)
                observation = {"chunks": c_res}
            elif action_tool == "tool_official_security_payment":
                req_type = action_input.get("request_type")
                if req_type == "BANK_ACCOUNT_INFO":
                    observation = {"bank_info": "Vietcombank HCM - STK: 0123456789 - Owner: Công ty TNHH Thú Cưng PetHome Việt Nam"}
                else:
                    observation = {"channels": "Zalo OA: PetHome Việt Nam (0988.123.456), Fanpage: PetHome Việt Nam - Đồ Dùng Thú Cưng"}
            elif action_tool == "tool_human_agent_transfer":
                observation = {
                    "ticket_created": True,
                    "category": action_input.get("issue_category", "Vấn đề khác"),
                    "priority": action_input.get("priority", "P1"),
                    "mode": "WAITING_HUMAN"
                }
                
            collected_observations.append({
                "turn": turn,
                "tool": action_tool,
                "input": action_input,
                "observation": observation
            })
            
            react_steps.append({
                "turn": turn,
                "agent_output": text,
                "tool_called": action_tool,
                "observation": observation
            })
            
            current_prompt += f"\n\n{text}\nObservation: {json.dumps(observation, ensure_ascii=False)}"
        else:
            react_steps.append({"turn": turn, "agent_output": text})
            break
            
    latency_ms = (time.perf_counter() - start_time) * 1000

    llm_output_summary = "\n".join([f"Turn {s['turn']}:\n{s['agent_output']}" for s in react_steps])
    raw_db_records = {"sql_items": all_sql_items, "vector_chunks": all_vector_chunks}
    final_context_prompt = build_final_context_str(all_sql_items, all_vector_chunks)

    return {
        "plan_code": "KH-08",
        "plan_name": "Multi-Agent ReAct Architecture",
        "react_steps_count": len(react_steps),
        "collected_observations": collected_observations,
        "llm_output": llm_output_summary,
        "raw_db_records": raw_db_records,
        "final_context_prompt": final_context_prompt,
        "latency_ms": round(latency_ms, 2)
    }

# Mapping of all retrievers
ALL_RETRIEVERS = {
    "KH-01": retrieve_kh01,
    "KH-02": retrieve_kh02,
    "KH-03": retrieve_kh03,
    "KH-04": retrieve_kh04,
    "KH-05": retrieve_kh05,
    "KH-06": retrieve_kh06,
    "KH-07": retrieve_kh07,
    "KH-08": retrieve_kh08,
}
