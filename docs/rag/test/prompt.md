# TÀI LIỆU KIẾN TRÚC KỸ THUẬT & TẬP PROMPTS TÍCH LŨY CHUẨN XÁC CHO 8 KẾ HOẠCH CHATBOT RAG

> **Mục đích**: Đặc tả chi tiết kiến trúc kỹ thuật, sơ đồ luồng dữ liệu (Dataflow Diagram), tiêu chí đánh giá Prompt tiền xử lý (Pre-Prompt Criteria Analysis), định nghĩa Function Calling Tools và tập Prompts LLM **hỗ trợ tra cứu hai nguồn CSDL (Relational SQL Products + Vector Knowledge DB bao gồm cả Chính sách & Hướng dẫn/FAQ Sản phẩm)** cho trọn vẹn 8 Kế hoạch RAG (KH-01 đến KH-08).
>
> **Phân định Hai Nguồn Dữ liệu CSDL trong Hệ thống (Từ `products_relational.json` & `knowledge_chunks_prepared.json`)**:
> 1. **CSDL Quan hệ SQL `products` (Relational Real-Time DB)**:
>    - Chứa thông tin cấu trúc, giá tiền (`price`, `sale_price`), tồn kho (`stock_quantity`, `status`) và thuộc tính kỹ thuật (`brand`, `weight`, `volume`, `target_age`, `origin`, `suitable_breed`, `material`, `flavor`, `warranty`).
> 2. **CSDL Vector `knowledge_chunks` (Unstructured Semantic Knowledge Base)**:
>    - **Chunks Chính sách CSKH**: 4 Bộ chính sách (*Chính sách Chăm sóc Khách hàng & Hỗ trợ Chuyển Chuyên viên, Chính sách Đổi trả & Hoàn tiền, Chính sách Vận chuyển & Giao nhận, Chính sách Thanh toán & Bán hàng*).
>    - **Chunks Tri thức Sản phẩm mở rộng (`doc_type: "PRODUCT_CHUNK"`)**: Chứa thông tin chi tiết về hướng dẫn sử dụng, liều lượng ăn, tình huống giải quyết vấn đề (VD: *mèo nuôi chung cư bị nôn búi lông, chó kén ăn, mèo lười uống nước*), câu hỏi FAQ tìm kiếm và tư vấn giải pháp chăm sóc thú cưng.

---

# 📌 PHẦN 1: KH-01 - NAIVE RAG (BASELINE ĐƠN SƠ NHẤT)

### 1.1. Tiền Phân tích Tiêu chí Thiết kế Prompt (Pre-Prompt Criteria)

| Tiêu chí Đánh giá | Mức độ Đáp ứng | Mô tả Chi tiết & Rào cản Kỹ thuật |
|---|:---:|---|
| **Role & Persona** | Cơ bản | Định danh Trợ lý CSKH PetHome cơ bản. |
| **Coreference Resolution** | KHÔNG | Chưa có cơ chế giải mã đại từ chỉ thị (*"nó"*, *"loại đó"*). Trượt ngữ cảnh khi chat nhiều lượt. |
| **Domain Boundary Guardrail** | KHÔNG | Không có rào chắn phạm vi. Nhận mọi câu hỏi bất kỳ và cố gắng Embed vector. |
| **Strict Grounding / Anti-Hallucination** | Thấp | Ép trả lời theo ngữ cảnh nhưng không có quy tắc phạt khi thiếu thông tin trong `<context>`. |
| **Graceful Fallback** | KHÔNG | Chưa có mẫu câu từ chối an toàn. Dễ bịa ra thông tin nếu vector search ra dữ liệu rác. |
| **Output Determinism** | Tự do | Trả về văn bản tự do, không quy định cấu trúc trích dẫn hay gạch đầu dòng. |

### 1.2. Kiến trúc Hệ thống & Tương tác Thành phần (System Architecture & Component Interactions)
* **Kiểu kiến trúc**: Single-pass Direct Pipeline (Một luồng xử lý thẳng không qua kiểm soát).
* **Giao tiếp các thành phần nội bộ**:
  1. `Frontend Chat UI` gửi `User Query` thô tới `API Gateway`.
  2. `API Gateway` chuyển query sang `Embedding Service` (`dangvantuan/vietnamese-embedding`) tạo vector 1024 chiều.
  3. `Vector Engine (pgvector)` tìm kiếm Cosine Similarity trên `knowledge_chunks` (gồm cả chunks chính sách & chunks tri thức sản phẩm), lấy $Top-3$ chunks.
  4. `LLM Generator` sinh câu trả lời trực tiếp.

* **Sơ đồ Luồng Dữ liệu (Dataflow Diagram)**:
  ```text
  [User Query thô] ──► [API Gateway] ──► [Embedding Service (1024D)]
                                                  │
                                                  ▼
  [Frontend UI] ◄── [LLM Generator] ◄── [Prompt Builder] ◄── [pgvector DB: Top-3 Chunks]
  ```

### 1.3. Tập Prompt LLM cho KH-01
```text
# ROLE & IDENTITY
You are the Virtual Support Assistant for PetHome Việt Nam - Chuỗi cửa hàng Đồ dùng Thú cưng (pet supplies, food, accessories). Answer customer inquiries strictly using the provided context.

# CONTEXT
<context>
{context}
</context>

# USER QUERY
<user_query>
{user_query}
</user_query>

# INSTRUCTION
Answer the <user_query> using only the information in <context>.
```

---

# 📌 PHẦN 2: KH-02 - RAG + SCORE THRESHOLDING (`[Thay thế Phương pháp]`)

### 2.1. Tiền Phân tích Tiêu chí Thiết kế Prompt (Pre-Prompt Criteria)

