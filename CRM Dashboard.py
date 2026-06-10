import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------
# Load data
# -----------------------------
df = pd.read_excel("Sales.xlsx")

df['order_date'] = pd.to_datetime(df['order_date'])
df['month'] = df['order_date'].dt.to_period('M').dt.to_timestamp()
df['profit_margin'] = df['profit'] / df['revenue']

# -----------------------------
# Streamlit Page Setup
# -----------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Performance Dashboard")

# -----------------------------
# Slicers (Filters)
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    region_filter = st.multiselect(
        "Select Region(s):",
        options=df['region'].unique(),
        default=df['region'].unique()
    )

with col2:
    month_filter = st.multiselect(
        "Select Month(s):",
        options=df['month'].unique(),
        default=df['month'].unique()
    )

# Apply filters
filtered = df[
    (df['region'].isin(region_filter)) &
    (df['month'].isin(month_filter))
]

# -----------------------------
# KPI Calculations
# -----------------------------
current_month = filtered['month'].max()
cm_mask = filtered['month'] == current_month
ytd_mask = filtered['order_date'].dt.year == current_month.year

cm_revenue = filtered.loc[cm_mask, 'revenue'].sum()
cm_profit = filtered.loc[cm_mask, 'profit'].sum()
cm_units = filtered.loc[cm_mask, 'units_sold'].sum()
cm_margin = cm_profit / cm_revenue if cm_revenue != 0 else 0

ytd_revenue = filtered.loc[ytd_mask, 'revenue'].sum()
ytd_profit = filtered.loc[ytd_mask, 'profit'].sum()
ytd_units = filtered.loc[ytd_mask, 'units_sold'].sum()
ytd_margin = ytd_profit / ytd_revenue if ytd_revenue != 0 else 0

# -----------------------------
# KPI Cards
# -----------------------------
st.subheader("📌 Current Month KPIs")

cm1, cm2, cm3, cm4 = st.columns(4)
cm1.metric("Revenue (CM)", f"${cm_revenue:,.0f}")
cm2.metric("Profit (CM)", f"${cm_profit:,.0f}")
cm3.metric("Profit Margin (CM)", f"{cm_margin:.1%}")
cm4.metric("Units Sold (CM)", f"{cm_units:,.0f}")

st.subheader("📌 Year-to-Date KPIs")

y1, y2, y3, y4 = st.columns(4)
y1.metric("Revenue (YTD)", f"${ytd_revenue:,.0f}")
y2.metric("Profit (YTD)", f"${ytd_profit:,.0f}")
y3.metric("Profit Margin (YTD)", f"{ytd_margin:.1%}")
y4.metric("Units Sold (YTD)", f"{ytd_units:,.0f}")

# -----------------------------
# Charts
# -----------------------------
st.subheader("📈 Monthly Revenue Trend")
fig1, ax1 = plt.subplots(figsize=(10,4))
sns.lineplot(data=filtered.groupby('month')['revenue'].sum(), ax=ax1, marker='o')
ax1.set_ylabel("Revenue")
ax1.set_xlabel("Month")
plt.xticks(rotation=45)
st.pyplot(fig1)

st.subheader("📊 Revenue by Region")
fig2, ax2 = plt.subplots(figsize=(10,4))
sns.barplot(data=filtered.groupby('region')['revenue'].sum().reset_index(),
            x='region', y='revenue', palette="Blues_d", ax=ax2)
st.pyplot(fig2)

st.subheader("📦 Revenue by Product Category")
fig3, ax3 = plt.subplots(figsize=(10,4))
sns.barplot(
    data=filtered.groupby('product_category')['revenue'].sum().reset_index(),
    x='product_category', y='revenue', palette="Greens_d", ax=ax3
)
plt.xticks(rotation=45)
st.pyplot(fig3)

# Top 10 / Bottom 10
st.subheader("🏆 Top 10 Products by Revenue")
fig4, ax4 = plt.subplots(figsize=(10,4))
top10 = filtered.groupby('product')['revenue'].sum().sort_values(ascending=False).head(10)
sns.barplot(x=top10.values, y=top10.index, palette="Blues", ax=ax4)
st.pyplot(fig4)

st.subheader("⚠️ Bottom 10 Products by Revenue")
fig5, ax5 = plt.subplots(figsize=(10,4))
bottom10 = filtered.groupby('product')['revenue'].sum().sort_values().head(10)
sns.barplot(x=bottom10.values, y=bottom10.index, palette="Reds", ax=ax5)
st.pyplot(fig5)
