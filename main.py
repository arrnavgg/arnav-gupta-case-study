import asyncio
from typing import List
from models.ticket import SupportTicket, TicketAnalysis
from agents.priority_agent import analyze_priority
from agents.category_agent import analyze_category
from agents.customer_value_agent import analyze_customer_value
from agents.routing_coordinator import coordinate_routing, analyze_sentiment
from evaluation.test_runner import run_evaluation
from tests.test_data import TEST_TICKETS
from google.genai.errors import ClientError

# Limit concurrent requests (tweak if needed)
SEMAPHORE = asyncio.Semaphore(3)

class MultiAgentTicketAnalyzer:
    def __init__(self):
        self.analysis_history = []

    async def analyze_ticket(self, ticket: SupportTicket) -> TicketAnalysis:
        async with SEMAPHORE:
            for attempt in range(3):  # Retry up to 3 times
                try:
                    print(f"🎫 Analyzing ticket {ticket.ticket_id}...")

                    priority_task = analyze_priority(ticket)
                    category_task = analyze_category(ticket)
                    customer_value_task = analyze_customer_value(ticket)
                    sentiment_task = analyze_sentiment(ticket)

                    priority_result, category_result, customer_value_result, sentiment_result = await asyncio.gather(
                        priority_task, category_task, customer_value_task, sentiment_task
                    )

                    print(f"  📊 Priority: {priority_result.priority}")
                    print(f"  📁 Category: {category_result.category}")
                    print(f"  💎 Customer Value: {customer_value_result.value_tier}")
                    print(f"  😊 Sentiment: {sentiment_result.sentiment}")

                    final_analysis = await coordinate_routing(
                        ticket, priority_result, category_result, customer_value_result, sentiment_result
                    )

                    print(f"  🎯 Final Routing: {final_analysis.routing_decision}")
                    print(f"  ⏱️  Est. Resolution: {final_analysis.estimated_resolution_time}h")
                    print(f"  🎯 Confidence: {final_analysis.confidence_score:.2f}\n")

                    self.analysis_history.append({
                        'ticket': ticket,
                        'priority': priority_result,
                        'category': category_result,
                        'customer_value': customer_value_result,
                        'sentiment': sentiment_result,
                        'final': final_analysis
                    })

                    return final_analysis

                except ClientError as e:
                    if "RESOURCE_EXHAUSTED" in str(e):
                        wait_time = 60  # Delay between retries
                        print(f"⚠️ Quota exceeded. Retrying in {wait_time}s...")
                        await asyncio.sleep(wait_time)
                    else:
                        raise  # Other API errors, don't retry
            raise RuntimeError(f"Failed to analyze ticket {ticket.ticket_id} after retries.")

    async def analyze_batch(self, tickets: List[SupportTicket]) -> List[TicketAnalysis]:
        results = []
        for ticket in tickets:
            result = await self.analyze_ticket(ticket)
            results.append(result)
        return results

    def get_analysis_summary(self) -> dict:
        if not self.analysis_history:
            return {}

        priorities = [analysis['final'].priority for analysis in self.analysis_history]
        categories = [analysis['final'].category for analysis in self.analysis_history]

        return {
            'total_tickets': len(self.analysis_history),
            'priority_distribution': {p: priorities.count(p) for p in set(priorities)},
            'category_distribution': {c: categories.count(c) for c in set(categories)},
            'avg_confidence': sum(analysis['final'].confidence_score for analysis in self.analysis_history) / len(self.analysis_history),
            'avg_resolution_time': sum(analysis['final'].estimated_resolution_time for analysis in self.analysis_history) / len(self.analysis_history)
        }

async def main():
    print("🚀 Customer Support Ticket Analyzer")
    print("=" * 60)

    analyzer = MultiAgentTicketAnalyzer()
    print("📋 Analyzing test tickets...")
    results = await analyzer.analyze_batch(TEST_TICKETS)

    print("📊 Analysis Summary:")
    summary = analyzer.get_analysis_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")

    print("\n🧪 Running evaluation...")
    evaluation_results = await run_evaluation(analyzer, TEST_TICKETS)

    print("\n✅ Analysis complete!")
    return results, evaluation_results

if __name__ == "__main__":
    asyncio.run(main())
