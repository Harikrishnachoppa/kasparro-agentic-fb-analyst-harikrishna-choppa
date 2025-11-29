# Agent Graph Architecture

## ASCII Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INPUT / QUERY                          │
│                   "Analyze ROAS drop in last 30 days"              │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       ORCHESTRATOR                                  │
│  • Coordinates agent workflow                                       │
│  • Manages state and context                                        │
│  • Handles error recovery                                           │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
                   ┌─────────────────┐
                   │ PLANNER AGENT   │
                   │                 │
                   │ • Parse query   │
                   │ • Define goals  │
                   │ • Create plan   │
                   └────────┬────────┘
                            │
                            │ (analysis_plan)
                            ▼
                   ┌─────────────────┐
                   │  DATA AGENT     │
                   │                 │
                   │ • Load CSV      │
                   │ • Filter data   │
                   │ • Compute stats │
                   └────────┬────────┘
                            │
                            │ (processed_data)
                            ▼
                   ┌─────────────────┐
                   │ INSIGHT AGENT   │
                   │                 │
                   │ • Analyze trends│
                   │ • Generate hyp. │
                   │ • Find patterns │
                   └────────┬────────┘
                            │
                            │ (hypotheses)
                            ▼
                   ┌─────────────────┐
                   │ EVALUATOR AGENT │
                   │                 │
                   │ • Score hypoths.│
                   │ • Validate      │
                   │ • Rank insights │
                   └────────┬────────┘
                            │
                            │ (validated_insights)
                            ▼
                   ┌─────────────────┐
                   │ CREATIVE AGENT  │
                   │                 │
                   │ • Generate ads  │
                   │ • Create CTAs   │
                   │ • Test variants │
                   └────────┬────────┘
                            │
                            │ (creative_output)
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        FINAL OUTPUT                                 │
│  • insights.json                                                    │
│  • creatives.json                                                   │
│  • report.md                                                        │
│  • logs/execution_log.json                                          │
└─────────────────────────────────────────────────────────────────────┘
```

## Agent Descriptions

### 1. Planner Agent
**Purpose**: Decomposes user queries into structured analysis plans

**Responsibilities**:
- Parse natural language queries
- Identify analysis objectives (e.g., "find cause of ROAS drop")
- Define metrics to analyze (ROAS, CTR, CPC, conversion rate)
- Specify time windows and segments
- Create structured plan for downstream agents

**Input Schema**:
```json
{
  "user_query": "string",
  "context": {
    "available_metrics": ["list"],
    "date_range": "object"
  }
}
```

**Output Schema**:
```json
{
  "plan_id": "string",
  "objectives": ["string"],
  "metrics_to_analyze": ["string"],
  "time_windows": {
    "baseline": "date_range",
    "comparison": "date_range"
  },
  "segments": ["string"],
  "priority_questions": ["string"]
}
```

**Key Capabilities**:
- Query intent recognition
- Metric selection based on objectives
- Time period segmentation
- Prioritization of analysis paths

---

### 2. Data Agent
**Purpose**: Retrieves, processes, and prepares data for analysis

**Responsibilities**:
- Load CSV data from file system
- Apply filters based on plan specifications
- Compute aggregated metrics (ROAS, CTR, CPC, etc.)
- Handle missing data and outliers
- Generate summary statistics

**Input Schema**:
```json
{
  "plan": "object",
  "data_source": "string",
  "filters": {
    "date_range": "object",
    "segments": ["string"]
  }
}
```

**Output Schema**:
```json
{
  "raw_data": "dataframe",
  "aggregated_metrics": {
    "metric_name": {
      "baseline": "float",
      "comparison": "float",
      "change_pct": "float"
    }
  },
  "summary_stats": "object",
  "data_quality_report": "object"
}
```

**Key Capabilities**:
- CSV parsing and validation
- Time-series aggregation
- Segment-based filtering
- Metric calculation (ROAS = Revenue / Spend, CTR = Clicks / Impressions)
- Data quality checks

---

### 3. Insight Agent
**Purpose**: Analyzes processed data to generate hypotheses and insights

**Responsibilities**:
- Identify trends and anomalies
- Generate hypotheses for performance changes
- Detect correlations between metrics
- Segment analysis (by campaign, creative, audience)
- Pattern recognition across dimensions

**Input Schema**:
```json
{
  "processed_data": "object",
  "plan": "object",
  "context": "object"
}
```

**Output Schema**:
```json
{
  "insights": [
    {
      "insight_id": "string",
      "type": "string",
      "title": "string",
      "description": "string",
      "evidence": {
        "metrics": "object",
        "data_points": "array"
      },
      "confidence": "float",
      "impact": "string"
    }
  ],
  "hypotheses": [
    {
      "hypothesis_id": "string",
      "statement": "string",
      "supporting_evidence": ["string"],
      "confidence": "float"
    }
  ]
}
```

**Key Capabilities**:
- Statistical analysis
- Trend detection
- Correlation analysis
- Anomaly detection
- Natural language insight generation

---

### 4. Evaluator Agent
**Purpose**: Validates, scores, and ranks insights and hypotheses

**Responsibilities**:
- Score hypotheses based on evidence strength
- Validate statistical significance
- Rank insights by impact and confidence
- Cross-check consistency
- Filter low-quality insights

**Input Schema**:
```json
{
  "insights": "array",
  "hypotheses": "array",
  "data": "object"
}
```

**Output Schema**:
```json
{
  "validated_insights": [
    {
      "insight_id": "string",
      "validation_score": "float",
      "confidence_adjusted": "float",
      "statistical_significance": "boolean",
      "ranking": "int",
      "validation_notes": "string"
    }
  ],
  "rejected_insights": ["object"],
  "quality_report": "object"
}
```

**Key Capabilities**:
- Statistical testing (t-tests, chi-square)
- Confidence scoring
- Evidence validation
- Ranking algorithms
- Quality assurance

---

### 5. Creative Generator Agent
**Purpose**: Generates actionable creative recommendations and ad content

**Responsibilities**:
- Create ad headlines based on insights
- Generate ad copy variants
- Produce CTAs aligned with objectives
- Suggest A/B test scenarios
- Output creative recommendations

**Input Schema**:
```json
{
  "validated_insights": "array",
  "brand_guidelines": "object",
  "objective": "string"
}
```

**Output Schema**:
```json
{
  "creatives": [
    {
      "creative_id": "string",
      "type": "string",
      "headline": "string",
      "body_text": "string",
      "cta": "string",
      "rationale": "string",
      "target_audience": "string",
      "expected_impact": "string"
    }
  ],
  "ab_test_recommendations": "array",
  "creative_strategy": "string"
}
```

**Key Capabilities**:
- Natural language generation
- Marketing copy creation
- A/B test design
- Audience targeting recommendations
- Brand-aligned content generation

---

## Data Flow Description

### Stage 1: Query Processing
1. User submits query → Orchestrator
2. Orchestrator → Planner Agent
3. Planner generates structured plan with objectives and metrics

### Stage 2: Data Retrieval
4. Plan → Data Agent
5. Data Agent loads CSV, filters by date/segment
6. Computes baseline vs comparison metrics
7. Returns processed data + summary stats

### Stage 3: Insight Generation
8. Processed data + plan → Insight Agent
9. Insight Agent analyzes trends, correlations, anomalies
10. Generates hypotheses with evidence
11. Returns insights + hypotheses

### Stage 4: Validation
12. Insights + data → Evaluator Agent
13. Evaluator scores, validates, ranks insights
14. Filters low-confidence hypotheses
15. Returns validated insights with rankings

### Stage 5: Creative Generation
16. Validated insights → Creative Generator
17. Creative Agent generates ad content
18. Creates headlines, copy, CTAs
19. Returns creative recommendations

### Stage 6: Output Assembly
20. Orchestrator collects all outputs
21. Generates insights.json
22. Generates creatives.json
23. Generates report.md
24. Writes execution logs

---

## Inter-Agent Communication

### Message Format
All agents communicate via standardized JSON messages:

```json
{
  "agent_id": "string",
  "timestamp": "ISO8601",
  "message_type": "request|response|error",
  "payload": "object",
  "metadata": {
    "execution_time": "float",
    "status": "string"
  }
}
```

### State Management
- Orchestrator maintains global state
- Each agent receives context from previous agents
- Agents are stateless (no internal state persistence)
- All intermediate results logged for debugging

---

## Error Handling & Recovery

- **Data Agent fails**: Return cached data or prompt for manual upload
- **Insight Agent fails**: Fallback to basic statistical summary
- **Evaluator Agent fails**: Skip validation, use raw insights
- **Creative Agent fails**: Return template-based recommendations
- All errors logged to `logs/execution_log.json`

---

## Scalability & Extensibility

### Adding New Agents
1. Create new agent file in `src/agents/`
2. Implement standard interface (input/output schemas)
3. Add agent to orchestrator workflow
4. Update agent_graph.md

### Modifying Workflows
- Orchestrator uses configurable workflow definitions
- Agent execution order defined in `config/config.yaml`
- Parallel execution supported for independent agents

---

## Version
**v1.0** - Initial release with 5-agent architecture
