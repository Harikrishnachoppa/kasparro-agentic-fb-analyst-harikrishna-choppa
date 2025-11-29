"""
Basic tests for all agents
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.planner_agent import PlannerAgent
from agents.data_agent import DataAgent
from agents.insight_agent import InsightAgent
from agents.creative_agent import CreativeAgent


class TestPlannerAgent:
    """Tests for Planner Agent"""
    
    def test_planner_initialization(self):
        """Test planner initializes"""
        config = {}
        planner = PlannerAgent(config)
        assert planner is not None
    
    def test_planner_execution(self):
        """Test planner processes query"""
        config = {}
        planner = PlannerAgent(config)
        
        result = planner.execute("Analyze ROAS drop")
        
        assert 'plan_id' in result
        assert 'objectives' in result
        assert 'metrics_to_analyze' in result
        assert len(result['objectives']) > 0
    
    def test_metric_identification(self):
        """Test metric identification from query"""
        config = {}
        planner = PlannerAgent(config)
        
        result = planner.execute("Why is CTR declining?")
        
        assert 'CTR' in result['metrics_to_analyze']


class TestDataAgent:
    """Tests for Data Agent"""
    
    def test_data_agent_initialization(self):
        """Test data agent initializes"""
        config = {'data_path': 'data/synthetic_fb_ads_undergarments.csv'}
        data_agent = DataAgent(config)
        assert data_agent is not None
    
    def test_metric_calculation(self):
        """Test that metrics are calculated correctly"""
        import pandas as pd
        import numpy as np
        
        # Create sample data
        df = pd.DataFrame({
            'Spend': [100],
            'Revenue': [350],
            'Impressions': [10000],
            'Clicks': [200],
            'Conversions': [20]
        })
        
        # Calculate ROAS
        roas = df['Revenue'][0] / df['Spend'][0]
        assert roas == 3.5
        
        # Calculate CTR
        ctr = (df['Clicks'][0] / df['Impressions'][0]) * 100
        assert ctr == 2.0
        
        # Calculate CPC
        cpc = df['Spend'][0] / df['Clicks'][0]
        assert cpc == 0.5


class TestInsightAgent:
    """Tests for Insight Agent"""
    
    def test_insight_agent_initialization(self):
        """Test insight agent initializes"""
        config = {}
        insight_agent = InsightAgent(config)
        assert insight_agent is not None
    
    def test_insight_generation(self):
        """Test insight generation"""
        config = {}
        insight_agent = InsightAgent(config)
        
        mock_data = {
            "metric_changes": {
                "ROAS": {
                    "baseline": 3.5,
                    "comparison": 2.8,
                    "percent_change": -20.0,
                    "direction": "down"
                }
            },
            "segment_analysis": {}
        }
        
        result = insight_agent.execute(mock_data, {})
        
        assert 'insights' in result
        assert 'hypotheses' in result
        assert len(result['insights']) > 0


class TestCreativeAgent:
    """Tests for Creative Agent"""
    
    def test_creative_agent_initialization(self):
        """Test creative agent initializes"""
        config = {'brand_name': 'Test Brand'}
        creative_agent = CreativeAgent(config)
        assert creative_agent is not None
    
    def test_creative_generation(self):
        """Test creative generation"""
        config = {'brand_name': 'Test Brand'}
        creative_agent = CreativeAgent(config)
        
        mock_insights = {
            "validated_insights": [
                {
                    "insight_id": "INS_001",
                    "category": "Engagement",
                    "title": "CTR declined"
                }
            ],
            "validated_hypotheses": []
        }
        
        result = creative_agent.execute(mock_insights)
        
        assert 'creatives' in result
        assert 'ab_test_recommendations' in result
        assert len(result['creatives']) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
