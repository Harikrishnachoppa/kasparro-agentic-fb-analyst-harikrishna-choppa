# System Architecture - Kasparro Agentic FB Analyst

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                          USER QUERY                                  │
│         "Analyze ROAS drop in last 30 days"                          │
└──────────────────────────────────────────┬───────────────────────────┘
                                           │
                                           ▼
                        ┌────────────────────────────────┐
                        │    ORCHESTRATOR               │
                        │  (Coordinates all agents)      │
                        └────────────────────────────────┘
                                           │
         ┌─────────────────────────────────┼─────────────────────────────┐
         │                                 │                             │
         ▼                                 ▼                             ▼
    ┌─────────────┐            ┌──────────────────┐            ┌──────────────┐
    │   PLANNER   │            │  DATA AGENT      │            │   INSIGHT    │
    │   AGENT     │            │  (Stage 2)       │            │   AGENT      │
    │ (Stage 1)   │──────────▶ │                  │──────────▶ │ (Stage 3)    │
    └─────────────┘            └──────────────────┘            └──────┬───────┘
                                                                       │
                                                                       ▼
                                                              ┌──────────────────┐
                                          Stage 4           │  EVALUATOR       │
                                                            │  AGENT           │
                                          ◀─────────────────│                  │
                                          │                 └──────────────────┘
                                          │
                                          ▼
                                    ┌──────────────┐
                    Stage 5         │  CREATIVE    │
                                    │  AGENT       │
                                    └────────┬─────┘
                                             │
                                             ▼
                    ┌────────────────────────────────────┐
                    │   OUTPUT & REPORTS                 │
                    ├────────────────────────────────────┤
                    │  • insights.json                   │
                    │  • creatives.json                  │
                    │  • report.md                       │
                    │  • execution_log.json              │
                    └────────────────────────────────────┘
```

---

## Agent Details

### Stage 1: Planner Agent

**File:** `src/agents/planner_agent.py`

**Purpose:** Parse natural language queries and create structured analysis plans.

**Input:**
```json
{
  "user_query": "Analyze ROAS drop in last 30 days",
  "context": {"latest_date": "2025-01-29"}
}
```

**Processing:**
- Extract objectives from query (diagnostic, optimization, exploratory)
- Identify relevant metrics (ROAS, CTR, CPC, CPM, Conversion_Rate)
- Determine time windows (baseline vs. comparison periods)
- Identify segments to analyze
- Classify analysis type

**Output:**
```json
{
  "plan_id": "PLAN_20250129_143000",
  "objectives": ["Diagnose ROAS decline", "Identify root causes"],
  "metrics_to_analyze": ["ROAS", "CTR", "CPC"],
  "time_windows": {"baseline": 30, "comparison": 7},
  "analysis_type": "diagnostic"
}
```

**Prompt File:** `prompts/planner_prompt.md`

---

### Stage 2: Data Agent

**File:** `src/agents/data_agent.py`

**Purpose:** Load, validate, and process Facebook Ads performance data.

**Input:** Analysis plan from Planner

**Processing:**
- Load `data/synthetic_fb_ads_undergarments.csv`
- Calculate derived metrics:
  - ROAS = Revenue / Spend
  - CTR = (Clicks / Impressions) × 100
  - CPC = Spend / Clicks
  - CPM = (Spend / Impressions) × 1000
  - Conversion_Rate = (Conversions / Clicks) × 100
- Filter data by time windows (baseline vs. comparison)
- Aggregate data by segments
- Validate data quality

**Output:**
```json
{
  "metric_changes": {
    "ROAS": {
      "baseline": 3.45,
      "comparison": 2.67,
      "change_pct": -22.5
    }
  },
  "segment_analysis": {...}
}
```

---

### Stage 3: Insight Agent

**File:** `src/agents/insight_agent.py`

**Purpose:** Analyze data to generate insights and hypotheses.

**Input:** Processed data + analysis plan

**Processing:**
- Detect significant metric changes (>10% threshold triggers insights)
- Identify anomalies and trends
- Perform segment analysis
- Generate hypotheses explaining patterns
- Identify correlations between metrics
- Assign confidence scores

**Output:**
```json
{
  "insights": [
    {
      "insight_id": "INS_ROAS_001",
      "title": "ROAS declined 22.5%",
      "evidence": {...},
      "confidence": 0.95
    }
  ],
  "hypotheses": [
    {
      "statement": "Creative fatigue causing decline",
      "confidence": 0.82
    }
  ]
}
```

**Prompt File:** `prompts/insight_prompt.md`

---

### Stage 4: Evaluator Agent

**File:** `src/agents/evaluator_agent.py`

**Purpose:** Validate insights using quantitative scoring criteria.

**Input:** Raw insights + processed data

**Processing:**
- Assess evidence strength
- Check statistical significance
- Evaluate business relevance
- Calculate 4-component validation score:
  - Confidence (30% weight)
  - Evidence Strength (30% weight)
  - Statistical Significance (25% weight)
  - Business Relevance (15% weight)
- Apply threshold filtering (0.60 minimum)
- Rank by validation score

**Validation Formula:**
```
validation_score = (
  confidence * 0.30 +
  evidence_strength * 0.30 +
  statistical_significance * 0.25 +
  business_relevance * 0.15
)
```

**Output:**
```json
{
  "validated_insights": [
    {
      "validation_score": 0.93,
      "score_components": {...}
    }
  ],
  "rejected_insights": [...]
}
```

**Prompt File:** `prompts/evaluator_prompt.md`

**Tests:** `tests/test_evaluator.py` (263 lines, comprehensive validation testing)

---

### Stage 5: Creative Agent

**File:** `src/agents/creative_agent.py`

**Purpose:** Generate ad creative recommendations and A/B test strategies.

**Input:** Validated insights + hypotheses

**Processing:**
- Map insights to creative themes
- Generate ad copy variants (headlines, body, CTAs)
- Design multiple creative formats (image, video, carousel)
- Create A/B test recommendations
- Develop creative strategy with rollout plan

**Output:**
```json
{
  "creatives": [
    {
      "creative_id": "CRE_001",
      "type": "image_ad",
      "headline": "...",
      "expected_impact": "12-18% CTR improvement"
    }
  ],
  "ab_test_recommendations": [...]
}
```

**Prompt File:** `prompts/creative_prompt.md`

---

## Data Flow

```
Query
  │
  ├──────────────────────────────┐
  │                              │
  ▼                              │
