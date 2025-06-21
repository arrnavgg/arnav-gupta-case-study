from pydantic_ai import Agent
from models.responses import PriorityResponse, CategoryResponse, CustomerValueResponse, SentimentResponse
from models.ticket import SupportTicket, TicketAnalysis
from dotenv import load_dotenv

load_dotenv()

routing_coordinator = Agent(
    'google-gla:gemini-1.5-flash',
    result_type=TicketAnalysis,
    system_prompt="""
    You are the Routing Coordinator Agent responsible for making final routing decisions based on all agent analyses.

    Your role is to synthesize inputs from multiple specialized agents and make the final routing decision.

    You will receive:
    1. Priority analysis (critical/high/medium/low)
    2. Category analysis (technical/billing/feature_request/security/account/other)
    3. Customer value analysis (vip/high/medium/low value)
    4. Sentiment analysis (negative/neutral/positive)

    Your job is to:
    1. Resolve any conflicts between agent recommendations
    2. Make final routing decisions considering all factors
    3. Estimate resolution time
    4. Provide comprehensive reasoning

    Routing Guidelines:
    - Critical + VIP/High Value → Senior Technical Team (immediate)
    - Security issues → Security Team (regardless of other factors)
    - Enterprise customers → Enterprise Support Team
    - Feature requests → Product Team
    - Billing issues → Billing Team
    - Technical issues → Technical Support Team
    - High negative sentiment → Escalation Team

    Resolution Time Estimates:
    - Critical: 2-4 hours
    - High: 4-8 hours
    - Medium: 8-24 hours
    - Low: 24-72 hours

    Always provide detailed reasoning for your decisions.
    """
)

async def coordinate_routing(
    ticket: SupportTicket,
    priority: PriorityResponse,
    category: CategoryResponse,
    customer_value: CustomerValueResponse,
    sentiment: SentimentResponse
) -> TicketAnalysis:
    """Coordinate final routing decision based on all agent inputs."""

    prompt = f"""
    Make the final routing decision for this ticket based on all agent analyses:

    TICKET DETAILS:
    ID: {ticket.ticket_id}
    Subject: {ticket.subject}
    Message: {ticket.message}
    Customer: {ticket.customer_tier}, ${ticket.monthly_revenue}/month, {ticket.account_age_days} days old

    AGENT ANALYSES:
    Priority Agent: {priority.priority} (confidence: {priority.confidence})
    Reasoning: {priority.reasoning}

    Category Agent: {category.category} - {category.subcategory} (confidence: {category.confidence})
    Reasoning: {category.reasoning}

    Customer Value Agent: {customer_value.value_tier} value, {customer_value.risk_level} risk (confidence: {customer_value.confidence})
    Reasoning: {customer_value.reasoning}

    Sentiment Agent: {sentiment.sentiment} sentiment, {sentiment.urgency_from_tone} urgency (risk: {sentiment.customer_satisfaction_risk})
    Reasoning: {sentiment.reasoning}

    Synthesize all this information to make the final routing decision, estimate resolution time, and provide comprehensive reasoning.
    """

    result = await routing_coordinator.run(prompt)
    return result.data

# Sentiment analysis helper
sentiment_agent = Agent(
    'google-gla:gemini-1.5-flash',
    result_type=SentimentResponse,
    system_prompt="""
    You are a Sentiment Analysis Agent specializing in understanding customer emotional state and satisfaction risk.

    Analyze the customer's message for:
    - Overall sentiment (negative/neutral/positive)
    - Urgency conveyed through tone
    - Risk to customer satisfaction

    Pay attention to:
    - Emotional language and tone
    - Urgency indicators
    - Frustration levels
    - Professionalism of communication

    Always provide reasoning for your assessment.
    """
)

async def analyze_sentiment(ticket: SupportTicket) -> SentimentResponse:
    """Analyze ticket sentiment using the sentiment agent."""
    prompt = f"""
    Analyze the sentiment and emotional tone of this support ticket:

    Subject: {ticket.subject}
    Message: {ticket.message}

    Context: This is from a {ticket.customer_tier} customer who has submitted {ticket.previous_tickets} previous tickets.

    Assess their emotional state and satisfaction risk.
    """

    result = await sentiment_agent.run(prompt)
    return result.data