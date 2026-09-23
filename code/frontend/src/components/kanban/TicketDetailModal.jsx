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

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-lg">
        <h2 className="text-xl font-bold mb-4">Chi tiết phiếu hỗ trợ</h2>
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">Mã phiếu</label>
          <div className="mt-1 text-sm text-gray-900">{ticket.id}</div>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">Tóm tắt sự cố</label>
          <div className="mt-1 text-sm text-gray-900">{ticket.summary}</div>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">Cập nhật trạng thái</label>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
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
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700">Kết quả xử lý <span className="text-red-500">*</span></label>
              <textarea
                value={note}
                onChange={(e) => {
                  setNote(e.target.value);
                  if (error) setError('');
                }}
                className={`mt-1 block w-full border ${error ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500'} rounded-md shadow-sm p-2`}
                rows="4"
                placeholder="Nhập nội dung kết quả xử lý (10-1000 ký tự)..."
              ></textarea>
              {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
            </div>
          )}

          <div className="flex justify-end gap-3 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Hủy
            </button>
            <button
              type="submit"
              className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Xác nhận hoàn thành
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
