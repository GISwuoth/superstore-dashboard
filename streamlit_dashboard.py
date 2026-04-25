import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")
st.title("🛒 Sales & Customer Analytics Dashboard")
st.markdown("Superstore Sales Data · Florence Owiti")

# ── Data loading ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("superstore_sales_data.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="mixed", dayfirst=False, errors="coerce")
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  format="mixed", dayfirst=False, errors="coerce")
    df["Year"]       = df["Order Date"].dt.year
    df["Month"]      = df["Order Date"].dt.to_period("M").astype(str)
    return df

df = load_data()

# ── Sidebar filters ──────────────────────────────────────────────────────────
st.sidebar.header("🔎 Filters")

region = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique()),
)

category = st.sidebar.multiselect(
    "Product Category",
    options=sorted(df["Product_Category"].unique()),
    default=sorted(df["Product_Category"].unique()),
)

segment = st.sidebar.multiselect(
    "Segment",
    options=sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique()),
)

years = sorted(df["Year"].unique())
year_range = st.sidebar.select_slider(
    "Year Range",
    options=years,
    value=(min(years), max(years)),
)

# Apply filters
filtered_df = df[
    df["Region"].isin(region) &
    df["Product_Category"].isin(category) &
    df["Segment"].isin(segment) &
    df["Year"].between(year_range[0], year_range[1])
]

st.sidebar.markdown(f"**{len(filtered_df):,}** rows selected")

# ── KPI row ──────────────────────────────────────────────────────────────────
st.subheader("📊 Key Metrics")
k1, k2, k3, k4 = st.columns(4)

total_sales   = filtered_df["Total_Sales"].sum()
avg_order     = filtered_df.groupby("Order ID")["Total_Sales"].sum().mean()
num_customers = filtered_df["Customer ID"].nunique()
num_orders    = filtered_df["Order ID"].nunique()

k1.metric("Total Sales",       f"${total_sales:,.0f}")
k2.metric("Avg Order Value",   f"${avg_order:,.2f}")
k3.metric("Unique Customers",  f"{num_customers:,}")
k4.metric("Total Orders",      f"{num_orders:,}")

st.markdown("---")

# ── Row 1: Sales by Category (bar) + Sales by Region (pie) ──────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Product Category")
    cat_df = (
        filtered_df.groupby("Product_Category")["Total_Sales"]
        .sum()
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )
    fig_cat = px.bar(
        cat_df,
        x="Product_Category",
        y="Total_Sales",
        color="Product_Category",
        labels={"Total_Sales": "Total Sales ($)", "Product_Category": "Category"},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_cat.update_layout(showlegend=False)
    st.plotly_chart(fig_cat, use_container_width=True)

with col2:
    st.subheader("Sales by Region")
    reg_df = (
        filtered_df.groupby("Region")["Total_Sales"]
        .sum()
        .reset_index()
    )
    fig_reg = px.pie(
        reg_df,
        names="Region",
        values="Total_Sales",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig_reg.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_reg, use_container_width=True)

# ── Row 2: Monthly Sales trend ───────────────────────────────────────────────
st.subheader("Monthly Sales Trend")
monthly_df = (
    filtered_df.groupby("Month")["Total_Sales"]
    .sum()
    .reset_index()
    .sort_values("Month")
)
fig_trend = px.line(
    monthly_df,
    x="Month",
    y="Total_Sales",
    markers=True,
    labels={"Total_Sales": "Total Sales ($)", "Month": "Month"},
    color_discrete_sequence=["#2196F3"],
)
fig_trend.update_xaxes(tickangle=45)
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# ── Row 3: Sales Distribution + Scatter ─────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("Sales Distribution by Category")
    fig_hist = px.histogram(
        filtered_df,
        x="Total_Sales",
        nbins=40,
        color="Product_Category",
        barmode="overlay",
        opacity=0.7,
        labels={"Total_Sales": "Total Sales ($)"},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col4:
    st.subheader("Sales by Category & Region (Scatter)")
    fig_scatter = px.scatter(
        filtered_df,
        x="Product_Category",
        y="Total_Sales",
        color="Region",
        size="Total_Sales",
        hover_data=["Customer Name", "Segment"],
        labels={"Total_Sales": "Total Sales ($)", "Product_Category": "Category"},
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ── Row 4: Top 10 customers + Sub-category breakdown ─────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.subheader("Top 10 Customers by Sales")
    top_customers = (
        filtered_df.groupby("Customer Name")["Total_Sales"]
        .sum()
        .nlargest(10)
        .reset_index()
        .sort_values("Total_Sales")
    )
    fig_top = px.bar(
        top_customers,
        x="Total_Sales",
        y="Customer Name",
        orientation="h",
        color="Total_Sales",
        color_continuous_scale="Blues",
        labels={"Total_Sales": "Total Sales ($)", "Customer Name": ""},
    )
    fig_top.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_top, use_container_width=True)

with col6:
    st.subheader("Sales by Sub-Category")
    sub_df = (
        filtered_df.groupby("Sub-Category")["Total_Sales"]
        .sum()
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
        .head(10)
    )
    fig_sub = px.bar(
        sub_df,
        x="Total_Sales",
        y="Sub-Category",
        orientation="h",
        color="Total_Sales",
        color_continuous_scale="Greens",
        labels={"Total_Sales": "Total Sales ($)", "Sub-Category": ""},
    )
    fig_sub.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_sub, use_container_width=True)

st.markdown("---")

# ── Correlation Heatmap ───────────────────────────────────────────────────────
st.subheader("Correlation Heatmap (Numerical Features)")
numeric_df = filtered_df.select_dtypes(include="number").drop(columns=["Row ID", "Postal Code"], errors="ignore")
if numeric_df.shape[1] >= 2:
    corr = numeric_df.corr()
    fig_corr, ax = plt.subplots(figsize=(5, 3))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax, linewidths=0.5)
    st.pyplot(fig_corr)
else:
    st.info("Not enough numeric columns for a heatmap with current filters.")

st.markdown("---")

# ── Raw data view ─────────────────────────────────────────────────────────────
with st.expander("📋 View Raw Data"):
    st.subheader("Filtered Dataset")
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
    st.write(f"**Shape:** {filtered_df.shape[0]:,} rows × {filtered_df.shape[1]} columns")

    st.subheader("Summary Statistics")
    st.write(filtered_df.describe())

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("Built with **Streamlit** · Superstore Sales Dataset · Florence Owiti")