| Tiêu chí Đánh giá | Mức độ Đáp ứng | Mô tả Chi tiết & Rào cản Kỹ thuật |
|---|:---:|---|
| **Role & Persona** | Khá | Hình tượng CSKH chuỗi đồ dùng thú cưng trung thực, tận tâm. |
| **Coreference Resolution** | KHÔNG | Chưa có bộ viết lại câu hỏi; chỉ xử lý các câu hỏi đơn lẻ lượt đầu. |
| **Domain Boundary Guardrail** | Khá | Lọc được câu hỏi ngoài ranh giới tài liệu nhờ cổng Cosine Similarity Score Check. |
| **Strict Grounding / Anti-Hallucination** | XUẤT SẮC | Cổng $\text{Threshold} \ge 0.65$ ngắt luồng gọi LLM khi điểm thấp; Prompt cấm bịa đặt thông tin. |
| **Graceful Fallback** | ĐẠT | Phản hồi mẫu câu từ chối tĩnh chuẩn khi tài liệu không chứa đủ dữ liệu. |
| **Output Determinism** | Cao | Cấu trúc câu trả lời có định dạng rõ ràng, lịch sự. |

### 2.2. Kiến trúc Hệ thống & Tương tác Thành phần (System Architecture & Component Interactions)
* **Kiểu kiến trúc**: Threshold-Gated Pipeline.
* **Giao tiếp các thành phần nội bộ**:
  1. `User Query` đi qua `Embedding Service` $\rightarrow$ `pgvector Engine`.
  2. `Threshold Evaluator Gate` kiểm tra $\max(\text{Score})$. Nếu $< 0.65$, ngắt luồng trả về `Static Fallback Response`. Nếu $\ge 0.65$, chuyển sang `Strict Generator LLM`.

* **Sơ đồ Luồng Dữ liệu (Dataflow Diagram)**:
  ```text
  [User Query] ──► [Embedding Service] ──► [pgvector Search]
                                                  │
                                                  ▼
                                     [Threshold Evaluator Gate]
                                      ├── Max Score < 0.65  ──► [Static Fallback Response (No LLM Call)]
                                      └── Max Score >= 0.65 ──► [Strict Generator LLM] ──► Output
  ```

### 2.3. Tập Prompt LLM cho KH-02 (`STRICT_GENERATOR_PROMPT_KH02`)
```text
# ROLE & BRAND PERSONA
You are the official Virtual Assistant for PetHome Việt Nam - Chuỗi cửa hàng Đồ dùng Thú cưng. Maintain a polite, empathetic tone ("mình" - "bạn").

# OPERATIONAL CONSTRAINTS & GUARDRAILS
1. STRICT GROUNDING: Use ONLY verified documentation in <context>. Never rely on external assumptions or prior training data.
2. HANDLING UNCERTAINTY & FALLBACK: If the answer is not explicitly stated or cannot be derived from <context>, output EXACTLY:
   "Rất tiếc, hiện tại tài liệu hướng dẫn của PetHome chưa có thông tin chi tiết về vấn đề này. Bạn có muốn mình kết nối trực tiếp với nhân viên tư vấn để được hỗ trợ cụ thể không ạ?"
3. ANTI-HALLUCINATION: Do NOT guess prices, warranty terms, or policy details not present in text.

# CONTEXT (Similarity Score >= 0.65)
<context>
{context}
</context>

# USER QUERY
<user_query>
{user_query}
</user_query>

# INSTRUCTION
Synthesize a concise, structured response to <user_query> strictly following constraints above.
```

---

# 📌 PHẦN 3: KH-03 - RAG + CONTEXTUAL QUERY REWRITER (`[Bổ sung Phát triển]`)

### 3.1. Tiền Phân tích Tiêu chí Thiết kế Prompt (Pre-Prompt Criteria)

| Tiêu chí Đánh giá | Mức độ Đáp ứng | Mô tả Chi tiết & Rào cản Kỹ thuật |
|---|:---:|---|
| **Role & Persona** | Cao | Phân định rõ vai trò Query Optimization Agent và Response Generator. |
| **Coreference Resolution** | ĐẠT | Giải quyết triệt để đại từ chỉ thị (*"nó"*, *"loại đó"*), biến câu hỏi thành Standalone Query. |
| **Domain Boundary Guardrail** | Khá | Kế thừa cổng Score Thresholding từ KH-02. |
| **Strict Grounding** | Cao | Generator nhận Standalone Query đã làm sạch ngữ cảnh. |
| **Graceful Fallback** | ĐẠT | Phản hồi từ chối tĩnh chuẩn khi tài liệu không chứa đủ dữ liệu. |
| **Output Determinism** | Cực cao | Ép đầu ra của Rewriter dưới dạng chuỗi Standalone Query thuần túy. |

### 3.2. Kiến trúc Hệ thống & Tương tác Thành phần (System Architecture & Component Interactions)
* **Kiểu kiến trúc**: Sequential Two-Stage Pipeline.
* **Giao tiếp các thành phần nội bộ**:
  1. `API Gateway` lấy `chat_history` và `user_query` nạp cho `LLM Query Rewriter Agent`.
  2. LLM Rewriter tạo `standalone_query` truyền sang `Embedding Service` $\rightarrow$ `pgvector Engine` $\rightarrow$ `Score Gate (>= 0.65)` $\rightarrow$ `Strict Generator LLM`.

* **Sơ đồ Luồng Dữ liệu (Dataflow Diagram)**:
  ```text
  [User Query + Chat History] ──► [LLM Query Rewriter] ──► [Standalone Query]
                                                                  │
                                                                  ▼
  [Strict Generator] ◄── [Score Gate >= 0.65] ◄── [pgvector Search] ◄── [Embedding]
  ```

