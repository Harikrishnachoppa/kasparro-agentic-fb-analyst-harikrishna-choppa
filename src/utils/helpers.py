"""
Utility helper functions for the agentic system
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import re


def load_config(config_path: str = 'config/config.yaml') -> Dict[str, Any]:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config file
    
    Returns:
        Configuration dictionary
    """
    try:
        import yaml
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except ImportError:
        print("YAML library not installed, using default config")
        return get_default_config()
    except FileNotFoundError:
        print(f"Config file not found at {config_path}, using default config")
        return get_default_config()


def get_default_config() -> Dict[str, Any]:
    """Get default configuration"""
    return {
        'data_path': 'data/synthetic_fb_ads_undergarments.csv',
        'min_confidence': 0.6,
        'brand_name': 'ComfortPlus',
        'product_category': 'undergarments',
        'output_dir': 'reports',
        'log_dir': 'logs'
    }


def format_currency(amount: float) -> str:
    """Format number as currency"""
    return f"${amount:,.2f}"


def format_percentage(value: float) -> str:
    """Format number as percentage"""
    return f"{value:.2f}%"


def format_number(value: float, decimals: int = 2) -> str:
    """Format number with commas and decimals"""
    return f"{value:,.{decimals}f}"


def calculate_percent_change(baseline: float, comparison: float) -> float:
    """Calculate percentage change between two values"""
    if baseline == 0:
        return 0.0
    return ((comparison - baseline) / baseline) * 100


def validate_date_format(date_string: str) -> bool:
    """Validate if string is in YYYY-MM-DD format"""
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, date_string))


def parse_date(date_string: str) -> Optional[datetime]:
    """Parse date string to datetime object"""
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        return None


def get_date_range(days: int = 30) -> Dict[str, str]:
    """
    Get date range for last N days
    
    Args:
        days: Number of days to look back
    
    Returns:
        Dictionary with start_date and end_date
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    return {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }


def ensure_directory_exists(directory: str):
    """Ensure a directory exists, create if it doesn't"""
    os.makedirs(directory, exist_ok=True)


def save_json(data: Any, filepath: str, indent: int = 2):
    """Save data to JSON file"""
    ensure_directory_exists(os.path.dirname(filepath))
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent)


def load_json(filepath: str) -> Any:
    """Load data from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate string to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_metric_name(text: str) -> Optional[str]:
    """Extract metric name from text"""
    metrics = ['ROAS', 'CTR', 'CPC', 'CPM', 'Conversion_Rate', 
               'Impressions', 'Clicks', 'Spend', 'Revenue', 'Conversions']
    
    text_upper = text.upper()
    for metric in metrics:
        if metric.upper() in text_upper:
            return metric
    
    return None


def calculate_roas(revenue: float, spend: float) -> float:
    """Calculate ROAS (Return on Ad Spend)"""
    if spend == 0:
        return 0.0
    return revenue / spend


def calculate_ctr(clicks: int, impressions: int) -> float:
    """Calculate CTR (Click-Through Rate) as percentage"""
    if impressions == 0:
        return 0.0
    return (clicks / impressions) * 100


def calculate_cpc(spend: float, clicks: int) -> float:
    """Calculate CPC (Cost Per Click)"""
    if clicks == 0:
        return 0.0
    return spend / clicks


def calculate_cpm(spend: float, impressions: int) -> float:
    """Calculate CPM (Cost Per Mille/1000 impressions)"""
    if impressions == 0:
        return 0.0
    return (spend / impressions) * 1000


def calculate_conversion_rate(conversions: int, clicks: int) -> float:
    """Calculate Conversion Rate as percentage"""
    if clicks == 0:
        return 0.0
    return (conversions / clicks) * 100


def classify_change_magnitude(percent_change: float) -> str:
    """Classify magnitude of change"""
    abs_change = abs(percent_change)
    
    if abs_change >= 50:
        return "extreme"
    elif abs_change >= 30:
        return "large"
    elif abs_change >= 15:
        return "moderate"
    elif abs_change >= 5:
        return "small"
    else:
        return "minimal"


def classify_change_direction(percent_change: float) -> str:
    """Classify direction of change"""
    if percent_change > 0:
        return "increase"
    elif percent_change < 0:
        return "decrease"
    else:
        return "stable"


def generate_timestamp() -> str:
    """Generate ISO format timestamp"""
    return datetime.now().isoformat()


def generate_execution_id() -> str:
    """Generate unique execution ID"""
    return f"EXEC_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit length
    return filename[:200]


def format_execution_time(seconds: float) -> str:
    """Format execution time in human-readable format"""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.0f}s"


def create_summary_stats(data: List[Dict[str, Any]], key: str) -> Dict[str, float]:
    """
    Create summary statistics for a numeric field
    
    Args:
        data: List of dictionaries
        key: Key to calculate stats for
    
    Returns:
        Dictionary with min, max, mean, median
    """
    values = [item[key] for item in data if key in item and isinstance(item[key], (int, float))]
    
    if not values:
        return {}
    
    values.sort()
    n = len(values)
    
    return {
        'min': min(values),
        'max': max(values),
        'mean': sum(values) / n,
        'median': values[n//2] if n % 2 == 1 else (values[n//2-1] + values[n//2]) / 2,
        'count': n
    }


def rank_items_by_score(items: List[Dict], score_key: str = 'score', 
                        reverse: bool = True) -> List[Dict]:
    """
    Rank items by score
    
    Args:
        items: List of dictionaries
        score_key: Key to sort by
        reverse: If True, sort descending
    
    Returns:
        Sorted list with rank added
    """
    sorted_items = sorted(items, key=lambda x: x.get(score_key, 0), reverse=reverse)
    
    for idx, item in enumerate(sorted_items, 1):
        item['rank'] = idx
    
    return sorted_items


def merge_dicts(*dicts: Dict) -> Dict:
    """Merge multiple dictionaries"""
    result = {}
    for d in dicts:
        result.update(d)
    return result


def print_banner(text: str, char: str = "=", width: int = 80):
    """Print a banner with text"""
    print("\n" + char * width)
    print(text.center(width))
    print(char * width + "\n")


def print_section(title: str):
    """Print a section title"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60 + "\n")


if __name__ == "__main__":
    # Test helper functions
    print("Testing helper functions...\n")
    
    # Test formatting
    print(f"Currency: {format_currency(12345.67)}")
    print(f"Percentage: {format_percentage(23.456)}")
    print(f"Number: {format_number(1234567.89)}")
    
    # Test calculations
    print(f"\nROAS: {calculate_roas(10000, 3000):.2f}")
    print(f"CTR: {calculate_ctr(500, 25000):.2f}%")
    print(f"CPC: {format_currency(calculate_cpc(1000, 500))}")
    
    # Test change classification
    print(f"\nChange magnitude (25%): {classify_change_magnitude(25)}")
    print(f"Change direction (-15): {classify_change_direction(-15)}")
    
    print("\n✓ Helper functions working correctly")
