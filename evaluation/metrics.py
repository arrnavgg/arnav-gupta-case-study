from typing import List, Dict, Any
from models.ticket import TicketAnalysis
import statistics

class EvaluationMetrics:
    """
    Evaluation metrics for the multi-agent ticket analysis system.
    """
    
    @staticmethod
    def consistency_score(analyses: List[TicketAnalysis]) -> float:
        """
        Measure consistency of priority assignments.
        Higher score means more consistent priority assignment patterns.
        """
        if len(analyses) < 2:
            return 1.0
        
        # Group by customer tier and check priority consistency
        tier_priorities = {}
        for analysis in analyses:
            # Extract customer tier from reasoning or use a lookup
            # For simplicity, we'll use a basic heuristic
            if 'enterprise' in analysis.reasoning.lower():
                tier = 'enterprise'
            elif 'premium' in analysis.reasoning.lower():
                tier = 'premium'
            else:
                tier = 'free'
            
            if tier not in tier_priorities:
                tier_priorities[tier] = []
            tier_priorities[tier].append(analysis.priority)
        
        # Calculate consistency within each tier
        consistencies = []
        for tier, priorities in tier_priorities.items():
            if len(priorities) > 1:
                # Measure how often the same priority appears
                priority_counts = {}
                for p in priorities:
                    priority_counts[p] = priority_counts.get(p, 0) + 1
                
                max_count = max(priority_counts.values())
                consistency = max_count / len(priorities)
                consistencies.append(consistency)
        
        return statistics.mean(consistencies) if consistencies else 1.0
    
    @staticmethod
    def confidence_reliability(analyses: List[TicketAnalysis]) -> Dict[str, float]:
        """
        Analyze the relationship between confidence scores and decision quality.
        """
        confidences = [a.confidence_score for a in analyses]
        
        return {
            'mean_confidence': statistics.mean(confidences),
            'confidence_std': statistics.stdev(confidences) if len(confidences) > 1 else 0,
            'min_confidence': min(confidences),
            'max_confidence': max(confidences)
        }
    
    @staticmethod
    def routing_appropriateness(analyses: List[TicketAnalysis]) -> float:
        """
        Evaluate whether routing decisions seem appropriate based on heuristics.
        """
        appropriate_count = 0
        
        for analysis in analyses:
            is_appropriate = True
            
            # Check security issues go to security team
            if analysis.category == 'security' and 'security' not in analysis.routing_decision.lower():
                is_appropriate = False
            
            # Check critical issues have short resolution times
            if analysis.priority == 'critical' and analysis.estimated_resolution_time > 8:
                is_appropriate = False
            
            # Check enterprise customers get appropriate attention
            if 'enterprise' in analysis.reasoning.lower() and analysis.estimated_resolution_time > 24:
                is_appropriate = False
            
            if is_appropriate:
                appropriate_count += 1
        
        return appropriate_count / len(analyses) if analyses else 0
    
    @staticmethod
    def resolution_time_reasonableness(analyses: List[TicketAnalysis]) -> Dict[str, Any]:
        """
        Evaluate whether estimated resolution times are reasonable.
        """
        times_by_priority = {}
        for analysis in analyses:
            if analysis.priority not in times_by_priority:
                times_by_priority[analysis.priority] = []
            times_by_priority[analysis.priority].append(analysis.estimated_resolution_time)
        
        results = {}
        for priority, times in times_by_priority.items():
            results[priority] = {
                'mean_time': statistics.mean(times),
                'min_time': min(times),
                'max_time': max(times),
                'count': len(times)
            }
        
        return results
    
    @staticmethod
    def agent_agreement_analysis(analysis_history: List[Dict]) -> Dict[str, Any]:
        """
        Analyze how often agents agree vs disagree in their assessments.
        """
        if not analysis_history:
            return {}
        
        agreements = {
            'priority_category_correlation': 0,
            'value_priority_correlation': 0,
            'sentiment_priority_correlation': 0
        }
        
        for history in analysis_history:
            # Check if high priority correlates with technical/security categories
            if (history['priority'].priority in ['high', 'critical'] and 
                history['category'].category in ['technical', 'security']):
                agreements['priority_category_correlation'] += 1
            
            # Check if high value customers get higher priority
            if (history['customer_value'].value_tier in ['high', 'vip'] and
                history['priority'].priority in ['medium', 'high', 'critical']):
                agreements['value_priority_correlation'] += 1
            
            # Check if negative sentiment correlates with higher priority
            if (history['sentiment'].sentiment == 'negative' and
                history['priority'].priority in ['medium', 'high', 'critical']):
                agreements['sentiment_priority_correlation'] += 1
        
        total = len(analysis_history)
        return {
            'priority_category_correlation': agreements['priority_category_correlation'] / total,
            'value_priority_correlation': agreements['value_priority_correlation'] / total,
            'sentiment_priority_correlation': agreements['sentiment_priority_correlation'] / total,
            'total_samples': total
        }