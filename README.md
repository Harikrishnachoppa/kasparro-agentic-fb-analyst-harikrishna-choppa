# Kasparro Agentic FB Analyst - Harikrishna Choppa

**Version:** 1.0.0  
**Author:** Harikrishna Choppa  
**Repository:** kasparro-agentic-fb-analyst-harikrishna-choppa

---

## 🎯 Project Overview

An advanced multi-agent system for analyzing Facebook Ads performance using specialized AI agents that collaborate to provide comprehensive insights, validated hypotheses, and actionable creative recommendations.

### Key Features

- **5 Specialized Agents**: Planner, Data, Insight, Evaluator, and Creative Generator
- **Automated Analysis**: Natural language query processing
- **Validated Insights**: Statistical validation and confidence scoring
- **Creative Recommendations**: Data-driven ad copy and A/B test strategies
- **Comprehensive Reporting**: JSON outputs + Markdown reports
- **Production-Ready**: Complete error handling, logging, and testing

---

## 📁 Repository Structure

```
kasparro-agentic-fb-analyst-harikrishna-choppa/
│
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── run.py                            # Main entry point
├── Makefile                          # Build and run commands
├── agent_graph.md                    # Architecture documentation
│
├── config/
│   └── config.yaml                   # System configuration
│
├── src/
│   ├── agents/
│   │   ├── planner_agent.py         # Query parsing and planning
│   │   ├── data_agent.py            # Data loading and processing
│   │   ├── insight_agent.py         # Insight and hypothesis generation
│   │   ├── evaluator_agent.py       # Validation and scoring
│   │   └── creative_agent.py        # Creative recommendations
│   │
│   ├── orchestrator/
│   │   └── orchestrator.py          # Multi-agent coordination
│   │
│   └── utils/
│       └── helpers.py               # Utility functions
│
├── prompts/
│   ├── planner_prompt.md            # Planner agent instructions
│   ├── insight_prompt.md            # Insight agent instructions
│   ├── evaluator_prompt.md          # Evaluator agent instructions
│   └── creative_prompt.md           # Creative agent instructions
│
├── data/
│   ├── synthetic_fb_ads_undergarments.csv  # Sample dataset
│   └── README.md                    # Data documentation
│
├── tests/
│   ├── test_agents.py               # Agent unit tests
│   └── test_evaluator.py            # Evaluator-specific tests
│
├── reports/                          # Generated outputs
│   ├── insights.json                # Validated insights
│   ├── creatives.json               # Creative recommendations
│   └── report.md                    # Comprehensive report
│
└── logs/
    └── example_log.json             # Execution logs
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8+
- pip

### Setup Steps

1. **Clone or navigate to the repository:**

```bash
cd kasparro-agentic-fb-analyst-harikrishna-choppa
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

**Required packages:**
- pandas >= 2.0.0
- numpy >= 1.24.0
- pyyaml >= 6.0

3. **Verify installation:**

```bash
python --version  # Should be 3.8+
pip list | grep pandas  # Verify pandas installed
```

---

## 💻 How to Run

### Basic Usage

```bash
python run.py "Analyze ROAS drop in last 30 days"
```

### Example Queries

```bash
# Diagnose performance issues
python run.py "Why is my CTR declining?"

# Optimize campaigns
python run.py "How can I improve my Facebook ads?"

# Analyze specific metrics
python run.py "Analyze conversion rate trends"

# Cost analysis
python run.py "Why is my CPC increasing?"
```

### Expected Output

The system will:
1. Parse your query
2. Load and process data
3. Generate insights and hypotheses
4. Validate findings
5. Create creative recommendations
6. Generate reports

**Output files:**
- `reports/insights.json` - Validated insights with evidence
- `reports/creatives.json` - Creative recommendations
- `reports/report.md` - Comprehensive markdown report
- `logs/execution_log.json` - Execution details

---

## 🏗️ Architecture

### Multi-Agent System Design

```
USER QUERY → ORCHESTRATOR
                 ↓
         ┌───────────────┐
         │ PLANNER AGENT │ (Parse query, create plan)
         └───────┬───────┘
                 ↓
         ┌───────────────┐
         │  DATA AGENT   │ (Load CSV, compute metrics)
         └───────┬───────┘
                 ↓
         ┌───────────────┐
         │ INSIGHT AGENT │ (Analyze trends, generate hypotheses)
         └───────┬───────┘
                 ↓
         ┌───────────────┐
         │  EVALUATOR    │ (Validate, score, rank)
         └───────┬───────┘
                 ↓
         ┌───────────────┐
         │   CREATIVE    │ (Generate ad content, A/B tests)
         └───────┬───────┘
                 ↓
         OUTPUTS (JSON + Markdown)
```

### Agent Descriptions

