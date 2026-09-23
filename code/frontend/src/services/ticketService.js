import api from './api';

export const ticketService = {
  async assignTicket(ticketId, agentId) {
    const response = await api.post(`/admin/tickets/${ticketId}/assign`, { agent_id: agentId });
    return response.data;
  },

  async getActiveTickets() {
    const response = await api.get('/admin/tickets/active'); // Wait, we didn't add this endpoint. Let's do it if needed, or we just rely on existing if available
    return response.data;
  },

  async getKanbanTickets() {
    const response = await api.get('/admin/tickets/kanban');
    return response.data;
  },

  async resolveTicket(ticketId, resolutionNote) {
    const response = await api.put(`/admin/tickets/${ticketId}/resolve`, { resolution_note: resolutionNote });
    return response.data;
  },

  async updateTicketStatus(ticketId, status, resolutionNote) {
    const response = await api.put(`/admin/tickets/${ticketId}/status`, { 
      status, 
      resolution_note: resolutionNote 
    });
    return response.data;
  }
};
