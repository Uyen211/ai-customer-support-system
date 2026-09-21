import api from './api';

export const agentService = {
  async getQueue() {
    const response = await api.get('/agent/conversations/queue');
    return response.data;
  },

  async takeOver(conversationId) {
    const response = await api.post(`/agent/conversations/${conversationId}/takeover`);
    return response.data;
  },

  async getMessages(conversationId, limit = 50, beforeId = null) {
    let url = `/agent/conversations/${conversationId}/messages?limit=${limit}`;
    if (beforeId) url += `&before_id=${beforeId}`;
    const response = await api.get(url);
    return response.data;
  },

  async sendMessage(conversationId, content) {
    const response = await api.post(`/agent/conversations/${conversationId}/messages`, { content });
    return response.data;
  },
};