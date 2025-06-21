from pydantic_ai import Agent
from models.responses import CategoryResponse
from models.ticket import SupportTicket
from dotenv import load_dotenv

load_dotenv()

category_agent = Agent(
    'google-gla:gemini-1.5-flash',
    result_type=CategoryResponse,
    system_prompt="""
    You are a Category Classification Agent specializing in categorizing customer support tickets.

    Your role is to analyze tickets and classify them into categories:
    - TECHNICAL: API issues, bugs, performance problems, integration issues
    - BILLING: Payment issues, subscription problems, pricing questions
    - FEATURE_REQUEST: New feature requests, enhancement suggestions
    - SECURITY: Security vulnerabilities, access issues, compliance questions
    - ACCOUNT: Account setup, user management, permissions
    - OTHER: General inquiries, feedback, unclear issues

    Also provide a specific subcategory for better routing.

    Consider:
    1. Keywords in subject and message
    2. Technical terminology used
    3. Context clues about the problem domain
    4. Customer's specific needs

    Always provide your reasoning and confidence level.
    """
)

async def analyze_category(ticket: SupportTicket) -> CategoryResponse:
    """Analyze ticket category using the category agent."""
    prompt = f"""
    Analyze this support ticket for category classification:

    Ticket ID: {ticket.ticket_id}
    Subject: {ticket.subject}
    Message: {ticket.message}
    Customer Context: {ticket.customer_tier} customer, {ticket.previous_tickets} previous tickets

    Classify the category and provide a specific subcategory for routing.
    """

    result = await category_agent.run(prompt)
    return result.data