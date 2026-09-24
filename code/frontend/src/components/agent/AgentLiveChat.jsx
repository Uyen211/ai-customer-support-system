import React, { useEffect, useRef, useState } from 'react';
import {
  AlertTriangle,
  CheckCircle2,
  Clock,
  Eye,
  Handshake,
  MessageSquare,
  PhoneCall,
  Plus,
  RefreshCw,
  Send,
  Sparkles,
  UserCheck,
  UserRound,
  X,
} from 'lucide-react';
import { useWebSocket } from '../../hooks/useWebSocket';
import { agentService } from '../../services/agentService';
import { cannedResponseService } from '../../services/cannedResponseService';
import { getWsBaseUrl } from '../../utils/constants';
import { formatTimeAgo } from '../../utils/formatters';
import { Badge } from '../../components/common/Badge';
import { Button } from '../../components/common/Button';

const SENTIMENT_META = {
  POSITIVE: { label: 'Tích cực', cls: 'text-emerald-700 bg-emerald-100 border-emerald-200' },
  NEUTRAL: { label: 'Trung tính', cls: 'text-stone-600 bg-stone-100 border-stone-200' },
  NEGATIVE: { label: 'Tiêu cực', cls: 'text-amber-700 bg-amber-100 border-amber-200' },
  CRITICAL: { label: 'Nghiêm trọng', cls: 'text-[#930500] bg-[#930500]/10 border-[#930500]/20' },
};

function sentimentMeta(value) {
  return SENTIMENT_META[value] || null;
}

