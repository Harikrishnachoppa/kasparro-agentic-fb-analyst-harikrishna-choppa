"""
Creative Generator Agent - Generates actionable creative recommendations
"""

import json
from typing import Dict, List, Any
from datetime import datetime
import random
import os


class CreativeAgent:
    """
    Responsible for generating ad creative recommendations based on insights.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.brand = config.get('brand_name', 'Your Brand')
        self.product_category = config.get('product_category', 'undergarments')
        self.prompt_template = self._load_prompt_template()
    
    def _load_prompt_template(self) -> str:
        """Load creative prompt template"""
        prompt_path = os.path.join('prompts', 'creative_prompt.md')
        try:
            with open(prompt_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return self._get_default_prompt()
    
    def _get_default_prompt(self) -> str:
        """Default prompt if file not found"""
        return """
        You are a creative copywriter. Generate compelling ad content based on data insights.
        Focus on addressing pain points and highlighting value propositions.
        """
    
    def execute(self, validated_insights: Dict[str, Any], objectives: List[str] = None) -> Dict[str, Any]:
        """
        Main execution method for the Creative Agent
        
        Args:
            validated_insights: Output from Evaluator Agent
            objectives: Business objectives (optional)
        
        Returns:
            Creative recommendations and ad content
        """
        print(f"\n[CREATIVE AGENT] Generating creative recommendations")
        
        insights = validated_insights.get('validated_insights', [])
        hypotheses = validated_insights.get('validated_hypotheses', [])
        
        # Generate creatives based on insights
        creatives = []
        
        # 1. Generate creatives addressing top insights
        for insight in insights[:3]:  # Focus on top 3 insights
            creative_set = self._generate_creative_from_insight(insight)
            creatives.extend(creative_set)
        
        # 2. Generate creatives addressing hypotheses
        for hypothesis in hypotheses[:2]:  # Top 2 hypotheses
            creative_set = self._generate_creative_from_hypothesis(hypothesis)
            creatives.extend(creative_set)
        
        # 3. Generate baseline best practice creatives
        baseline_creatives = self._generate_baseline_creatives()
        creatives.extend(baseline_creatives)
        
        # 4. Generate A/B test recommendations
        ab_tests = self._generate_ab_test_recommendations(insights, hypotheses)
        
        # 5. Create creative strategy
        strategy = self._create_creative_strategy(insights, hypotheses)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "creatives": creatives,
            "ab_test_recommendations": ab_tests,
            "creative_strategy": strategy,
            "summary": {
                "total_creatives": len(creatives),
                "creative_types": list(set([c['type'] for c in creatives])),
                "recommended_tests": len(ab_tests)
            }
        }
        
        print(f"[CREATIVE AGENT] Generated {len(creatives)} creative variants")
        print(f"[CREATIVE AGENT] Recommended {len(ab_tests)} A/B tests")
        
        return result
    
    def _generate_creative_from_insight(self, insight: Dict) -> List[Dict]:
        """Generate creatives addressing specific insight"""
        creatives = []
        category = insight.get('category', '')
        title = insight.get('title', '')
        
        creative_id_base = f"CRE_{insight.get('insight_id', 'UNK')}"
        
        # CTR/Engagement focused
        if 'CTR' in category or 'Engagement' in category:
            creatives.append({
                "creative_id": f"{creative_id_base}_A",
                "type": "image_ad",
                "format": "single_image",
                "headline": "New Arrival: Comfort Meets Style",
                "body_text": "Discover our latest collection of premium undergarments. Designed for all-day comfort. Limited time offer - Shop now!",
                "cta": "Shop New Arrivals",
                "rationale": "Fresh creative to combat fatigue and improve engagement",
                "target_audience": "Existing customers + Lookalike 1%",
                "expected_impact": "10-15% CTR improvement",
                "visual_concept": "Lifestyle imagery showing product in use"
            })
            
            creatives.append({
                "creative_id": f"{creative_id_base}_B",
                "type": "video_ad",
                "format": "short_video",
                "headline": "Feel the Difference",
                "body_text": "See why thousands choose our undergarments for superior comfort. 4.8★ rated. Free shipping on orders over $50.",
                "cta": "Watch & Shop",
                "rationale": "Video format drives higher engagement rates",
                "target_audience": "New customers + Interest-based targeting",
                "expected_impact": "20-25% CTR improvement vs static",
                "visual_concept": "15-second product demo with testimonials"
            })
        
        # ROAS/Revenue focused
        elif 'ROAS' in category or 'Revenue' in category:
            creatives.append({
                "creative_id": f"{creative_id_base}_A",
                "type": "carousel_ad",
                "format": "multi_product",
                "headline": "Bundle & Save 25%",
                "body_text": "Mix and match your favorites. Buy 3, get 25% off. Premium quality, unbeatable value.",
                "cta": "Shop Bundle Deal",
                "rationale": "Bundle offers increase AOV and ROAS",
                "target_audience": "High-intent shoppers",
                "expected_impact": "15-20% ROAS improvement",
                "visual_concept": "Carousel showing bundle options"
            })
        
        # Cost/Efficiency focused
        elif 'Cost' in category or 'CPC' in title:
            creatives.append({
                "creative_id": f"{creative_id_base}_A",
                "type": "image_ad",
                "format": "single_image",
                "headline": "Premium Quality, Fair Price",
                "body_text": "No markup. Just quality undergarments delivered to your door. Start with our bestsellers.",
                "cta": "Shop Best Sellers",
                "rationale": "Value-focused messaging to improve cost efficiency",
                "target_audience": "Price-conscious shoppers",
                "expected_impact": "8-12% CPC reduction",
                "visual_concept": "Clean product shot with price highlight"
            })
        
        return creatives
    
    def _generate_creative_from_hypothesis(self, hypothesis: Dict) -> List[Dict]:
        """Generate creatives testing specific hypothesis"""
        creatives = []
        statement = hypothesis.get('statement', '').lower()
        creative_id_base = f"CRE_{hypothesis.get('hypothesis_id', 'UNK')}"
        
        # Creative fatigue hypothesis
        if 'creative fatigue' in statement or 'fatigue' in statement:
            creatives.append({
                "creative_id": f"{creative_id_base}_FRESH",
                "type": "image_ad",
                "format": "single_image",
                "headline": "Introducing: Cloud Comfort Technology",
                "body_text": "Experience next-level softness. Our new collection uses innovative fabric for all-day comfort. Try it risk-free.",
                "cta": "Discover Cloud Comfort",
                "rationale": "New creative angle to test fatigue hypothesis",
                "target_audience": "Fatigued audience segments",
                "expected_impact": "Test for CTR lift vs existing creative",
                "visual_concept": "New photography style, bright colors"
            })
        
        # Audience saturation hypothesis
        if 'audience saturation' in statement or 'saturation' in statement:
            creatives.append({
                "creative_id": f"{creative_id_base}_EXPAND",
                "type": "image_ad",
                "format": "single_image",
                "headline": "Join 50,000+ Happy Customers",
                "body_text": "Rated 4.8★ for comfort and quality. See why we're becoming the #1 choice. First order ships free.",
                "cta": "Join The Comfort Club",
                "rationale": "Social proof for new audience expansion",
                "target_audience": "Lookalike 2-3% (broader audiences)",
                "expected_impact": "Lower CPM, maintain conversion quality",
                "visual_concept": "Community/lifestyle imagery"
            })
        
        # Landing page hypothesis
        if 'landing page' in statement:
            creatives.append({
                "creative_id": f"{creative_id_base}_LP",
                "type": "image_ad",
                "format": "single_image",
                "headline": "Your Perfect Fit Awaits",
                "body_text": "Take our 60-second fit quiz. Get personalized recommendations. Free returns on all orders.",
                "cta": "Find My Fit",
                "rationale": "Direct to improved landing experience",
                "target_audience": "All segments",
                "expected_impact": "Test conversion rate improvement",
                "visual_concept": "Interactive quiz preview"
            })
        
        return creatives
    
    def _generate_baseline_creatives(self) -> List[Dict]:
        """Generate baseline best practice creatives"""
        return [
            {
                "creative_id": "CRE_BASE_001",
                "type": "image_ad",
                "format": "single_image",
                "headline": "Comfort That Lasts All Day",
                "body_text": "Premium undergarments designed for your lifestyle. Breathable, durable, and stylish. Shop the collection.",
                "cta": "Shop Now",
                "rationale": "Baseline performance creative",
                "target_audience": "Broad audience",
                "expected_impact": "Control group for testing",
                "visual_concept": "Hero product shot"
            },
            {
                "creative_id": "CRE_BASE_002",
                "type": "image_ad",
                "format": "single_image",
                "headline": "Limited Time: 20% Off Sitewide",
                "body_text": "Upgrade your essentials. Premium quality at an unbeatable price. Use code SAVE20 at checkout.",
                "cta": "Get 20% Off",
                "rationale": "Promotional creative for conversion",
                "target_audience": "Cart abandoners + High intent",
                "expected_impact": "Higher conversion rate",
                "visual_concept": "Promotional banner overlay"
            },
            {
                "creative_id": "CRE_BASE_003",
                "type": "carousel_ad",
                "format": "multi_product",
                "headline": "Our Best Sellers",
                "body_text": "Customer favorites, restocked. See what everyone's raving about. 4.8★ average rating.",
                "cta": "Shop Best Sellers",
                "rationale": "Product showcase creative",
                "target_audience": "New customers",
                "expected_impact": "Strong ROAS performance",
                "visual_concept": "Top 5 products carousel"
            }
        ]
    
    def _generate_ab_test_recommendations(self, insights: List[Dict], hypotheses: List[Dict]) -> List[Dict]:
        """Generate A/B test recommendations"""
        tests = []
        
        # Test 1: Creative refresh
        tests.append({
            "test_id": "AB_TEST_001",
            "test_name": "Creative Refresh Impact",
            "hypothesis": "New creative will improve CTR by 15%+",
            "variant_a": {
                "description": "Current creative (control)",
                "creative_ids": ["CRE_BASE_001"]
            },
            "variant_b": {
                "description": "Fresh creative with new visuals",
                "creative_ids": ["CRE_HYP_001_FRESH"]
            },
            "success_metric": "CTR",
            "target_lift": "15%",
            "duration_days": 7,
            "budget_split": "50/50"
        })
        
        # Test 2: Messaging angle
        tests.append({
            "test_id": "AB_TEST_002",
            "test_name": "Value vs. Quality Messaging",
            "hypothesis": "Quality-focused messaging will drive higher ROAS",
            "variant_a": {
                "description": "Price/value focused messaging",
                "creative_ids": ["CRE_BASE_002"]
            },
            "variant_b": {
                "description": "Quality/comfort focused messaging",
                "creative_ids": ["CRE_BASE_001"]
            },
            "success_metric": "ROAS",
            "target_lift": "10%",
            "duration_days": 14,
            "budget_split": "50/50"
        })
        
        # Test 3: Format test
        tests.append({
            "test_id": "AB_TEST_003",
            "test_name": "Image vs. Video Format",
            "hypothesis": "Video ads will achieve better engagement",
            "variant_a": {
                "description": "Static image ad",
                "creative_ids": ["CRE_INS_CTR_001_A"]
            },
            "variant_b": {
                "description": "15-second video ad",
                "creative_ids": ["CRE_INS_CTR_001_B"]
            },
            "success_metric": "Engagement Rate",
            "target_lift": "25%",
            "duration_days": 7,
            "budget_split": "40/60 (favor video)"
        })
        
        # Test 4: Audience expansion
        tests.append({
            "test_id": "AB_TEST_004",
            "test_name": "Audience Expansion Test",
            "hypothesis": "Broader lookalike audiences maintain efficiency",
            "variant_a": {
                "description": "Current LAL 1% audience",
                "creative_ids": ["CRE_BASE_001"]
            },
            "variant_b": {
                "description": "LAL 2-3% audience with social proof",
                "creative_ids": ["CRE_HYP_002_EXPAND"]
            },
            "success_metric": "CPA",
            "target_lift": "Maintain or improve CPA",
            "duration_days": 14,
            "budget_split": "60/40 (favor proven audience)"
        })
        
        return tests
    
    def _create_creative_strategy(self, insights: List[Dict], hypotheses: List[Dict]) -> str:
        """Create overall creative strategy narrative"""
        strategy = f"""
