import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Page config
st.set_page_config(page_title="Sneaker Dashboard", layout="wide")

# Title
st.markdown("<h1 style='text-align: center;'>👟 Sneaker Resale Dashboard</h1>", unsafe_allow_html=True)

# Connect MySQL
engine = create_engine("mysql+pymysql://root:#Rishi123@localhost/sneaker_analysis")

# Load data
df = pd.read_sql("SELECT * FROM sales", engine)

# Convert date
df['Sale_Date'] = pd.to_datetime(df['Sale_Date'])

# ===================== KPIs =====================
st.markdown("## 📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"${int(df['Resale_Price_USD'].sum())}")
col2.metric("📈 Total Profit", f"${int(df['Profit_Margin_USD'].sum())}")
col3.metric("📦 Avg Inventory Days", int(df['Days_in_Inventory'].mean()))
col4.metric("👟 Total Sales", len(df))

st.markdown("---")

# ===================== SIDEBAR FILTERS =====================
st.sidebar.header("🔎 Filters")

model = st.sidebar.multiselect("Shoe Model", df['Shoe_Model'].unique())
channel = st.sidebar.multiselect("Sales Channel", df['Sales_Channel'].unique())
condition = st.sidebar.multiselect("Condition", df['Condition'].unique())

filtered_df = df.copy()

if model:
    filtered_df = filtered_df[filtered_df['Shoe_Model'].isin(model)]

if channel:
    filtered_df = filtered_df[filtered_df['Sales_Channel'].isin(channel)]

if condition:
    filtered_df = filtered_df[filtered_df['Condition'].isin(condition)]

# ===================== CHARTS =====================
col1, col2 = st.columns(2)

# Sales trend
with col1:
    st.subheader("📈 Sales Trend")
    trend = filtered_df.groupby('Sale_Date')['Resale_Price_USD'].sum()
    st.line_chart(trend)

# Top models
with col2:
    st.subheader("📊 Top Models")
    st.bar_chart(filtered_df['Shoe_Model'].value_counts().head(10))

st.markdown("---")

# ===================== SECOND ROW =====================
col3, col4 = st.columns(2)

# Channel profit
with col3:
    st.subheader("🛒 Profit by Channel")
    st.bar_chart(filtered_df.groupby('Sales_Channel')['Profit_Margin_USD'].sum())

# Inventory vs Profit
with col4:
    st.subheader("📦 Inventory vs Profit")
    st.scatter_chart(filtered_df[['Days_in_Inventory', 'Profit_Margin_USD']])

st.markdown("---")

# ===================== INSIGHTS =====================
st.subheader("🔍 Key Insights")

st.markdown("""
- Top sneaker models contribute most of the revenue  
- Online channels generate higher profit  
- Longer inventory duration reduces profitability  
- Certain models dominate resale market  
""")