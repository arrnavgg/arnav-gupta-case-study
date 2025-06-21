from pydantic_ai import Agent
from models.responses import PriorityResponse
from models.ticket import SupportTicket
from dotenv import load_dotenv

load_dotenv()

priority_agent = Agent(
    'google-gla:gemini-1.5-flash',
    result_type=PriorityResponse,
    system_prompt="""
    You are a Priority Classification Agent specializing in determining the urgency of customer support tickets.

    Your role is to analyze tickets and classify them into priority levels:
    - CRITICAL: System down, security vulnerabilities, data loss, revenue-blocking issues
    - HIGH: Major functionality broken, enterprise customer issues, API failures
    - MEDIUM: Minor bugs, feature questions, configuration issues
    - LOW: General questions, cosmetic issues, documentation requests

    Consider these factors:
    1. Impact on customer operations
    2. Customer tier (enterprise > premium > free)
    3. Revenue implications
    4. Security concerns
    5. Tone and urgency in the message

    Always provide your reasoning and confidence level.
    """
)

async def analyze_priority(ticket: SupportTicket) -> PriorityResponse:
    """Analyze ticket priority using the priority agent."""
    prompt = f"""
    Analyze this support ticket for priority classification:

    Ticket ID: {ticket.ticket_id}
    Customer Tier: {ticket.customer_tier}
    Subject: {ticket.subject}
    Message: {ticket.message}
    Previous Tickets: {ticket.previous_tickets}
    Monthly Revenue: ${ticket.monthly_revenue}
    Account Age: {ticket.account_age_days} days

    Classify the priority level and provide detailed reasoning.
    """

    result = await priority_agent.run(prompt)
    return result.data