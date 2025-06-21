from pydantic import BaseModel
from typing import Literal

class PriorityResponse(BaseModel):
    priority: Literal["low", "medium", "high", "critical"]
    reasoning: str
    confidence: float

class CategoryResponse(BaseModel):
    category: Literal["technical", "billing", "feature_request", "security", "account", "other"]
    subcategory: str
    reasoning: str
    confidence: float

class CustomerValueResponse(BaseModel):
    value_tier: Literal["low", "medium", "high", "vip"]
    risk_level: Literal["low", "medium", "high"]
    retention_priority: bool
    reasoning: str
    confidence: float

class SentimentResponse(BaseModel):
    sentiment: Literal["negative", "neutral", "positive"]
    urgency_from_tone: Literal["low", "medium", "high"]
    customer_satisfaction_risk: float
    reasoning: str