### 3.3. Tập Prompts LLM cho KH-03

#### Prompt 1: Contextual Query Rewriter Agent (`REWRITER_PROMPT_KH03`)
```text
# ROLE & TASK
You are the Query Optimization Agent for PetHome - Chuỗi cửa hàng Đồ dùng Thú cưng. Analyze <chat_history> and <user_query>, resolve all coreferences/pronouns ("nó", "loại này", "cái đó"), and output a single, self-contained Standalone Query in Vietnamese for vector retrieval.

# CONVERSATION CONTEXT
<chat_history>
{chat_history}
</chat_history>

# CURRENT INPUT
<user_query>
{user_query}
</user_query>

# OUTPUT FORMAT
Output ONLY the raw string of the rewritten standalone query. Do not include markdown wraps or explanations.
```

#### Prompt 2: Contextual Response Generator (`STRICT_GENERATOR_PROMPT_KH03`)
```text
# ROLE & BRAND PERSONA
You are the official Virtual Assistant for PetHome Việt Nam - Chuỗi cửa hàng Đồ dùng Thú cưng.

# CONTEXT (Score >= 0.65)
<context>
{context}
</context>

# STANDALONE USER QUERY
<user_query>
{rewritten_query}
</user_query>

# INSTRUCTION
Synthesize a clear, polite response addressing <user_query>.
```

---

# 📌 PHẦN 4: KH-04 - RAG + INTENT GUARDRAIL ROUTER (`[Bổ sung Phát triển]`)

### 4.1. Tiền Phân tích Tiêu chí Thiết kế Prompt (Pre-Prompt Criteria)

| Tiêu chí Đánh giá | Mức độ Đáp ứng | Mô tả Chi tiết & Rào cản Kỹ thuật |
|---|:---:|---|
| **Token Optimization** | XUẤT SẮC | **Gộp Rewriter & Intent Router thành 1 lượt gọi LLM duy nhất (Single-pass Multi-task)**. |
| **Role & Persona** | Cao | Trợ lý Đồ dùng thú cưng kiêm Bộ phân loại ý định & giải mã ngữ cảnh. |
| **Domain Boundary Guardrail** | XUẤT SẮC | Định nghĩa rõ Scope 4 Bộ chính sách, 5 Danh mục sản phẩm và Loài thú cưng hợp lệ. |
| **Strict Grounding** | ĐẠT | Chặn ngay các câu hỏi Out-of-Domain (Bò, Ngựa, áo mưa người) mà không tốn token Vector DB. |
| **Graceful Fallback** | ĐẠT | Phân nhánh trực tiếp sang Template từ chối Scope hoặc Chuyển Human Agent. |
| **Output Determinism** | Cực cao | Ép đầu ra JSON Schema đa nhiệm cho backend parsing. |

### 4.2. Kiến trúc Hệ thống & Tương tác Thành phần (System Architecture & Component Interactions)
* **Kiểu kiến trúc**: Single-Pass Multi-Task Guardrail Pipeline.
* **Giao tiếp các thành phần nội bộ**:
  1. `Merged Multi-task Pre-processor LLM` thực thi Rewriter + Intent Router cùng lúc, xuất JSON chứa `standalone_query`, `intent`, `reasoning`.
  2. `Intent Dispatcher` kiểm tra: `GREETING`/`OUT_OF_DOMAIN` $\rightarrow$ Fast Static Template; `HUMAN_AGENT_REQUEST` $\rightarrow$ Transfer Ticket; `PRODUCT_POLICY_QUERY` $\rightarrow$ Vector Search + Generator.

* **Sơ đồ Luồng Dữ liệu (Dataflow Diagram)**:
  ```text
  [User Query + Chat History] ──► [1. Merged Pre-processor LLM (Rewriter + Intent Router)]
                                        │
                                        ├── Output JSON: { "standalone_query", "intent", "reasoning" }
                                        │
                                        ├── If GREETING / OUT_OF_DOMAIN ──► [Fast Static Template Response]
                                        ├── If HUMAN_AGENT_REQUEST      ──► [Handover to Human Agent]
                                        └── If PRODUCT_POLICY_QUERY
                                                │
                                                ▼
  [Guarded Generator LLM] ◄── [Score Gate >= 0.65] ◄── [pgvector Search Top-3] ◄── [Embedding]
  ```

### 4.3. Tập Prompts LLM cho KH-04 (Gộp còn 2 Prompts)

#### Prompt 1: Merged Multi-task Pre-processor Prompt (`MERGED_PREPROCESSOR_PROMPT_KH04`)
```text
# ROLE & TASK
You are the Multi-Task Pre-processor for PetHome Việt Nam - Chuỗi cửa hàng Đồ dùng Thú cưng. Perform TWO operations in a SINGLE pass:
1. COREFERENCE RESOLUTION: Rewrite <user_query> using <chat_history> into a self-contained standalone query in Vietnamese.
2. INTENT CLASSIFICATION: Categorize the query into exactly one intent class based on our domain scope.

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
{chat_history}
</chat_history>

<user_query>
{user_query}
</user_query>

# OUTPUT FORMAT (STRICT JSON ONLY)
{
  "standalone_query": "The rewritten standalone query in Vietnamese",
  "intent": "GREETING_CHITCHAT" | "OUT_OF_DOMAIN" | "HUMAN_AGENT_REQUEST" | "PRODUCT_POLICY_QUERY",
  "reasoning": "A single brief sentence explaining the classification decision"
}
```

