import React, { useState } from 'react';

export default function TicketDetailModal({ ticket, onClose, onSave }) {
  const isPendingStatusUpdate = ticket.pendingTargetStatus != null;
  const initialStatus = isPendingStatusUpdate ? ticket.pendingTargetStatus : ticket.status;
  
  const [status, setStatus] = useState(initialStatus);
  const [note, setNote] = useState('');
  const [error, setError] = useState('');

  const statusOrder = { "PENDING": 1, "IN_PROGRESS": 2, "RESOLVED": 3, "CLOSED": 4 };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (status === 'RESOLVED') {
      if (!note || note.length < 10 || note.length > 1000) {
        setError('Nội dung kết quả xử lý là bắt buộc, độ dài từ 10 đến 1.000 ký tự');
        return;
      }
    }

    onSave(status, note);
  };
  const handleSecondaryAction = (actionName) => {
    alert(`Tính năng "${actionName}" đang được phát triển.`);
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50 p-4">
      <div className="bg-white p-6 rounded-3xl shadow-xl w-full max-w-lg border border-[#EFE7D3]">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-serif-editorial font-bold text-[#2B2523]">Chi tiết phiếu hỗ trợ</h2>
          <span className="px-3 py-1 bg-gray-100 text-gray-600 font-mono text-sm rounded-lg border border-gray-200">
            #{ticket.id.split('-')[0]}
          </span>
        </div>
        
        <div className="mb-5 bg-[#FFF8E7]/50 p-4 rounded-2xl border border-[#EFE7D3]">
          <label className="block text-xs uppercase tracking-wider font-semibold text-[#2B2523]/70 mb-1">Tóm tắt sự cố</label>
          <div className="text-sm font-medium text-[#2B2523]">{ticket.summary}</div>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-5">
            <label className="block text-xs uppercase tracking-wider font-semibold text-[#2B2523]/70 mb-2">Cập nhật trạng thái</label>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              className="w-full bg-white text-[#2B2523] border border-[#EFE7D3] rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#95BBEA] transition-all"
              disabled={isPendingStatusUpdate}
            >
              {Object.keys(statusOrder).map(s => (
                <option key={s} value={s} disabled={statusOrder[s] <= statusOrder[ticket.status] && s !== ticket.status && s !== ticket.pendingTargetStatus}>
                  {s === 'PENDING' ? 'Chờ tiếp nhận' : 
                   s === 'IN_PROGRESS' ? 'Đang xử lý' : 
                   s === 'RESOLVED' ? 'Đã giải quyết' : 'Đóng phiếu'}
                </option>
              ))}
            </select>
          </div>

          {status === 'RESOLVED' && (
            <div className="mb-6">
              <label className="block text-xs uppercase tracking-wider font-semibold text-[#2B2523]/70 mb-2">Kết quả xử lý <span className="text-[#930500]">*</span></label>
              <textarea
                value={note}
                onChange={(e) => {
                  setNote(e.target.value);
                  if (error) setError('');
                }}
                className={`w-full bg-[#FFF8E7]/50 text-[#2B2523] border rounded-xl px-4 py-3 text-sm outline-none resize-y min-h-[100px] transition-colors ${error ? 'border-[#930500] focus:ring-1 focus:ring-[#930500]' : 'border-[#EFE7D3] focus:border-[#95BBEA] focus:ring-1 focus:ring-[#95BBEA]'}`}
                placeholder="Nhập nội dung kết quả xử lý (10-1000 ký tự)..."
              ></textarea>
              {error && <p className="mt-1.5 text-xs text-[#930500] font-medium">{error}</p>}
            </div>
          )}

          <div className="flex flex-col sm:flex-row justify-between items-center gap-3 pt-4 border-t border-[#EFE7D3]">
            <div className="flex gap-2 w-full sm:w-auto">
              <button type="button" onClick={() => handleSecondaryAction('Chuyển tiếp')} className="flex-1 sm:flex-none px-4 py-2 bg-[#FFF8E7] text-[#2B2523] border border-[#EFE7D3] hover:bg-[#EFE7D3] rounded-full text-sm font-medium transition-colors">
                Chuyển tiếp
              </button>
              <button type="button" onClick={() => handleSecondaryAction('Tạm dừng')} className="flex-1 sm:flex-none px-4 py-2 bg-[#FFF8E7] text-[#2B2523] border border-[#EFE7D3] hover:bg-[#EFE7D3] rounded-full text-sm font-medium transition-colors">
                Tạm dừng
              </button>
            </div>

            <div className="flex gap-2 w-full sm:w-auto">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 sm:flex-none px-5 py-2.5 bg-transparent text-[#2B2523]/70 hover:text-[#2B2523] hover:bg-gray-100 rounded-full text-sm font-medium transition-colors"
              >
                Hủy
              </button>
              <button
                type="submit"
                className="flex-1 sm:flex-none px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm rounded-full shadow-md shadow-emerald-600/20 transition-all duration-300 active:scale-95 flex items-center justify-center gap-2"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                Xác nhận đã xử lý
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
