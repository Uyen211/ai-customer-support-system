import api from './api';

export const ticketService = {
  async assignTicket(ticketId, agentId) {
    const response = await api.post(`/admin/tickets/${ticketId}/assign`, { agent_id: agentId });
    return response.data;
  },
};
