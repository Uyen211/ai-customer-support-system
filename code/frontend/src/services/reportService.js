import api from './api';

export const reportService = {
  async getPerformanceReport(params) {
    const response = await api.get('/admin/reports/performance', { params });
    return response.data;
  }
};
