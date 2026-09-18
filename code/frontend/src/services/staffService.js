import api from './api';

export const staffService = {
  async loginStaff(data) {
    const response = await api.post('/auth/agent/login', data);
    return response.data;
  },

  async getMe() {
    const response = await api.get('/auth/agent/me');
    return response.data;
  },

  async updateStatus(status) {
    const response = await api.put('/agent/status', { status });
    return response.data;
  },

  async listStaff() {
    const response = await api.get('/admin/users');
    return response.data;
  },

  async createStaff(data) {
    const response = await api.post('/admin/users', data);
    return response.data;
  },
};
