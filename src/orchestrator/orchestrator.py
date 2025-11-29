"""
Orchestrator - Coordinates the multi-agent workflow
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
import traceback

from src.agents.planner_agent import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent


class Orchestrator:
    """
    Coordinates the execution of all agents in the correct sequence.
    Manages state, handles errors, and produces final outputs.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.execution_log = []
        self.state = {}
        
        # Initialize agents
        print("\n[ORCHESTRATOR] Initializing agents...")
        self.planner = PlannerAgent(config)
        self.data_agent = DataAgent(config)
        self.insight_agent = InsightAgent(config)
        self.evaluator = EvaluatorAgent(config)
        self.creative_agent = CreativeAgent(config)
        
        print("[ORCHESTRATOR] All agents initialized successfully")
    
    def execute(self, user_query: str) -> Dict[str, Any]:
        """
        Execute the complete multi-agent workflow
        
        Args:
            user_query: Natural language query from user
        
        Returns:
            Complete analysis results
        """
        print("\n" + "="*80)
        print(f"[ORCHESTRATOR] Starting analysis for query: '{user_query}'")
        print("="*80)
        
        start_time = datetime.now()
        
        try:
            # Get data context (latest date from CSV) for planner
            import pandas as pd
            data_path = self.config.get('data_path', 'data/synthetic_fb_ads_undergarments.csv')
            try:
                df_dates = pd.read_csv(data_path)
                latest_date = df_dates['date'].max()
                context = {"latest_date": str(latest_date)}
            except:
                context = {}
            
            # Stage 1: Planning
            print("\n[ORCHESTRATOR] Stage 1/5: Planning")
            plan = self._execute_agent_stage(
                "planner",
                self.planner.execute,
                user_query,
                context
            )
            
            # Stage 2: Data Retrieval
            print("\n[ORCHESTRATOR] Stage 2/5: Data Retrieval & Processing")
            data = self._execute_agent_stage(
                "data_agent",
                self.data_agent.execute,
                plan
            )
            
            # Stage 3: Insight Generation
            print("\n[ORCHESTRATOR] Stage 3/5: Insight Generation")
            insights = self._execute_agent_stage(
                "insight_agent",
                self.insight_agent.execute,
                data,
                plan
            )
            
            # Stage 4: Evaluation
            print("\n[ORCHESTRATOR] Stage 4/5: Validation & Evaluation")
            validated = self._execute_agent_stage(
                "evaluator",
                self.evaluator.execute,
                insights,
                data
            )
            
            # Stage 5: Creative Generation
            print("\n[ORCHESTRATOR] Stage 5/5: Creative Generation")
            creatives = self._execute_agent_stage(
                "creative_agent",
                self.creative_agent.execute,
                validated,
                plan.get('objectives', [])
            )
            
            # Compile final results
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            results = {
                "query": user_query,
                "execution_time_seconds": execution_time,
                "timestamp": end_time.isoformat(),
                "plan": plan,
                "data_summary": data.get('data_summary', {}),
                "insights": validated.get('validated_insights', []),
                "hypotheses": validated.get('validated_hypotheses', []),
                "creatives": creatives.get('creatives', []),
                "ab_tests": creatives.get('ab_test_recommendations', []),
                "creative_strategy": creatives.get('creative_strategy', ''),
                "execution_log": self.execution_log
            }
            
            # Save outputs
            self._save_outputs(results)
            
            print("\n" + "="*80)
            print(f"[ORCHESTRATOR] Analysis complete in {execution_time:.2f}s")
            print("="*80)
            
            return results
            
        except Exception as e:
            error_details = {
                "error": str(e),
                "traceback": traceback.format_exc(),
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"\n[ORCHESTRATOR] ERROR: {str(e)}")
            print(traceback.format_exc())
            
            self._log_execution("error", "orchestrator", error_details)
            
            return {
                "query": user_query,
                "error": True,
                "error_details": error_details,
                "execution_log": self.execution_log
            }
    
    def _execute_agent_stage(self, agent_name: str, agent_func, *args) -> Any:
        """
        Execute a single agent stage with error handling and logging
        
        Args:
            agent_name: Name of the agent
            agent_func: Agent execution function
            *args: Arguments to pass to agent
        
        Returns:
            Agent output
        """
        stage_start = datetime.now()
        
        try:
            result = agent_func(*args)
            
            stage_end = datetime.now()
            execution_time = (stage_end - stage_start).total_seconds()
            
            self._log_execution(
                "success",
                agent_name,
                {
                    "execution_time": execution_time,
                    "output_size": len(str(result))
                }
            )
            
            return result
            
        except Exception as e:
            self._log_execution(
                "failure",
                agent_name,
                {
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
            )
            raise
    
    def _log_execution(self, status: str, agent: str, details: Dict):
        """Log execution details"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "status": status,
            "details": details
        }
        self.execution_log.append(log_entry)
    
    def _save_outputs(self, results: Dict):
        """Save outputs to files"""
        print("\n[ORCHESTRATOR] Saving outputs...")
        
        # Ensure directories exist
        os.makedirs('reports', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
        # Save insights.json
        insights_output = {
            "timestamp": results['timestamp'],
            "query": results['query'],
            "insights": results['insights'],
            "hypotheses": results['hypotheses'],
            "summary": {
                "total_insights": len(results['insights']),
                "total_hypotheses": len(results['hypotheses']),
                "execution_time": results['execution_time_seconds']
            }
        }
        
        with open('reports/insights.json', 'w', encoding='utf-8') as f:
            json.dump(insights_output, f, indent=2, ensure_ascii=False)
        
        print("[ORCHESTRATOR] ✓ Saved reports/insights.json")
        
        # Save creatives.json
        creatives_output = {
            "timestamp": results['timestamp'],
            "query": results['query'],
            "creatives": results['creatives'],
            "ab_test_recommendations": results['ab_tests'],
            "summary": {
                "total_creatives": len(results['creatives']),
                "total_tests": len(results['ab_tests'])
            }
        }
        
        with open('reports/creatives.json', 'w', encoding='utf-8') as f:
            json.dump(creatives_output, f, indent=2, ensure_ascii=False)
        
        print("[ORCHESTRATOR] ✓ Saved reports/creatives.json")
        
        # Save report.md
        report_md = self._generate_markdown_report(results)
        with open('reports/report.md', 'w', encoding='utf-8') as f:
            f.write(report_md)
        
        print("[ORCHESTRATOR] ✓ Saved reports/report.md")
        
        # Save execution log
        with open('logs/execution_log.json', 'w', encoding='utf-8') as f:
            json.dump({
                "execution_id": f"EXEC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "query": results['query'],
                "timestamp": results['timestamp'],
                "execution_time_seconds": results['execution_time_seconds'],
                "log": self.execution_log
            }, f, indent=2, ensure_ascii=False)
        
        print("[ORCHESTRATOR] ✓ Saved logs/execution_log.json")
    
    def _generate_markdown_report(self, results: Dict) -> str:
        """Generate comprehensive Markdown report"""
        
        report = f"""# Facebook Ads Performance Analysis Report

**Generated:** {results['timestamp']}  
**Query:** {results['query']}  
**Execution Time:** {results['execution_time_seconds']:.2f} seconds

---

## Executive Summary

This report analyzes Facebook Ads performance for the undergarments category based on the query: "{results['query']}".

### Key Findings
"""
        
        # Add key insights
        insights = results['insights'][:5]  # Top 5
        if insights:
            report += "\n"
            for i, insight in enumerate(insights, 1):
                report += f"{i}. **{insight['title']}** (Confidence: {insight.get('confidence', 0):.0%})\n"
        
        report += "\n---\n\n## Performance Metrics Overview\n\n"
        
        # Add metrics table
        data_summary = results.get('data_summary', {})
        if data_summary:
            report += f"""
**Data Range:** {data_summary.get('date_range', {}).get('min', 'N/A')} to {data_summary.get('date_range', {}).get('max', 'N/A')}  
**Total Records:** {data_summary.get('total_rows', 0):,}  
**Baseline Period:** {data_summary.get('baseline_rows', 0):,} records  
**Comparison Period:** {data_summary.get('comparison_rows', 0):,} records

"""
        
        report += "\n## Detailed Insights\n\n"
        
        # Detailed insights
        for idx, insight in enumerate(insights, 1):
            report += f"### {idx}. {insight['title']}\n\n"
            report += f"**Category:** {insight.get('category', 'N/A')}  \n"
            report += f"**Impact:** {insight.get('impact', 'N/A')}  \n"
            report += f"**Confidence:** {insight.get('confidence', 0):.0%}  \n\n"
            report += f"{insight.get('description', 'No description available')}\n\n"
            
            evidence = insight.get('evidence', {})
            if evidence:
                report += "**Evidence:**\n"
                for key, value in evidence.items():
                    if isinstance(value, (int, float)):
                        report += f"- {key}: {value:,.2f}\n"
                    else:
                        report += f"- {key}: {value}\n"
            
            report += "\n"
        
        report += "---\n\n## Hypotheses\n\n"
        
        # Add hypotheses
        hypotheses = results.get('hypotheses', [])[:3]  # Top 3
        for idx, hyp in enumerate(hypotheses, 1):
            report += f"### Hypothesis {idx}: {hyp.get('statement', 'N/A')}\n\n"
            report += f"**Confidence:** {hyp.get('confidence', 0):.0%}  \n"
            report += f"**Testable:** {'Yes' if hyp.get('testable', False) else 'No'}  \n\n"
            
            report += f"{hyp.get('reasoning', 'No reasoning provided')}\n\n"
            
            evidence = hyp.get('supporting_evidence', [])
            if evidence:
                report += "**Supporting Evidence:**\n"
                for ev in evidence:
                    report += f"- {ev}\n"
            
            if hyp.get('recommended_test'):
                report += f"\n**Recommended Test:** {hyp['recommended_test']}\n"
            
            report += "\n"
        
        report += "---\n\n## Creative Recommendations\n\n"
        
        # Add creative recommendations
        creatives = results.get('creatives', [])[:5]  # Top 5
        for idx, creative in enumerate(creatives, 1):
            report += f"### Creative {idx}: {creative.get('headline', 'N/A')}\n\n"
            report += f"**Type:** {creative.get('type', 'N/A')}  \n"
            report += f"**Format:** {creative.get('format', 'N/A')}  \n"
            report += f"**CTA:** {creative.get('cta', 'N/A')}  \n\n"
            
            report += f"**Body Text:**  \n{creative.get('body_text', 'N/A')}\n\n"
            report += f"**Rationale:** {creative.get('rationale', 'N/A')}  \n"
            report += f"**Target Audience:** {creative.get('target_audience', 'N/A')}  \n"
            report += f"**Expected Impact:** {creative.get('expected_impact', 'N/A')}  \n\n"
        
        report += "---\n\n## A/B Testing Recommendations\n\n"
        
        # Add A/B test recommendations
        ab_tests = results.get('ab_tests', [])[:3]  # Top 3
        for idx, test in enumerate(ab_tests, 1):
            report += f"### Test {idx}: {test.get('test_name', 'N/A')}\n\n"
            report += f"**Hypothesis:** {test.get('hypothesis', 'N/A')}  \n"
            report += f"**Success Metric:** {test.get('success_metric', 'N/A')}  \n"
            report += f"**Target Lift:** {test.get('target_lift', 'N/A')}  \n"
            report += f"**Duration:** {test.get('duration_days', 0)} days  \n"
            report += f"**Budget Split:** {test.get('budget_split', 'N/A')}  \n\n"
        
        report += "---\n\n## Creative Strategy\n\n"
        report += results.get('creative_strategy', 'No strategy provided.')
        
        report += "\n\n---\n\n## Next Steps\n\n"
        report += """
1. **Immediate Actions (0-48 hours)**
   - Review top 3 insights with marketing team
   - Launch creative refresh test
   - Pause underperforming ad sets

2. **Short-term (1-2 weeks)**
   - Implement recommended A/B tests
   - Monitor new creative performance
   - Expand to new audience segments

3. **Medium-term (2-4 weeks)**
   - Analyze A/B test results
   - Scale winning combinations
   - Iterate on creative strategy

4. **Long-term (1-3 months)**
   - Build systematic testing framework
   - Develop creative rotation schedule
   - Implement automated performance monitoring

---

*Report generated by Kasparro Agentic FB Analyst v1.0*
"""
        
        return report


if __name__ == "__main__":
    # Test orchestrator
    config = {
        'data_path': 'data/synthetic_fb_ads_undergarments.csv',
        'min_confidence': 0.6,
        'brand_name': 'ComfortPlus',
        'product_category': 'undergarments'
    }
    
    orchestrator = Orchestrator(config)
    result = orchestrator.execute("Analyze ROAS drop in last 30 days")
    
    print("\n✓ Analysis complete!")
    print(f"✓ Generated {len(result['insights'])} insights")
    print(f"✓ Generated {len(result['creatives'])} creative recommendations")
