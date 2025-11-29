"""
Planner Agent - Decomposes user queries into structured analysis plans
"""

import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os


class PlannerAgent:
    """
    Responsible for parsing user queries and creating structured analysis plans.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.available_metrics = [
            'roas', 'ctr', 'cpc', 'cpm', 'conversion_rate', 
            'impressions', 'clicks', 'spend', 'revenue', 'purchases'
        ]
        self.available_segments = ['campaign_name', 'creative_type', 'audience_type', 'platform', 'country']
        self.prompt_template = self._load_prompt_template()
    
    def _load_prompt_template(self) -> str:
        """Load planner prompt template"""
        prompt_path = os.path.join('prompts', 'planner_prompt.md')
        try:
            with open(prompt_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return self._get_default_prompt()
    
    def _get_default_prompt(self) -> str:
        """Default prompt if file not found"""
        return """
        You are a marketing analytics planner. Parse the user query and create an analysis plan.
        Focus on identifying the key metrics, time periods, and objectives.
        """
    
    def execute(self, user_query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main execution method for the Planner Agent
        
        Args:
            user_query: Natural language query from user
            context: Additional context (date ranges, available data, etc.)
        
        Returns:
            Structured analysis plan
        """
        print(f"\n[PLANNER AGENT] Processing query: '{user_query}'")
        
        # Parse query intent
        objectives = self._extract_objectives(user_query)
        metrics = self._identify_metrics(user_query, objectives)
        time_windows = self._determine_time_windows(user_query, context)
        segments = self._identify_segments(user_query)
        priority_questions = self._generate_priority_questions(objectives, metrics)
        
        plan = {
            "plan_id": f"PLAN_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "user_query": user_query,
            "objectives": objectives,
            "metrics_to_analyze": metrics,
            "time_windows": time_windows,
            "segments": segments,
            "priority_questions": priority_questions,
            "analysis_type": self._classify_analysis_type(user_query)
        }
        
        print(f"[PLANNER AGENT] Plan created with {len(objectives)} objectives")
        print(f"[PLANNER AGENT] Metrics to analyze: {', '.join(metrics)}")
        
        return plan
    
    def _extract_objectives(self, query: str) -> List[str]:
        """Extract analysis objectives from query"""
        query_lower = query.lower()
        objectives = []
        
        if any(word in query_lower for word in ['drop', 'decline', 'decrease', 'down', 'falling']):
            objectives.append("Identify causes of performance decline")
        
        if any(word in query_lower for word in ['improve', 'optimize', 'increase', 'boost']):
            objectives.append("Find optimization opportunities")
        
        if 'roas' in query_lower:
            objectives.append("Analyze ROAS trends and drivers")
        
        if any(word in query_lower for word in ['ctr', 'click']):
            objectives.append("Analyze click-through rate performance")
        
        if any(word in query_lower for word in ['conversion', 'convert']):
            objectives.append("Analyze conversion funnel")
        
        if 'spend' in query_lower or 'cost' in query_lower:
            objectives.append("Analyze cost efficiency")
        
        if not objectives:
            objectives.append("Perform comprehensive performance analysis")
        
        return objectives
    
    def _identify_metrics(self, query: str, objectives: List[str]) -> List[str]:
        """Identify which metrics to analyze - use lowercase CSV column names"""
        query_lower = query.lower()
        metrics = set()
        
        # Direct metric mentions - map to lowercase metric names from CSV
        metric_keywords = {
            'roas': 'roas',
            'ctr': 'ctr',
            'cpc': 'cpc',
            'cpm': 'cpm',
            'conversion': 'conversion_rate',
            'impression': 'impressions',
            'click': 'clicks',
            'spend': 'spend',
            'revenue': 'revenue',
            'purchase': 'purchases'
        }
        
        for keyword, metric in metric_keywords.items():
            if keyword in query_lower:
                metrics.add(metric)
        
        # Add implied metrics based on objectives
        if "roas" in metrics or "performance decline" in str(objectives):
            metrics.update(['roas', 'spend', 'revenue', 'conversion_rate'])
        
        if "ctr" in metrics:
            metrics.update(['ctr', 'impressions', 'clicks'])
        
        if "cost" in query_lower:
            metrics.update(['cpc', 'cpm', 'spend'])
        
        # Always include core metrics if none specified
        if not metrics:
            metrics.update(['roas', 'ctr', 'cpc', 'spend', 'revenue'])
        
        return sorted(list(metrics))
    
    def _determine_time_windows(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Determine time windows for analysis - use latest date from data or current date"""
        query_lower = query.lower()
        
        # Try to use the latest date from context, fallback to now()
        if context and 'latest_date' in context:
            end_date = pd.to_datetime(context['latest_date'])
        else:
            end_date = datetime.now()
        
        # Determine comparison period length
        if 'last 7 days' in query_lower or '7 days' in query_lower:
            comparison_days = 7
        elif 'last 14 days' in query_lower or '14 days' in query_lower:
            comparison_days = 14
        elif 'last 30 days' in query_lower or '30 days' in query_lower or 'month' in query_lower:
            comparison_days = 30
        elif 'last 60 days' in query_lower or '60 days' in query_lower:
            comparison_days = 60
        elif 'last 90 days' in query_lower or '90 days' in query_lower or 'quarter' in query_lower:
            comparison_days = 90
        else:
            comparison_days = 30  # Default
        
        comparison_start = end_date - timedelta(days=comparison_days)
        baseline_start = comparison_start - timedelta(days=comparison_days)
        
        # Ensure dates are strings
        baseline_start_str = baseline_start.strftime('%Y-%m-%d') if hasattr(baseline_start, 'strftime') else str(baseline_start)
        comparison_start_str = comparison_start.strftime('%Y-%m-%d') if hasattr(comparison_start, 'strftime') else str(comparison_start)
        end_date_str = end_date.strftime('%Y-%m-%d') if hasattr(end_date, 'strftime') else str(end_date)
        
        return {
            "baseline": {
                "start_date": baseline_start_str,
                "end_date": comparison_start_str,
                "label": "Previous Period"
            },
            "comparison": {
                "start_date": comparison_start_str,
                "end_date": end_date_str,
                "label": "Current Period"
            },
            "comparison_days": comparison_days
        }
    
    def _identify_segments(self, query: str) -> List[str]:
        """Identify which segments to analyze - use CSV column names (lowercase)"""
        query_lower = query.lower()
        segments = []
        
        if 'campaign' in query_lower:
            segments.append('campaign_name')
        
        if 'creative' in query_lower or 'ad' in query_lower:
            segments.append('creative_type')
        
        if 'audience' in query_lower or 'segment' in query_lower:
            segments.append('audience_type')
        
        if 'device' in query_lower:
            segments.append('platform')
        
        if 'country' in query_lower or 'region' in query_lower or 'geo' in query_lower:
            segments.append('country')
        
        # Default segments for comprehensive analysis
        if not segments:
            segments = ['campaign_name', 'creative_type']
        
        return segments
    
    def _generate_priority_questions(self, objectives: List[str], metrics: List[str]) -> List[str]:
        """Generate priority questions to guide analysis"""
        questions = []
        
        if 'ROAS' in metrics:
            questions.append("What is the primary driver of ROAS change?")
            questions.append("Which campaigns/creatives have the best/worst ROAS?")
        
        if 'CTR' in metrics:
            questions.append("Has CTR declined across all segments or specific ones?")
        
        if 'CPC' in metrics:
            questions.append("Are we experiencing cost inflation?")
        
        if 'Spend' in metrics and 'Revenue' in metrics:
            questions.append("Is the issue spend-driven or revenue-driven?")
        
        questions.append("Are there any clear outliers or anomalies?")
        questions.append("What segments show the strongest performance?")
        
        return questions
    
    def _classify_analysis_type(self, query: str) -> str:
        """Classify the type of analysis needed"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['drop', 'decline', 'problem', 'issue']):
            return "diagnostic"
        elif any(word in query_lower for word in ['optimize', 'improve', 'increase']):
            return "optimization"
        elif any(word in query_lower for word in ['predict', 'forecast']):
            return "predictive"
        else:
            return "exploratory"


if __name__ == "__main__":
    # Test the planner agent
    config = {}
    planner = PlannerAgent(config)
    
    test_query = "Analyze ROAS drop in last 30 days"
    result = planner.execute(test_query)
    
    print("\n=== PLANNER OUTPUT ===")
    print(json.dumps(result, indent=2))
