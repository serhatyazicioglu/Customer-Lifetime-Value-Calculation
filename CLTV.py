import pandas as pd
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_ = pd.read_excel("online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()

df[~df["Invoice"].str.contains("C", na=False)]

df = df[df["Quantity"] > 0]

df.dropna(inplace=True)

df["TotalPrice"] = df["Quantity"] * df["Price"]

df_cltv = df.groupby('Customer ID').agg({'Invoice': lambda x: len(x),
                                         'Quantity': lambda x: x.sum(),
                                         'TotalPrice': lambda x: x.sum()})

df_cltv.columns = ['total_transaction', 'total_unit', 'total_price']

#  Customer_Value = Average_Order_Value * Purchase_Frequency
df_cltv["average_order_value"] = df_cltv["total_price"] / df_cltv["total_transaction"]

df_cltv.shape[0]  # total customer number
df_cltv["purchase_frequency"] = df_cltv['total_transaction'] / df_cltv.shape[0]

# customer value 
df_cltv["customer_value"] = df_cltv["average_order_value"] * df_cltv["purchase_frequency"]

# Churn_Rate = 1 - Repeat_Rate

repeat_rate = df_cltv[df_cltv["total_transaction"] > 1].shape[0] / df_cltv.shape[0]
churn_rate = 1 - repeat_rate

# profit margin
df_cltv["profit_margin"] = df_cltv["total_price"] * 0.05

# CLTV = (Customer_Value / Churn_Rate) x Profit_margin.
df_cltv["CLTV"] = (df_cltv["customer_value"] / churn_rate) * df_cltv["profit_margin"]

# segmentation
df_cltv["Segment"] = pd.qcut(df_cltv["CLTV"], 5, labels=["E", "D", "C", "B", "A"])

df_cltv[["total_price", "CLTV", "Segment"]].sort_values(by="Segment", ascending=False).head()

