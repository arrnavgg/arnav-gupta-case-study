import asyncio
from typing import List
from models.ticket import SupportTicket
from evaluation.metrics import EvaluationMetrics

async def run_evaluation(analyzer, test_tickets: List[SupportTicket]) -> dict:
    """
    Run comprehensive evaluation of the multi-agent system.
    """
    print("Running Evaluation Framework")
    print("-" * 40)
    
    # Get all analyses
    analyses = [history['final'] for history in analyzer.analysis_history]
    
    # Run all evaluation metrics
    metrics = EvaluationMetrics()
    
    print("Computing metrics...")
    
    # 1. Consistency Score
    consistency = metrics.consistency_score(analyses)
    print(f"Consistency Score: {consistency:.3f}")
    
    # 2. Confidence Reliability
    confidence_stats = metrics.confidence_reliability(analyses)
    print(f"Mean Confidence: {confidence_stats['mean_confidence']:.3f}")
    print(f"Confidence Range: {confidence_stats['min_confidence']:.3f} - {confidence_stats['max_confidence']:.3f}")
    
    # 3. Routing Appropriateness
    routing_score = metrics.routing_appropriateness(analyses)
    print(f"Routing Appropriateness: {routing_score:.3f}")
    
    # 4. Resolution Time Analysis
    time_analysis = metrics.resolution_time_reasonableness(analyses)
    print(f"Resolution Time Analysis:")
    for priority, stats in time_analysis.items():
        print(f"    {priority}: {stats['mean_time']:.1f}h avg ({stats['count']} tickets)")
    
    # 5. Agent Agreement Analysis
    agreement_analysis = metrics.agent_agreement_analysis(analyzer.analysis_history)
    print(f"Agent Agreement Analysis:")
    for metric, score in agreement_analysis.items():
        if metric != 'total_samples':
            print(f"    {metric}: {score:.3f}")
    
    # Compile final evaluation report
    evaluation_report = {
        'consistency_score': consistency,
        'confidence_stats': confidence_stats,
        'routing_appropriateness': routing_score,
        'resolution_time_analysis': time_analysis,
        'agent_agreement': agreement_analysis,
        'overall_score': (consistency + routing_score + confidence_stats['mean_confidence']) / 3
    }
    
    print(f"\n Overall System Score: {evaluation_report['overall_score']:.3f}")
    
    return evaluation_report