# Creative Strategy Recommendations

## Executive Summary
Based on analysis of {len(insights)} validated insights, we recommend a three-pronged creative strategy:

1. **Creative Refresh**: Combat engagement fatigue with new visual styles and messaging angles
2. **Audience Expansion**: Scale to broader audiences with social proof-driven creatives
3. **Conversion Optimization**: Improve post-click experience with clearer value propositions

## Key Strategic Pillars

### 1. Address Creative Fatigue
- Rotate in 3-5 new creative variants immediately
- Test video formats to drive re-engagement
- Introduce new visual styles (lifestyle vs. product-focused)
- Update copy to emphasize different benefits (comfort → quality → value)

### 2. Optimize for Efficiency
- Bundle offers to increase AOV and improve ROAS
- Value-focused messaging for price-conscious segments
- Social proof to reduce friction for new audiences
- Clear CTAs that set conversion expectations

### 3. Scale What Works
- Identify top-performing creative/audience combinations
- Create variations of winners (not duplicates)
- Systematically test into new audience segments
- Monitor for saturation signals (rising CPM, declining CTR)

## Immediate Action Items
1. Launch creative refresh test within 48 hours
2. Implement carousel ads for bundle promotion
3. Expand to LAL 2-3% audiences with social proof creative
4. Create video variants of top static performers

