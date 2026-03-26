import streamlit as st
import pandas as pd

# ===================== PAGE CONFIG =====================
st.set_page_config(page_title="Sneaker Dashboard", layout="wide")

# ===================== TITLE =====================
st.markdown("<h1 style='text-align: center;'>👟 Sneaker Resale Dashboard</h1>", unsafe_allow_html=True)

# ===================== LOAD DATA =====================
try:
    df = pd.read_csv("data/jordan_market_dataset_2026.csv")
except:
    st.error("❌ Dataset not found. Please check file path.")
    st.stop()

# ===================== DATA PREPROCESSING =====================
df['Sale_Date'] = pd.to_datetime(df['Sale_Date'])

# ===================== SIDEBAR FILTERS =====================
st.sidebar.header("🔎 Filters")

model = st.sidebar.multiselect("Shoe Model", df['Shoe_Model'].unique())
channel = st.sidebar.multiselect("Sales Channel", df['Sales_Channel'].unique())
condition = st.sidebar.multiselect("Condition", df['Condition'].unique())

# Date filter
date_range = st.sidebar.date_input("Select Date Range", [])

# Apply filters
filtered_df = df.copy()

if model:
    filtered_df = filtered_df[filtered_df['Shoe_Model'].isin(model)]

if channel:
    filtered_df = filtered_df[filtered_df['Sales_Channel'].isin(channel)]

if condition:
    filtered_df = filtered_df[filtered_df['Condition'].isin(condition)]

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['Sale_Date'] >= pd.to_datetime(date_range[0])) &
        (filtered_df['Sale_Date'] <= pd.to_datetime(date_range[1]))
    ]

# ===================== KPIs =====================
st.markdown("## 📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"${int(filtered_df['Resale_Price_USD'].sum())}")
col2.metric("📈 Total Profit", f"${int(filtered_df['Profit_Margin_USD'].sum())}")
col3.metric("📦 Avg Inventory Days", int(filtered_df['Days_in_Inventory'].mean()))
col4.metric("👟 Total Sales", len(filtered_df))

st.markdown("---")

# ===================== CHARTS ROW 1 =====================
col1, col2 = st.columns(2)

# Sales Trend
with col1:
    st.subheader("📈 Sales Trend")
    trend = filtered_df.groupby('Sale_Date')['Resale_Price_USD'].sum().sort_index()
    st.line_chart(trend)

# Top Models
with col2:
    st.subheader("📊 Top Models")
    top_models = filtered_df['Shoe_Model'].value_counts().head(10)
    st.bar_chart(top_models)

st.markdown("---")

# ===================== CHARTS ROW 2 =====================
col3, col4 = st.columns(2)

# Profit by Channel
with col3:
    st.subheader("🛒 Profit by Channel")
    channel_profit = filtered_df.groupby('Sales_Channel')['Profit_Margin_USD'].sum()
    st.bar_chart(channel_profit)

# Inventory vs Profit
with col4:
    st.subheader("📦 Inventory vs Profit")
    st.scatter_chart(filtered_df[['Days_in_Inventory', 'Profit_Margin_USD']])

st.markdown("---")

# ===================== INSIGHTS =====================
st.subheader("🔍 Key Insights")

st.markdown("""
- Top sneaker models contribute significantly to total revenue  
- Online sales channels tend to generate higher profits  
- Longer inventory duration negatively impacts profitability  
- Certain sneaker models dominate the resale market  
""")