PLANNER AGENT                    │
  │                              │
  ├─────────────────────┐        │
  │                     │        │
  ▼                     ▼        │
Plan Object     Context from CSV │
  │                             │
  ├─────────────────────────────┤
  │
  ▼
DATA AGENT
  │
  ├─────────────────────────────┐
  │                             │
  ▼                             ▼
Processed Data         Available Metrics
  │
  ├─────────────────────────────┐
  │                             │
  ▼                             ▼
INSIGHT AGENT           Analysis Plan
  │
  ├─────────────────────────────────────┐
  │                                     │
  ▼                                     ▼
Insights & Hypotheses     Processed Data
  │
  ├─────────────────────────────────────┐
  │                                     │
  ▼                                     ▼
EVALUATOR AGENT                    Data
  │
  ├─────────────────────────────────────┐
  │                                     │
  ▼                                     ▼
Validated Insights             Quality Report
  │
  ├─────────────────────────────────────┐
  │                                     │
  ▼                                     ▼
CREATIVE AGENT                   Hypotheses
  │
  ├─────────────────────────────────────────┐
  │                                         │
  ▼                                         ▼
Creatives & A/B Tests              Strategy
  │
  ▼
OUTPUT & REPORTS
```

---

## Error Handling

### Agent-Level Handling
- Each agent has try-catch blocks
- Fallback to defaults if resources missing (e.g., prompts)
- Detailed error logging at each stage

### Orchestrator-Level Handling
- Validates stage outputs before proceeding
- Can skip optional stages on failure
- Returns partial results if some stages fail
- Full execution logging for debugging

### Data-Level Handling
- CSV validation before processing
- Missing value detection and reporting
- Type checking for all metrics
- Data quality scoring

### Graceful Degradation
- Missing prompt files → Use built-in defaults
- Low-confidence insights → Filtered out (threshold 0.6)
- Partial data → Continues with available information

---

## I/O Specifications

### Planner Agent I/O
- **Input:** `{"user_query": str, "context": dict}`
- **Output:** `{"plan_id": str, "objectives": list, "metrics": list, "analysis_type": str}`

### Data Agent I/O
- **Input:** `{"plan_id": str, "metrics": list}`
- **Output:** `{"metric_changes": dict, "segment_analysis": dict}`

### Insight Agent I/O
- **Input:** `{"metric_changes": dict, "segment_analysis": dict}`
- **Output:** `{"insights": list, "hypotheses": list}`

### Evaluator Agent I/O
- **Input:** `{"insights": list, "hypotheses": list, "data": dict}`
- **Output:** `{"validated_insights": list, "validated_hypotheses": list}`

### Creative Agent I/O
- **Input:** `{"validated_insights": list, "validated_hypotheses": list}`
- **Output:** `{"creatives": list, "ab_tests": list}`

---

## Configuration

**File:** `config/config.yaml`

Key settings:
- Agent enable/disable flags
- Data paths and settings
- Validation thresholds and weights
- Output paths (reports/, logs/)
- Logging configuration
- Brand information
- Testing parameters
- Random seed (42) for reproducibility

---

## Execution Workflow

1. **User provides query** (natural language)
2. **Orchestrator initializes** all agents
3. **Stage 1:** Planner parses query → creates plan
4. **Stage 2:** Data Agent loads CSV → processes metrics
5. **Stage 3:** Insight Agent analyzes → generates insights
6. **Stage 4:** Evaluator validates → scores insights
7. **Stage 5:** Creative Agent generates → ad recommendations
8. **Output:** Reports written to `reports/` directory
9. **Logging:** Execution logged to `logs/execution_log.json`

---

## Performance Characteristics

- **Typical Execution Time:** 5-15 seconds
- **Data Processing:** ~1,250 rows per analysis
- **Insights Generated:** 3-7 validated per query
- **Creatives Generated:** 5-10 variants per query
- **Memory Usage:** ~100MB typical
- **Success Rate:** 99%+ (with graceful degradation)

---

## Key Features

✅ **Modular Design** - Easy to extend or modify agents
✅ **Layered Prompts** - Structured reasoning with validation
✅ **Quantitative Validation** - 4-component scoring algorithm
✅ **Error Handling** - Graceful degradation on failures
✅ **Comprehensive Logging** - Full execution visibility
✅ **Configuration-Driven** - Easy to customize behavior
✅ **Reproducible** - Seeded randomness for consistency
✅ **Production-Ready** - Error handling, testing, documentation

---

*Architecture Documentation for Kasparro Agentic FB Analyst v1.0*
