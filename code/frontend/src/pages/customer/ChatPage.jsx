import React, { useState, useEffect, useCallback } from 'react';
import { Plus, Search, MessageSquare, LogOut, Home, ArrowLeft, Bot, RefreshCw } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { useSSEChat } from '../../hooks/useSSEChat';
import { chatService } from '../../services/chatService';
import { ChatWindow } from '../../components/chat/ChatWindow';
import { Badge } from '../../components/common/Badge';
import { Button } from '../../components/common/Button';
import { formatTimeAgo } from '../../utils/formatters';

export function ChatPage({ onNavigate }) {
  const { user, logout } = useAuth();
  const { isStreaming, streamedContent, sendMessage, stopStream } = useSSEChat();

  const [conversations, setConversations] = useState([]);
  const [activeConvId, setActiveConvId] = useState(null);
  const [activeConversation, setActiveConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoadingConvs, setIsLoadingConvs] = useState(true);
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const [hasMore, setHasMore] = useState(false);
  const [isLoadingMore, setIsLoadingMore] = useState(false);

  // Load conversations on mount
  const fetchConversations = useCallback(async () => {
    setIsLoadingConvs(true);
    try {
      const list = await chatService.getConversations();
      setConversations(list || []);
      if (list && list.length > 0 && !activeConvId) {
        setActiveConvId(list[0].id);
      }
    } catch (err) {
      console.error('Lỗi lấy danh sách phiên:', err);
    } finally {
      setIsLoadingConvs(false);
    }
  }, [activeConvId]);

  useEffect(() => {
    fetchConversations();
  }, []);

  // Fetch detail and messages when activeConvId changes
  useEffect(() => {
    if (!activeConvId) return;

    async function loadConvData() {
      setIsLoadingMessages(true);
      try {
        const detail = await chatService.getConversationDetail(activeConvId);
        setActiveConversation(detail);

        const msgRes = await chatService.getMessages(activeConvId, 50);
        setMessages(msgRes.messages || []);
        setHasMore(msgRes.has_more || false);
      } catch (err) {
        console.error('Lỗi tải tin nhắn phiên:', err);
      } finally {
        setIsLoadingMessages(false);
      }
    }

    loadConvData();
  }, [activeConvId]);

  // Create New Chat
  const handleCreateNewChat = async () => {
    try {
      const newConv = await chatService.createConversation();
      await fetchConversations();
      setActiveConvId(newConv.conversation_id);
    } catch (err) {
      console.error('Lỗi tạo phiên mới:', err);
    }
  };

  // Load More Messages (Lazy Loading)
  const handleLoadMore = async () => {
    if (!activeConvId || !hasMore || isLoadingMore || messages.length === 0) return;
    const oldestMsgId = messages[0].id;
    setIsLoadingMore(true);

    try {
      const msgRes = await chatService.getMessages(activeConvId, 50, oldestMsgId);
      setMessages((prev) => [...(msgRes.messages || []), ...prev]);
      setHasMore(msgRes.has_more || false);
    } catch (err) {
      console.error('Lỗi nạp tin nhắn cũ:', err);
    } finally {
      setIsLoadingMore(false);
    }
  };

  // Send Message via SSE Stream
  const handleSendUserMessage = async (text) => {
    if (!activeConvId) return;

    const tempUserMsg = {
      id: `temp-${Date.now()}`,
      sender_type: 'CUSTOMER',
      content: text,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, tempUserMsg]);

    await sendMessage({
      conversationId: activeConvId,
      message: text,
      onComplete: ({ fullText, citations }) => {
        setMessages((prev) => [
          ...prev,
          {
            id: `bot-${Date.now()}`,
            sender_type: 'BOT',
            content: fullText,
            citations: citations || [],
            created_at: new Date().toISOString(),
          },
        ]);
        fetchConversations();
      },
      onError: (errText) => {
        setMessages((prev) => [
          ...prev,
          {
            id: `err-${Date.now()}`,
            sender_type: 'BOT',
            content: `⚠️ ${errText}`,
            created_at: new Date().toISOString(),
          },
        ]);
      },
    });
  };

  // Close Conversation
  const handleCloseConversation = async () => {
    if (!activeConvId) return;
    try {
      await chatService.closeConversation(activeConvId);
      setActiveConversation((prev) => (prev ? { ...prev, mode: 'CLOSED' } : null));
      fetchConversations();
    } catch (err) {
      console.error('Lỗi đóng phiên:', err);
    }
  };

  // Filtered Conversations
  const filteredConversations = conversations.filter((c) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      (c.last_message_snippet && c.last_message_snippet.toLowerCase().includes(q)) ||
      (c.id && String(c.id).toLowerCase().includes(q))
    );
  });

  return (
    <div className="h-screen bg-[#FFF8E7] flex flex-col selection:bg-[#930500] selection:text-[#FFF8E7] overflow-hidden">
      
      {/* Top Header Navigation Bar */}
      <header className="h-16 border-b border-[#EFE7D3] px-6 bg-[#FFF8E7] flex items-center justify-between shrink-0">
        <div className="flex items-center gap-4">
          <button
            onClick={() => onNavigate('landing')}
            className="p-2 rounded-full hover:bg-[#EFE7D3] text-[#2B2523] transition-colors"
            title="Về Trang Chủ"
          >
            <Home className="w-5 h-5" />
          </button>
          <div className="flex items-center gap-2">
            <span className="font-serif-editorial text-2xl font-bold text-[#2B2523]">PetHome</span>
            <span className="text-xs uppercase tracking-wider text-[#930500] font-semibold">CSKH AI Workspace</span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-right hidden sm:block">
            <p className="text-xs font-semibold text-[#2B2523]">{user?.full_name || 'Khách hàng'}</p>
            <p className="text-[10px] text-[#2B2523]/60">{user?.email || 'Tài khoản khách hàng'}</p>
          </div>
          <Button
            variant="ghost"
            size="sm"
            icon={LogOut}
            onClick={logout}
            className="text-xs text-[#930500] hover:bg-[#930500]/10"
          >
            Đăng xuất
          </Button>
        </div>
      </header>

      {/* Main Workspace: Sidebar + Chat Window */}
      <div className="flex-1 flex p-4 gap-4 overflow-hidden max-w-[1600px] w-full mx-auto">
        
        {/* Left Sidebar: Conversation List */}
        <aside className="w-80 sm:w-96 flex flex-col bg-[#FFF8E7] rounded-3xl border border-[#EFE7D3] shadow-editorial shrink-0 overflow-hidden">
          
          {/* New Chat CTA */}
          <div className="p-4 border-b border-[#EFE7D3]">
            <Button
              variant="primary"
              size="md"
              icon={Plus}
              onClick={handleCreateNewChat}
              className="w-full justify-center"
            >
              Bắt Đầu Cuộc Trò Chuyện Mới
            </Button>
          </div>

          {/* Search Box */}
          <div className="px-4 py-3 border-b border-[#EFE7D3]">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-3 text-[#2B2523]/40" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Tìm kiếm phiên trò chuyện..."
                className="w-full bg-[#FFF8E7] border border-[#EFE7D3] rounded-2xl py-2 pl-9 pr-3 text-xs focus:outline-none focus:ring-2 focus:ring-[#930500]/20"
              />
            </div>
          </div>

          {/* Conversations List */}
          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            {isLoadingConvs ? (
              <div className="text-center py-8 text-xs text-[#2B2523]/60">Đang tải lịch sử phiên...</div>
            ) : filteredConversations.length === 0 ? (
              <div className="text-center py-8 text-xs text-[#2B2523]/60 font-light">
                Chưa có phiên trò chuyện nào. Bấm nút trên để bắt đầu!
              </div>
            ) : (
              filteredConversations.map((c) => {
                const isActive = c.id === activeConvId;
                return (
                  <div
                    key={c.id}
                    onClick={() => setActiveConvId(c.id)}
                    className={`p-3.5 rounded-2xl cursor-pointer transition-all duration-300 border ${
                      isActive
                        ? 'bg-[#95BBEA]/30 border-[#95BBEA] shadow-diffused-sm'
                        : 'bg-[#FFF8E7] hover:bg-[#EFE7D3]/60 border-[#EFE7D3]'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <Badge variant={c.mode || 'BOT'}>{c.mode || 'BOT'}</Badge>
                      <span className="text-[10px] text-[#2B2523]/50">
                        {formatTimeAgo(c.last_message_at || c.updated_at)}
                      </span>
                    </div>

                    <p className="text-xs font-semibold text-[#2B2523] truncate">
                      {c.last_message_snippet || 'Trò chuyện mới cùng AI Bot'}
                    </p>
                    <p className="text-[10px] text-[#2B2523]/50 mt-1">
                      Mã phiên: #{String(c.id).slice(0, 8)}
                    </p>
                  </div>
                );
              })
            )}
          </div>

        </aside>

        {/* Right Main Chat Area */}
        <main className="flex-1 flex flex-col h-full overflow-hidden">
          {activeConvId ? (
            <ChatWindow
              conversation={activeConversation}
              messages={messages}
              isStreaming={isStreaming}
              streamedContent={streamedContent}
              hasMore={hasMore}
              isLoadingMore={isLoadingMore}
              onLoadMore={handleLoadMore}
              onSendMessage={handleSendUserMessage}
              onStopStream={stopStream}
              onCloseConversation={handleCloseConversation}
            />
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center bg-[#FFF8E7] rounded-3xl border border-[#EFE7D3] p-8 text-center">
              <Bot className="w-16 h-16 text-[#95BBEA] mb-4" />
              <h3 className="font-serif-editorial text-2xl text-[#2B2523]">Chào Mừng Đến Với PetHome AI Workspace</h3>
              <p className="text-sm text-[#2B2523]/70 mt-2 max-w-md font-light">
                Chọn một cuộc trò chuyện ở danh sách bên trái hoặc tạo cuộc trò chuyện mới để được tư vấn.
              </p>
              <Button variant="primary" size="md" icon={Plus} onClick={handleCreateNewChat} className="mt-6">
                Tạo Phiên Trò Chuyện Mới
              </Button>
            </div>
          )}
        </main>

      </div>
    </div>
  );
}
