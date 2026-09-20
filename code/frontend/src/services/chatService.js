import api from './api';

export const chatService = {
  async getConversations() {
    const response = await api.get('/conversations');
    return response.data;
  },

  async createConversation() {
    const response = await api.post('/conversations');
    return response.data;
  },

  async getConversationDetail(conversationId) {
    const response = await api.get(`/conversations/${conversationId}`);
    return response.data;
  },

  async getMessages(conversationId, limit = 50, beforeId = null) {
    let url = `/conversations/${conversationId}/messages?limit=${limit}`;
    if (beforeId) {
      url += `&before_id=${beforeId}`;
    }
    const response = await api.get(url);
    return response.data;
  },

  async closeConversation(conversationId) {
    const response = await api.post(`/conversations/${conversationId}/close`);
    return response.data;
  },

  async deleteConversation(conversationId) {
    const response = await api.delete(`/conversations/${conversationId}`);
    return response.data;
  },
};

