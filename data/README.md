# Data Directory

This directory contains the Facebook Ads performance dataset used by the Kasparro Agentic FB Analyst system.

## Dataset: synthetic_fb_ads_undergarments.csv

### Purpose

Synthetic dataset representing Facebook Ads performance for an e-commerce undergarments brand. Used for demonstration, testing, and validation of the multi-agent analytics system.

### Data Schema

| Column | Type | Description |
|--------|------|-------------|
| date | datetime | Date of ad performance record |
| campaign_name | string | Name of advertising campaign |
| creative_type | string | Type of creative (image, video, carousel) |
| audience_segment | string | Target audience segment |
| device_type | string | Device viewing ad (mobile, desktop, tablet) |
| placement | string | Ad placement location (feed, stories, sidebar) |
| impressions | integer | Number of times ad was shown |
| clicks | integer | Number of clicks on ad |
| spend | float | Amount spent in USD |
| revenue | float | Revenue generated in USD |
| conversions | integer | Number of conversions |

### Calculated Metrics

The Data Agent automatically derives these metrics:

- **ROAS** (Return on Ad Spend) = Revenue / Spend
- **CTR** (Click-Through Rate) = (Clicks / Impressions) × 100
- **CPC** (Cost Per Click) = Spend / Clicks
- **CPM** (Cost Per Thousand Impressions) = (Spend / Impressions) × 1000
- **Conversion_Rate** = (Conversions / Clicks) × 100

### Dataset Characteristics

| Property | Value |
|----------|-------|
| Date Range | 90 days of synthetic data |
| Granularity | Daily performance records |
| Total Records | ~1,250 rows |
| Active Campaigns | 5 campaigns |
| Creative Variants | 12 variants |
| Audience Segments | 4 main segments |
| Device Types | Mobile, Desktop, Tablet |
| Ad Placements | Feed, Stories, Sidebar |

### Data Quality Attributes

✅ **Completeness:** No missing values
✅ **Validity:** All metrics within realistic ranges
✅ **Consistency:** Temporal data consistent across records
✅ **Accuracy:** Realistic Facebook Ads performance patterns
✅ **Reliability:** Suitable for analysis and testing

### Metric Ranges

**Performance Metrics:**
- ROAS: 2.5 - 4.0
- CTR: 1.5% - 2.5%
- CPC: $0.75 - $1.25
- CPM: $10 - $15
- Conversion Rate: 2.5% - 3.5%

**Volume Metrics (daily):**
- Impressions: 5,000 - 25,000
- Clicks: 100 - 500
- Conversions: 3 - 20
- Spend: $400 - $800

### Campaign Structure

**Campaign 1: Brand Awareness**
- Focus: Reach and impressions
- CTR: 1.7% - 2.0%
- ROAS: 2.8 - 3.2

**Campaign 2: Engagement**
- Focus: Engagement and clicks
- CTR: 2.1% - 2.4%
- ROAS: 3.0 - 3.5

**Campaign 3: Conversion**
- Focus: Conversions and ROI
- CTR: 1.9% - 2.2%
- ROAS: 3.2 - 3.8

**Campaign 4: Retargeting**
- Focus: Existing customers
- CTR: 2.3% - 2.7%
- ROAS: 3.5 - 4.0

**Campaign 5: Testing**
- Focus: Testing new audiences
- CTR: 1.5% - 1.9%
- ROAS: 2.5 - 3.0

### Usage in System

The Data Agent automatically handles this file:

```python
# Data Agent loads and processes
df = pd.read_csv('data/synthetic_fb_ads_undergarments.csv')

# Calculates metrics
roas = df['Revenue'] / df['Spend']
ctr = (df['Clicks'] / df['Impressions']) * 100

# Filters by time windows
baseline = df[df['date'] > (latest_date - 30 days)]
comparison = df[df['date'] > (latest_date - 7 days)]

# Aggregates by segments
segment_performance = df.groupby('campaign_name')[metrics].mean()
```

### Example Data Row

```json
{
  "date": "2025-01-29",
  "campaign_name": "Engagement Campaign",
  "creative_type": "image",
  "audience_segment": "Existing Customers",
  "device_type": "mobile",
  "placement": "feed",
  "impressions": 15000,
  "clicks": 315,
  "spend": 450.00,
  "revenue": 1350.00,
  "conversions": 9
}
```

### Analysis Capabilities

**Time-Series Analysis:**
- Daily trend analysis
- Week-over-week comparison
- Baseline vs. comparison period analysis
- Seasonal pattern detection

**Segment Analysis:**
- Campaign performance comparison
- Creative type effectiveness
- Audience segment performance
- Device type optimization
- Placement performance

**Metric Correlation:**
- CTR vs. CPC relationship
- Frequency vs. CTR fatigue
- Spend vs. revenue correlation

### Integration Points

**Planner Agent:**
Uses data schema to validate requested metrics and segments

**Data Agent:**
Loads, validates, and processes this CSV file

**Insight Agent:**
Analyzes processed data to generate insights

**Evaluator Agent:**
Uses raw data to validate insight claims

**Creative Agent:**
Considers data patterns when recommending creatives

### Testing Data

The system is configured to use this synthetic data for:
- Unit testing (pytest)
- Integration testing
- System validation
- Example output generation
- Demo queries

### Configuration

**Data Path:** Set in `config/config.yaml`
```yaml
data_path: 'data/synthetic_fb_ads_undergarments.csv'
use_sample_data: true
random_seed: 42
```

### Reproducibility

- **Randomness Control:** Random seed set to 42 in config
- **Data Stability:** Synthetic data unchanging
- **Deterministic Processing:** All calculations produce same results
- **Consistent Results:** Same query produces identical analysis

### Future Enhancements

- Integration with real Facebook Ads API
- Real-time data streaming support
- Multi-account support
- Historical data archiving
- Custom dataset uploads

### Notes

- This is synthetic data created for demonstration and testing purposes
- Patterns reflect realistic Facebook Ads scenarios
- Safe for testing, experimentation, and learning
- No real business data included
- Suitable for validating the analytics system

---

*Data Directory for Kasparro Agentic FB Analyst v1.0*
