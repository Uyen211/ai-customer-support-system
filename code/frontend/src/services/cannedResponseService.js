import api from './api';

export const cannedResponseService = {
  async listResponses(category = null, q = null) {
    let url = '/canned-responses';
    const params = [];
    if (category) params.push(`category=${encodeURIComponent(category)}`);
    if (q) params.push(`q=${encodeURIComponent(q)}`);
    if (params.length) url += `?${params.join('&')}`;
    const response = await api.get(url);
    return response.data;
  },

  async createResponse(data) {
    const response = await api.post('/canned-responses', data);
    return response.data;
  },

  async updateResponse(id, data) {
    const response = await api.put(`/canned-responses/${id}`, data);
    return response.data;
  },

  async deleteResponse(id) {
    const response = await api.delete(`/canned-responses/${id}`);
    return response.data;
  },
};