export function AgentLiveChat({ currentUser }) {
  const [queue, setQueue] = useState([]);
  const [activeConv, setActiveConv] = useState(null);
  const [messages, setMessages] = useState([]);
  const [mode, setMode] = useState('BOT');
  const [inputText, setInputText] = useState('');
  const [isLoadingQueue, setIsLoadingQueue] = useState(false);
  const [isLoadingMsgs, setIsLoadingMsgs] = useState(false);
  const [isTakingOver, setIsTakingOver] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [notice, setNotice] = useState(null);
  const [loadError, setLoadError] = useState(null);

  // Gợi ý mẫu phản hồi khi gõ "/"
  const [suggestIndex, setSuggestIndex] = useState(0);
  const inputRef = useRef(null);

  // Canned Responses
  const [cannedOpen, setCannedOpen] = useState(false);
  const [cannedList, setCannedList] = useState([]);
  const [isCannedLoading, setIsCannedLoading] = useState(false);
  const [isCannedModalOpen, setIsCannedModalOpen] = useState(false);
  const [cannedForm, setCannedForm] = useState({ shortcut: '', title: '', content: '', category: '' });

  const msgEndRef = useRef(null);
  const scrollTimer = useRef(null);

  const roomSocket = useWebSocket(
    activeConv ? `${getWsBaseUrl()}/ws/chat/${activeConv.id}` : null,
    { autoReconnect: true }
  );

  // Lắng nghe sự kiện toàn cục để cập nhật hàng đợi theo thời gian thực
  const globalAlerts = useWebSocket(`${getWsBaseUrl()}/ws/alerts`, { autoReconnect: true });

  useEffect(() => {
    const m = globalAlerts.lastMessage;
    if (m && ['QUEUE_UPDATED', 'CHAT_MODE_CHANGED', 'CONVERSATION_DELETED', 'TICKET_ASSIGNED'].includes(m.event)) {
      loadQueue();
    }
    if (m && m.event === 'CANNED_RESPONSE_CREATED') {
      cannedResponseService.listResponses().then((list) => setCannedList(list || [])).catch(() => {});
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [globalAlerts.lastMessage]);

  const clearNotice = () => {
    if (scrollTimer.current) clearTimeout(scrollTimer.current);
    scrollTimer.current = setTimeout(() => setNotice(null), 5000);
  };

  const showNotice = (type, message) => {
    setNotice({ type, message });
    clearNotice();
  };

  const loadQueue = async () => {
    try {
      const data = await agentService.getQueue();
      setQueue(data || []);
      setLoadError(null);
      if (!activeConv && data && data.length > 0) {
        setActiveConv(data[0]);
      }
    } catch (error) {
      setLoadError(error.response?.data?.detail || 'Không thể tải hàng đợi hội thoại.');
    } finally {
      setIsLoadingQueue(false);
    }
  };

  useEffect(() => {
    setIsLoadingQueue(true);
    loadQueue();
    const poll = setInterval(loadQueue, 15000);
    return () => clearInterval(poll);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Nạp sẵn danh sách mẫu phản hồi nhanh để gõ "/" gợi ý ngay khi mở console
  useEffect(() => {
    cannedResponseService.listResponses().then((list) => setCannedList(list || [])).catch(() => {});
  }, []);

  const loadMessages = async (convId) => {
    setIsLoadingMsgs(true);
    try {
      const res = await agentService.getMessages(convId, 50);
      setMessages(res.messages || []);
      setMode(res.mode || 'BOT');
    } catch (error) {
      showNotice('error', error.response?.data?.detail || 'Không thể tải lịch sử tin nhắn.');
    } finally {
      setIsLoadingMsgs(false);
    }
  };

  useEffect(() => {
    if (!activeConv) {
      setMessages([]);
      setMode('BOT');
      return;
    }
    loadMessages(activeConv.id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeConv?.id]);

  const appendMessage = (payload) => {
    setMessages((prev) => {
      if (payload?.id && prev.find((m) => m.id === payload.id || m.id === `temp-${payload.id}`)) return prev;
      return [...prev, payload];
    });
  };

  // Xử lý sự kiện thời gian thực từ phòng chat
  useEffect(() => {
    const msg = roomSocket.lastMessage;
    if (!msg) return;

    if (msg.event === 'CHAT_MESSAGE' && msg.payload) {
      appendMessage(msg.payload);
    } else if (msg.event === 'CHAT_MODE_CHANGED' && msg.payload) {
      const p = msg.payload;
      setMode(p.mode || 'HUMAN');
      if (p.notice_message) appendMessage(p.notice_message);
      setActiveConv((prev) =>
        prev
          ? {
              ...prev,
              mode: p.mode || 'HUMAN',
              assigned_agent_id: p.assigned_agent_id || prev.assigned_agent_id,
              assigned_agent_name: p.assigned_agent_name || prev.assigned_agent_name,
            }
          : prev
      );
      loadQueue();
    } else if (msg.event === 'CONVERSATION_DELETED' && msg.payload) {
      const deletedId = msg.payload.conversation_id || msg.payload.deleted_id;
      setQueue((prev) => prev.filter((c) => c.id !== deletedId));
      if (activeConv && activeConv.id === deletedId) {
        setActiveConv(null);
        setMessages([]);
      }
    } else if (msg.event === 'ERROR' && msg.payload?.error) {
      showNotice('error', msg.payload.error);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [roomSocket.lastMessage]);

  const handleSelectConversation = (item) => {
    setActiveConv(item);
  };

  const formatErrorDetail = (detail) => {
    if (Array.isArray(detail)) {
      return detail.map(d => d.msg || JSON.stringify(d)).join('; ');
    }
    return detail;
  };

  const handleTakeover = async (convObj = activeConv) => {
    // Nếu convObj là React Event (do truyền thẳng vào onClick), bỏ qua và dùng activeConv
    const targetConv = (convObj && convObj.id) ? convObj : activeConv;
    if (!targetConv || !targetConv.id) return;
    
    setIsTakingOver(true);
    try {
      const detail = await agentService.takeOver(targetConv.id);
      setMode(detail.mode || 'HUMAN');
      setActiveConv((prev) => (prev && prev.id === targetConv.id ? { ...prev, mode: detail.mode || 'HUMAN', assigned_agent_id: currentUser.id, assigned_agent_name: currentUser.full_name, is_flagged: false } : prev));
      showNotice('success', `Bạn đã tiếp quản cuộc trò chuyện với ${targetConv.customer_name || 'khách hàng'}.`);
      loadQueue();
      await loadMessages(targetConv.id);
    } catch (error) {
      showNotice('error', formatErrorDetail(error.response?.data?.detail) || 'Tiếp quản thất bại.');
      loadQueue();
    } finally {
      setIsTakingOver(false);
    }
  };


  useEffect(() => {
    const handleGlobalSelect = async (e) => {
      const { conversation_id, autoTakeover } = e.detail;
      if (!conversation_id) return;
      
      let conv = queue.find(c => c.id === conversation_id);
      
      if (!conv) {
        // If not in current queue view, try to load fresh queue
        const freshQueue = await agentService.getQueue();
        setQueue(freshQueue || []);
        conv = freshQueue?.find(c => c.id === conversation_id);
      }

      if (conv) {
        setActiveConv(conv);
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
        if (autoTakeover && conv.mode !== 'HUMAN') {
          handleTakeover(conv);
        }
      } else {
        showNotice('error', 'Không tìm thấy phiên hội thoại này trong hàng đợi.');
      }
    };

    window.addEventListener('agent:select_chat', handleGlobalSelect);
    return () => window.removeEventListener('agent:select_chat', handleGlobalSelect);
  }, [queue, currentUser]);


  const handleSend = async (e) => {
    e?.preventDefault();
    if (!activeConv || !inputText.trim() || isSending || isReadOnly) return;
    const content = inputText.trim();
    setInputText('');

    if (roomSocket.isConnected) {
      roomSocket.send({ type: 'send_message', content });
      return;
    }

    setIsSending(true);
    try {
      const res = await agentService.sendMessage(activeConv.id, content);
      if (res?.message) appendMessage(res.message);
    } catch (error) {
      showNotice('error', formatErrorDetail(error.response?.data?.detail) || 'Không thể gửi tin nhắn.');
    } finally {
      setIsSending(false);
    }
  };

  const toggleCanned = async () => {
    if (!cannedOpen) {
      setCannedOpen(true);
      setIsCannedLoading(true);
      try {
        const list = await cannedResponseService.listResponses();
        setCannedList(list || []);
      } catch (error) {
        showNotice('error', error.response?.data?.detail || 'Không thể tải mẫu phản hồi nhanh.');
      } finally {
        setIsCannedLoading(false);
      }
    } else {
      setCannedOpen(false);
    }
  };

  const handlePickCanned = (item) => {
    setInputText((prev) => (prev ? `${prev}\n${item.content}` : item.content));
  };

  // Phím tắt "/" để chèn mẫu phản hồi (UC 3.4: gõ / -> bảng gợi ý)
  const getSuggestMatch = (text) => {
    const m = text.match(/(^|\s)(\/[^\s]*)$/);
    if (!m) return null;
    const start = m[1].length === 0 ? 0 : m.index + m[1].length;
    return { start, token: m[2].toLowerCase() };
  };

  const suggestMatch = getSuggestMatch(inputText);
  const suggestQuery = suggestMatch ? suggestMatch.token.slice(1) : '';
  const suggestItems = suggestMatch
    ? cannedList
        .filter((item) => {
          const st = `/${item.shortcut.toLowerCase()}`;
          return st.startsWith(suggestMatch.token) || item.title.toLowerCase().includes(suggestQuery);
        })
        .slice(0, 7)
    : [];

  const applySuggestion = (item) => {
    if (!suggestMatch || !item) return;
    const { start, token } = suggestMatch;
    const before = inputText.slice(0, start);
    const after = inputText.slice(start + token.length);
    setInputText(`${before}${item.content}${after}`);
    setSuggestIndex(0);
    inputRef.current?.focus();
  };

  const handleInputKeyDown = (e) => {
    if (suggestItems.length > 0) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSuggestIndex((i) => (i + 1) % suggestItems.length);
        return;
      }
      if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSuggestIndex((i) => (i - 1 + suggestItems.length) % suggestItems.length);
        return;
      }
      if (e.key === 'Enter' || e.key === 'Tab') {
        e.preventDefault();
        applySuggestion(suggestItems[suggestIndex]);
        return;
      }
      if (e.key === 'Escape') {
        e.preventDefault();
        setSuggestIndex(0);
        setInputText((prev) => `${prev} `);
        return;
      }
    } else {
      setSuggestIndex(0);
    }
  };

  const isManager = ['MANAGER', 'ADMIN'].includes(currentUser?.role);
  const isReadOnly =
    activeConv && activeConv.assigned_agent_id && activeConv.assigned_agent_id !== currentUser?.id && !isManager;

  const canChat = (mode === 'HUMAN' || mode === 'WAITING_HUMAN') && !isReadOnly;

  return (
    <div className="rounded-3xl border border-[#EFE7D3] bg-white shadow-editorial overflow-hidden">
      <div className="flex items-center gap-3 px-6 py-5 border-b border-[#EFE7D3]">
        <div className="w-10 h-10 rounded-2xl bg-[#95BBEA] text-[#2B2523] flex items-center justify-center shadow-inner">
          <Handshake className="w-5 h-5" />
        </div>
        <div className="flex-1">
          <h2 className="font-serif-editorial text-2xl font-bold">Hàng Đợi Hội Thoại Trực Tuyến</h2>
          <p className="text-xs text-[#2B2523]/70 mt-0.5">
            Các phiên khách hàng đang chờ nhân viên tiếp quản (Cờ đỏ / WAITING_HUMAN)
            {roomSocket.isConnected ? ' — Real-time: Online' : ' — Real-time: Reconnecting...'}
          </p>
        </div>
        <Button variant="soft" size="sm" icon={RefreshCw} onClick={loadQueue}>Làm mới</Button>
      </div>

      {notice && (
        <div className={`px-6 py-3 border-b text-sm flex items-center gap-2 ${notice.type === 'success' ? 'bg-emerald-50 border-emerald-100 text-emerald-800' : 'bg-[#930500]/10 border-[#930500]/20 text-[#930500]'}`}>
          {notice.type === 'success' ? <CheckCircle2 className="w-4 h-4 shrink-0" /> : <AlertTriangle className="w-4 h-4 shrink-0" />}
          {notice.message}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-0">
        {/* Cột hàng đợi */}
        <div className="lg:col-span-2 border-r border-[#EFE7D3] max-h-[560px] overflow-y-auto p-3 space-y-2 bg-[#FFF8E7]/40">
          {isLoadingQueue ? (
            <div className="text-center py-10 text-xs text-[#2B2523]/50">Đang tải hàng đợi...</div>
          ) : queue.length === 0 ? (
            <div className="py-12 text-center rounded-2xl border border-dashed border-[#EFE7D3]">
              <UserRound className="w-10 h-10 mx-auto text-[#2B2523]/25 mb-2" />
              <p className="text-sm font-medium text-[#2B2523]/60">Hàng đợi trống</p>
              <p className="text-xs text-[#2B2523]/40 mt-1">Chưa có hội thoại nào cần nhân viên.</p>
            </div>
          ) : (
            queue.map((item) => {
              const isActive = activeConv && activeConv.id === item.id;
              const isMine = item.assigned_agent_id === currentUser.id;
              return (
                <button
                  key={item.id}
                  onClick={() => handleSelectConversation(item)}
                  className={`w-full text-left p-4 rounded-2xl border transition-all duration-300 cursor-pointer group relative ${
                    isActive
                      ? 'bg-[#95BBEA]/30 border-[#95BBEA] shadow-diffused-sm'
                      : 'bg-white hover:bg-[#EFE7D3]/60 border-[#EFE7D3]'
                  }`}
                >
                  {item.is_flagged && (
                    <span className="absolute top-3 right-3">
                      <AlertTriangle className="w-4 h-4 text-[#930500]" />
                    </span>
                  )}
                  <div className="flex items-center gap-2 mb-1.5">
                    <span className="w-7 h-7 rounded-full bg-[#2B2523] text-[#FFF8E7] flex items-center justify-center text-xs font-bold">
                      {(item.customer_name || 'K').charAt(0)}
                    </span>
                    <span className="text-sm font-semibold text-[#2B2523] truncate flex-1">
                      {item.customer_name || 'Khách hàng'}
                    </span>
                    <Badge variant={item.mode}>{item.mode}</Badge>
                  </div>
                  {sentimentMeta(item.last_sentiment) && (
                    <div className="flex items-center gap-1.5 mb-1.5">
                      <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full border text-[10px] font-bold ${sentimentMeta(item.last_sentiment).cls}`}>
                        <span className="w-1.5 h-1.5 rounded-full bg-current" />
                        {sentimentMeta(item.last_sentiment).label}
                      </span>
                    </div>
                  )}
                  <p className="text-xs text-[#2B2523]/70 line-clamp-2 min-h-[2rem]">{item.last_message_content || 'Cuộc trò chuyện mới — chưa có tin nhắn.'}</p>
                  <div className="flex items-center justify-between mt-2 text-[10px] text-[#2B2523]/50">
                    <span>{item.last_message_time ? formatTimeAgo(item.last_message_time) : '—'}</span>
                    <span className="flex items-center gap-1">
                      {isMine ? <UserCheck className="w-3.5 h-3.5 text-emerald-600" /> : <Clock className="w-3.5 h-3.5" />}
                      {isMine ? 'Của bạn' : (item.assigned_agent_name || 'Chưa ai nhận')}
                    </span>
                  </div>
                </button>
              );
            })
          )}
        </div>

        {/* Cột chat */}
        <div className="lg:col-span-3 flex flex-col h-[560px]">
          {!activeConv ? (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
              <MessageSquare className="w-14 h-14 text-[#95BBEA]" />
              <h3 className="font-serif-editorial text-xl mt-4">Chọn một hội thoại ở hàng đợi</h3>
              <p className="text-sm text-[#2B2523]/60 mt-1">Xem trước tin nhắn, sau đó bấm "Tiếp quản" để vào cuộc trò chuyện thời gian thực.</p>
            </div>
          ) : (
            <>
              {/* Header phiên */}
              <div className="px-6 py-4 border-b border-[#EFE7D3] bg-[#FFF8E7]/60 flex items-center justify-between gap-3">
                <div className="flex items-center gap-3 min-w-0">
                  <div className="w-9 h-9 rounded-full bg-[#2B2523] text-[#FFF8E7] flex items-center justify-center text-sm font-bold shrink-0">
                    {(activeConv.customer_name || 'K').charAt(0)}
                  </div>
                  <div className="min-w-0">
                    <h3 className="font-semibold text-[#2B2523] truncate">{activeConv.customer_name || 'Khách hàng'}</h3>
                    <div className="flex items-center gap-2 text-[11px] text-[#2B2523]/60">
                      <span className="font-mono">#{activeConv.id.slice(0, 8)}</span>
                      {activeConv.assigned_agent_name && (
                        <span className="inline-flex items-center gap-1 text-emerald-700">
                          <UserCheck className="w-3.5 h-3.5" /> {activeConv.assigned_agent_name}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {mode !== 'HUMAN' && !isReadOnly && (
                  <Button variant="primary" size="sm" icon={PhoneCall} isLoading={isTakingOver} onClick={() => handleTakeover()}>
                    Tiếp Quản
                  </Button>
                )}
                {mode === 'HUMAN' && (
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold">
                    <UserCheck className="w-4 h-4" /> Đang phục vụ
                  </span>
                )}
                {isReadOnly && (
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#2B2523]/10 text-[#2B2523] text-xs font-bold">
                    <Eye className="w-4 h-4" /> Chỉ xem
                  </span>
                )}
              </div>

              {/* Trạng thái chờ sau khi vào, trước khi nhân viên nhận */}
              {mode === 'WAITING_HUMAN' && (
                <div className="px-6 py-2.5 bg-[#FEF3C7] border-b border-[#FDE68A] text-xs text-[#92400E] flex items-center gap-2">
                  <Clock className="w-4 h-4 text-[#D97706] shrink-0" />
                  <span>Khách hàng đang chờ nhân viên tiếp quản. Bấm "Tiếp Quản" để nhận cuộc trò chuyện.</span>
                </div>
              )}

              {/* E-1: Phiên đã được nhân viên khác tiếp quản -> Chỉ xem */}
              {isReadOnly && (
                <div className="px-6 py-2.5 bg-[#2B2523]/5 border-b border-[#EFE7D3] text-xs text-[#2B2523]/70 flex items-center gap-2">
                  <Eye className="w-4 h-4 shrink-0" />
                  <span>
                    Cuộc trò chuyện này đã được nhân viên {activeConv.assigned_agent_name || 'khác'} tiếp quản. Bạn chỉ được xem.
                  </span>
                </div>
              )}

              {/* Danh sách tin nhắn */}
              <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-[#FFF8E7]/30">
                {isLoadingMsgs ? (
                  <div className="text-center py-10 text-xs text-[#2B2523]/50">Đang tải tin nhắn...</div>
                ) : messages.length === 0 ? (
                  <div className="text-center py-10 text-xs text-[#2B2523]/40">Chưa có tin nhắn trong phiên này.</div>
                ) : (
                  messages.map((m, idx) => {
                    const fromCustomer = m.sender_type === 'CUSTOMER';
                    return (
                      <div key={m.id || idx} className={`flex ${fromCustomer ? 'justify-end' : 'justify-start'}`}>
                        <div
                          className={`max-w-[78%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed shadow-sm ${
                            fromCustomer
                              ? 'bg-[#2B2523] text-[#FFF8E7] rounded-br-md'
                              : m.sender_type === 'AGENT'
                                ? 'bg-[#95BBEA] text-[#1F242B] rounded-bl-md'
                                : 'bg-[#EFE7D3] text-[#2B2523] italic rounded-bl-md'
                          }`}
                        >
                          {m.sender_type === 'AGENT' && (
                            <p className="text-[10px] font-bold uppercase tracking-wider opacity-70 mb-0.5">{activeConv.assigned_agent_name || 'Bạn'}</p>
                          )}
                          {m.sender_type === 'BOT' && (
                            <p className="text-[10px] font-bold uppercase tracking-wider opacity-60 mb-0.5">Hệ thống</p>
                          )}
                          <p className="whitespace-pre-wrap break-words">{m.content}</p>
                          <p className="text-[10px] opacity-60 mt-1 text-right">{formatTimeAgo(m.created_at)}</p>
                        </div>
                      </div>
                    );
                  })
                )}
                <div ref={msgEndRef} />
              </div>

              {/* Input + Canned */}
              <div className="p-4 border-t border-[#EFE7D3] bg-white">
                {cannedOpen && (
                  <div className="mb-3 rounded-2xl border border-[#EFE7D3] bg-[#FFF8E7] max-h-44 overflow-y-auto">
                    <div className="flex items-center justify-between px-4 py-2 border-b border-[#EFE7D3]">
                      <span className="text-xs font-bold uppercase tracking-wider text-[#930500]">Mẫu Phản Hồi Nhanh</span>
                      <div className="flex items-center gap-2">
                        <button
                          type="button"
                          onClick={() => setIsCannedModalOpen(true)}
                          className="inline-flex items-center gap-1 text-[11px] font-semibold text-[#930500] hover:text-[#7a0400] cursor-pointer"
                        >
                          <Plus className="w-3.5 h-3.5" /> Tạo mẫu
                        </button>
                        <button type="button" onClick={() => setCannedOpen(false)} className="text-[#2B2523]/50 hover:text-[#930500] cursor-pointer">
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                    {isCannedLoading ? (
                      <p className="px-4 py-3 text-xs text-[#2B2523]/50">Đang tải...</p>
                    ) : cannedList.length === 0 ? (
                      <p className="px-4 py-3 text-xs text-[#2B2523]/50">Chưa có mẫu phản hồi nào.</p>
                    ) : (
                      <div className="divide-y divide-[#EFE7D3]">
                        {cannedList.map((item) => (
                          <button
                            key={item.id}
                            type="button"
                            onClick={() => handlePickCanned(item)}
                            className="w-full text-left px-4 py-2.5 hover:bg-[#95BBEA]/15 transition-colors cursor-pointer"
                          >
                            <span className="text-[11px] font-mono text-[#930500] font-bold">/{item.shortcut}</span>
                            <span className="ml-2 text-sm font-semibold text-[#2B2523]">{item.title}</span>
                            <span className="block text-xs text-[#2B2523]/60 line-clamp-1 mt-0.5">{item.content}</span>
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {suggestItems.length > 0 && (
                  <div className="mb-3 rounded-2xl border border-[#95BBEA] bg-white shadow-editorial overflow-hidden">
                    <div className="flex items-center justify-between px-4 py-2 bg-[#95BBEA]/20 border-b border-[#95BBEA]/40">
                      <span className="text-[11px] font-bold uppercase tracking-wider text-[#930500]">
                        Mẫu phản hồi nhanh — bấm Enter để chèn
                      </span>
                      <span className="text-[10px] text-[#2B2523]/50">↑↓ duyệt · Esc đóng</span>
                    </div>
                    <div className="max-h-44 overflow-y-auto divide-y divide-[#EFE7D3]">
                      {suggestItems.map((item, idx) => (
                        <button
                          key={item.id}
                          type="button"
                          onClick={() => applySuggestion(item)}
                          onMouseEnter={() => setSuggestIndex(idx)}
                          className={`w-full text-left px-4 py-2.5 transition-colors cursor-pointer ${idx === suggestIndex ? 'bg-[#95BBEA]/25' : 'hover:bg-[#95BBEA]/10'}`}
                        >
                          <span className="text-[11px] font-mono text-[#930500] font-bold">/{item.shortcut}</span>
                          <span className="ml-2 text-sm font-semibold text-[#2B2523]">{item.title}</span>
                          <span className="block text-xs text-[#2B2523]/60 line-clamp-1 mt-0.5">{item.content}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                <form onSubmit={handleSend} className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={toggleCanned}
                    title="Mở mẫu phản hồi nhanh"
                    className="w-9 h-9 rounded-full bg-[#EFE7D3] text-[#2B2523] flex items-center justify-center hover:bg-[#95BBEA]/40 transition-colors cursor-pointer shrink-0"
                  >
                    <Sparkles className="w-4 h-4" />
                  </button>
                  <textarea
                    ref={inputRef}
                    rows={1}
                    value={inputText}
                    onChange={(e) => { setInputText(e.target.value); setSuggestIndex(0); }}
                    onKeyDown={handleInputKeyDown}
                    placeholder={
                      isReadOnly
                        ? 'Phiên đã được nhân viên khác tiếp quản — bạn chỉ được xem...'
                        : canChat
                          ? 'Nhập câu trả lời cho khách hàng...'
                          : 'Bấm "Tiếp Quản" để nhận và trả lời cuộc trò chuyện...'
                    }
                    disabled={isReadOnly}
                    className="flex-1 bg-[#FFF8E7] text-[#2B2523] placeholder-[#2B2523]/40 border border-[#EFE7D3] focus:border-[#930500] rounded-2xl py-3 px-4 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-[#930500]/20 transition-all disabled:opacity-50"
                  />
                  <button
                    type="submit"
                    disabled={!inputText.trim() || !canChat || isSending}
                    className="w-9 h-9 rounded-full bg-[#930500] text-[#FFF8E7] flex items-center justify-center hover:bg-[#7a0400] disabled:opacity-40 transition-all cursor-pointer shrink-0 shadow-diffused-sm"
                    title="Gửi tin nhắn"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                </form>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Modal tạo mẫu phản hồi */}
      {isCannedModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#2B2523]/40 backdrop-blur-sm animate-fade-in">
          <div className="bg-[#FFF8E7] w-full max-w-lg rounded-[32px] p-8 shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 left-0 w-32 h-32 bg-[#930500]/10 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2 pointer-events-none" />
            <h3 className="font-serif-editorial text-2xl font-bold mb-1">Tạo mẫu phản hồi nhanh</h3>
            <p className="text-sm text-[#2B2523]/70 mb-6">Mẫu sẽ hiển thị trong danh sách gợi ý để chèn nhanh vào khung chat.</p>

            <div className="space-y-4">
              <div>
                <label className="text-xs uppercase tracking-wider font-semibold text-[#2B2523]/80 block mb-1.5">Shortcut</label>
                <input
                  value={cannedForm.shortcut}
                  onChange={(e) => setCannedForm((p) => ({ ...p, shortcut: e.target.value }))}
                  placeholder="/hoan-tien"
                  className="w-full bg-white border border-[#EFE7D3] rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#930500]/20"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs uppercase tracking-wider font-semibold text-[#2B2523]/80 block mb-1.5">Tiêu đề</label>
                  <input
                    value={cannedForm.title}
                    onChange={(e) => setCannedForm((p) => ({ ...p, title: e.target.value }))}
                    placeholder="Chính sách hoàn tiền"
                    className="w-full bg-white border border-[#EFE7D3] rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#930500]/20"
                  />
                </div>
                <div>
                  <label className="text-xs uppercase tracking-wider font-semibold text-[#2B2523]/80 block mb-1.5">Danh mục</label>
                  <input
                    value={cannedForm.category}
                    onChange={(e) => setCannedForm((p) => ({ ...p, category: e.target.value }))}
                    placeholder="Chính sách"
                    className="w-full bg-white border border-[#EFE7D3] rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#930500]/20"
                  />
                </div>
              </div>
              <div>
                <label className="text-xs uppercase tracking-wider font-semibold text-[#2B2523]/80 block mb-1.5">Nội dung mẫu</label>
                <textarea
                  rows={4}
                  value={cannedForm.content}
                  onChange={(e) => setCannedForm((p) => ({ ...p, content: e.target.value }))}
                  placeholder="Chào bạn, chúng tôi sẽ hoàn tiền..."
                  className="w-full bg-white border border-[#EFE7D3] rounded-2xl px-4 py-3 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-[#930500]/20"
                />
              </div>
            </div>

            <div className="flex items-center justify-end gap-3 mt-6">
              <button
                onClick={() => { setIsCannedModalOpen(false); setCannedForm({ shortcut: '', title: '', content: '', category: '' }); }}
                className="px-6 py-3 rounded-full text-sm font-semibold text-[#2B2523]/70 hover:bg-black/5 transition-colors cursor-pointer"
              >
                Hủy
              </button>
              <button
                onClick={async () => {
                  if (!cannedForm.shortcut || !cannedForm.content || !cannedForm.title || !cannedForm.category) {
                    showNotice('error', 'Vui lòng điền đầy đủ thông tin mẫu.');
                    return;
                  }
                  try {
                    await cannedResponseService.createResponse(cannedForm);
                    showNotice('success', 'Đã tạo mẫu phản hồi nhanh.');
                    setIsCannedModalOpen(false);
                    setCannedForm({ shortcut: '', title: '', content: '', category: '' });
                    const list = await cannedResponseService.listResponses();
                    setCannedList(list || []);
                  } catch (error) {
                    showNotice('error', error.response?.data?.detail || 'Không thể tạo mẫu phản hồi.');
                  }
                }}
                className="px-6 py-3 rounded-full bg-[#930500] text-white text-sm font-semibold shadow-md shadow-[#930500]/20 hover:bg-[#7a0400] transition-all cursor-pointer"
              >
                Lưu mẫu
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}