#### Prompt 2: Guarded Generator (`GUARDED_GENERATOR_PROMPT_KH04`)
```text
# ROLE & BRAND PERSONA
You are the official Virtual Assistant for PetHome Việt Nam - Chuỗi cửa hàng Đồ dùng Thú cưng. Maintain a warm, respectful tone ("mình" - "bạn").

# OPERATIONAL CONSTRAINTS
1. STRICT GROUNDING: Use ONLY documentation in <context>. Do not fabricate policies or prices.
2. OFFICIAL CHANNELS: PetHome operates online exclusively via Zalo OA "PetHome Việt Nam" (Hotline: 0988.123.456) and Fanpage Facebook. Note: PetHome currently DOES NOT have an e-commerce website.
3. FALLBACK: If <context> lacks detail, politely admit and offer transfer to a human agent.

# CONTEXT (Score >= 0.65)
<context>
{context}
</context>

# USER QUERY
<user_query>
{rewritten_query}
</user_query>

# INSTRUCTION
Provide a clear, formatted response addressing <user_query>.
```

---

# 📌 PHẦN 5: KH-05 - HYBRID RAG + DIRECT SQL CATALOG LOOKUP (`[Bổ sung Phát triển]`)

### 5.1. Tiền Phân tích Tiêu chí Thiết kế Prompt (Pre-Prompt Criteria)

| Tiêu chí Đánh giá | Mức độ Đáp ứng | Mô tả Chi tiết & Rào cản Kỹ thuật |
|---|:---:|---|
| **Token Optimization** | XUẤT SẮC | **Gộp Rewriter + Intent Router + SQL Parameter Extractor thành 1 lượt gọi LLM duy nhất**. |
| **Data Sources Division** | TOÀN DIỆN | SQL `products` cho dữ liệu giá/tồn kho/thông số kỹ thuật real-time; Vector `knowledge_chunks` cho cả Chính sách VÀ Tri thức/FAQ Hướng dẫn Sản phẩm (`doc_type: PRODUCT_CHUNK`). |
| **Cumulative JSON Schema** | TUYỆT ĐỐI | Trả về đầy đủ `"standalone_query"`, `"intent"`, `"reasoning"`, `"query_type"`, `"product_search_keyword"`, `"pet_type"`, `"category"`. |
| **Strict Grounding** | XUẤT SẮC | Giá tiền, tồn kho và thông số kỹ thuật real-time lấy chính xác từ bảng SQL `products`. |

### 5.2. Kiến trúc Hệ thống & Tương tác Thành phần (System Architecture & Component Interactions)
* **Kiểu kiến trúc**: Hybrid Multi-Source Pipeline (Phân luồng đa nguồn CSDL Quan hệ SQL + Vector DB).
* **Giao tiếp các thành phần nội bộ**:
  1. `Merged Hybrid Router LLM` nhận query, giải mã đại từ, phân loại intent và trích xuất các thuộc tính tra cứu SQL (`brand`, `pet_type`, `category`, `product_search_keyword`).
  2. `Data Orchestrator Service` thực thi truy vấn SQL linh hoạt trên bảng `products` (giá, tồn kho, thuộc tính mở rộng) và/hoặc tìm kiếm Vector `knowledge_chunks` (chứa cả chunks chính sách và chunks tri thức/FAQ hướng dẫn sản phẩm).
  3. `Hybrid Synthesizer LLM` nhận dữ liệu sản phẩm SQL và ngữ cảnh tri thức Vector để tổng hợp phản hồi.

* **Sơ đồ Luồng Dữ liệu (Dataflow Diagram)**:
  ```text
  [User Query + Chat History] ──► [1. Merged Hybrid Router LLM]
                                        │
                                        ├── Output JSON: { "standalone_query", "intent", "reasoning", "query_type", "product_search_keyword", "pet_type", "category" }
                                        │
                                        ├── SQL_ONLY     ──► [Supabase SQL Query `products`]        ──► Real-time Product Data ──┐
                                        ├── VECTOR_ONLY  ──► [pgvector Search (Policy + Prod FAQs)]  ──► Semantic Knowledge Chunks ┼─► [2. Hybrid Synthesizer LLM]
                                        └── HYBRID_BOTH  ──► [SQL + Vector Parallel Search] ────────────────────────────────────┘
  ```

### 5.3. Tập Prompts LLM cho KH-05 (2 Prompts gộp đa nhiệm)

