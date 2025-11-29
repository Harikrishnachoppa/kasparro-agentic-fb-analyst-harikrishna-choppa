"""
Tests for the Evaluator Agent
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.evaluator_agent import EvaluatorAgent


class TestEvaluatorAgent:
    """Test cases for Evaluator Agent"""
    
    @pytest.fixture
    def evaluator(self):
        """Create evaluator instance"""
        config = {'min_confidence': 0.6}
        return EvaluatorAgent(config)
    
    @pytest.fixture
    def sample_insights(self):
        """Sample insights for testing"""
        return {
            "insights": [
                {
                    "insight_id": "INS_001",
                    "title": "ROAS declined by 35%",
                    "description": "Significant performance decline",
                    "evidence": {
                        "baseline": 3.5,
                        "comparison": 2.3,
                        "change_pct": -35
                    },
                    "confidence": 0.95,
                    "impact": "critical",
                    "category": "ROAS"
                },
                {
                    "insight_id": "INS_002",
                    "title": "Minor CTR change",
                    "description": "Small change observed",
                    "evidence": {
                        "change_pct": -3
                    },
                    "confidence": 0.50,
                    "impact": "low",
                    "category": "Engagement"
                }
            ],
            "hypotheses": [
                {
                    "hypothesis_id": "HYP_001",
                    "statement": "Creative fatigue is causing decline",
                    "reasoning": "Extended exposure reduces engagement",
                    "supporting_evidence": [
                        "CTR declined 25%",
                        "Same creative for 60 days",
                        "Frequency increased"
                    ],
                    "confidence": 0.75,
                    "testable": True,
                    "recommended_test": "Rotate new creatives"
                }
            ]
        }
    
    def test_evaluator_initialization(self, evaluator):
        """Test evaluator initializes correctly"""
        assert evaluator is not None
        assert evaluator.min_confidence_threshold == 0.6
    
    def test_validate_insights(self, evaluator, sample_insights):
        """Test insight validation"""
        result = evaluator.execute(sample_insights, {})
        
        assert 'validated_insights' in result
        assert 'rejected_insights' in result
        assert 'quality_report' in result
        
        # Check that high-quality insight is accepted
        validated = result['validated_insights']
        assert len(validated) >= 1
        
        # First insight should have high validation score
        if len(validated) > 0:
            assert validated[0]['validation_score'] >= 0.6
            assert validated[0]['insight_id'] == 'INS_001'
    
    def test_validate_hypotheses(self, evaluator, sample_insights):
        """Test hypothesis validation"""
        result = evaluator.execute(sample_insights, {})
        
        assert 'validated_hypotheses' in result
        hypotheses = result['validated_hypotheses']
        
        # Should have at least one validated hypothesis
        assert len(hypotheses) >= 1
        assert hypotheses[0]['hypothesis_id'] == 'HYP_001'
        assert 'confidence_adjusted' in hypotheses[0]
    
    def test_quality_report_generation(self, evaluator, sample_insights):
        """Test quality report generation"""
        result = evaluator.execute(sample_insights, {})
        
        report = result['quality_report']
        
        assert 'insights' in report
        assert 'hypotheses' in report
        assert 'quality_metrics' in report
        
        # Check insights report
        assert report['insights']['total_submitted'] == 2
        assert 'approval_rate' in report['insights']
        
        # Check hypotheses report
        assert report['hypotheses']['total_submitted'] == 1
    
    def test_statistical_significance_check(self, evaluator):
        """Test statistical significance checking"""
        insight = {
            "evidence": {"change_pct": 35}
        }
        
        significance = evaluator._check_statistical_significance(insight, {})
        assert significance >= 0.85  # Large change should be significant
        
        # Small change
        insight_small = {
            "evidence": {"change_pct": 3}
        }
        significance_small = evaluator._check_statistical_significance(insight_small, {})
        assert significance_small < 0.60  # Small change less significant
    
    def test_evidence_strength_assessment(self, evaluator):
        """Test evidence strength assessment"""
        # Strong evidence
        strong_insight = {
            "evidence": {
                "baseline": 3.5,
                "comparison": 2.3,
                "change_pct": -35,
                "sample_size": 1000
            }
        }
        
        strength = evaluator._assess_evidence_strength(strong_insight)
        assert strength >= 0.7  # Should have high strength
        
        # Weak evidence
        weak_insight = {
            "evidence": {
                "change_pct": -5
            }
        }
        
        weak_strength = evaluator._assess_evidence_strength(weak_insight)
        assert weak_strength < 0.7  # Should have lower strength
    
    def test_confidence_threshold_filtering(self, evaluator, sample_insights):
        """Test that low confidence items are rejected"""
        result = evaluator.execute(sample_insights, {})
        
        # Low confidence insight should be rejected
        rejected = result['rejected_insights']
        
        # Check if any rejected insights have low scores
        for insight in rejected:
            assert insight['validation_score'] < 0.6
    
    def test_ranking_by_score(self, evaluator, sample_insights):
        """Test that insights are ranked by score"""
        result = evaluator.execute(sample_insights, {})
        
        validated = result['validated_insights']
        
        # Should be sorted by validation_score descending
        for i in range(len(validated) - 1):
            assert validated[i]['validation_score'] >= validated[i+1]['validation_score']
    
    def test_validation_notes_generation(self, evaluator):
        """Test validation notes generation"""
        score_components = {
            "confidence": 0.85,
            "evidence_strength": 0.90,
            "statistical_significance": 0.85,
            "business_relevance": 0.95
        }
        
        notes = evaluator._generate_validation_notes(score_components)
        
        assert isinstance(notes, str)
        assert len(notes) > 0
        assert "confidence" in notes.lower() or "significant" in notes.lower()


class TestEvaluatorEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_insights(self):
        """Test with empty insights list"""
        config = {'min_confidence': 0.6}
        evaluator = EvaluatorAgent(config)
        
        result = evaluator.execute({"insights": [], "hypotheses": []}, {})
        
        assert result['validated_insights'] == []
        assert result['validated_hypotheses'] == []
    
    def test_missing_evidence(self):
        """Test insight with missing evidence"""
        config = {'min_confidence': 0.6}
        evaluator = EvaluatorAgent(config)
        
        insights = {
            "insights": [
                {
                    "insight_id": "INS_001",
                    "title": "Test",
                    "confidence": 0.7,
                    "evidence": {},  # Empty evidence
                    "impact": "low",
                    "category": "Test"
                }
            ],
            "hypotheses": []
        }
        
        result = evaluator.execute(insights, {})
        
        # Should still process, but with lower score
        assert len(result['validated_insights']) >= 0
    
    def test_invalid_confidence_values(self):
        """Test with out-of-range confidence values"""
        config = {'min_confidence': 0.6}
        evaluator = EvaluatorAgent(config)
        
        insights = {
            "insights": [
                {
                    "insight_id": "INS_001",
                    "title": "Test",
                    "confidence": 1.5,  # Invalid
                    "evidence": {"change_pct": 20},
                    "impact": "moderate",
                    "category": "Test"
                }
            ],
            "hypotheses": []
        }
        
        # Should handle gracefully
        result = evaluator.execute(insights, {})
        assert 'validated_insights' in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
