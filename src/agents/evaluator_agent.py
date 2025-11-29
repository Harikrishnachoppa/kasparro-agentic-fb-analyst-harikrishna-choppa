"""
Evaluator Agent - Validates, scores, and ranks insights and hypotheses
"""

import json
from typing import Dict, List, Any
from datetime import datetime
import os


class EvaluatorAgent:
    """
    Responsible for validating and scoring insights and hypotheses.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.prompt_template = self._load_prompt_template()
        self.min_confidence_threshold = config.get('min_confidence', 0.6)
    
    def _load_prompt_template(self) -> str:
        """Load evaluator prompt template"""
        prompt_path = os.path.join('prompts', 'evaluator_prompt.md')
        try:
            with open(prompt_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return self._get_default_prompt()
    
    def _get_default_prompt(self) -> str:
        """Default prompt if file not found"""
        return """
        You are a data validation expert. Evaluate insights and hypotheses for accuracy and relevance.
        Score based on evidence strength, statistical significance, and business impact.
        """
    
    def execute(self, insights_data: Dict[str, Any], processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method for the Evaluator Agent
        
        Args:
            insights_data: Output from Insight Agent
            processed_data: Data from Data Agent for validation
        
        Returns:
            Validated and ranked insights
        """
        print(f"\n[EVALUATOR AGENT] Validating insights and hypotheses")
        
        insights = insights_data.get('insights', [])
        hypotheses = insights_data.get('hypotheses', [])
        
        # Validate and score insights
        validated_insights = self._validate_insights(insights, processed_data)
        
        # Validate and score hypotheses
        validated_hypotheses = self._validate_hypotheses(hypotheses, processed_data)
        
        # Rank by score
        validated_insights = sorted(validated_insights, key=lambda x: x['validation_score'], reverse=True)
        validated_hypotheses = sorted(validated_hypotheses, key=lambda x: x['confidence_adjusted'], reverse=True)
        
        # Filter low-confidence items
        high_quality_insights = [i for i in validated_insights if i['validation_score'] >= self.min_confidence_threshold]
        high_quality_hypotheses = [h for h in validated_hypotheses if h['confidence_adjusted'] >= self.min_confidence_threshold]
        
        # Generate quality report
        quality_report = self._generate_quality_report(
            validated_insights, 
            validated_hypotheses,
            high_quality_insights,
            high_quality_hypotheses
        )
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "validated_insights": high_quality_insights,
            "validated_hypotheses": high_quality_hypotheses,
            "rejected_insights": [i for i in validated_insights if i['validation_score'] < self.min_confidence_threshold],
            "rejected_hypotheses": [h for h in validated_hypotheses if h['confidence_adjusted'] < self.min_confidence_threshold],
            "quality_report": quality_report
        }
        
        print(f"[EVALUATOR AGENT] Validated {len(high_quality_insights)}/{len(insights)} insights")
        print(f"[EVALUATOR AGENT] Validated {len(high_quality_hypotheses)}/{len(hypotheses)} hypotheses")
        
        return result
    
    def _validate_insights(self, insights: List[Dict], data: Dict[str, Any]) -> List[Dict]:
        """Validate and score insights"""
        validated = []
        
        for idx, insight in enumerate(insights):
            # Calculate validation score
            score_components = {
                "confidence": insight.get('confidence', 0.5),
                "evidence_strength": self._assess_evidence_strength(insight),
                "statistical_significance": self._check_statistical_significance(insight, data),
                "business_relevance": self._assess_business_relevance(insight)
            }
            
            # Weighted average
            validation_score = (
                score_components['confidence'] * 0.3 +
                score_components['evidence_strength'] * 0.3 +
                score_components['statistical_significance'] * 0.25 +
                score_components['business_relevance'] * 0.15
            )
            
            validated_insight = insight.copy()
            validated_insight.update({
                "validation_score": round(validation_score, 2),
                "confidence_adjusted": round(insight.get('confidence', 0.5) * validation_score, 2),
                "score_components": score_components,
                "ranking": idx + 1,
                "validation_notes": self._generate_validation_notes(score_components),
                "statistical_significance": score_components['statistical_significance'] > 0.7
            })
            
            validated.append(validated_insight)
        
        return validated
    
    def _validate_hypotheses(self, hypotheses: List[Dict], data: Dict[str, Any]) -> List[Dict]:
        """Validate and score hypotheses"""
        validated = []
        
        for idx, hypothesis in enumerate(hypotheses):
            # Calculate adjusted confidence
            original_confidence = hypothesis.get('confidence', 0.5)
            
            score_components = {
                "original_confidence": original_confidence,
                "evidence_count": min(len(hypothesis.get('supporting_evidence', [])) / 3, 1.0),
                "testability": 1.0 if hypothesis.get('testable', False) else 0.5,
                "specificity": self._assess_hypothesis_specificity(hypothesis)
            }
            
            # Adjusted confidence
            confidence_adjusted = (
                score_components['original_confidence'] * 0.4 +
                score_components['evidence_count'] * 0.3 +
                score_components['testability'] * 0.2 +
                score_components['specificity'] * 0.1
            )
            
            validated_hypothesis = hypothesis.copy()
            validated_hypothesis.update({
                "confidence_adjusted": round(confidence_adjusted, 2),
                "score_components": score_components,
                "ranking": idx + 1,
                "validation_notes": self._generate_hypothesis_notes(score_components)
            })
            
            validated.append(validated_hypothesis)
        
        return validated
    
    def _assess_evidence_strength(self, insight: Dict) -> float:
        """Assess the strength of evidence provided"""
        evidence = insight.get('evidence', {})
        
        score = 0.5  # Base score
        
        # Check for quantitative evidence
        if any(isinstance(v, (int, float)) for v in evidence.values()):
            score += 0.2
        
        # Check for multiple evidence points
        if len(evidence) >= 3:
            score += 0.15
        
        # Check for large effect size
        if 'change_pct' in evidence:
            change = abs(evidence['change_pct'])
            if change > 20:
                score += 0.15
        
        return min(score, 1.0)
    
    def _check_statistical_significance(self, insight: Dict, data: Dict[str, Any]) -> float:
        """Check if changes are statistically significant"""
        evidence = insight.get('evidence', {})
        
        # Simple heuristic: larger changes are more likely significant
        if 'change_pct' in evidence:
            change = abs(evidence['change_pct'])
            
            if change > 30:
                return 0.95
            elif change > 20:
                return 0.85
            elif change > 10:
                return 0.70
            elif change > 5:
                return 0.55
            else:
                return 0.40
        
        return 0.50
    
    def _assess_business_relevance(self, insight: Dict) -> float:
        """Assess business relevance and impact"""
        impact = insight.get('impact', 'low')
        category = insight.get('category', '')
        
        score = 0.5
        
        # Impact level
        if impact == 'critical':
            score += 0.3
        elif impact == 'moderate':
            score += 0.2
        
        # High-value categories
        high_value_categories = ['ROAS', 'Revenue', 'Efficiency', 'Cost']
        if category in high_value_categories:
            score += 0.2
        
        return min(score, 1.0)
    
    def _assess_hypothesis_specificity(self, hypothesis: Dict) -> float:
        """Assess how specific and actionable the hypothesis is"""
        statement = hypothesis.get('statement', '')
        has_test = bool(hypothesis.get('recommended_test', ''))
        
        score = 0.5
        
        # Check for specific terms
        specific_terms = ['creative', 'audience', 'landing page', 'bidding', 'targeting']
        if any(term in statement.lower() for term in specific_terms):
            score += 0.3
        
        # Has recommended test
        if has_test:
            score += 0.2
        
        return min(score, 1.0)
    
    def _generate_validation_notes(self, score_components: Dict) -> str:
        """Generate validation notes for insight"""
        notes = []
        
        if score_components['confidence'] > 0.8:
            notes.append("High initial confidence")
        
        if score_components['statistical_significance'] > 0.8:
            notes.append("Statistically significant change")
        
        if score_components['evidence_strength'] > 0.7:
            notes.append("Strong supporting evidence")
        
        if score_components['business_relevance'] > 0.7:
            notes.append("High business impact")
        
        if not notes:
            notes.append("Moderate confidence, requires further validation")
        
        return "; ".join(notes)
    
    def _generate_hypothesis_notes(self, score_components: Dict) -> str:
        """Generate validation notes for hypothesis"""
        notes = []
        
        if score_components['testability'] == 1.0:
            notes.append("Testable hypothesis")
        else:
            notes.append("Difficult to test directly")
        
        if score_components['evidence_count'] > 0.7:
            notes.append("Well-supported by evidence")
        
        if score_components['specificity'] > 0.7:
            notes.append("Specific and actionable")
        
        return "; ".join(notes)
    
    def _generate_quality_report(self, all_insights: List, all_hypotheses: List,
                                 approved_insights: List, approved_hypotheses: List) -> Dict:
        """Generate quality assurance report"""
        return {
            "insights": {
                "total_submitted": len(all_insights),
                "approved": len(approved_insights),
                "rejected": len(all_insights) - len(approved_insights),
                "approval_rate": round(len(approved_insights) / len(all_insights) * 100, 1) if all_insights else 0,
                "average_score": round(sum(i['validation_score'] for i in all_insights) / len(all_insights), 2) if all_insights else 0
            },
            "hypotheses": {
                "total_submitted": len(all_hypotheses),
                "approved": len(approved_hypotheses),
                "rejected": len(all_hypotheses) - len(approved_hypotheses),
                "approval_rate": round(len(approved_hypotheses) / len(all_hypotheses) * 100, 1) if all_hypotheses else 0,
                "average_confidence": round(sum(h['confidence_adjusted'] for h in all_hypotheses) / len(all_hypotheses), 2) if all_hypotheses else 0
            },
            "quality_metrics": {
                "high_confidence_insights": len([i for i in approved_insights if i['validation_score'] > 0.8]),
                "actionable_hypotheses": len([h for h in approved_hypotheses if h.get('testable', False)]),
                "statistically_significant": len([i for i in approved_insights if i.get('statistical_significance', False)])
            }
        }


if __name__ == "__main__":
    # Test the evaluator agent
    config = {'min_confidence': 0.6}
    evaluator = EvaluatorAgent(config)
    
    # Mock insights
    mock_insights = {
        "insights": [
            {
                "insight_id": "INS_001",
                "title": "ROAS declined by 20%",
                "confidence": 0.95,
                "impact": "critical",
                "evidence": {"change_pct": -20, "baseline": 3.5, "comparison": 2.8},
                "category": "ROAS"
            }
        ],
        "hypotheses": [
            {
                "hypothesis_id": "HYP_001",
                "statement": "Creative fatigue",
                "confidence": 0.75,
                "supporting_evidence": ["CTR declined", "Extended exposure"],
                "testable": True
            }
        ]
    }
    
    result = evaluator.execute(mock_insights, {})
    
    print("\n=== EVALUATOR AGENT OUTPUT ===")
    print(json.dumps(result['quality_report'], indent=2))
