import numpy as np
import pandas as pd
df = pd.read_excel("Phase_2.xlsx")
df['InvoiceDate (R)'] = pd.to_datetime(df['InvoiceDate (R)'])
analysis_date = df['InvoiceDate (R)'].max() + pd.Timedelta(days=1)
print(analysis_date)
rfm = df.groupby('Customer ID').agg({
    'InvoiceDate (R)': lambda x: (analysis_date - x.max()).days,
    'Invoice (F)': 'nunique',
    'TotalAmount (M)': 'sum'
})
rfm.columns = ['Recency', 'Frequency', 'Monetary']
rfm = rfm.reset_index()
rfm['R_Score'] = pd.qcut(
    rfm['Recency'],
    5,
    labels=[5, 4, 3, 2, 1]
)
rfm['F_Score'] = pd.qcut(
    rfm['Frequency'].rank(method='first'),
    5,
    labels=[1, 2, 3, 4, 5]
)
rfm['M_Score'] = pd.qcut(
    rfm['Monetary'],
    5,
    labels=[1, 2, 3, 4, 5]
)
rfm[['R_Score', 'F_Score', 'M_Score']] = rfm[['R_Score', 'F_Score', 'M_Score']].astype(int)
rfm['RFM_Code'] = (
    rfm['R_Score'].astype(str) +
    rfm['F_Score'].astype(str) +
    rfm['M_Score'].astype(str)
)
print(rfm)
rfm.to_excel("RFM_Output.xlsx", index=False)