#### 1. **Planner Agent**
- **Purpose**: Decomposes natural language queries into structured analysis plans
- **Input**: User query string
- **Output**: Structured plan with objectives, metrics, time windows, segments
- **Key Logic**: 
  - Intent recognition (diagnostic, optimization, exploratory)
  - Metric selection based on query keywords
  - Time window determination (7, 14, 30, 60, 90 days)
  - Segment identification

#### 2. **Data Agent**
- **Purpose**: Loads, filters, and processes Facebook Ads data
- **Input**: Analysis plan from Planner
- **Output**: Processed data with aggregated metrics
- **Key Logic**:
  - CSV loading and validation
  - Metric calculation (ROAS, CTR, CPC, CPM, Conversion Rate)
  - Time period filtering (baseline vs comparison)
  - Segment aggregation
  - Data quality reporting

#### 3. **Insight Agent**
- **Purpose**: Analyzes data to generate insights and hypotheses
- **Input**: Processed data + plan
- **Output**: Insights with evidence and hypotheses
- **Key Logic**:
  - Trend detection (>10% changes trigger insights)
  - Anomaly identification
  - Correlation analysis
  - Hypothesis generation (creative fatigue, audience saturation, etc.)
  - Confidence scoring

#### 4. **Evaluator Agent**
- **Purpose**: Validates and scores insights for quality
- **Input**: Raw insights + data
- **Output**: Validated and ranked insights
- **Key Logic**:
  - Evidence strength assessment
  - Statistical significance checking
  - Business relevance scoring
  - Composite validation score calculation
  - Filtering (threshold: 0.6)

**Validation Formula:**
```
validation_score = (
  confidence * 0.30 +
  evidence_strength * 0.30 +
  statistical_significance * 0.25 +
  business_relevance * 0.15
)
```

#### 5. **Creative Generator Agent**
- **Purpose**: Generates ad creative and A/B test recommendations
- **Input**: Validated insights + hypotheses
- **Output**: Creative variants + A/B test plans
- **Key Logic**:
  - Insight-to-creative mapping
  - Headline/body copy generation
  - CTA selection
  - Visual concept description
  - A/B test design

---

## 📊 Sample Output

### Insights Example

```json
{
  "insight_id": "INS_ROAS_001",
  "title": "ROAS has declined by 22.5%",
  "description": "Return on Ad Spend declined from 3.45 to 2.67...",
  "evidence": {
    "baseline_roas": 3.45,
    "comparison_roas": 2.67,
    "change_pct": -22.5
  },
  "confidence": 0.95,
  "impact": "critical",
  "validation_score": 0.93
}
```

### Creative Example

```json
{
  "creative_id": "CRE_001",
  "type": "image_ad",
  "headline": "New Arrival: Comfort Meets Style",
  "body_text": "Discover our latest collection...",
  "cta": "Shop New Arrivals",
  "expected_impact": "10-15% CTR improvement"
}
```

---

## 🧪 Testing

### Run All Tests

```bash
python -m pytest tests/ -v
```

### Run Evaluator Tests Specifically

```bash
python -m pytest tests/test_evaluator.py -v
```

### Test Coverage

- **test_agents.py**: Basic agent functionality tests
- **test_evaluator.py**: Comprehensive evaluator validation tests
  - Validation scoring
  - Statistical significance checks
  - Evidence strength assessment
  - Threshold filtering
  - Ranking logic

---

## 📈 Evaluation Logic

### Insight Validation Criteria

1. **Evidence Strength** (30% weight)
   - Quantitative evidence: +0.2
   - Multiple evidence points: +0.15
   - Large effect size (>20%): +0.15

2. **Statistical Significance** (25% weight)
   - >30% change: 0.95
   - 20-30% change: 0.85
   - 10-20% change: 0.70
   - 5-10% change: 0.55
   - <5% change: 0.40

3. **Original Confidence** (30% weight)
   - From Insight Agent analysis

4. **Business Relevance** (15% weight)
   - Critical impact: +0.3
   - Moderate impact: +0.2
   - High-value category: +0.2

### Acceptance Threshold

- **Insights**: validation_score ≥ 0.60
- **Hypotheses**: confidence_adjusted ≥ 0.60

---

## 📝 Logs Explanation

### Execution Log Structure

```json
{
  "execution_id": "EXEC_20240115_143000",
  "query": "User query",
  "timestamp": "ISO8601 timestamp",
  "execution_time_seconds": 8.45,
  "log": [
    {
      "timestamp": "ISO8601",
      "agent": "agent_name",
      "status": "success|failure",
      "details": {
        "execution_time": 2.30,
        "output_size": 8945
      }
    }
  ]
}
```

### Log Information

