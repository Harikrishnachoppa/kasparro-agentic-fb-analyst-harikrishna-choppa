"""
Insight Agent - Analyzes processed data to generate hypotheses and insights
"""

import json
from typing import Dict, List, Any
from datetime import datetime
import os


class InsightAgent:
    """
    Responsible for analyzing data and generating hypotheses and insights.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.prompt_template = self._load_prompt_template()
    
    def _load_prompt_template(self) -> str:
        """Load insight prompt template"""
        prompt_path = os.path.join('prompts', 'insight_prompt.md')
        try:
            with open(prompt_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return self._get_default_prompt()
    
    def _get_default_prompt(self) -> str:
        """Default prompt if file not found"""
        return """
        You are a marketing analytics expert. Analyze the data and generate actionable insights.
        Focus on identifying trends, anomalies, and root causes.
        """
    
    def execute(self, data: Dict[str, Any], plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method for the Insight Agent
        
        Args:
            data: Processed data from Data Agent
            plan: Analysis plan from Planner Agent
        
        Returns:
            Insights and hypotheses
        """
        print(f"\n[INSIGHT AGENT] Analyzing data and generating insights")
        
        metric_changes = data.get('metric_changes', {})
        segment_analysis = data.get('segment_analysis', {})
        
        # Generate insights
        insights = []
        hypotheses = []
        
        # 1. Overall performance insights
        performance_insights = self._analyze_overall_performance(metric_changes)
        insights.extend(performance_insights)
        
        # 2. Metric-specific insights
        metric_insights = self._analyze_metric_trends(metric_changes)
        insights.extend(metric_insights)
        
        # 3. Segment insights
        segment_insights = self._analyze_segment_performance(segment_analysis)
        insights.extend(segment_insights)
        
        # 4. Generate hypotheses
        hypotheses = self._generate_hypotheses(metric_changes, segment_analysis)
        
        # 5. Identify correlations
        correlations = self._identify_correlations(metric_changes)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "insights": insights,
            "hypotheses": hypotheses,
            "correlations": correlations,
            "summary": self._create_summary(insights, hypotheses)
        }
        
        print(f"[INSIGHT AGENT] Generated {len(insights)} insights and {len(hypotheses)} hypotheses")
        
        return result
    
    def _analyze_overall_performance(self, metric_changes: Dict) -> List[Dict]:
        """Analyze overall performance trends"""
        insights = []
        
        if 'ROAS' in metric_changes:
            roas_data = metric_changes['ROAS']
            pct_change = roas_data['percent_change']
            
            if abs(pct_change) > 10:
                severity = "critical" if abs(pct_change) > 30 else "moderate"
                direction = "declined" if pct_change < 0 else "improved"
                
                insights.append({
                    "insight_id": "INS_ROAS_001",
                    "type": "performance_change",
                    "title": f"ROAS has {direction} by {abs(pct_change):.1f}%",
                    "description": f"Return on Ad Spend {direction} from {roas_data['baseline']:.2f} to {roas_data['comparison']:.2f}, representing a {abs(pct_change):.1f}% {roas_data['direction']}ward movement.",
                    "evidence": {
                        "baseline_roas": roas_data['baseline'],
                        "comparison_roas": roas_data['comparison'],
                        "change_pct": pct_change
                    },
                    "confidence": 0.95,
                    "impact": severity,
                    "category": "ROAS"
                })
        
        # Spend efficiency
        if 'Spend' in metric_changes and 'Revenue' in metric_changes:
            spend_change = metric_changes['Spend']['percent_change']
            revenue_change = metric_changes['Revenue']['percent_change']
            
            if spend_change > 10 and revenue_change < spend_change:
                insights.append({
                    "insight_id": "INS_EFF_001",
                    "type": "efficiency",
                    "title": "Spending increased faster than revenue",
                    "description": f"Ad spend increased by {spend_change:.1f}% while revenue only grew by {revenue_change:.1f}%, indicating declining efficiency.",
                    "evidence": {
                        "spend_change": spend_change,
                        "revenue_change": revenue_change,
                        "efficiency_gap": spend_change - revenue_change
                    },
                    "confidence": 0.90,
                    "impact": "moderate",
                    "category": "Efficiency"
                })
        
        return insights
    
    def _analyze_metric_trends(self, metric_changes: Dict) -> List[Dict]:
        """Analyze individual metric trends"""
        insights = []
        
        # CTR Analysis
        if 'CTR' in metric_changes:
            ctr_data = metric_changes['CTR']
            pct_change = ctr_data['percent_change']
            
            if abs(pct_change) > 15:
                insights.append({
                    "insight_id": "INS_CTR_001",
                    "type": "engagement",
                    "title": f"Click-through rate {'declined' if pct_change < 0 else 'improved'} significantly",
                    "description": f"CTR changed from {ctr_data['baseline']:.2f}% to {ctr_data['comparison']:.2f}%, a {abs(pct_change):.1f}% change. This may indicate creative fatigue or improved ad relevance.",
                    "evidence": {
                        "baseline_ctr": ctr_data['baseline'],
                        "comparison_ctr": ctr_data['comparison'],
                        "change_pct": pct_change
                    },
                    "confidence": 0.85,
                    "impact": "moderate",
                    "category": "Engagement"
                })
        
        # CPC Analysis
        if 'CPC' in metric_changes:
            cpc_data = metric_changes['CPC']
            pct_change = cpc_data['percent_change']
            
            if pct_change > 20:
                insights.append({
                    "insight_id": "INS_CPC_001",
                    "type": "cost",
                    "title": "Cost per click has increased significantly",
                    "description": f"CPC rose from ${cpc_data['baseline']:.2f} to ${cpc_data['comparison']:.2f}, a {pct_change:.1f}% increase. This could indicate increased competition or reduced ad quality.",
                    "evidence": {
                        "baseline_cpc": cpc_data['baseline'],
                        "comparison_cpc": cpc_data['comparison'],
                        "change_pct": pct_change
                    },
                    "confidence": 0.88,
                    "impact": "moderate",
                    "category": "Cost"
                })
        
        # Conversion Rate Analysis
        if 'Conversion_Rate' in metric_changes:
            conv_data = metric_changes['Conversion_Rate']
            pct_change = conv_data['percent_change']
            
            if abs(pct_change) > 10:
                insights.append({
                    "insight_id": "INS_CONV_001",
                    "type": "conversion",
                    "title": f"Conversion rate {'dropped' if pct_change < 0 else 'increased'}",
                    "description": f"Conversion rate moved from {conv_data['baseline']:.2f}% to {conv_data['comparison']:.2f}%. This may be related to landing page performance or audience quality.",
                    "evidence": {
                        "baseline_conv": conv_data['baseline'],
                        "comparison_conv": conv_data['comparison'],
                        "change_pct": pct_change
                    },
                    "confidence": 0.82,
                    "impact": "moderate",
                    "category": "Conversion"
                })
        
        return insights
    
    def _analyze_segment_performance(self, segment_analysis: Dict) -> List[Dict]:
        """Analyze performance by segments"""
        insights = []
        
        for segment_name, segment_data in segment_analysis.items():
            top_performers = segment_data.get('top_performers', [])
            bottom_performers = segment_data.get('bottom_performers', [])
            
            if top_performers and bottom_performers:
                top_roas = top_performers[0].get('ROAS', 0)
                bottom_roas = bottom_performers[-1].get('ROAS', 0)
                
                if top_roas > 0 and bottom_roas >= 0:
                    roas_gap = top_roas - bottom_roas
                    
                    if roas_gap > 1.0:  # Significant gap
                        insights.append({
                            "insight_id": f"INS_SEG_{segment_name}_001",
                            "type": "segment_variance",
                            "title": f"Wide ROAS variance across {segment_name}",
                            "description": f"Top performing {segment_name} ('{top_performers[0].get(segment_name, 'N/A')}') has ROAS of {top_roas:.2f}, while lowest ('{bottom_performers[-1].get(segment_name, 'N/A')}') has {bottom_roas:.2f}. Consider reallocating budget to top performers.",
                            "evidence": {
                                "segment": segment_name,
                                "top_performer": top_performers[0],
                                "bottom_performer": bottom_performers[-1],
                                "roas_gap": roas_gap
                            },
                            "confidence": 0.80,
                            "impact": "moderate",
                            "category": "Segmentation"
                        })
        
        return insights
    
    def _generate_hypotheses(self, metric_changes: Dict, segment_analysis: Dict) -> List[Dict]:
        """Generate hypotheses about performance drivers"""
        hypotheses = []
        
        # Hypothesis 1: Creative Fatigue
        if 'CTR' in metric_changes:
            ctr_change = metric_changes['CTR']['percent_change']
            if ctr_change < -10:
                hypotheses.append({
                    "hypothesis_id": "HYP_001",
                    "statement": "Creative fatigue is contributing to declining CTR",
                    "reasoning": "Significant CTR decline suggests audiences are becoming less responsive to current creative assets",
                    "supporting_evidence": [
                        f"CTR declined by {abs(ctr_change):.1f}%",
                        "Extended exposure to same creative reduces engagement"
                    ],
                    "confidence": 0.75,
                    "testable": True,
                    "recommended_test": "Rotate new creative variants and measure CTR improvement"
                })
        
        # Hypothesis 2: Audience Saturation
        if 'CPM' in metric_changes:
            cpm_change = metric_changes['CPM']['percent_change']
            if cpm_change > 15:
                hypotheses.append({
                    "hypothesis_id": "HYP_002",
                    "statement": "Audience saturation is driving up costs",
                    "reasoning": "Rising CPM suggests increased frequency and reduced available inventory within target audiences",
                    "supporting_evidence": [
                        f"CPM increased by {cpm_change:.1f}%",
                        "Higher frequency typically correlates with audience saturation"
                    ],
                    "confidence": 0.70,
                    "testable": True,
                    "recommended_test": "Expand to lookalike audiences and measure cost efficiency"
                })
        
        # Hypothesis 3: Seasonal Impact
        hypotheses.append({
            "hypothesis_id": "HYP_003",
            "statement": "Seasonal factors may be influencing performance",
            "reasoning": "Undergarment purchases often show seasonal patterns based on fashion trends and holidays",
            "supporting_evidence": [
                "E-commerce typically shows seasonal variance",
                "Consumer behavior shifts with seasons"
            ],
            "confidence": 0.60,
            "testable": True,
            "recommended_test": "Compare with same period last year"
        })
        
        # Hypothesis 4: Competition Intensity
        if 'CPC' in metric_changes:
            cpc_change = metric_changes['CPC']['percent_change']
            if cpc_change > 20:
                hypotheses.append({
                    "hypothesis_id": "HYP_004",
                    "statement": "Increased competition is driving up acquisition costs",
                    "reasoning": "Significant CPC increases often indicate more advertisers competing for same audience",
                    "supporting_evidence": [
                        f"CPC increased by {cpc_change:.1f}%",
                        "Market competition affects auction dynamics"
                    ],
                    "confidence": 0.65,
                    "testable": False,
                    "recommended_test": "Monitor competitor activity and adjust bidding strategy"
                })
        
        # Hypothesis 5: Landing Page Issues
        if 'Conversion_Rate' in metric_changes:
            conv_change = metric_changes['Conversion_Rate']['percent_change']
            if conv_change < -15:
                hypotheses.append({
                    "hypothesis_id": "HYP_005",
                    "statement": "Landing page experience is negatively impacting conversions",
                    "reasoning": "Significant conversion rate decline despite maintained traffic suggests post-click issues",
                    "supporting_evidence": [
                        f"Conversion rate dropped by {abs(conv_change):.1f}%",
                        "Click volume maintained but conversions declined"
                    ],
                    "confidence": 0.72,
                    "testable": True,
                    "recommended_test": "Conduct landing page A/B test with simplified checkout"
                })
        
        return hypotheses
    
    def _identify_correlations(self, metric_changes: Dict) -> List[Dict]:
        """Identify correlations between metrics"""
        correlations = []
        
        # Check if CTR decline correlates with CPC increase
        if 'CTR' in metric_changes and 'CPC' in metric_changes:
            ctr_change = metric_changes['CTR']['percent_change']
            cpc_change = metric_changes['CPC']['percent_change']
            
            if ctr_change < -10 and cpc_change > 10:
                correlations.append({
                    "correlation_id": "CORR_001",
                    "metrics": ["CTR", "CPC"],
                    "relationship": "inverse",
                    "description": "Declining CTR is correlated with rising CPC, suggesting reduced ad relevance",
                    "strength": 0.75
                })
        
        # Check spend vs revenue efficiency
        if 'Spend' in metric_changes and 'Revenue' in metric_changes:
            spend_change = metric_changes['Spend']['percent_change']
            revenue_change = metric_changes['Revenue']['percent_change']
            
            if abs(spend_change) > 5 and abs(revenue_change) > 5:
                efficiency_ratio = revenue_change / spend_change if spend_change != 0 else 0
                
                correlations.append({
                    "correlation_id": "CORR_002",
                    "metrics": ["Spend", "Revenue"],
                    "relationship": "direct",
                    "description": f"Spend-to-revenue efficiency ratio: {efficiency_ratio:.2f}",
                    "strength": 0.80
                })
        
        return correlations
    
    def _create_summary(self, insights: List[Dict], hypotheses: List[Dict]) -> Dict[str, Any]:
        """Create executive summary"""
        critical_insights = [i for i in insights if i.get('impact') == 'critical']
        moderate_insights = [i for i in insights if i.get('impact') == 'moderate']
        
        return {
            "total_insights": len(insights),
            "critical_insights": len(critical_insights),
            "moderate_insights": len(moderate_insights),
            "total_hypotheses": len(hypotheses),
            "high_confidence_hypotheses": len([h for h in hypotheses if h.get('confidence', 0) > 0.7]),
            "key_findings": [i['title'] for i in insights[:3]]
        }


if __name__ == "__main__":
    # Test the insight agent
    config = {}
    insight_agent = InsightAgent(config)
    
    # Mock data
    mock_data = {
        "metric_changes": {
            "ROAS": {"baseline": 3.5, "comparison": 2.8, "percent_change": -20.0, "direction": "down"},
            "CTR": {"baseline": 2.5, "comparison": 1.8, "percent_change": -28.0, "direction": "down"},
            "CPC": {"baseline": 1.2, "comparison": 1.6, "percent_change": 33.3, "direction": "up"}
        },
        "segment_analysis": {}
    }
    
    mock_plan = {"objectives": ["Analyze ROAS decline"]}
    
    result = insight_agent.execute(mock_data, mock_plan)
    
    print("\n=== INSIGHT AGENT OUTPUT ===")
    print(json.dumps(result['summary'], indent=2))