#### Prompt 1: Merged Multi-task Hybrid Router Prompt (`MERGED_HYBRID_ROUTER_PROMPT_KH05`)
```text
# ROLE & TASK
You are the Multi-Task Hybrid Router for PetHome - Chuỗi cửa hàng Đồ dùng Thú cưng. Perform THREE operations in a SINGLE pass:
1. COREFERENCE RESOLUTION: Rewrite <user_query> using <chat_history> into a standalone query.
2. INTENT CLASSIFICATION: Categorize query intent (GREETING_CHITCHAT, OUT_OF_DOMAIN, HUMAN_AGENT_REQUEST, PRODUCT_POLICY_QUERY).
3. SOURCE ROUTING & PARAMETER EXTRACTION: Determine target source (`SQL_ONLY`, `VECTOR_ONLY`, `HYBRID_BOTH`, `OUT_OF_DOMAIN`) and extract search parameters for relational SQL execution.

# DATA SOURCES DEFINITION
1. SQL DATABASE (`products` table): Real-time stock status, exact prices, attributes (`brand`, `weight`, `volume`, `target_age`, `origin`, `suitable_breed`, `material`, `flavor`, `warranty`) for categories: [Thức ăn, Vệ sinh, Đồ chơi, Phụ kiện, Chăm sóc].
2. VECTOR DATABASE (`knowledge_chunks` table): Policy rules (CSKH, Shipping, Returns, Payment) AND Unstructured Product Knowledge (Usage guidelines, dosage, problem-solving FAQs for pet conditions like vomiting hairballs, picky eaters, etc.).

# FULL SQL DATABASE SCHEMA GUIDANCE (`products` table)
Queryable Columns & JSONB Attributes:
- `name`: Product title string
- `sku`: Product unique SKU code
- `category`: Product category enum ["Thức ăn", "Vệ sinh", "Đồ chơi", "Phụ kiện", "Chăm sóc"]
- `pet_type`: Target animal enum ["CAT", "DOG", "BIRD"]
- `price`, `sale_price`: Pricing integers (VNĐ)
- `stock_quantity`, `status`: Inventory status ('IN_STOCK', 'OUT_OF_STOCK')
- `attributes` (JSONB): brand, weight, volume, target_age, origin, suitable_breed, material, flavor, warranty
- `description`: Text summary of benefits and usage

*Note: If query is purely about store policy or pet care advice without requiring real-time catalog price/stock, set query_type to "VECTOR_ONLY" and product_search_keyword to null.*

# INPUT
<chat_history>
{chat_history}
</chat_history>

<user_query>
{user_query}
</user_query>

# OUTPUT FORMAT (STRICT JSON ONLY - FULL CUMULATIVE SCHEMA)
{
  "standalone_query": "The rewritten standalone query in Vietnamese",
  "intent": "GREETING_CHITCHAT" | "OUT_OF_DOMAIN" | "HUMAN_AGENT_REQUEST" | "PRODUCT_POLICY_QUERY",
  "reasoning": "A single brief sentence explaining the classification decision",
  "query_type": "SQL_ONLY" | "VECTOR_ONLY" | "HYBRID_BOTH" | "OUT_OF_DOMAIN",
  "product_search_keyword": "Extracted product name keyword (or null)",
  "pet_type": "CAT" | "DOG" | "BIRD" | null,
  "category": "Thức ăn" | "Vệ sinh" | "Đồ chơi" | "Phụ kiện" | "Chăm sóc" | null
}
```

#### Prompt 2: Hybrid Knowledge Synthesizer (`HYBRID_SYNTHESIZER_PROMPT_KH05`)
```text
# ROLE & BRAND PERSONA
You are the Virtual Assistant for PetHome Việt Nam - Chuỗi cửa hàng Đồ dùng Thú cưng.

# OPERATIONAL CONSTRAINTS
1. FACTUAL ACCURACY: State accurate product attributes (brand, weight, age, origin, breed suitability), prices, and stock status directly based on <product_catalog_data>. If a product is out of stock, inform the customer politely and suggest available alternatives.
2. POLICY & GUIDELINE COMPLIANCE: Shipping rates, return windows, payment methods, and product usage/care advice MUST strictly follow <knowledge_context>.
3. BRAND TONE: Polite, clear, friendly ("mình" - "bạn").

# DATA SOURCES
--- PRODUCT CATALOG DATA (SQL) ---
<product_catalog_data>
{product_catalog_data}
</product_catalog_data>

--- KNOWLEDGE CONTEXT: POLICIES & PRODUCT FAQS (VECTOR RAG) ---
<knowledge_context>
{knowledge_context}
</knowledge_context>

# USER QUERY
<user_query>
{rewritten_query}
</user_query>

# INSTRUCTION
Synthesize a unified, polite response addressing customer query.
```

---

# 📌 PHẦN 6: KH-06 - HYBRID RAG + SUB-QUERY DECOMPOSITION (`[Bổ sung Phát triển]`)

### 6.1. Tiền Phân tích Tiêu chí Thiết kế Prompt (Pre-Prompt Criteria)

| Tiêu chí Đánh giá | Mức độ Đáp ứng | Mô tả Chi tiết & Rào cản Kỹ thuật |
|---|:---:|---|
| **Token Optimization** | XUẤT SẮC | **Gộp Rewriter + Intent Router + Sub-query Decomposition thành 1 lượt gọi LLM duy nhất**. |
| **Cumulative JSON Schema** | TUYỆT ĐỐI | Trả về đầy đủ `"standalone_query"`, `"intent"`, `"reasoning"`, `"is_complex"`, `"sub_queries"`. |
| **Strict Grounding** | XUẤT SẮC | Tránh hiện tượng Vector DB bỏ sót ý khi câu hỏi thô gộp quá nhiều chủ đề. |

### 6.2. Kiến trúc Hệ thống & Tương tác Thành phần (System Architecture & Component Interactions)
* **Kiểu kiến trúc**: Parallel Sub-query Decomposition Pipeline.
* **Giao tiếp các thành phần nội bộ**:
  1. `Merged Decomposer LLM` bẻ câu hỏi phức tạp thành mảng `sub_queries`, gán `target_source` (`SQL_PRODUCT` hoặc `VECTOR_KNOWLEDGE`) và trích xuất tham số SQL cho từng câu hỏi nhỏ.
  2. `Parallel Retrieval Workers` thực thi đồng thời các truy vấn SQL `products` và Vector `knowledge_chunks` (gồm cả Chunks chính sách lẫn Chunks tri thức/FAQ sản phẩm).
  3. `Multi-Context Synthesizer LLM` tổng hợp kết quả đa luồng trả lời khách hàng.

* **Sơ đồ Luồng Dữ liệu (Dataflow Diagram)**:
  ```text
  [Complex Multi-intent Query] ──► [1. Merged Decomposer LLM]
                                           │
                                           ├── Output JSON: { "sub_queries": [ Sub1, Sub2, Sub3 ] }
                                           │
                                           ├── Sub1 (SQL_PRODUCT)      ──► [SQL Worker]    ──► Result 1 ──┐
                                           ├── Sub2 (VECTOR_KNOWLEDGE) ──► [Vector Worker] ──► Result 2 ┼─► [Context Aggregator] ──► [2. Multi-Context Synthesizer]
                                           └── Sub3 (VECTOR_KNOWLEDGE) ──► [Vector Worker] ──► Result 3 ──┘
  ```

