import api from './api';

export const authService = {
  async registerCustomer(data) {
    const response = await api.post('/auth/customer/register', data);
    return response.data;
  },

  async loginCustomer(data) {
    const response = await api.post('/auth/customer/login', data);
    return response.data;
  },

  async getMe() {
    const response = await api.get('/auth/customer/me');
    return response.data;
  },
};
