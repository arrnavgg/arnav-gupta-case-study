# Multi-Agent Customer Support Ticket Analyzer

A sophisticated AI-powered customer support ticket routing system that uses multiple specialized agents to analyze, prioritize, and route support tickets intelligently.

## 🎯 Overview

This system employs a multi-agent architecture where specialized AI agents work in parallel to analyze different aspects of customer support tickets:

- **Priority Agent**: Determines urgency level based on business impact
- **Category Agent**: Classifies issue types and subcategories  
- **Customer Value Agent**: Assesses customer importance and churn risk
- **Sentiment Agent**: Analyzes emotional tone and satisfaction risk
- **Routing Coordinator**: Makes final routing decisions by synthesizing all agent inputs

## 🏗️ Architecture

The system uses a **separation of concerns** approach where each agent specializes in one analysis dimension:

```
Support Ticket → [Priority Agent]     ↘
                [Category Agent]       → Routing Coordinator → Final Decision
                [Customer Value Agent] ↗
                [Sentiment Agent]     ↗
```

### Key Benefits
- **Parallel Processing**: All agents analyze simultaneously for faster results
- **Specialized Expertise**: Each agent focuses on its domain of expertise
- **Conflict Resolution**: Coordinator resolves disagreements using business rules
- **Transparency**: Clear reasoning trail for all decisions
- **Scalability**: Easy to add new analysis dimensions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google AI API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd multi-agent-support-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
```

4. Run the system:
```bash
python main.py
```

## 📊 Usage Example

```python
from models.ticket import SupportTicket
from main import MultiAgentTicketAnalyzer

# Create a ticket
ticket = SupportTicket(
    ticket_id="SUP-001",
    customer_tier="enterprise",
    subject="API is down",
    message="Our production API calls are failing with 500 errors",
    previous_tickets=5,
    monthly_revenue=25000,
    account_age_days=365
)

# Analyze the ticket
analyzer = MultiAgentTicketAnalyzer()
analysis = await analyzer.analyze_ticket(ticket)

print(f"Priority: {analysis.priority}")
print(f"Routing: {analysis.routing_decision}")
print(f"ETA: {analysis.estimated_resolution_time} hours")
```

## 🤖 Agent Specifications

### Priority Agent
**Determines**: Critical, High, Medium, Low
**Considers**: Business impact, customer tier, revenue implications, security concerns

### Category Agent  
**Determines**: Technical, Billing, Feature Request, Security, Account, Other
**Considers**: Keywords, technical terminology, problem domain context

### Customer Value Agent
**Determines**: VIP, High, Medium, Low value tiers
**Considers**: Revenue contribution, account age, growth potential, churn risk

### Sentiment Agent
**Determines**: Positive, Neutral, Negative sentiment
**Considers**: Emotional language, urgency indicators, frustration levels

### Routing Coordinator
**Determines**: Final team assignment and resolution timeline
**Considers**: All agent inputs plus business rules for conflict resolution

## 📈 Evaluation Framework

The system includes comprehensive evaluation metrics:

- **Consistency Score**: Measures consistent priority assignment patterns
- **Confidence Reliability**: Analyzes confidence score distributions
- **Routing Appropriateness**: Validates routing decisions against business rules
- **Resolution Time Analysis**: Ensures realistic time estimates
- **Agent Agreement Analysis**: Measures correlation between agent assessments

Run evaluation:
```bash
python -c "import asyncio; from evaluation.test_runner import run_evaluation; asyncio.run(run_evaluation())"
```

## 🔧 Configuration

### Priority Levels
- **Critical**: System down, security vulnerabilities, data loss (2-4 hours)
- **High**: Major functionality broken, enterprise issues (4-8 hours)  
- **Medium**: Minor bugs, configuration issues (8-24 hours)
- **Low**: General questions, documentation requests (24-72 hours)

### Customer Tiers
- **VIP**: Enterprise customers >$20k/month or strategic importance
- **High**: Premium/Enterprise customers >$5k/month
- **Medium**: Premium customers or long-term free users
- **Low**: New or low-engagement free users

### Routing Rules
- Critical + VIP/High Value → Senior Technical Team (immediate)
- Security issues → Security Team (regardless of other factors)
- Enterprise customers → Enterprise Support Team
- Feature requests → Product Team
- Billing issues → Billing Team
- High negative sentiment → Escalation Team

## 📁 Project Structure

```
├── agents/                 # AI agent implementations
│   ├── priority_agent.py   # Priority classification
│   ├── category_agent.py   # Issue categorization
│   ├── customer_value_agent.py # Customer value assessment
│   └── routing_coordinator.py  # Final routing decisions
├── models/                 # Data models
│   ├── ticket.py          # Ticket and analysis models
│   └── responses.py       # Agent response models
├── evaluation/            # Evaluation framework
│   ├── metrics.py         # Evaluation metrics
│   └── test_runner.py     # Test execution
├── tests/                 # Test data and cases
│   └── test_data.py       # Sample tickets
├── docs/                  # Documentation
│   └── architecture.md    # Detailed architecture docs
├── main.py               # Main application entry point
├── requirements.txt      # Python dependencies
└── .env                 # Environment variables
```

## 🧪 Testing

The system includes comprehensive test data covering various scenarios:

- Angry free-tier customers with basic issues
- Enterprise customers with minor UI problems  
- Premium customers requesting new features
- Technical API questions from paying customers
- Security vulnerabilities from enterprise clients

Run tests:
```bash
python main.py
```

## 📊 Sample Output

```
🎫 Analyzing ticket SUP-005...
  📊 Priority: critical
  📁 Category: security
  💎 Customer Value: vip  
  😊 Sentiment: neutral
  🎯 Final Routing: Security Team - Immediate Escalation
  ⏱️  Est. Resolution: 2h
  🎯 Confidence: 0.95

📊 Analysis Summary:
  total_tickets: 5
  priority_distribution: {'critical': 1, 'high': 1, 'medium': 2, 'low': 1}
  category_distribution: {'security': 1, 'technical': 2, 'feature_request': 1, 'other': 1}
  avg_confidence: 0.87
  avg_resolution_time: 12.4

Overall System Score: 0.891
```

## 🔄 Rate Limiting & Error Handling

The system includes:
- Automatic retry logic for API rate limits
- Semaphore-based concurrency control
- Graceful error handling with exponential backoff

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 🎖️ Acknowledgments

Built with:
- [PydanticAI](https://github.com/pydantic/pydantic-ai) - AI agent framework
- [Google Gemini](https://deepmind.google/technologies/gemini/) - Language model
- [Pydantic](https://pydantic.dev/) - Data validation