### 6.3. Tập Prompts LLM cho KH-06 (2 Prompts gộp đa nhiệm)

#### Prompt 1: Merged Decomposer Prompt (`MERGED_DECOMPOSER_PROMPT_KH06`)
```text
# ROLE & TASK
You are the Multi-Task Decomposer for PetHome - Chuỗi cửa hàng Đồ dùng Thú cưng. Analyze <chat_history> and <user_query>:
1. COREFERENCE RESOLUTION: Resolve all pronouns into explicit entities.
2. INTENT CLASSIFICATION: Categorize query intent (GREETING_CHITCHAT, OUT_OF_DOMAIN, HUMAN_AGENT_REQUEST, PRODUCT_POLICY_QUERY).
3. SUB-QUERY DECOMPOSITION: If query contains multiple distinct sub-questions (e.g. price/brand AND shipping AND usage advice), decompose into 2-3 focused atomic sub-queries with target source labels (`SQL_PRODUCT` vs `VECTOR_KNOWLEDGE`) and SQL search parameters.

# SQL SCHEMA GUIDANCE (`products` table attributes)
Queryable fields: name, sku, category [Thức ăn, Vệ sinh, Đồ chơi, Phụ kiện, Chăm sóc], pet_type [CAT, DOG, BIRD], price, sale_price, stock_quantity, status, brand, weight, volume, target_age, origin, suitable_breed, material, flavor, warranty.

# INPUT
<chat_history>
{chat_history}
</chat_history>

<user_query>
{user_query}
</user_query>

# OUTPUT FORMAT (STRICT JSON ONLY - FULL CUMULATIVE SCHEMA)
{
  "standalone_query": "The main rewritten standalone query",
  "intent": "GREETING_CHITCHAT" | "OUT_OF_DOMAIN" | "HUMAN_AGENT_REQUEST" | "PRODUCT_POLICY_QUERY",
  "reasoning": "A single brief sentence explaining the classification decision",
  "is_complex": true | false,
  "sub_queries": [
    {
      "id": 1,
      "query": "Fully qualified atomic sub-query string",
      "target_source": "SQL_PRODUCT" | "VECTOR_KNOWLEDGE",
      "product_search_keyword": "Extracted keyword or null",
      "pet_type": "CAT" | "DOG" | "BIRD" | null,
      "category": "Thức ăn" | "Vệ sinh" | "Đồ chơi" | "Phụ kiện" | "Chăm sóc" | null
    }
  ]
}
```

#### Prompt 2: Multi-Context Synthesizer (`MULTI_CONTEXT_SYNTHESIZER_PROMPT_KH06`)
```text
# ROLE & BRAND PERSONA
You are the official Assistant for PetHome Việt Nam - Chuỗi cửa hàng Đồ dùng Thú cưng.

# OPERATIONAL CONSTRAINTS
1. COMPLETE COVERAGE: Address ALL sub-questions raised by customer in structured bullet points. Do NOT omit sub-topics.
2. GROUNDING: Ensure strict factual consistency with retrieved contexts (SQL product catalog data and Vector knowledge chunks).

# AGGREGATED RETRIEVAL CONTEXTS
<aggregated_contexts>
{aggregated_contexts}
</aggregated_contexts>

# ORIGINAL USER QUERY
<user_query>
{rewritten_query}
</user_query>

# INSTRUCTION
Synthesize a comprehensive, friendly response covering all customer inquiry points.
```

---

# 📌 PHẦN 7: KH-07 - HYBRID SEARCH (VECTOR + BM25) + CROSS-ENCODER RE-RANKER (`[Thay thế Phương pháp]`)

### 7.1. Tiền Phân tích Tiêu chí Thiết kế Prompt (Pre-Prompt Criteria)

| Tiêu chí Đánh giá | Mức độ Đáp ứng | Mô tả Chi tiết & Rào cản Kỹ thuật |
|---|:---:|---|
| **Role & Persona** | Cao | Nâng cấp mô hình retrieval bằng kết hợp Dense Vector + Sparse BM25 và Cross-Encoder Re-ranker. |
| **Strict Grounding** | HOÀN HẢO | Re-ranker đánh lại điểm tương đồng ngữ nghĩa chính xác cho cả chunks chính sách lẫn chunks tri thức sản phẩm trước khi nạp vào LLM Generator. |
| **Graceful Fallback** | ĐẠT | Áp dụng ngưỡng điểm Re-ranker Score $\ge 0.70$ để ngắt luồng ảo giác. |

### 7.2. Kiến trúc Hệ thống & Tương tác Thành phần (System Architecture & Component Interactions)
* **Kiểu kiến trúc**: Hybrid Multi-stage Search & Re-ranking Pipeline.
* **Giao tiếp các thành phần nội bộ**:
  1. Query sau tiền xử lý được đưa đồng thời vào `Dense Vector Retriever` (pgvector Cosine trên `knowledge_chunks`) và `Sparse BM25 Search Engine` (PostgreSQL Full-Text Search).
  2. `RRF Fusion Merger` hợp nhất 40 candidates, chuyển sang `Cross-Encoder Re-ranker Model` (`bge-reranker-large`).
  3. `Re-ranker Score Gate (>= 0.70)` giữ lại Top-3 chunks xuất sắc nhất đưa vào `RERANKED_GENERATOR_PROMPT_KH07`.

