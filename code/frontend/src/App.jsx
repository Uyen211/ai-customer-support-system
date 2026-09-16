import React from 'react';
import { 
  Bot, 
  UserCheck, 
  Kanban, 
  ShieldAlert, 
  FolderTree, 
  FileText,
  Sparkles,
  Layers
} from 'lucide-react';

export default function App() {
  return (
    <div className="min-h-screen bg-[#FDFBF7] text-[#2C2623] font-sans">
      {/* Header Bar */}
      <header className="bg-[#930500] text-white py-4 px-6 shadow-md flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-white/10 rounded-xl flex items-center justify-center font-bold text-xl border border-white/20">
            🐾
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-wide">PetHome AI Customer Support System</h1>
            <p className="text-xs text-white/80">Hệ thống Trợ lý Trực ca CSKH AI & Giám sát Vận hành Tự động</p>
          </div>
        </div>
        <div className="flex items-center space-x-2 bg-white/10 px-3 py-1.5 rounded-lg border border-white/20 text-xs">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Frontend Architecture Ready</span>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-mx-auto p-6 md:p-8 space-y-8">
        {/* Welcome Section */}
        <div className="bg-white rounded-2xl p-6 md:p-8 border border-[#EBE5D8] shadow-sm space-y-4">
          <div className="flex items-center space-x-3 text-[#930500]">
            <FolderTree className="w-7 h-7" />
            <h2 className="text-2xl font-bold">Cấu Trúc Mã Nguồn Frontend Đã Chuẩn Hóa</h2>
          </div>
          <p className="text-gray-600 leading-relaxed">
            Thư mục <code className="bg-amber-50 text-[#930500] px-2 py-0.5 rounded font-mono text-sm border border-amber-200">code/frontend/src/</code> 
            đã được sắp xếp và khởi tạo hoàn chỉnh theo đúng sơ đồ kiến trúc tại 
            <code className="bg-amber-50 text-[#930500] px-2 py-0.5 rounded font-mono text-sm border border-amber-200">docs/overview/cautruc.md</code>.
          </p>
        </div>

        {/* 4 Core Modules Overview Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Module 1 */}
          <div className="bg-white rounded-xl p-6 border border-[#EBE5D8] shadow-sm hover:border-[#930500]/40 transition space-y-3">
            <div className="flex items-center space-x-3">
              <div className="p-2.5 bg-amber-50 text-[#930500] rounded-lg">
                <Bot className="w-6 h-6" />
              </div>
              <div>
                <h3 className="font-bold text-lg text-[#2C2623]">Khối 1: Customer RAG Chatbot</h3>
                <span className="text-xs text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                  src/components/chat/ & src/pages/customer/
                </span>
              </div>
            </div>
            <p className="text-sm text-gray-600">
              Trợ lý ảo thông minh trả lời tự động 24/7, gõ chữ SSE token-by-token, trích dẫn tài liệu RAG và quản lý phiên trò chuyện.
            </p>
          </div>

          {/* Module 2 */}
          <div className="bg-white rounded-xl p-6 border border-[#EBE5D8] shadow-sm hover:border-[#930500]/40 transition space-y-3">
            <div className="flex items-center space-x-3">
              <div className="p-2.5 bg-rose-50 text-rose-700 rounded-lg">
                <ShieldAlert className="w-6 h-6" />
              </div>
              <div>
                <h3 className="font-bold text-lg text-[#2C2623]">Khối 2: AI Auto-Triage</h3>
                <span className="text-xs text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                  src/pages/admin/AIRulesPage.jsx
                </span>
              </div>
            </div>
            <p className="text-sm text-gray-600">
              Giám sát cảm xúc ngầm, tự động ngắt Bot AI khi giận dữ mức CRITICAL và mở Ticket khẩn cấp.
            </p>
          </div>

          {/* Module 3 */}
          <div className="bg-white rounded-xl p-6 border border-[#EBE5D8] shadow-sm hover:border-[#930500]/40 transition space-y-3">
            <div className="flex items-center space-x-3">
              <div className="p-2.5 bg-blue-50 text-blue-700 rounded-lg">
                <UserCheck className="w-6 h-6" />
              </div>
              <div>
                <h3 className="font-bold text-lg text-[#2C2623]">Khối 3: Live Support Console</h3>
                <span className="text-xs text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                  src/components/agent/ & src/pages/admin/LiveConsolePage.jsx
                </span>
              </div>
            </div>
            <p className="text-sm text-gray-600">
              Bàn làm việc thời gian thực của Nhân viên CSKH, xem hàng đợi, nhận tiếp quản và chat 2 chiều qua WebSocket.
            </p>
          </div>

          {/* Module 4 */}
          <div className="bg-white rounded-xl p-6 border border-[#EBE5D8] shadow-sm hover:border-[#930500]/40 transition space-y-3">
            <div className="flex items-center space-x-3">
              <div className="p-2.5 bg-emerald-50 text-emerald-700 rounded-lg">
                <Kanban className="w-6 h-6" />
              </div>
              <div>
                <h3 className="font-bold text-lg text-[#2C2623]">Khối 4: SLA Engine & Kanban</h3>
                <span className="text-xs text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                  src/components/kanban/ & src/pages/admin/KanbanPage.jsx
                </span>
              </div>
            </div>
            <p className="text-sm text-gray-600">
              Thuật toán phân việc Least-Loaded, bảng Kanban 4 cột, đếm ngược SLA và chuông báo động đỏ quá hạn.
            </p>
          </div>
        </div>

        {/* Guide Box */}
        <div className="bg-amber-50 rounded-xl p-6 border border-amber-200 text-sm text-amber-900 flex items-start space-x-3">
          <Sparkles className="w-5 h-5 text-amber-700 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-bold mb-1">Hướng dẫn Phát triển Tiếp theo:</p>
            <p className="text-amber-800">
              Vui lòng xem chi tiết tài liệu hướng dẫn tại <code className="font-mono font-semibold">code/frontend/README.md</code> 
              để tiến hành xây dựng các Components, Hooks và API Services tương ứng theo kế hoạch.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