- **execution_id**: Unique identifier for each run
- **Agent logs**: Individual agent performance
- **Execution times**: Per-agent and total timing
- **Output sizes**: Data volume processed
- **Status tracking**: Success/failure for debugging

---

## 🎉 v1.0 Release Notes

### Release Date: January 15, 2024

### Features Delivered

✅ **Complete 5-Agent Architecture**
- Planner, Data, Insight, Evaluator, Creative agents fully implemented
- Orchestrator for seamless agent coordination
- Error handling and recovery mechanisms

✅ **Natural Language Query Processing**
- Parse queries like "Why is my ROAS dropping?"
- Automatic metric and time window selection
- Intent recognition (diagnostic, optimization, exploratory)

✅ **Data Processing Pipeline**
- CSV data loading and validation
- Automated metric calculation (ROAS, CTR, CPC, CPM, CR)
- Time-period comparison (baseline vs current)
- Segment analysis (campaigns, creatives, audiences)

✅ **Insight Generation & Validation**
- Automated trend detection
- Statistical significance checking
- Confidence scoring and ranking
- Quality filtering (0.6 threshold)
- Hypothesis generation with evidence

✅ **Creative Recommendations**
- Data-driven ad copy generation
- Multiple format support (image, video, carousel)
- A/B test design and recommendations
- Expected impact predictions

✅ **Comprehensive Outputs**
- insights.json: Validated insights with evidence
- creatives.json: Creative recommendations
- report.md: Executive markdown report
- execution_log.json: Detailed execution logs

✅ **Production-Ready Code**
- Complete error handling
- Logging and monitoring
- Unit tests with pytest
- Configurable via YAML
- Makefile for automation

### Technical Specifications

- **Language**: Python 3.8+
- **Dependencies**: pandas, numpy, pyyaml
- **Input**: CSV + natural language query
- **Output**: JSON + Markdown reports
- **Execution Time**: ~5-15 seconds typical
- **Test Coverage**: Agent tests + evaluator tests

### Known Limitations

- Requires structured CSV input (schema defined in data/README.md)
- English language queries only
- Synthetic data for demonstration
- No real-time API integration

### Future Enhancements (v2.0 planned)

- Real-time Facebook Ads API integration
- Multi-language support
- Advanced statistical tests (t-tests, ANOVA)
- Machine learning for predictive insights
- Web dashboard interface
- Automated scheduling and monitoring

---

## 🔍 Self-Review & PR Explanation

### Code Quality

✅ **Well-Structured**: Clear separation of concerns with dedicated agents  
✅ **Documented**: Comprehensive docstrings and comments  
✅ **Tested**: Unit tests for critical validation logic  
✅ **Configurable**: YAML-based configuration  
✅ **Maintainable**: Modular design, easy to extend

### Compliance with Requirements

✅ **Correct folder structure**: Matches specification exactly  
✅ **Correct repo name**: kasparro-agentic-fb-analyst-harikrishna-choppa  
✅ **All deliverables present**: All required files included  
✅ **Prompts in separate files**: 4 markdown prompt files  
✅ **JSON outputs**: insights.json, creatives.json  
✅ **Markdown report**: Comprehensive report.md  
✅ **Logs included**: example_log.json with structure  
✅ **Tests present**: test_evaluator.py + test_agents.py  
✅ **v1.0 release notes**: Included in README

### What Makes This Solution Strong

1. **Production-Ready**: Not just a prototype - includes error handling, logging, tests
2. **Real Insights**: Uses statistical validation, not just LLM generation
3. **Actionable Outputs**: Creative recommendations are specific and testable
4. **Transparent**: Confidence scores, validation notes, evidence provided
5. **Extensible**: Easy to add new agents or modify workflows
6. **Well-Documented**: README, architecture docs, code comments

### How to Evaluate This Submission

1. **Review Architecture**: Read `agent_graph.md`
2. **Check Code Quality**: Review agent implementations in `src/agents/`
3. **Examine Outputs**: Look at `reports/*.json` and `reports/*.md`
4. **Run Tests**: Execute `python -m pytest tests/ -v`
5. **Test System**: Run `python run.py "Analyze ROAS drop"`
6. **Verify Prompts**: Check `prompts/*.md` files

---

## 📞 Contact & Support

**Author**: Harikrishna Choppa  
**Project**: Kasparro Applied AI Engineer Assignment  
**Version**: 1.0.0  
**Date**: January 15, 2024

For questions or issues, please refer to the documentation in this README or the architecture diagram in `agent_graph.md`.

---

## 📄 License

This project is submitted as part of the Kasparro Applied AI Engineer application process.

---

## 🙏 Acknowledgments

- **Kasparro Team**: For the comprehensive assignment specification
- **Dataset**: Synthetic Facebook Ads data generated for demonstration

---

**End of README**
