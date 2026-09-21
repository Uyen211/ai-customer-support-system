import unittest
from unittest.mock import MagicMock, patch
from app.workers.ticket_dispatcher_worker import process_ticket_sync

class TestTicketDispatcher(unittest.TestCase):

    @patch("app.workers.ticket_dispatcher_worker.SessionLocal")
    @patch("app.workers.ticket_dispatcher_worker.get_redis")
    def test_process_ticket_sync_no_ticket(self, mock_get_redis, mock_session_local):
        """Test case: Ticket không tồn tại trong DB."""
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        mock_redis = MagicMock()
        mock_get_redis.return_value = mock_redis
        
        # Setup mock query return None for ticket
        mock_db.query().with_for_update().filter().first.return_value = None
        
        process_ticket_sync("invalid-ticket-id")
        
        # Assert ticket was removed from processing queue
        mock_redis.lrem.assert_called_with("queue:tickets:processing", 0, "invalid-ticket-id")
        mock_db.close.assert_called_once()

    @patch("app.workers.ticket_dispatcher_worker.SessionLocal")
    @patch("app.workers.ticket_dispatcher_worker.get_redis")
    def test_process_ticket_sync_success(self, mock_get_redis, mock_session_local):
        """Test case: Có Agent hợp lệ, phân công thành công."""
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        mock_redis = MagicMock()
        mock_get_redis.return_value = mock_redis
        
        # Mock ticket
        mock_ticket = MagicMock()
        mock_ticket.id = "valid-ticket-id"
        mock_ticket.status = "PENDING"
        mock_ticket.category = "support"
        mock_db.query().with_for_update().filter().first.return_value = mock_ticket
        
        # Mock agents (Least-Loaded)
        mock_agent = MagicMock()
        mock_agent.id = "agent-1"
        mock_agent.current_tickets = 0
        mock_db.query().outerjoin().filter().group_by().order_by().all.return_value = [mock_agent]
        
        process_ticket_sync("valid-ticket-id")
        
        self.assertEqual(mock_ticket.assigned_to, "agent-1")
        self.assertEqual(mock_ticket.status, "IN_PROGRESS")
        mock_db.commit.assert_called_once()
        mock_redis.publish.assert_called_once()
        mock_redis.lrem.assert_called_with("queue:tickets:processing", 0, "valid-ticket-id")

    @patch("app.workers.ticket_dispatcher_worker.SessionLocal")
    @patch("app.workers.ticket_dispatcher_worker.get_redis")
    def test_process_ticket_sync_no_agents(self, mock_get_redis, mock_session_local):
        """Test case: Không có Agent nào hợp lệ, báo động Admin."""
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        mock_redis = MagicMock()
        mock_get_redis.return_value = mock_redis
        
        # Mock ticket
        mock_ticket = MagicMock()
        mock_ticket.id = "valid-ticket-id"
        mock_ticket.status = "PENDING"
        mock_ticket.category = "support"
        mock_db.query().with_for_update().filter().first.return_value = mock_ticket
        
        # Mock empty agent list
        mock_db.query().outerjoin().filter().group_by().order_by().all.return_value = []
        
        process_ticket_sync("valid-ticket-id")
        
        self.assertIsNone(mock_ticket.assigned_to)
        self.assertEqual(mock_ticket.status, "PENDING")
        mock_db.commit.assert_called_once()
        
        # Check if UNASSIGNED_TICKET_ALERT was published
        mock_redis.publish.assert_called_once()
        args, _ = mock_redis.publish.call_args
        self.assertEqual(args[0], "channel:ws_alerts")
        self.assertIn("UNASSIGNED_TICKET_ALERT", args[1])
        mock_redis.lrem.assert_called_with("queue:tickets:processing", 0, "valid-ticket-id")

if __name__ == '__main__':
    unittest.main()
