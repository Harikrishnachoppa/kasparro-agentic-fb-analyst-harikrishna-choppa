# Quick Start Guide

## Kasparro Agentic FB Analyst

Get started in 3 simple steps!

---

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- pandas (data processing)
- numpy (numerical computing)
- pyyaml (configuration)

---

## Step 2: Run the System

```bash
python run.py "Analyze ROAS drop in last 30 days"
```

### More Example Queries

```bash
# Performance diagnostics
python run.py "Why is my CTR declining?"

# Optimization requests
python run.py "How can I improve my Facebook ads?"

# Metric-specific analysis
python run.py "Analyze conversion rate trends"

# Cost analysis
python run.py "Why is my CPC increasing?"
```

---

## Step 3: View Results

Check the `reports/` directory:

- **insights.json** - Validated insights with evidence and confidence scores
- **creatives.json** - Creative recommendations and A/B test strategies
- **report.md** - Comprehensive markdown report with visualizations
- **logs/execution_log.json** - Detailed execution timeline

---

## Expected Output

```
================================================================================
            KASPARRO AGENTIC FB ANALYST v1.0
================================================================================
Multi-Agent Facebook Ads Performance Analysis System
================================================================================

📊 Query: Analyze ROAS drop in last 30 days
⏰ Started at: 2024-01-15 14:30:00

✓ Configuration loaded from config/config.yaml

[ORCHESTRATOR] Initializing agents...
[ORCHESTRATOR] All agents initialized successfully

================================================================================
[ORCHESTRATOR] Starting analysis for query: 'Analyze ROAS drop in last 30 days'
================================================================================

[ORCHESTRATOR] Stage 1/5: Planning
[PLANNER AGENT] Processing query: 'Analyze ROAS drop in last 30 days'
[PLANNER AGENT] Plan created with 2 objectives
[PLANNER AGENT] Metrics to analyze: ROAS, Spend, Revenue, ...

[ORCHESTRATOR] Stage 2/5: Data Retrieval & Processing
[DATA AGENT] Loading data from data/synthetic_fb_ads_undergarments.csv
[DATA AGENT] Loaded 1847 rows
[DATA AGENT] Baseline period: 923 rows
[DATA AGENT] Comparison period: 924 rows
[DATA AGENT] Processing complete

[ORCHESTRATOR] Stage 3/5: Insight Generation
[INSIGHT AGENT] Analyzing data and generating insights
[INSIGHT AGENT] Generated 12 insights and 5 hypotheses

[ORCHESTRATOR] Stage 4/5: Validation & Evaluation
[EVALUATOR AGENT] Validating insights and hypotheses
[EVALUATOR AGENT] Validated 5/12 insights
[EVALUATOR AGENT] Validated 3/5 hypotheses

[ORCHESTRATOR] Stage 5/5: Creative Generation
[CREATIVE AGENT] Generating creative recommendations
[CREATIVE AGENT] Generated 10 creative variants
[CREATIVE AGENT] Recommended 5 A/B tests

[ORCHESTRATOR] Saving outputs...
[ORCHESTRATOR] ✓ Saved reports/insights.json
[ORCHESTRATOR] ✓ Saved reports/creatives.json
[ORCHESTRATOR] ✓ Saved reports/report.md
[ORCHESTRATOR] ✓ Saved logs/execution_log.json

================================================================================
[ORCHESTRATOR] Analysis complete in 8.45s
================================================================================

================================================================================
📈 ANALYSIS COMPLETE
================================================================================

✓ Execution time: 8.45 seconds
✓ Insights generated: 5
✓ Hypotheses generated: 3
✓ Creative recommendations: 10
✓ A/B test recommendations: 5

📁 Output files generated:
   • reports/insights.json
   • reports/creatives.json
   • reports/report.md
   • logs/execution_log.json

💡 Top 3 Insights:
   1. ROAS has declined by 22.5%
      Impact: critical | Confidence: 95%
   2. Click-through rate declined significantly
      Impact: moderate | Confidence: 85%
   3. Cost per click has increased significantly
      Impact: moderate | Confidence: 88%

🎨 Top 3 Creative Recommendations:
   1. Bundle & Save 25%
      Type: carousel_ad | Expected Impact: 15-20% ROAS improvement
   2. New Arrival: Comfort Meets Style
      Type: image_ad | Expected Impact: 10-15% CTR improvement
   3. Feel the Difference
      Type: video_ad | Expected Impact: 20-25% CTR improvement vs static

📄 View full report: reports/report.md

================================================================================
✅ SUCCESS - Analysis complete!
================================================================================
```

---

## Understanding the Output

### insights.json
Contains validated insights with:
- Confidence scores (0-1)
- Evidence (quantitative data)
- Impact level (critical/moderate/low)
- Validation notes
- Statistical significance

### creatives.json
Contains creative recommendations with:
- Headlines (40 chars max)
- Body text (125 chars max)
- Call-to-action
- Target audience
- Expected impact
- A/B test designs

### report.md
A comprehensive markdown report with:
- Executive summary
- Detailed insights
- Hypotheses with evidence
- Creative recommendations
- A/B testing roadmap
- Next steps

---

## Customization

### Edit Configuration

Modify `config/config.yaml` to:
- Change confidence thresholds
- Adjust time windows
- Modify brand settings
- Configure output paths

### Use Your Own Data

Replace `data/synthetic_fb_ads_undergarments.csv` with your data.

**Required columns:**
- Date
- Campaign_Name
- Creative_Type
- Audience_Segment
- Impressions
- Clicks
- Spend
- Revenue
- Conversions

---

## Troubleshooting

### Issue: "File not found"
**Solution:** Ensure you're in the project directory
```bash
cd kasparro-agentic-fb-analyst-harikrishna-choppa
```

### Issue: "Module not found"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "No data loaded"
**Solution:** Check that CSV file exists in `data/` directory

---

## Run Tests

Verify everything works:

```bash
python -m pytest tests/ -v
```

Expected output:
```
tests/test_agents.py::TestPlannerAgent::test_planner_initialization PASSED
tests/test_agents.py::TestPlannerAgent::test_planner_execution PASSED
tests/test_evaluator.py::TestEvaluatorAgent::test_evaluator_initialization PASSED
tests/test_evaluator.py::TestEvaluatorAgent::test_validate_insights PASSED
...
==================== 15 passed in 2.34s ====================
```

---

## Next Steps

1. **Review Outputs:** Check `reports/` directory
2. **Read Full Report:** Open `reports/report.md`
3. **Understand Architecture:** Read `agent_graph.md`
4. **Explore Code:** Browse `src/agents/`
5. **Try Different Queries:** Experiment with various questions

---

## Need Help?

- **Documentation:** See `README.md`
- **Architecture:** See `agent_graph.md`
- **Data Format:** See `data/README.md`
- **Delivery Summary:** See `DELIVERY_SUMMARY.md`

---

**You're all set! 🚀**

Run `python run.py "Analyze ROAS drop"` to begin analyzing Facebook Ads performance.
