# Data Directory

This directory contains the Facebook Ads performance data used for analysis.

## Dataset: synthetic_fb_ads_undergarments.csv

### Description
Synthetic Facebook Ads performance data for an undergarments e-commerce brand. Contains campaign metrics including spend, revenue, impressions, clicks, and conversions.

### Schema

| Column | Type | Description |
|--------|------|-------------|
| Date | datetime | Date of ad performance |
| Campaign_Name | string | Name of the advertising campaign |
| Creative_Type | string | Type of creative (image, video, carousel) |
| Audience_Segment | string | Target audience segment |
| Device_Type | string | Device type (mobile, desktop, tablet) |
| Placement | string | Ad placement (feed, stories, etc.) |
| Impressions | integer | Number of times ad was shown |
| Clicks | integer | Number of clicks on ad |
| Spend | float | Amount spent in USD |
| Revenue | float | Revenue generated in USD |
| Conversions | integer | Number of conversions |

### Derived Metrics
The following metrics are calculated by the Data Agent:

- **ROAS** = Revenue / Spend
- **CTR** = (Clicks / Impressions) × 100
- **CPC** = Spend / Clicks
- **CPM** = (Spend / Impressions) × 1000
- **Conversion_Rate** = (Conversions / Clicks) × 100

### Usage

```python
import pandas as pd

# Load the data
df = pd.read_csv('data/synthetic_fb_ads_undergarments.csv')

# View summary
print(df.describe())
print(df.info())
```

### Data Quality

- **Completeness**: All required fields present
- **Date Range**: Varies based on synthetic generation
- **Granularity**: Daily-level data
- **Segments**: Multiple campaigns, creatives, audiences

### Notes

- This is synthetic data for demonstration purposes
- Data patterns reflect realistic Facebook Ads scenarios
- Used for testing and evaluation of the agentic system
