from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class SupportTicket(BaseModel):
    ticket_id: str
    customer_tier: Literal["free", "premium", "enterprise"]
    subject: str
    message: str
    previous_tickets: int
    monthly_revenue: float
    account_age_days: int

class TicketAnalysis(BaseModel):
    ticket_id: str
    priority: Literal["low", "medium", "high", "critical"]
    category: Literal["technical", "billing", "feature_request", "security", "account", "other"]
    customer_value: Literal["low", "medium", "high", "vip"]
    sentiment: Literal["negative", "neutral", "positive"]
    estimated_resolution_time: int  # in hours
    routing_decision: str
    confidence_score: float
    reasoning: str