* **Sơ đồ Luồng Dữ liệu (Dataflow Diagram)**:
  ```text
  [Pre-processed Query] ──┬──► [Dense Vector Search (pgvector)] ──► Top-20 Candidates ──┐
                          │                                                            ├──► [RRF Fusion Merger] ──► 40 Candidates ──► [Cross-Encoder Re-ranker]
                          └──► [Sparse BM25 Search (Postgres FTS)] ──► Top-20 Candidates ──┘                                                      │
                                                                                                                                                 ▼
  [Output Response] ◄── [Reranked Generator LLM] ◄── [Re-ranker Score Gate >= 0.70 (Top-3)] ───────────────────────────────────────────────────┘
  ```

### 7.3. Tập Prompt LLM cho KH-07 (`RERANKED_GENERATOR_PROMPT_KH07`)
```text
# ROLE & BRAND PERSONA
You are the official Assistant for PetHome Việt Nam - Chuỗi cửa hàng Đồ dùng Thú cưng.

# OPERATIONAL CONSTRAINTS & GUARDRAILS
1. STRICT GROUNDING: Use ONLY top re-ranked chunks in <reranked_context>. Do not fabricate information.
2. CITATION REQUIREMENT: Attribute policy or product guide source titles inside brackets, e.g., [Nguồn: Chính sách Đổi trả & Hoàn tiền] hoặc [Nguồn: Hướng dẫn sản phẩm Royal Canin Indoor].

# RE-RANKED CONTEXT (Dense Vector + Sparse BM25 + Cross-Encoder Score >= 0.70)
<reranked_context>
{reranked_context}
</reranked_context>

# USER QUERY
<user_query>
{rewritten_query}
</user_query>

# INSTRUCTION
Synthesize an accurate, well-cited response strictly following constraints above.
```

---

# 📌 PHẦN 8: KH-08 - MULTI-AGENT ARCHITECTURE (PLANNER + TOOL ROUTER + REACT LOOP) (`[Bổ sung Phát triển]`)

### 8.1. Tiền Phân tích Tiêu chí Thiết kế Prompt (Pre-Prompt Criteria)

| Tiêu chí Đánh giá | Mức độ Đáp ứng | Mô tả Chi tiết & Rào cản Kỹ thuật |
|---|:---:|---|
| **Role & Persona** | TOÀN DIỆN | Phân rã hệ thống thành 3 Agents chuyên biệt: Master Planner, Reflection Agent, Response Generator. |
| **Tool Multi-Source Capability** | XUẤT SẮC | `tool_vector_knowledge_search` tìm kiếm cả Chunks chính sách CSKH VÀ Chunks tri thức/FAQ hướng dẫn sản phẩm mở rộng (`doc_type: PRODUCT_CHUNK`). |
| **Graceful Fallback & Handover** | HOÀN HẢO | Tích hợp `tool_human_agent_transfer` tạo Ticket trên bảng `tickets` khi vượt quá năng lực AI. |

### 8.2. Kiến trúc Hệ thống & Tương tác Thành phần (System Architecture & Component Interactions)
* **Kiểu kiến trúc**: Multi-Agent ReAct Architecture.
* **Giao tiếp các thành phần nội bộ**:
  1. `ReAct Master Planner Agent` phát ra Tool Action Call dạng JSON.
  2. `Tool Execution Engine` kích hoạt 1 trong 4 Tools:
     - `tool_sql_product_catalog`: Tra cứu SQL linh hoạt theo từ khóa, category, pet_type, thương hiệu, độ tuổi, giá bán, tồn kho.
     - `tool_vector_knowledge_search`: Tìm kiếm vector bảng `knowledge_chunks` (gồm cả Chunks chính sách CSKH VÀ Chunks tri thức/FAQ hướng dẫn sản phẩm).
     - `tool_official_security_payment`: Lấy thông tin STK Vietcombank `0123456789` / Kênh Zalo OA/Facebook.
     - `tool_human_agent_transfer`: Tạo phiếu hỗ trợ CSDL `tickets` và đổi mode sang `WAITING_HUMAN`.
  3. `ReAct Reflection Agent` kiểm định độ đầy đủ của dữ liệu.
  4. `Response Generator Agent` tổng hợp câu phản hồi gửi khách hàng.

* **Sơ đồ Luồng Dữ liệu (Dataflow Diagram)**:
  ```text
  [User Query] ──► [ReAct Master Planner Agent] ◄─── ReAct Loop (Thought -> Action -> Observation)
                          │                         ├── tool_sql_product_catalog (SQL DB - Catalog & Stock)
                          │                         ├── tool_vector_knowledge_search (Vector DB - Policies & Product FAQs)
                          │                         ├── tool_official_security_payment (Static Auth)
                          │                         └── tool_human_agent_transfer (Ticket DB)
                          ▼
              [ReAct Reflection Agent] ──► (Verify Data Completeness)
                          │
                          ▼ (If Sufficient)
              [Response Generator Agent] ──► Final Customer Response
  ```

### 8.3. Định nghĩa Khai báo 4 Function Calling Tools (JSON Schemas)