## Success Metrics
- **CTR**: Target 15% improvement within 7 days
- **CPC**: Target 10% reduction within 14 days
- **ROAS**: Target return to 3.2+ within 30 days
- **Conversion Rate**: Target 12% improvement with new landing page

## Testing Roadmap
- Week 1-2: Creative refresh + format tests
- Week 3-4: Audience expansion tests
- Week 5-6: Messaging angle tests
- Ongoing: Iterate on winners, kill losers
"""
        
        return strategy


if __name__ == "__main__":
    # Test the creative agent
    config = {'brand_name': 'ComfortPlus', 'product_category': 'undergarments'}
    creative_agent = CreativeAgent(config)
    
    # Mock validated insights
    mock_insights = {
        "validated_insights": [
            {
                "insight_id": "INS_001",
                "category": "Engagement",
                "title": "CTR declined significantly"
            }
        ],
        "validated_hypotheses": [
            {
                "hypothesis_id": "HYP_001",
                "statement": "Creative fatigue is contributing to declining CTR"
            }
        ]
    }
    
    result = creative_agent.execute(mock_insights)
    
    print("\n=== CREATIVE AGENT OUTPUT ===")
    print(f"Generated {len(result['creatives'])} creatives")
    print(f"Recommended {len(result['ab_test_recommendations'])} A/B tests")
