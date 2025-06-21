from models.ticket import SupportTicket

TEST_TICKETS = [
    SupportTicket(
        ticket_id="SUP-001",
        customer_tier="free",
        subject="This product is completely broken!!!",
        message="Nothing works! I can't even log in. This is the worst software I've ever used. I'm switching to a competitor if this isn't fixed immediately!",
        previous_tickets=0,
        monthly_revenue=0,
        account_age_days=2
    ),
    SupportTicket(
        ticket_id="SUP-002",
        customer_tier="enterprise",
        subject="Minor UI issue with dashboard",
        message="Hi team, just noticed the dashboard numbers are slightly misaligned on mobile view when using Safari. Not urgent but wanted to report it. Thanks for the great product!",
        previous_tickets=15,
        monthly_revenue=25000,
        account_age_days=730
    ),
    SupportTicket(
        ticket_id="SUP-003",
        customer_tier="premium",
        subject="Feature Request: Bulk export",
        message="We need bulk export functionality for our quarterly reports. Currently exporting one by one is very time consuming. Would this be possible to add?",
        previous_tickets=5,
        monthly_revenue=5000,
        account_age_days=400
    ),
    SupportTicket(
        ticket_id="SUP-004",
        customer_tier="premium",
        subject="API rate limits unclear",
        message="Getting rate limited but documentation says we should have 1000 requests/hour. We're only making about 500 requests/hour. Can you help clarify?",
        previous_tickets=8,
        monthly_revenue=3000,
        account_age_days=180
    ),
    SupportTicket(
        ticket_id="SUP-005",
        customer_tier="enterprise",
        subject="Urgent: Security vulnerability?",
        message="Our security team flagged that your API responses include internal server paths in error messages. This could be a security risk. Please investigate ASAP.",
        previous_tickets=20,
        monthly_revenue=50000,
        account_age_days=900
    )
]