# Facebook Ads Analyzer

A Python-based multi-agent system for analyzing Facebook Ads performance and generating actionable insights and recommendations.

## Overview

This project implements a 5-agent architecture that processes Facebook Ads data to:
- Analyze ad performance metrics (ROAS, CTR, CPC, CPM, conversion rates)
- Generate insights from data trends and anomalies
- Validate insights with statistical and business logic
- Recommend creative improvements and A/B test strategies

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Running the System

```bash
python run.py "Why is my ROAS declining?"
```

Example queries:
```bash
python run.py "Analyze CTR trends over the last 30 days"
python run.py "What's causing high CPC?"
python run.py "Generate creative recommendations for engagement"
```

## Architecture

The system uses 5 coordinated agents:

1. **Planner Agent** - Parses user queries and creates analysis plans
2. **Data Agent** - Loads CSV data and calculates metrics
3. **Insight Agent** - Analyzes trends and generates hypotheses
4. **Evaluator Agent** - Validates insights with statistical scoring
5. **Creative Agent** - Generates ad copy and A/B test recommendations

The orchestrator coordinates execution and handles data flow between agents.

## Directory Structure

```
├── src/
│   ├── agents/              # Agent implementations
│   ├── orchestrator/        # Orchestration logic
│   └── utils/              # Helper functions
├── config/
│   └── config.yaml         # Configuration settings
├── data/
│   └── synthetic_fb_ads_undergarments.csv
├── tests/                  # Unit tests
├── run.py                  # Entry point
└── Makefile               # Build commands
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Output

The system generates:
- `reports/insights.json` - Validated insights with confidence scores
- `reports/creatives.json` - Creative recommendations
- `reports/report.md` - Markdown report
- `logs/execution_log.json` - Execution details

## Configuration

Edit `config/config.yaml` to customize thresholds, validation weights, and other settings.

## Requirements

- Python 3.8+
- pandas >= 2.0.0
- numpy >= 1.24.0
- pyyaml >= 6.0
- pytest (for testing)
