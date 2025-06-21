from pydantic_ai import Agent
from models.responses import CustomerValueResponse
from models.ticket import SupportTicket
from dotenv import load_dotenv

load_dotenv()

customer_value_agent = Agent(
    'google-gla:gemini-1.5-flash',
    result_type=CustomerValueResponse,
    system_prompt="""
    You are a Customer Value Assessment Agent specializing in evaluating customer importance and risk.

    Your role is to analyze customer data and determine:
    - VALUE_TIER: low, medium, high, vip
    - RISK_LEVEL: likelihood of churn if not handled well
    - RETENTION_PRIORITY: whether this customer needs special attention

    Consider these factors:
    1. Customer tier (enterprise > premium > free)
    2. Monthly revenue contribution
    3. Account age and loyalty
    4. Previous ticket history (frequency could indicate frustration)
    5. Growth potential

    Value Tier Guidelines:
    - VIP: Enterprise customers with high revenue (>$20k/month) or strategic importance
    - HIGH: Premium/Enterprise customers with solid revenue (>$5k/month)
    - MEDIUM: Premium customers or long-term free users with growth potential
    - LOW: New or low-engagement free users

    Always provide your reasoning and confidence level.
    """
)

async def analyze_customer_value(ticket: SupportTicket) -> CustomerValueResponse:
    """Analyze customer value using the customer value agent."""
    prompt = f"""
    Analyze this customer for value assessment:

    Customer Tier: {ticket.customer_tier}
    Monthly Revenue: ${ticket.monthly_revenue}
    Account Age: {ticket.account_age_days} days
    Previous Tickets: {ticket.previous_tickets}

    Current Issue Context:
    Subject: {ticket.subject}
    Message: {ticket.message}

    Assess the customer's value tier, churn risk, and retention priority.
    """

    result = await customer_value_agent.run(prompt)
    return result.data