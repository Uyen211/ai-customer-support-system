# Import Base and all models so Alembic and SQLAlchemy have a complete view of metadata
from app.db.base_class import Base
from app.models.user import User
from app.models.customer import Customer
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.ticket import Ticket
from app.models.sla_policy import SLAPolicy
from app.models.canned_response import CannedResponse
from app.models.ai_rule import AIRule
from app.models.product import Product
from app.models.knowledge_chunk import KnowledgeChunk

__all__ = [
    "Base",
    "User",
    "Customer",
    "Conversation",
    "Message",
    "Ticket",
    "SLAPolicy",
    "CannedResponse",
    "AIRule",
    "Product",
    "KnowledgeChunk",
]
