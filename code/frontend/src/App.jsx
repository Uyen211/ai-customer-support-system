import React, { useState } from 'react';
import { 
  Bot, 
  UserCheck, 
  ShieldAlert, 
  Kanban, 
  Sparkles, 
  Send, 
  BookOpen, 
  AlertTriangle, 
  Clock, 
  CheckCircle2, 
  ArrowRight, 
  Database, 
  Zap, 
  Cpu
} from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('khok1');
  const [demoQuery, setDemoQuery] = useState('Chính sách đổi trả hàng bị lỗi do vận chuyển thế nào?');
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamedText, setStreamedText] = useState('');
  const [showCitation, setShowCitation] = useState(false);
  const [agentStatus, setAgentStatus] = useState('ONLINE');
  const [demoSentiment] = useState(-0.85); // Critical

  // Simulate RAG Streaming effect
  const handleSimulateRAG = () => {
    setIsStreaming(true);
    setStreamedText('');
    setShowCitation(false);
    
    const fullText = "Theo Điều 4 - Chính sách Đổi Trả 2026: Sản phẩm hư hỏng do vận chuyển sẽ được hỗ trợ đổi mới 100% trong vòng 7 ngày làm việc kể từ khi nhận hàng. Quý khách vui lòng cung cấp video khui hàng để được hỗ trợ tức thì.";
    let index = 0;
    
    const timer = setInterval(() => {
      if (index < fullText.length) {
        setStreamedText((prev) => prev + fullText.charAt(index));
        index++;
      } else {
        clearInterval(timer);
        setIsStreaming(false);
        setShowCitation(true);
      }
    }, 25);
  };

  return (
    <div className="min-h-screen bg-[#FFF8E7] text-[#2B2523] selection:bg-[#930500] selection:text-[#FFF8E7]">
      
      {/* 1. HEADER / NAVIGATION */}
      <header className="sticky top-0 z-50 bg-[#FFF8E7]/90 backdrop-blur-md border-b border-[#EFE7D3]">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-[#930500] text-[#FFF8E7] flex items-center justify-center font-bold text-xl shadow-md">
              A
            </div>
            <div>
              <span className="font-bold text-lg tracking-tight block leading-tight">OMNICHANNEL CSKH</span>
              <span className="text-[10px] uppercase tracking-widest text-[#930500] font-semibold">AI Agent & Ticket System</span>
            </div>
          </div>

          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-[#2B2523]/80">
            <a href="#visual-identity" className="hover:text-[#930500] transition-colors">Triết lý Thẩm mỹ</a>
            <a href="#functional-modules" className="hover:text-[#930500] transition-colors">4 Khối Chức năng</a>
            <a href="#live-preview" className="hover:text-[#930500] transition-colors">Trải nghiệm Demo</a>
            <a href="#tech-architecture" className="hover:text-[#930500] transition-colors">Kiến trúc Docker</a>
          </nav>

          <div className="flex items-center gap-3">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#95BBEA]/30 text-[#2B2523] text-xs font-semibold border border-[#95BBEA]/50">
              <span className="w-2 h-2 rounded-full bg-[#930500] animate-pulse"></span>
              Docker Containerized
            </span>
            <a 
              href="#live-preview"
              className="px-5 py-2.5 rounded-full bg-[#930500] text-[#FFF8E7] text-xs font-semibold uppercase tracking-wider hover:bg-[#780400] transition-all shadow-sm hover:shadow-md"
            >
              Xem Demo UI
            </a>
          </div>
        </div>
      </header>

      {/* 2. HERO SECTION */}
      <section className="relative pt-16 pb-20 overflow-hidden">
        {/* Soft background color block */}
        <div className="absolute top-12 right-10 w-96 h-96 rounded-full bg-[#95BBEA]/20 blur-3xl -z-10"></div>
        <div className="absolute bottom-10 left-10 w-80 h-80 rounded-full bg-[#EFE7D3] blur-2xl -z-10"></div>

        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            
            {/* Left Content Column */}
            <div className="lg:col-span-7 space-y-6">
              <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#95BBEA]/40 text-[#2B2523] text-xs font-bold uppercase tracking-widest border border-[#95BBEA]/60">
                <Sparkles className="w-3.5 h-3.5 text-[#930500]" />
                Editorial Calm & Organic Minimalism
              </div>

              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-[1.15] text-[#2B2523] tracking-tight">
                Giao thoa giữa <span className="text-[#930500]">Trí tuệ Nhân tạo</span> & Cảm xúc Con người
              </h1>

              <p className="text-base sm:text-lg text-[#2B2523]/80 font-normal leading-relaxed max-w-2xl">
                Hệ thống Chăm sóc Khách hàng Đa kênh thông minh: Tự động trả lời RAG 24/7, tự động lắng nghe cảm xúc ngầm, mở Ticket khẩn cấp và điều phối công việc cho nhân viên thời gian thực.
              </p>

              {/* Design Token Highlights */}
              <div className="pt-2 flex flex-wrap gap-4 text-xs font-medium">
                <div className="flex items-center gap-2 px-3.5 py-2 rounded-2xl bg-white/60 border border-[#EFE7D3]">
                  <span className="w-4 h-4 rounded-full bg-[#FFF8E7] border border-[#EFE7D3] shadow-inner"></span>
                  <span><strong>60%</strong> Cosmic Latte</span>
                </div>
                <div className="flex items-center gap-2 px-3.5 py-2 rounded-2xl bg-white/60 border border-[#EFE7D3]">
                  <span className="w-4 h-4 rounded-full bg-[#95BBEA]"></span>
                  <span><strong>30%</strong> Cornflower Blue</span>
                </div>
                <div className="flex items-center gap-2 px-3.5 py-2 rounded-2xl bg-white/60 border border-[#EFE7D3]">
                  <span className="w-4 h-4 rounded-full bg-[#930500]"></span>
                  <span><strong>10%</strong> Sangria Red</span>
                </div>
              </div>

              <div className="pt-4 flex items-center gap-4">
                <a 
                  href="#live-preview" 
                  className="px-7 py-3.5 rounded-full bg-[#930500] text-[#FFF8E7] font-semibold text-sm hover:bg-[#780400] transition-all flex items-center gap-2 shadow-lg shadow-[#930500]/10"
                >
                  Khám phá Giao diện
                  <ArrowRight className="w-4 h-4" />
                </a>
                <a 
                  href="#functional-modules" 
                  className="px-7 py-3.5 rounded-full bg-white/70 text-[#2B2523] font-semibold text-sm border border-[#EFE7D3] hover:bg-white transition-all"
                >
                  Xem 4 Khối Chức năng
                </a>
              </div>
            </div>

            {/* Right Card / Visual Showcase */}
            <div className="lg:col-span-5">
              <div className="relative">
                {/* Background decorative stacked shape */}
                <div className="absolute -inset-3 rounded-[36px] bg-[#95BBEA]/40 transform rotate-2"></div>
                
                {/* Main Glass Card */}
                <div className="relative rounded-[32px] bg-white/80 backdrop-blur-xl p-8 border border-[#EFE7D3] shadow-editorial">
                  <div className="flex items-center justify-between pb-6 border-b border-[#EFE7D3]">
                    <div className="flex items-center gap-3">
                      <div className="w-3 h-3 rounded-full bg-[#930500]"></div>
                      <span className="font-bold text-lg">Hệ thống Trực ca AI</span>
                    </div>
                    <span className="px-3 py-1 rounded-full bg-[#95BBEA]/30 text-xs font-semibold text-[#2B2523]">
                      Live Real-Time
                    </span>
                  </div>

                  <div className="space-y-4 py-6">
                    {/* Metric 1 */}
                    <div className="p-4 rounded-2xl bg-[#FFF8E7] border border-[#EFE7D3] flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <Bot className="w-5 h-5 text-[#930500]" />
                        <div>
                          <p className="text-xs text-[#2B2523]/70 font-medium">Khối 1: AI RAG Engine</p>
                          <p className="text-sm font-semibold">Streaming SSE + Supabase Vector</p>
                        </div>
                      </div>
                      <span className="text-xs font-bold text-[#930500]">99.8% Chính xác</span>
                    </div>

                    {/* Metric 2 */}
                    <div className="p-4 rounded-2xl bg-[#95BBEA]/20 border border-[#95BBEA]/40 flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <ShieldAlert className="w-5 h-5 text-[#930500]" />
                        <div>
                          <p className="text-xs text-[#2B2523]/70 font-medium">Khối 2: AI Auto-Triage</p>
                          <p className="text-sm font-semibold">Tự ngắt Bot khi CRITICAL</p>
                        </div>
                      </div>
                      <span className="px-2.5 py-0.5 rounded-full bg-[#930500] text-[#FFF8E7] text-[10px] font-bold">WAITING_HUMAN</span>
                    </div>

                    {/* Metric 3 */}
                    <div className="p-4 rounded-2xl bg-[#FFF8E7] border border-[#EFE7D3] flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <UserCheck className="w-5 h-5 text-[#2B2523]" />
                        <div>
                          <p className="text-xs text-[#2B2523]/70 font-medium">Khối 3 & 4: Live Console & SLA</p>
                          <p className="text-sm font-semibold">WebSocket Takeover & Kanban</p>
                        </div>
                      </div>
                      <span className="text-xs font-bold text-emerald-700">Least-Loaded OK</span>
                    </div>
                  </div>

                  <div className="pt-2 text-center text-xs text-[#2B2523]/60 font-medium">
                    "Editorial Calm & Organic Minimalism for Modern CSKH"
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* 3. VISUAL LANGUAGE & DESIGN TOKENS DEMO */}
      <section id="visual-identity" className="py-16 border-y border-[#EFE7D3] bg-white/40">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-2xl mx-auto mb-12 space-y-3">
            <span className="text-xs font-bold uppercase tracking-widest text-[#930500]">Design Token Standards</span>
            <h2 className="text-3xl sm:text-4xl font-bold">Ngôn ngữ Thị giác & Bảng màu Chuẩn</h2>
            <p className="text-sm text-[#2B2523]/70">
              Thiết kế theo triết lý gốm sứ Scandinavia: đường cong Squircle mộc mạc, nhịp thở thông thoáng, loại bỏ viền gắt và đổ bóng tàng hình.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {/* Swatch 1 */}
            <div className="p-6 rounded-3xl bg-[#FFF8E7] border border-[#EFE7D3] space-y-4 shadow-sm">
              <div className="h-20 rounded-2xl bg-[#FFF8E7] border border-[#EFE7D3] flex items-end p-3">
                <span className="text-xs font-mono font-bold text-[#2B2523]">#FFF8E7</span>
              </div>
              <div>
                <h4 className="font-bold text-base">Cosmic Latte (60%)</h4>
                <p className="text-xs text-[#2B2523]/70 mt-1">Nền kem bơ ấm áp làm chủ đạo, dịu mắt và tạo chiều sâu hữu cơ.</p>
              </div>
            </div>

            {/* Swatch 2 */}
            <div className="p-6 rounded-3xl bg-[#FFF8E7] border border-[#EFE7D3] space-y-4 shadow-sm">
              <div className="h-20 rounded-2xl bg-[#95BBEA] flex items-end p-3 text-white">
                <span className="text-xs font-mono font-bold text-[#2B2523]">#95BBEA</span>
              </div>
              <div>
                <h4 className="font-bold text-base">Cornflower Blue (30%)</h4>
                <p className="text-xs text-[#2B2523]/70 mt-1">Sắc xanh mờ thanh thoát dành cho các mảng khối phụ và thẻ phân loại.</p>
              </div>
            </div>

            {/* Swatch 3 */}
            <div className="p-6 rounded-3xl bg-[#FFF8E7] border border-[#EFE7D3] space-y-4 shadow-sm">
              <div className="h-20 rounded-2xl bg-[#930500] flex items-end p-3 text-white">
                <span className="text-xs font-mono font-bold text-[#FFF8E7]">#930500</span>
              </div>
              <div>
                <h4 className="font-bold text-base">Sangria Red (10%)</h4>
                <p className="text-xs text-[#2B2523]/70 mt-1">Màu đỏ rượu đằm thắm, tạo điểm nhấn quyền lực tại nút CTA chính và cảnh báo.</p>
              </div>
            </div>

            {/* Swatch 4 */}
            <div className="p-6 rounded-3xl bg-[#FFF8E7] border border-[#EFE7D3] space-y-4 shadow-sm">
              <div className="h-20 rounded-2xl bg-[#2B2523] flex items-end p-3 text-white">
                <span className="text-xs font-mono font-bold text-[#FFF8E7]">#2B2523</span>
              </div>
              <div>
                <h4 className="font-bold text-base">Deep Espresso (Text)</h4>
                <p className="text-xs text-[#2B2523]/70 mt-1">Màu chữ cà phê đậm, tương phản dịu nhẹ thay thế cho màu đen tuyền `#000000`.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 4. FOUR FUNCTIONAL MODULES SHOWCASE */}
      <section id="functional-modules" className="py-20">
        <div className="max-w-7xl mx-auto px-6 space-y-16">
          <div className="text-center max-w-3xl mx-auto space-y-3">
            <span className="text-xs font-bold uppercase tracking-widest text-[#930500]">System Architecture</span>
            <h2 className="text-3xl sm:text-4xl font-bold">4 Khối Chức năng Cốt lõi của Dự án</h2>
            <p className="text-sm text-[#2B2523]/70">
              Được thiết kế đồng bộ theo mô hình Modular Monolith, tích hợp mượt mà giữa AI ngầm, Real-time Gateway và Quản lý công việc.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            
            {/* Module 1 Card */}
            <div className="rounded-[32px] bg-white p-8 border border-[#EFE7D3] shadow-editorial-hover space-y-6 flex flex-col justify-between">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-12 h-12 rounded-2xl bg-[#FFF8E7] text-[#930500] border border-[#EFE7D3] flex items-center justify-center">
                    <Bot className="w-6 h-6" />
                  </div>
                  <span className="px-3 py-1 rounded-full bg-[#95BBEA]/30 text-xs font-bold text-[#2B2523]">Thành viên 1</span>
                </div>
                <h3 className="text-2xl font-bold">Khối 1: Trợ lý Tra cứu Thông tin Khách hàng</h3>
                <p className="text-sm text-[#2B2523]/80 leading-relaxed">
                  Tự động giải đáp 24/7 dựa trên tài liệu chính sách nội bộ qua Supabase Vector (`knowledge_chunks` với HNSW Index).
                </p>
                <ul className="space-y-2 text-xs text-[#2B2523]/80 pt-2">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-[#930500]" />
                    <span>Phản hồi dạng gõ chữ trực tiếp (Streaming SSE token-by-token).</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-[#930500]" />
                    <span>Trích dẫn minh bạch nguồn gốc tài liệu tham khảo (Citations JSONB).</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-[#930500]" />
                    <span>Tự động đưa ra câu trả lời mặc định & gợi ý gặp tư vấn viên khi không có dữ liệu.</span>
                  </li>
                </ul>
              </div>
              <div className="pt-4 border-t border-[#EFE7D3] flex items-center justify-between text-xs">
                <span className="font-semibold text-[#930500]">Customer RAG Chatbot</span>
                <span className="text-[#2B2523]/60">Supabase pgvector + SSE</span>
              </div>
            </div>

            {/* Module 2 Card */}
            <div className="rounded-[32px] bg-white p-8 border border-[#EFE7D3] shadow-editorial-hover space-y-6 flex flex-col justify-between">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-12 h-12 rounded-2xl bg-[#930500] text-[#FFF8E7] flex items-center justify-center">
                    <ShieldAlert className="w-6 h-6" />
                  </div>
                  <span className="px-3 py-1 rounded-full bg-[#95BBEA]/30 text-xs font-bold text-[#2B2523]">Thành viên 2</span>
                </div>
                <h3 className="text-2xl font-bold">Khối 2: Giám sát AI & Auto-Triage</h3>
                <p className="text-sm text-[#2B2523]/80 leading-relaxed">
                  Lắng nghe ngầm tin nhắn, đo chỉ số cảm xúc giận dữ và tự động trích xuất lý do mở Ticket khẩn cấp (P1/P2/P3).
                </p>
                <ul className="space-y-2 text-xs text-[#2B2523]/80 pt-2">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-[#930500]" />
                    <span><strong>Cơ chế ngắt Bot AI ngay lập tức:</strong> Khi gặp nguy cơ CRITICAL, tự động chuyển `mode = WAITING_HUMAN` và đẩy tin nhắn hệ thống nhờ khách chờ.</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-[#930500]" />
                    <span>Gắn cờ cảnh báo nguy cơ (`is_flagged = TRUE`) và đẩy sự kiện sang Redis Queue.</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-[#930500]" />
                    <span>Quản lý tự tùy chỉnh bảng quy tắc ngưỡng cảm xúc (`ai_rules`).</span>
                  </li>
                </ul>
              </div>
              <div className="pt-4 border-t border-[#EFE7D3] flex items-center justify-between text-xs">
                <span className="font-semibold text-[#930500]">Conversation Intelligence</span>
                <span className="text-[#2B2523]/60">Structured Output + Redis Queue</span>
              </div>
            </div>

            {/* Module 3 Card */}
            <div className="rounded-[32px] bg-white p-8 border border-[#EFE7D3] shadow-editorial-hover space-y-6 flex flex-col justify-between">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-12 h-12 rounded-2xl bg-[#95BBEA]/40 text-[#2B2523] border border-[#95BBEA]/60 flex items-center justify-center">
                    <UserCheck className="w-6 h-6" />
                  </div>
                  <span className="px-3 py-1 rounded-full bg-[#95BBEA]/30 text-xs font-bold text-[#2B2523]">Thành viên 3</span>
                </div>
                <h3 className="text-2xl font-bold">Khối 3: Live Support Console</h3>
                <p className="text-sm text-[#2B2523]/80 leading-relaxed">
                  Bàn làm việc thời gian thực giúp nhân viên theo dõi danh sách trợ giúp và bấm tiếp quản phiên trò chuyện trực tiếp từ Bot AI.
                </p>
                <ul className="space-y-2 text-xs text-[#2B2523]/80 pt-2">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-[#930500]" />
                    <span>Tiếp quản cuộc trò chuyện (Takeover) có kiểm tra chống xung đột (Read-only nếu đã có nhân viên nhận).</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-[#930500]" />
                    <span>Nhắn tin hai chiều tức thì qua WebSocket (`mode = HUMAN`).</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-[#930500]" />
                    <span>Mẫu câu phản hồi nhanh phím tắt (`/chao`, `/xloi`) từ `canned_responses`.</span>
                  </li>
                </ul>
              </div>
              <div className="pt-4 border-t border-[#EFE7D3] flex items-center justify-between text-xs">
                <span className="font-semibold text-[#930500]">Real-time Gateway</span>
                <span className="text-[#2B2523]/60">WebSocket Manager + Presence</span>
              </div>
            </div>

            {/* Module 4 Card */}
            <div className="rounded-[32px] bg-white p-8 border border-[#EFE7D3] shadow-editorial-hover space-y-6 flex flex-col justify-between">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-12 h-12 rounded-2xl bg-[#FFF8E7] text-[#2B2523] border border-[#EFE7D3] flex items-center justify-center">
                    <Kanban className="w-6 h-6" />
                  </div>
                  <span className="px-3 py-1 rounded-full bg-[#95BBEA]/30 text-xs font-bold text-[#2B2523]">Thành viên 4</span>
                </div>
                <h3 className="text-2xl font-bold">Khối 4: Dispatcher, SLA Engine & Analytics</h3>
                <p className="text-sm text-[#2B2523]/80 leading-relaxed">
                  Tự động phân chia công việc công bằng, đếm ngược cam kết thời gian xử lý và báo động đỏ khi vi phạm quá hạn.
                </p>
                <ul className="space-y-2 text-xs text-[#2B2523]/80 pt-2">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-[#930500]" />
                    <span>Phân chia Ticket tự động cho nhân viên ít việc nhất (Least-Loaded Dispatcher).</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-[#930500]" />
                    <span>Giám sát đếm ngược SLA & phát thông báo báo động đỏ qua Redis Pub/Sub khi quá hạn (`SLA Breach`).</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-[#930500]" />
                    <span>Quản lý tiến độ trên bảng Kanban & Báo cáo biểu đồ thống kê hiệu suất.</span>
                  </li>
                </ul>
              </div>
              <div className="pt-4 border-t border-[#EFE7D3] flex items-center justify-between text-xs">
                <span className="font-semibold text-[#930500]">SLA & Routing Engine</span>
                <span className="text-[#2B2523]/60">Least-Loaded + Kanban</span>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* 5. INTERACTIVE LIVE DEMO PREVIEW WIDGET */}
      <section id="live-preview" className="py-20 bg-white/60 border-t border-[#EFE7D3]">
        <div className="max-w-7xl mx-auto px-6 space-y-10">
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
            <div className="space-y-2">
              <span className="text-xs font-bold uppercase tracking-widest text-[#930500]">Interactive Prototype</span>
              <h2 className="text-3xl sm:text-4xl font-bold">Trải nghiệm Trực quan Giao diện</h2>
              <p className="text-sm text-[#2B2523]/70">
                Thử nghiệm tương tác các kịch bản thực tế theo đúng ngôn ngữ thiết kế Editorial Calm & Organic Minimalism.
              </p>
            </div>

            {/* Tab Selector */}
            <div className="flex p-1.5 rounded-full bg-[#FFF8E7] border border-[#EFE7D3] self-start md:self-auto overflow-x-auto max-w-full">
              <button 
                onClick={() => setActiveTab('khok1')}
                className={`px-5 py-2 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${activeTab === 'khok1' ? 'bg-[#930500] text-[#FFF8E7] shadow-sm' : 'text-[#2B2523]/70 hover:text-[#2B2523]'}`}
              >
                Khối 1: RAG Chatbot
              </button>
              <button 
                onClick={() => setActiveTab('khok2')}
                className={`px-5 py-2 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${activeTab === 'khok2' ? 'bg-[#930500] text-[#FFF8E7] shadow-sm' : 'text-[#2B2523]/70 hover:text-[#2B2523]'}`}
              >
                Khối 2: Auto-Triage
              </button>
              <button 
                onClick={() => setActiveTab('khok3')}
                className={`px-5 py-2 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${activeTab === 'khok3' ? 'bg-[#930500] text-[#FFF8E7] shadow-sm' : 'text-[#2B2523]/70 hover:text-[#2B2523]'}`}
              >
                Khối 3: Live Console
              </button>
              <button 
                onClick={() => setActiveTab('khok4')}
                className={`px-5 py-2 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${activeTab === 'khok4' ? 'bg-[#930500] text-[#FFF8E7] shadow-sm' : 'text-[#2B2523]/70 hover:text-[#2B2523]'}`}
              >
                Khối 4: Kanban & SLA
              </button>
            </div>
          </div>

          {/* Interactive Screen Area */}
          <div className="rounded-[36px] bg-[#FFF8E7] border border-[#EFE7D3] p-8 shadow-editorial relative overflow-hidden">
            
            {/* Tab 1: RAG Chatbot Simulation */}
            {activeTab === 'khok1' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between pb-4 border-b border-[#EFE7D3]">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-[#95BBEA]/40 text-[#2B2523] flex items-center justify-center font-bold">
                      <Bot className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="font-bold text-base">Khung Chat Khách hàng (RAG Streaming)</h4>
                      <p className="text-xs text-[#2B2523]/60">Chế độ: AI Bot Trả lời Tự động (Supabase Vector Search)</p>
                    </div>
                  </div>
                  <span className="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-semibold">
                    mode = 'BOT'
                  </span>
                </div>

                <div className="min-h-[220px] space-y-4 max-w-3xl">
                  {/* Customer Question Bubble */}
                  <div className="flex justify-end">
                    <div className="max-w-md p-4 rounded-3xl rounded-br-xs bg-[#2B2523] text-[#FFF8E7] text-sm shadow-sm">
                      {demoQuery}
                    </div>
                  </div>

                  {/* AI Bot Response Bubble */}
                  <div className="flex justify-start items-start gap-3">
                    <div className="w-8 h-8 rounded-full bg-[#930500] text-[#FFF8E7] flex items-center justify-center shrink-0 text-xs font-bold">
                      AI
                    </div>
                    <div className="space-y-3">
                      <div className="max-w-lg p-5 rounded-3xl rounded-tl-xs bg-white border border-[#EFE7D3] text-sm leading-relaxed shadow-sm">
                        {isStreaming ? (
                          <span className="inline-flex items-center gap-1">
                            {streamedText}
                            <span className="w-2 h-4 bg-[#930500] animate-pulse inline-block"></span>
                          </span>
                        ) : streamedText ? (
                          streamedText
                        ) : (
                          <span className="text-[#2B2523]/50 italic">Nhấn nút bên dưới để thử nghiệm luồng SSE Streaming...</span>
                        )}
                      </div>

                      {/* Citations Popup Button */}
                      {showCitation && (
                        <div className="p-3 rounded-2xl bg-[#95BBEA]/20 border border-[#95BBEA]/50 max-w-lg text-xs space-y-1.5 animate-fadeIn">
                          <div className="flex items-center gap-1.5 font-bold text-[#930500]">
                            <BookOpen className="w-3.5 h-3.5" />
                            <span>Nguồn trích dẫn tài liệu tham khảo (Citations JSONB):</span>
                          </div>
                          <p className="text-[#2B2523]/80">
                            📄 <strong>File:</strong> `Chinh_sach_doi_tra.pdf` — <strong>Mục:</strong> Điều 4 (Trang 2)
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Simulation Control Bar */}
                <div className="pt-4 border-t border-[#EFE7D3] flex flex-wrap items-center justify-between gap-4">
                  <input 
                    type="text" 
                    value={demoQuery}
                    onChange={(e) => setDemoQuery(e.target.value)}
                    className="flex-1 min-w-[280px] px-5 py-3 rounded-full bg-white border border-[#EFE7D3] text-sm focus:outline-none focus:border-[#930500]"
                    placeholder="Nhập câu hỏi thử nghiệm..."
                  />
                  <button 
                    onClick={handleSimulateRAG}
                    disabled={isStreaming}
                    className="px-6 py-3 rounded-full bg-[#930500] text-[#FFF8E7] font-semibold text-xs uppercase tracking-wider hover:bg-[#780400] transition-all flex items-center gap-2 disabled:opacity-50"
                  >
                    <Send className="w-3.5 h-3.5" />
                    Thử nghiệm Streaming SSE
                  </button>
                </div>
              </div>
            )}

            {/* Tab 2: Auto-Triage & Critical Bot Pause */}
            {activeTab === 'khok2' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between pb-4 border-b border-[#EFE7D3]">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-[#930500] text-[#FFF8E7] flex items-center justify-center font-bold">
                      <ShieldAlert className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="font-bold text-base">Giám sát Ngầm & Tự động ngắt Bot AI</h4>
                      <p className="text-xs text-[#2B2523]/60">Chế độ: Đo điểm Sentiment Score ngầm & Kích hoạt Ticket</p>
                    </div>
                  </div>
                  <span className="px-3 py-1 rounded-full bg-[#930500] text-[#FFF8E7] text-xs font-bold">
                    CRITICAL DETECTED
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Gauge / Sentiment Score Display */}
                  <div className="p-6 rounded-3xl bg-white border border-[#EFE7D3] space-y-4">
                    <h5 className="font-bold text-sm text-[#2B2523]/80">Chỉ số Cảm xúc Khách hàng (Sentiment Score)</h5>
                    <div className="flex items-center justify-between">
                      <span className="text-3xl font-bold text-[#930500]">{demoSentiment}</span>
                      <span className="px-3 py-1 rounded-full bg-red-100 text-red-800 text-xs font-bold">Giận dữ Cực độ (CRITICAL)</span>
                    </div>
                    
                    {/* Meter bar */}
                    <div className="w-full bg-[#EFE7D3] h-3 rounded-full overflow-hidden">
                      <div className="bg-[#930500] h-full rounded-full transition-all duration-500" style={{ width: '85%' }}></div>
                    </div>

                    <div className="text-xs text-[#2B2523]/70 pt-2 border-t border-[#EFE7D3]">
                      Threshold Nguy cơ trong `ai_rules`: $\le -0.60$ $\rightarrow$ Kích hoạt ngắt Bot AI.
                    </div>
                  </div>

                  {/* Auto System Notice Trigger Card */}
                  <div className="p-6 rounded-3xl bg-[#930500] text-[#FFF8E7] space-y-4 shadow-lg">
                    <div className="flex items-center gap-2 text-amber-200 text-xs font-bold uppercase tracking-wider">
                      <AlertTriangle className="w-4 h-4" />
                      <span>Cơ chế Tự động Ngắt Bot AI đang kích hoạt</span>
                    </div>

                    <div className="p-4 rounded-2xl bg-white/10 text-xs space-y-2 border border-white/20">
                      <p className="font-semibold">Bản ghi CSDL được cập nhật:</p>
                      <p>• `conversations.mode` = <strong className="text-amber-200">'WAITING_HUMAN'</strong></p>
                      <p>• `conversations.is_flagged` = <strong className="text-amber-200">TRUE</strong></p>
                    </div>

                    <div className="p-3 rounded-2xl bg-white text-[#2B2523] text-xs leading-relaxed font-medium">
                      💬 <strong>Tin nhắn Hệ thống gửi Khách hàng:</strong><br />
                      "Hệ thống nhận thấy bạn cần hỗ trợ chuyên sâu, vui lòng chờ trong giây lát tư vấn viên đang vào hỗ trợ bạn."
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Tab 3: Live Support Console */}
            {activeTab === 'khok3' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between pb-4 border-b border-[#EFE7D3]">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-[#95BBEA]/40 text-[#2B2523] flex items-center justify-center font-bold">
                      <UserCheck className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="font-bold text-base">Bàn làm việc Nhân viên CSKH (Live Console)</h4>
                      <p className="text-xs text-[#2B2523]/60">Kênh WebSocket 2 chiều & Tiếp quản cuộc trò chuyện (Takeover)</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-[#2B2523]/70">Trạng thái Nhân viên:</span>
                    <button 
                      onClick={() => setAgentStatus(agentStatus === 'ONLINE' ? 'BUSY' : 'ONLINE')}
                      className={`px-3 py-1 rounded-full text-xs font-bold ${agentStatus === 'ONLINE' ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' : 'bg-amber-100 text-amber-800'}`}
                    >
                      ● {agentStatus}
                    </button>
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Left Conversation Queue */}
                  <div className="p-4 rounded-3xl bg-white border border-[#EFE7D3] space-y-3">
                    <div className="text-xs font-bold uppercase tracking-wider text-[#930500] px-1">Hàng đợi Cảnh báo (Is_flagged)</div>
                    <div className="p-3 rounded-2xl bg-[#930500]/10 border border-[#930500]/30 space-y-1 cursor-pointer">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-xs">KH: Nguyễn Văn A</span>
                        <span className="text-[10px] font-bold text-[#930500]">CRITICAL</span>
                      </div>
                      <p className="text-xs text-[#2B2523]/70 truncate">Sản phẩm bị vỡ nát khi nhận hàng!</p>
                    </div>
                  </div>

                  {/* Main Work Area */}
                  <div className="lg:col-span-2 p-5 rounded-3xl bg-white border border-[#EFE7D3] space-y-4 flex flex-col justify-between">
                    <div className="flex items-center justify-between pb-3 border-b border-[#EFE7D3]">
                      <span className="text-xs text-[#2B2523]/70">Chế độ hiện tại: <strong>WAITING_HUMAN</strong></span>
                      <button className="px-4 py-2 rounded-full bg-[#930500] text-[#FFF8E7] text-xs font-bold hover:bg-[#780400] transition-all shadow-sm">
                        Bấm Tiếp quản Cuộc trò chuyện (Takeover)
                      </button>
                    </div>

                    {/* Canned response shortcut pills */}
                    <div className="pt-2">
                      <span className="text-[11px] text-[#2B2523]/60 block mb-1.5 font-medium">Mẫu câu trả lời nhanh (`canned_responses`):</span>
                      <div className="flex flex-wrap gap-2">
                        <span className="px-3 py-1 rounded-full bg-[#FFF8E7] border border-[#EFE7D3] text-xs font-semibold cursor-pointer hover:border-[#930500]">
                          `/chao` — Dạ chào anh/chị, em là tư vấn viên...
                        </span>
                        <span className="px-3 py-1 rounded-full bg-[#FFF8E7] border border-[#EFE7D3] text-xs font-semibold cursor-pointer hover:border-[#930500]">
                          `/xloi` — Rất tiếc vì sự cố vừa qua...
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Tab 4: Dispatcher, Kanban & SLA */}
            {activeTab === 'khok4' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between pb-4 border-b border-[#EFE7D3]">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-[#FFF8E7] text-[#2B2523] border border-[#EFE7D3] flex items-center justify-center font-bold">
                      <Kanban className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="font-bold text-base">Điều phối Ticket & Giám sát Đồng hồ SLA</h4>
                      <p className="text-xs text-[#2B2523]/60">Thuật toán Least-Loaded Dispatcher & Đếm ngược SLA</p>
                    </div>
                  </div>
                  <span className="px-3 py-1 rounded-full bg-blue-100 text-blue-800 text-xs font-bold">
                    P1 - SLA: 15 Phút
                  </span>
                </div>

                {/* Simulated Kanban Columns */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  {/* PENDING Column */}
                  <div className="p-4 rounded-3xl bg-white border border-[#EFE7D3] space-y-3">
                    <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-[#2B2523]/70">
                      <span>Chờ xử lý (PENDING)</span>
                      <span className="w-5 h-5 rounded-full bg-[#FFF8E7] flex items-center justify-center text-[10px]">1</span>
                    </div>
                    <div className="p-4 rounded-2xl bg-[#FFF8E7] border border-[#EFE7D3] space-y-2 text-xs">
                      <div className="flex items-center justify-between font-bold">
                        <span>#TK-9021</span>
                        <span className="text-[#930500]">Ưu tiên P1</span>
                      </div>
                      <p className="text-[#2B2523]/80">Hàng vỡ hỏng do vận chuyển</p>
                      <div className="pt-2 flex items-center gap-1.5 text-red-700 font-bold">
                        <Clock className="w-3.5 h-3.5" />
                        <span>Hạn chót: 12:45 (Còn 08m:15s)</span>
                      </div>
                    </div>
                  </div>

                  {/* IN_PROGRESS Column */}
                  <div className="p-4 rounded-3xl bg-white border border-[#EFE7D3] space-y-3">
                    <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-[#930500]">
                      <span>Đang xử lý (IN_PROGRESS)</span>
                      <span className="w-5 h-5 rounded-full bg-[#FFF8E7] flex items-center justify-center text-[10px]">2</span>
                    </div>
                    <div className="p-4 rounded-2xl bg-[#95BBEA]/20 border border-[#95BBEA]/40 space-y-2 text-xs">
                      <div className="flex items-center justify-between font-bold">
                        <span>#TK-8812</span>
                        <span className="text-emerald-800">Least-Loaded Assigned</span>
                      </div>
                      <p className="text-[#2B2523]/80">Gán cho Agent: Lê Thị B (1 việc)</p>
                      <div className="pt-2 flex items-center gap-1.5 text-emerald-800 font-bold">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>SLA Met Target</span>
                      </div>
                    </div>
                  </div>

                  {/* RESOLVED Column */}
                  <div className="p-4 rounded-3xl bg-white border border-[#EFE7D3] space-y-3">
                    <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-emerald-800">
                      <span>Đã giải quyết (RESOLVED)</span>
                      <span className="w-5 h-5 rounded-full bg-[#FFF8E7] flex items-center justify-center text-[10px]">12</span>
                    </div>
                    <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 space-y-2 text-xs">
                      <div className="flex items-center justify-between font-bold">
                        <span>#TK-7740</span>
                        <span className="text-emerald-700">SLA Met</span>
                      </div>
                      <p className="text-[#2B2523]/80">Hoàn thành trong 06 phút</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

          </div>
        </div>
      </section>

      {/* 6. TECHNICAL ARCHITECTURE SHOWCASE */}
      <section id="tech-architecture" className="py-20">
        <div className="max-w-7xl mx-auto px-6 space-y-12">
          <div className="text-center max-w-2xl mx-auto space-y-3">
            <span className="text-xs font-bold uppercase tracking-widest text-[#930500]">Full Containerized Environment</span>
            <h2 className="text-3xl sm:text-4xl font-bold">Công nghệ & Đóng gói Docker Trọn gói</h2>
            <p className="text-sm text-[#2B2523]/70">
              Khởi chạy tức thì trên mọi máy tính với duy nhất 1 lệnh `docker compose up --build -d`.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-8 rounded-[32px] bg-white border border-[#EFE7D3] shadow-sm space-y-4">
              <div className="w-10 h-10 rounded-2xl bg-[#FFF8E7] text-[#930500] flex items-center justify-center font-bold">
                <Database className="w-5 h-5" />
              </div>
              <h4 className="font-bold text-xl">Supabase PostgreSQL</h4>
              <p className="text-xs text-[#2B2523]/70 leading-relaxed">
                Kết nối ORM SQLAlchemy, sử dụng extension `pgvector` tạo bảng `knowledge_chunks` tích hợp chỉ mục HNSW Index cho RAG search.
              </p>
            </div>

            <div className="p-8 rounded-[32px] bg-white border border-[#EFE7D3] shadow-sm space-y-4">
              <div className="w-10 h-10 rounded-2xl bg-[#95BBEA]/30 text-[#2B2523] flex items-center justify-center font-bold">
                <Zap className="w-5 h-5" />
              </div>
              <h4 className="font-bold text-xl">Redis Event Bus</h4>
              <p className="text-xs text-[#2B2523]/70 leading-relaxed">
                Xử lý hàng đợi Queue chia việc cho Dispatcher Worker và kênh Pub/Sub phát sự kiện cảnh báo vi phạm SLA Breach.
              </p>
            </div>

            <div className="p-[#2B2523] p-8 rounded-[32px] bg-white border border-[#EFE7D3] shadow-sm space-y-4">
              <div className="w-10 h-10 rounded-2xl bg-[#930500] text-[#FFF8E7] flex items-center justify-center font-bold">
                <Cpu className="w-5 h-5" />
              </div>
              <h4 className="font-bold text-xl">FastAPI + React Vite</h4>
              <p className="text-xs text-[#2B2523]/70 leading-relaxed">
                Backend bất đồng bộ xử lý SSE Streaming & WebSocket 2 chiều, kết hợp Frontend React Tailwind CSS v4 dịu mát.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 7. FOOTER */}
      <footer className="bg-[#2B2523] text-[#FFF8E7] py-12 border-t border-[#2B2523]">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="space-y-1 text-center md:text-left">
            <h3 className="text-xl font-bold">Hệ thống AI Agent CSKH Đa kênh & Smart Ticket Routing</h3>
            <p className="text-xs text-[#FFF8E7]/60">Báo cáo Đồ án / Dự án Kiểm thử & Thiết kế Hệ thống 2026</p>
          </div>

          <div className="flex items-center gap-6 text-xs text-[#FFF8E7]/80">
            <span>Cosmic Latte #FFF8E7</span>
            <span>•</span>
            <span>Cornflower Blue #95BBEA</span>
            <span>•</span>
            <span>Sangria Red #930500</span>
          </div>
        </div>
      </footer>

    </div>
  );
}
