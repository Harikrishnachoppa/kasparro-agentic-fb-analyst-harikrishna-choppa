"""
Data Agent - Retrieves, processes, and prepares data for analysis
Column mapping: CSV uses lowercase (date, spend, impressions, clicks, purchases, revenue, roas, ctr)
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any
import os


class DataAgent:
    """
    Responsible for loading, filtering, and computing metrics from Facebook Ads data.
    Works with CSV columns: date, spend, impressions, clicks, purchases, revenue, roas, ctr
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_path = config.get('data_path', 'data/synthetic_fb_ads_undergarments.csv')
        self.df = None
    
    def execute(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method for the Data Agent
        
        Args:
            plan: Analysis plan from Planner Agent
        
        Returns:
            Processed data with aggregated metrics
        """
        print(f"\n[DATA AGENT] Loading data from {self.data_path}")
        
        # Load data
        self.df = self._load_data()
        
        if self.df is None:
            return self._create_error_response("Failed to load data")
        
        print(f"[DATA AGENT] Loaded {len(self.df)} rows")
        
        # Ensure date column is datetime
        self.df['date'] = pd.to_datetime(self.df['date'])
        
        # Calculate derived metrics
        self._calculate_metrics()
        
        # Filter by time windows
        baseline_data = self._filter_by_date_range(
            plan['time_windows']['baseline']['start_date'],
            plan['time_windows']['baseline']['end_date']
        )
        
        comparison_data = self._filter_by_date_range(
            plan['time_windows']['comparison']['start_date'],
            plan['time_windows']['comparison']['end_date']
        )
        
        print(f"[DATA AGENT] Baseline period: {len(baseline_data)} rows")
        print(f"[DATA AGENT] Comparison period: {len(comparison_data)} rows")
        
        # Compute aggregated metrics
        baseline_metrics = self._compute_aggregate_metrics(baseline_data)
        comparison_metrics = self._compute_aggregate_metrics(comparison_data)
        
        # Calculate changes
        metric_changes = self._calculate_metric_changes(baseline_metrics, comparison_metrics)
        
        # Segment analysis
        segment_analysis = self._analyze_segments(
            baseline_data, 
            comparison_data, 
            plan.get('segments', [])
        )
        
        # Data quality report
        quality_report = self._generate_quality_report()
        
        result = {
            "data_summary": {
                "total_rows": len(self.df),
                "baseline_rows": len(baseline_data),
                "comparison_rows": len(comparison_data),
                "date_range": {
                    "min": self.df['date'].min().strftime('%Y-%m-%d'),
                    "max": self.df['date'].max().strftime('%Y-%m-%d')
                }
            },
            "baseline_metrics": baseline_metrics,
            "comparison_metrics": comparison_metrics,
            "metric_changes": metric_changes,
            "segment_analysis": segment_analysis,
            "data_quality_report": quality_report,
            "raw_data": {
                "baseline": baseline_data.to_dict('records'),
                "comparison": comparison_data.to_dict('records')
            }
        }
        
        print(f"[DATA AGENT] Processing complete")
        
        return result
    
    def _load_data(self) -> pd.DataFrame:
        """Load CSV data"""
        try:
            df = pd.read_csv(self.data_path)
            return df
        except FileNotFoundError:
            print(f"[DATA AGENT] ERROR: File not found at {self.data_path}")
            return None
        except Exception as e:
            print(f"[DATA AGENT] ERROR: {str(e)}")
            return None
    
    def _calculate_metrics(self):
        """Calculate derived metrics"""
        # Already have roas, ctr, purchases, revenue from CSV
        # Map column names to match CSV
        if 'spend' in self.df.columns:
            # CTR already in CSV but let's ensure it's calculated correctly
            self.df['ctr_calc'] = np.where(
                self.df['impressions'] > 0,
                (self.df['clicks'] / self.df['impressions']) * 100,
                0
            )
            
            # CPC = Spend / Clicks
            self.df['cpc'] = np.where(
                self.df['clicks'] > 0,
                self.df['spend'] / self.df['clicks'],
                0
            )
            
            # CPM = (Spend / Impressions) * 1000
            self.df['cpm'] = np.where(
                self.df['impressions'] > 0,
                (self.df['spend'] / self.df['impressions']) * 1000,
                0
            )
            
            # Conversion Rate = Purchases / Clicks
            self.df['conversion_rate'] = np.where(
                self.df['clicks'] > 0,
                (self.df['purchases'] / self.df['clicks']) * 100,
                0
            )
    
    def _filter_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Filter dataframe by date range"""
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        return self.df[(self.df['date'] >= start) & (self.df['date'] <= end)].copy()
    
    def _compute_aggregate_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """Compute aggregated metrics for a dataframe - using lowercase CSV column names"""
        if len(df) == 0:
            return {}
        
        total_spend = df['spend'].sum()
        total_revenue = df['revenue'].sum()
        total_impressions = df['impressions'].sum()
        total_clicks = df['clicks'].sum()
        total_purchases = df['purchases'].sum()
        
        return {
            "spend": round(total_spend, 2),
            "revenue": round(total_revenue, 2),
            "impressions": int(total_impressions),
            "clicks": int(total_clicks),
            "purchases": int(total_purchases),
            "roas": round(total_revenue / total_spend, 2) if total_spend > 0 else 0,
            "ctr": round((total_clicks / total_impressions) * 100, 2) if total_impressions > 0 else 0,
            "cpc": round(total_spend / total_clicks, 2) if total_clicks > 0 else 0,
            "cpm": round((total_spend / total_impressions) * 1000, 2) if total_impressions > 0 else 0,
            "conversion_rate": round((total_purchases / total_clicks) * 100, 2) if total_clicks > 0 else 0
        }
    
    def _calculate_metric_changes(self, baseline: Dict, comparison: Dict) -> Dict[str, Any]:
        """Calculate percentage changes between baseline and comparison"""
        changes = {}
        
        for metric in baseline.keys():
            if metric in comparison:
                baseline_val = baseline[metric]
                comparison_val = comparison[metric]
                
                if baseline_val != 0:
                    pct_change = ((comparison_val - baseline_val) / baseline_val) * 100
                else:
                    pct_change = 0
                
                changes[metric] = {
                    "baseline": baseline_val,
                    "comparison": comparison_val,
                    "absolute_change": round(comparison_val - baseline_val, 2),
                    "percent_change": round(pct_change, 2),
                    "direction": "up" if pct_change > 0 else "down" if pct_change < 0 else "flat"
                }
        
        return changes
    
    def _analyze_segments(self, baseline_df: pd.DataFrame, comparison_df: pd.DataFrame, 
                         segments: List[str]) -> Dict[str, Any]:
        """Analyze performance by segments"""
        segment_analysis = {}
        
        for segment in segments:
            if segment not in baseline_df.columns:
                continue
            
            # Top performers in comparison period
            segment_metrics = comparison_df.groupby(segment).agg({
                'spend': 'sum',
                'revenue': 'sum',
                'clicks': 'sum',
                'purchases': 'sum'
            }).reset_index()
            
            segment_metrics['roas'] = np.where(
                segment_metrics['spend'] > 0,
                segment_metrics['revenue'] / segment_metrics['spend'],
                0
            )
            
            segment_metrics = segment_metrics.sort_values('roas', ascending=False)
            
            segment_analysis[segment] = {
                "top_performers": segment_metrics.head(3).to_dict('records'),
                "bottom_performers": segment_metrics.tail(3).to_dict('records')
            }
        
        return segment_analysis
    
    def _generate_quality_report(self) -> Dict[str, Any]:
        """Generate data quality report"""
        return {
            "missing_values": self.df.isnull().sum().to_dict(),
            "zero_spend_rows": int((self.df['spend'] == 0).sum()),
            "zero_impressions_rows": int((self.df['impressions'] == 0).sum()),
            "negative_values": {
                col: int((self.df[col] < 0).sum()) 
                for col in ['spend', 'revenue', 'clicks', 'impressions', 'purchases']
                if col in self.df.columns
            }
        }
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create error response"""
        return {
            "error": True,
            "message": error_message,
            "data_summary": {},
            "baseline_metrics": {},
            "comparison_metrics": {},
            "metric_changes": {},
            "segment_analysis": {},
            "data_quality_report": {}
        }


if __name__ == "__main__":
    # Test the data agent
    config = {'data_path': 'data/synthetic_fb_ads_undergarments.csv'}
    data_agent = DataAgent(config)
    
    # Mock plan
    from datetime import timedelta
    end = datetime.now()
    start_comp = end - timedelta(days=30)
    start_base = start_comp - timedelta(days=30)
    
    plan = {
        "time_windows": {
            "baseline": {
                "start_date": start_base.strftime('%Y-%m-%d'),
                "end_date": start_comp.strftime('%Y-%m-%d')
            },
            "comparison": {
                "start_date": start_comp.strftime('%Y-%m-%d'),
                "end_date": end.strftime('%Y-%m-%d')
            }
        },
        "segments": ['campaign_name', 'creative_type']
    }
    
    result = data_agent.execute(plan)
    print("\n=== DATA AGENT OUTPUT (Summary) ===")
    print(f"Baseline ROAS: {result['baseline_metrics'].get('roas', 0)}")
    print(f"Comparison ROAS: {result['comparison_metrics'].get('roas', 0)}")
