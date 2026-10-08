import pandas as pd

def rolling_anomalies(df,value_columns,window=24,z_threshold=2.0):
    out=df.copy()
    for col in value_columns:
        mean=out[col].rolling(window,min_periods=max(3,window//4)).mean();std=out[col].rolling(window,min_periods=max(3,window//4)).std().replace(0,pd.NA)
        out[f'{col}_zscore']=(out[col]-mean)/std;out[f'{col}_anomaly']=out[f'{col}_zscore'].abs()>z_threshold
    return out
def health_summary(df):
    return {c:{'p50':float(df[c].quantile(.5)),'p95':float(df[c].quantile(.95)),'p99':float(df[c].quantile(.99))} for c in ['latency_ms','error_rate','record_count'] if c in df}