```json
[
  {
    "name": "tool_sql_product_catalog",
    "description": "Tra cứu giá bán (VNĐ), giá khuyến mãi, tồn kho thực tế và các thuộc tính kỹ thuật (thương hiệu, trọng lượng, dung tích, độ tuổi, xuất xứ, giống loài phù hợp, chất liệu, hương vị, bảo hành) từ CSDL SQL products của PetHome. product_keyword có thể null nếu tra cứu theo category/pet_type.",
    "parameters": {
      "type": "object",
      "properties": {
        "product_keyword": { "type": ["string", "null"], "description": "Tên hoặc từ khóa sản phẩm/thương hiệu" },
        "category": { "type": ["string", "null"], "enum": ["Thức ăn", "Vệ sinh", "Đồ chơi", "Phụ kiện", "Chăm sóc", "Tất cả", null] },
        "pet_type": { "type": ["string", "null"], "enum": ["CAT", "DOG", "BIRD", "Tất cả", null] }
      },
      "required": []
    }
  },
  {
    "name": "tool_vector_knowledge_search",
    "description": "Tìm kiếm vector ngữ cảnh trong CSDL knowledge_chunks của PetHome, bao gồm CẢ 4 bộ chính sách CSKH (Chăm sóc Khách hàng, Đổi trả 7 ngày, Vận chuyển, Thanh toán) VÀ các Chunks tri thức sản phẩm mở rộng (Hướng dẫn sử dụng, liều lượng, FAQ giải quyết tình huống mèo nôn búi lông, chó kén ăn, mèo lười uống nước).",
    "parameters": {
      "type": "object",
      "properties": {
        "query_text": { "type": "string", "description": "Từ khóa hoặc nội dung ngữ cảnh cần tra cứu tri thức vector" },
        "knowledge_type": { "type": ["string", "null"], "enum": ["POLICY_DOCS", "PRODUCT_KNOWLEDGE", "ALL", null], "description": "Loại tri thức thu hẹp phạm vi tìm kiếm" }
      },
      "required": ["query_text"]
    }
  },
  {
    "name": "tool_official_security_payment",
    "description": "Lấy thông tin tài khoản chuyển khoản ngân hàng chính thức và xác thực kênh bán hàng online duy nhất của PetHome (Zalo OA / Fanpage Facebook).",
    "parameters": {
      "type": "object",
      "properties": {
        "request_type": { "type": "string", "enum": ["BANK_ACCOUNT_INFO", "OFFICIAL_CHANNELS_INFO"] }
      },
      "required": ["request_type"]
    }
  },
  {
    "name": "tool_human_agent_transfer",
    "description": "Tạo Ticket khiếu nại (bảng tickets CSDL) và chuyển ngay phiên hội thoại sang chế độ chờ Nhân viên tư vấn trực ca (mode WAITING_HUMAN) khi gặp sự cố phức tạp hoặc khách bức xúc.",
    "parameters": {
      "type": "object",
      "properties": {
        "issue_category": { "type": "string", "enum": ["Lỗi đơn hàng", "Đổi trả/Hoàn tiền", "Sản phẩm lỗi/Hư hại", "Lỗi thanh toán", "Thái độ phục vụ", "Vấn đề khác"] },
        "priority": { "type": "string", "enum": ["P1", "P2", "P3"] },
        "reason_summary": { "type": "string", "description": "Tóm tắt ngắn gọn lý do chuyển nhân viên" }
      },
      "required": ["issue_category", "priority", "reason_summary"]
    }
  }
]
```

---

### 8.4. Tập Prompts LLM cho KH-08 (Multi-Agent System)

#### Prompt 1: ReAct Master Planner System Prompt (`REACT_PLANNER_PROMPT_KH08`)
```text
# ROLE & TASK
You are the ReAct Master Planner Agent for PetHome Việt Nam - Chuỗi cửa hàng Đồ dùng Thú cưng. Your objective is to analyze customer queries, formulate a step-by-step reasoning trajectory (Thought), select and invoke appropriate Tools (Action), analyze execution results (Observation), and repeat until all facts are gathered.

# DOMAIN SCOPE & STORE INFORMATION
1. STORE TYPE: Pet Supplies & Equipment Store (Food, litter, accessories, grooming tools. NO live animals).
2. OFFICIAL POLICIES: CSKH & Transfer, Returns & Refunds, Shipping, Payment.
3. VECTOR KNOWLEDGE BASE: Policies AND Unstructured Product Chunks (Usage guidelines, dosage, FAQ problem solving for pet conditions).
4. SQL PRODUCT CATALOG (Relational): Name, SKU, category, pet_type, price, sale_price, stock_quantity, status, brand, weight, volume, target_age, origin, suitable_breed, material, flavor, warranty.
5. OFFICIAL PAYMENT & CHANNELS:
   - Bank Account: Vietcombank HCM | STK: 0123456789 | Owner: Công ty TNHH Thú Cưng PetHome Việt Nam.
   - Official Online Channels: Zalo OA (Hotline: 0988.123.456) and Fanpage Facebook. (No website).

# REACT REASONING FORMAT
Thought: Reason about what information is missing or what step to take next.
Action: The tool to call, strictly one of [tool_sql_product_catalog, tool_vector_knowledge_search, tool_official_security_payment, tool_human_agent_transfer].
Action Input: JSON payload matching tool schema.

(After Observation is returned, repeat Thought/Action up to 3 iterations)

Thought: I have gathered all necessary information.
Final Action: FINISH
Final Payload: Structured summary of all retrieved data facts.

# USER QUERY
<user_query>
{rewritten_query}
</user_query>
```

#### Prompt 2: Response Generator Agent Prompt (`FINAL_GENERATOR_PROMPT_KH08`)
```text
# ROLE & BRAND PERSONA
You are the Response Generator Agent for PetHome Việt Nam - Chuỗi cửa hàng Đồ dùng Thú cưng. Synthesize final customer response based strictly on verified data facts collected by Master Planner Agent.

# OPERATIONAL CONSTRAINTS
1. FACTUAL ACCURACY: Strictly adhere to verified tool outputs in <verified_tool_data> (Product attributes, prices, stock levels, policy rules, usage advice, Vietcombank STK 0123456789).
2. TICKET NOTIFICATION: If `tool_human_agent_transfer` was invoked, inform customer of created support Ticket category and assure them an agent will join shortly.
3. BRAND VOICE: Empathetic, polite, clear, structured with bullet points ("mình" - "bạn").

# VERIFIED TOOL DATA
<verified_tool_data>
{verified_tool_data}
</verified_tool_data>

# ORIGINAL USER QUERY
<user_query>
{user_query}
</user_query>

# OFFICIAL PETHOME RESPONSE:
```
