import pandas as pd
df = pd.read_csv('data/synthetic_fb_ads_undergarments.csv')
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Total rows: {len(df)}")
