import React, { useState, useEffect } from 'react';
import { BriefcaseBusiness, LogOut, AlertTriangle, RefreshCw, BarChart3, Download } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { reportService } from '../../services/reportService';
import { staffService } from '../../services/staffService';

export function PerformanceReportPage({ onNavigate }) {
  const { user, logout } = useAuth();
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [agentId, setAgentId] = useState('');
  const [priority, setPriority] = useState('');
  const [category, setCategory] = useState('');
  const [dateError, setDateError] = useState('');
  
  const [staffList, setStaffList] = useState([]);
  
  const [loading, setLoading] = useState(false);
  const [reportData, setReportData] = useState(null);
  const [networkError, setNetworkError] = useState(false);

  const handleLogout = () => {
    logout();
    onNavigate('staff-login');
  };

  const formatDateString = (dateObj) => {
    const d = String(dateObj.getDate()).padStart(2, '0');
    const m = String(dateObj.getMonth() + 1).padStart(2, '0');
    const y = dateObj.getFullYear();
    return `${d}/${m}/${y}`;
  };

  const handleQuickSelect = (type) => {
    setDateError('');
    const today = new Date();
    let start = new Date();
    let end = new Date();

    if (type === 'Hôm nay') {
      // already today
    } else if (type === '7 ngày qua') {
      start.setDate(today.getDate() - 7);
    } else if (type === '30 ngày qua') {
      start.setDate(today.getDate() - 30);
    } else if (type === 'Tháng này') {
      start = new Date(today.getFullYear(), today.getMonth(), 1);
    }

    setStartDate(formatDateString(start));
    setEndDate(formatDateString(end));
  };

  const validateDates = () => {
    setDateError('');
    const dateRegex = /^(\d{2})\/(\d{2})\/(\d{4})$/;
    
    if (!dateRegex.test(startDate) || !dateRegex.test(endDate)) {
      setDateError("Ngày nhập không đúng định dạng DD/MM/YYYY");
      return false;
    }

    const [sd, sm, sy] = startDate.split('/');
    const [ed, em, ey] = endDate.split('/');
    
    const startDt = new Date(`${sy}-${sm}-${sd}`);
    const endDt = new Date(`${ey}-${em}-${ed}`);
    const today = new Date();

    if (startDt > endDt) {
      setDateError("Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc");
      return false;
    }

    if (endDt > today) {
      setDateError("Ngày kết thúc không được vượt quá ngày hiện tại");
      return false;
    }

    const diffDays = Math.ceil(Math.abs(endDt - startDt) / (1000 * 60 * 60 * 24));
    if (diffDays > 365) {
      setDateError("Khoảng thời gian tra cứu tối đa không vượt quá 365 ngày");
      return false;
    }

    return true;
  };

  const fetchReport = async () => {
    if (!validateDates()) return;

    setLoading(true);
    setNetworkError(false);
    
    try {
      const params = { start_date: startDate, end_date: endDate };
      if (agentId) params.agent_id = agentId;
      if (priority) params.priority = priority;
      if (category) params.category = category;

      const data = await reportService.getPerformanceReport(params);
      setReportData(data);
    } catch (err) {
      setNetworkError(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleQuickSelect('7 ngày qua');
    staffService.listStaff().then(list => {
      if (list) setStaffList(list);
    }).catch(err => console.error("Lỗi tải danh sách nhân viên:", err));
  }, []);

  if (!user) return null;

  const isE3 = reportData && reportData.n_total === 0;

  return (
    <div className="h-screen bg-[#FFF8E7] text-[#2B2523] selection:bg-[#930500] selection:text-[#FFF8E7] font-sans flex flex-col overflow-hidden">
      <header className="shrink-0 h-16 bg-[#FFF8E7] border-b border-[#EFE7D3] px-6 flex items-center justify-between z-10 shadow-sm">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-[#2B2523] text-[#FFF8E7] flex items-center justify-center">
              <BriefcaseBusiness className="w-4 h-4" />
            </div>
            <div>
              <h1 className="font-serif-editorial text-lg font-bold tracking-tight leading-none">PetHome Live Support</h1>
            </div>
          </div>
          
          <nav className="flex items-center gap-6 border-l border-[#EFE7D3] pl-6">
            <button onClick={() => onNavigate('staff-console')} className="text-sm font-semibold text-[#2B2523]/60 hover:text-[#930500] transition-colors">
              Hàng đợi & Live Chat
            </button>
            <button onClick={() => onNavigate('kanban')} className="text-sm font-semibold text-[#2B2523]/60 hover:text-[#930500] transition-colors">
              Bảng công việc Kanban
            </button>
            <button className="text-sm font-bold text-[#930500] border-b-2 border-[#930500] pb-1">
              Báo cáo thống kê
            </button>
          </nav>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-3 pl-4">
            <div className="text-right">
              <p className="text-sm font-bold leading-none">{user.full_name}</p>
              <p className="text-[10px] text-[#2B2523]/70 mt-0.5">{user.email} • {user.role}</p>
            </div>
            <Button variant="soft" size="sm" icon={LogOut} onClick={handleLogout} className="px-3 py-1.5 h-8 text-xs">Thoát</Button>
          </div>
        </div>
      </header>

      <main className="flex-1 overflow-y-auto p-8 relative">
        <div className="max-w-7xl mx-auto space-y-6">
          <div className="flex justify-between items-end">
            <h2 className="font-serif-editorial text-3xl font-bold">Báo cáo thống kê hiệu suất</h2>
            <Button variant="outline" icon={Download}>Xuất báo cáo</Button>
          </div>

          {networkError && (
            <div className="bg-orange-100 border border-orange-300 text-orange-800 p-4 rounded-xl flex items-center justify-between">
              <div className="flex items-center gap-3">
                <AlertTriangle className="w-5 h-5" />
                <span className="text-sm font-semibold">Không thể tải dữ liệu báo cáo do mất kết nối. Vui lòng kiểm tra lại đường truyền và thử lại!</span>
              </div>
              <Button variant="primary" size="sm" onClick={fetchReport}>Thử lại</Button>
            </div>
          )}

          {/* Filters */}
          <div className="bg-white p-6 rounded-3xl border border-[#EFE7D3] shadow-sm">
            <div className="flex flex-col gap-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 items-end">
                <div className="lg:col-span-1">
                  <Input 
                    label="Từ ngày (DD/MM/YYYY)" 
                    value={startDate} 
                    onChange={(e) => setStartDate(e.target.value)} 
                    className={dateError ? 'border-red-500' : ''}
                  />
                </div>
                <div className="lg:col-span-1">
                  <Input 
                    label="Đến ngày (DD/MM/YYYY)" 
                    value={endDate} 
                    onChange={(e) => setEndDate(e.target.value)} 
                    className={dateError ? 'border-red-500' : ''}
                  />
                </div>
                <div className="lg:col-span-1 w-full flex flex-col gap-1.5">
                  <label className="text-xs uppercase tracking-wider font-semibold text-[#2B2523]/80">Nhân viên phụ trách</label>
                  <select value={agentId} onChange={(e) => setAgentId(e.target.value)} className="w-full bg-[#FFF8E7] text-[#2B2523] border border-[#EFE7D3] rounded-2xl px-4 py-3 text-sm outline-none">
                    <option value="">Tất cả nhân viên</option>
                    {staffList.filter(s => s.role === 'AGENT').map(agent => (
                      <option key={agent.id} value={agent.id}>{agent.full_name}</option>
                    ))}
                  </select>
                </div>
                <div className="lg:col-span-1 w-full flex flex-col gap-1.5">
                  <label className="text-xs uppercase tracking-wider font-semibold text-[#2B2523]/80">Mức độ ưu tiên</label>
                  <select value={priority} onChange={(e) => setPriority(e.target.value)} className="w-full bg-[#FFF8E7] text-[#2B2523] border border-[#EFE7D3] rounded-2xl px-4 py-3 text-sm outline-none">
                    <option value="">Tất cả các mức</option>
                    <option value="P1">P1 (Cực kỳ khẩn cấp)</option>
                    <option value="P2">P2 (Khẩn cấp cao)</option>
                    <option value="P3">P3 (Trung bình)</option>
                  </select>
                </div>
                <div className="lg:col-span-1 w-full flex flex-col gap-1.5">
                  <label className="text-xs uppercase tracking-wider font-semibold text-[#2B2523]/80">Danh mục sự cố</label>
                  <select value={category} onChange={(e) => setCategory(e.target.value)} className="w-full bg-[#FFF8E7] text-[#2B2523] border border-[#EFE7D3] rounded-2xl px-4 py-3 text-sm outline-none">
                    <option value="">Tất cả danh mục</option>
                    <option value="Lỗi đơn hàng">Lỗi đơn hàng</option>
                    <option value="Đổi trả/Hoàn tiền">Đổi trả/Hoàn tiền</option>
                    <option value="Sản phẩm lỗi">Sản phẩm lỗi</option>
                    <option value="Lỗi thanh toán">Lỗi thanh toán</option>
                    <option value="Thái độ phục vụ">Thái độ phục vụ</option>
                    <option value="Vấn đề khác">Vấn đề khác</option>
                  </select>
                </div>
              </div>
              
              <div className="flex justify-between items-center mt-2">
                <div>
                  {dateError && <p className="text-xs text-red-500 font-semibold mb-2">{dateError}</p>}
                  <div className="flex gap-2">
                    <span className="text-sm font-semibold text-gray-500 mr-2">Chọn nhanh:</span>
                    {['Hôm nay', '7 ngày qua', '30 ngày qua', 'Tháng này'].map(type => (
                      <button 
                        key={type} 
                        onClick={() => handleQuickSelect(type)}
                        className="text-xs px-3 py-1.5 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium transition-colors cursor-pointer"
                      >
                        {type}
                      </button>
                    ))}
                  </div>
                </div>
                <Button 
                  variant="primary" 
                  icon={loading ? RefreshCw : BarChart3} 
                  onClick={fetchReport} 
                  disabled={loading}
                  className={loading ? 'opacity-70 cursor-not-allowed' : ''}
                >
                  {loading ? 'Đang tải dữ liệu...' : 'Lọc dữ liệu'}
                </Button>
              </div>
            </div>
          </div>

          {/* Data display */}
          {reportData && (
            isE3 ? (
              <div className="bg-white p-12 rounded-3xl border border-dashed border-[#EFE7D3] text-center">
                <BarChart3 className="w-16 h-16 mx-auto text-gray-300 mb-4" />
                <p className="text-lg font-semibold text-gray-700">Không có dữ liệu phiếu hỗ trợ nào phát sinh trong khoảng thời gian đã chọn</p>
                <div className="mt-8 grid grid-cols-5 gap-4 opacity-50">
                  <MetricCard title="Tổng số" value="0" />
                  <MetricCard title="Đã giải quyết" value="0" />
                  <MetricCard title="Đang xử lý" value="0" />
                  <MetricCard title="Vi phạm SLA" value="0" />
                  <MetricCard title="Tỷ lệ vi phạm" value="0%" />
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                  <MetricCard title="Tổng số phiếu" value={reportData.n_total} />
                  <MetricCard title="Đã giải quyết" value={reportData.n_resolved} color="text-emerald-600" />
                  <MetricCard title="Đang xử lý" value={reportData.n_in_progress} color="text-amber-600" />
                  <MetricCard title="Vi phạm SLA" value={reportData.n_breached} color="text-[#930500]" />
                  <MetricCard title="Tỷ lệ vi phạm SLA" value={`${reportData.sla_breach_rate}%`} color="text-[#930500]" />
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="bg-white p-6 rounded-3xl border border-[#EFE7D3] shadow-sm">
                    <h3 className="font-serif-editorial text-xl font-bold mb-6">Phân bổ cảm xúc khách hàng</h3>
                    <div className="space-y-4">
                      {Object.entries(reportData.sentiment_distribution).map(([key, count]) => {
                        const pct = reportData.n_total > 0 ? (count / reportData.n_total) * 100 : 0;
                        return (
                          <div key={key}>
                            <div className="flex justify-between text-sm mb-1 font-semibold">
                              <span>{key}</span>
                              <span>{count} ({pct.toFixed(1)}%)</span>
                            </div>
                            <div className="w-full bg-gray-100 rounded-full h-2">
                              <div className={`h-2 rounded-full ${key === 'Tích cực' ? 'bg-emerald-500' : key === 'Bình thường' ? 'bg-gray-400' : key === 'Tiêu cực nhẹ' ? 'bg-amber-500' : 'bg-[#930500]'}`} style={{ width: `${pct}%` }}></div>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>

                  <div className="bg-white p-6 rounded-3xl border border-[#EFE7D3] shadow-sm">
                    <h3 className="font-serif-editorial text-xl font-bold mb-6">Năng suất giải quyết (Theo nhân viên)</h3>
                    <div className="space-y-4 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar">
                      {reportData.agent_performance.map(agent => {
                        const pct = agent.n_total > 0 ? (agent.n_resolved / agent.n_total) * 100 : 0;
                        return (
                          <div key={agent.agent_id} className="p-4 border border-gray-100 rounded-xl bg-gray-50">
                            <div className="flex justify-between items-center mb-2">
                              <span className="font-bold text-sm">{agent.agent_name}</span>
                              <span className="text-xs font-semibold text-emerald-700 bg-emerald-100 px-2 py-1 rounded-full">{agent.n_resolved} / {agent.n_total} giải quyết</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-1.5 mt-2">
                              <div className="bg-emerald-500 h-1.5 rounded-full" style={{ width: `${pct}%` }}></div>
                            </div>
                          </div>
                        )
                      })}
                      {reportData.agent_performance.length === 0 && (
                        <div className="text-center text-sm text-gray-500 py-4">Chưa có phân công nào.</div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )
          )}
        </div>
      </main>
    </div>
  );
}

function MetricCard({ title, value, color = "text-gray-900" }) {
  return (
    <div className="bg-white p-5 rounded-3xl border border-[#EFE7D3] shadow-sm">
      <p className="text-xs font-semibold uppercase tracking-wider text-gray-500 mb-2">{title}</p>
      <p className={`text-3xl font-bold font-serif-editorial ${color}`}>{value}</p>
    </div>
  );
}
