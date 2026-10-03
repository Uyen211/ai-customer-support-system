import sys
import os
import asyncio
import json

# Thêm thư mục backend vào sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.rag.decomposer import decomposer_service

async def main():
    test_query = "Cho tôi gặp nhân viên tư vấn"
    sample_chat_history = [
        {"role": "user", "content": "Xin chào"},
        {"role": "assistant", "content": "Xin chào! Mình là Trợ lý tư vấn PetHome. Bạn cần hỗ trợ gì ạ?"}
    ]
    
    print("=" * 70)
    print(f"🔍 [TEST PROMPT 1 - DECOMPOSER INTENT ROUTER]")
    print(f"📩 Câu hỏi đầu vào: '{test_query}'")
    print("=" * 70)
    
    try:
        output = await decomposer_service.decompose(
            query=test_query,
            chat_history=sample_chat_history
        )
        
        print("\n✅ Kết quả phân tích (Parsed Pydantic Model):")
        print(f"- Standalone Query : {output.standalone_query}")
        print(f"- Reason           : {output.reasoning}")
        print(f"- Is Complex       : {output.is_complex}")
        print(f"- Sentiment Score  : {output.sentiment_score}")
        print(f"- Urgency Level    : {output.urgency_level}")
        print(f"- Incident Summary : {output.incident_summary}")
        print(f"- Incident Category: {output.incident_category}")
        
        print("\n📋 Danh sách Sub-queries & Intent:")
        for idx, sq in enumerate(output.sub_queries, 1):
            print(f"  [{idx}] Sub-query     : {sq.query}")
            print(f"      Intent        : {sq.intent}")
            print(f"      Target Source : {sq.target_source}")
            print(f"      Pet Type      : {sq.pet_type}")
            print(f"      Category      : {sq.category}")
            print(f"      Brand         : {sq.brand}")

        print("\n📄 Định dạng JSON trả về từ Prompt 1:")
        print(json.dumps(output.model_dump(), ensure_ascii=False, indent=2))
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Lỗi khi gửi Prompt 1 lên LLM Gemini: {e}")

if __name__ == "__main__":
    asyncio.run(main())
