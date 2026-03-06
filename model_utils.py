import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def analyze_dataset(df):

    total_rows = df.shape[0]
    total_columns = df.shape[1]
#Missing Values
    total_missing = df.isnull().sum().sum()
    missing_percent = (total_missing/(total_rows*total_columns))*100
#Duplicate rows
    duplicate_rows = df.duplicated().sum()
    duplicate_percent = (duplicate_rows/total_rows)*100

#Numeric Columns
    numeric_df = df.select_dtypes(include=np.number)
    anomaly_percent = 0
    preds = None
    if not numeric_df.empty:
        model = IsolationForest(contamination=0.05, random_state=42)
        preds = model.fit_predict(numeric_df)
        anomaly_count = np.sum(preds == -1)
        anomaly_percent = (anomaly_count/total_rows)*100
#Quality score
    quality_score = 100-(missing_percent*0.4)\
          - (duplicate_percent*0.3) \
          - (anomaly_percent*0.3)
    quality_score = max(0,round(quality_score,2))
#Grade
    if quality_score >= 90:
        grade = "A"
    elif quality_score >= 75:
        grade = "B"
    elif quality_score >= 50:
        grade = "C"
    else:
        grade = "D"
#Column level analysis
    column_scores = []
    for col in numeric_df.columns:
        col_missing = df[col].isnull().sum()/total_rows*100
        model = IsolationForest(contamination=0.05,random_state=42)
        preds = model.fit_predict(df[[col]].dropna())
        col_anomaly = (preds == -1).sum()/len(preds)*100
        col_score = 100 - (col_missing*0.5)-(col_anomaly*0.5)
        column_scores.append({
            "column": col,
            "missing_percent": round(col_missing,2),
            "anomaly_percent": round(col_anomaly,2),
            "score": round(col_score,2)
        })
#Cleaning suggestions
    suggestions = []
    if missing_percent > 10:
        suggestions.append("High missing values detected. Consider data imputation.")
    if duplicate_percent > 5:
        suggestions.append("Dataset contains duplicates. Remove duplicate rows.")
    if anomaly_percent > 5:
        suggestions.append("Siginificant anomalies detected. Review suspicious records.")
    return {
        "rows": total_rows,
        "columns": total_columns,
        "missing_percent": round(missing_percent,2),
        "duplicate_percent": round(duplicate_percent,2),
        "anomaly_percent": round(anomaly_percent,2),
        "quality_score": quality_score,
        "grade": grade,
        "column_analysis": column_scores,
        "suggestions": suggestions
    }    
