import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

# Set default plotly theme
# Set default plotly theme
# pio.templates.default = "plotly_dark"  # Commented out to allow dynamic theme adaptation
import sys
import os

import io

# Add analysis directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analysis.data_processing import load_data, clean_data, feature_engineering
from analysis.insights import get_product_profitability, get_division_performance, get_pareto_data, get_monthly_trends, get_state_performance, get_cost_breakdown, get_customer_profitability
from analysis.forecasting import generate_forecast
from analysis.scenario import run_scenario

# Page config
st.set_page_config(layout="wide", page_title="Nassau Candy Profitability Analysis")

# Constants & Theme
COLOR_SEQUENCE = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#6366F1', '#14B8A6']


# Styling
# Styling
st.markdown("""
<style>
    /* Main Background - Handled by Streamlit Theme */
    
    /* Metrics Cards */
    [data-testid="stMetric"], [data-testid="metric-container"] {
        background-color: var(--secondary-background-color);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s;
        color: var(--text-color);
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* Metric Labels */
    [data-testid="stMetricLabel"] {
        color: var(--text-color) !important;
        opacity: 0.8;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    /* Metric Values */
    [data-testid="stMetricValue"] {
        color: var(--text-color) !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 8px;
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 0 20px;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(128, 128, 128, 0.1);
        color: var(--text-color);
    }
    
    /* High Contrast Active Tab */
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
        border: 2px solid #3B82F6 !important;
        border-bottom: none !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        font-weight: 700 !important;
    }

    /* Streamlit Components */
    .stDataFrame {
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 8px;
    }
    
    /* Custom Headers */
    h1, h2, h3 {
        color: var(--text-color) !important;
        font-weight: 600 !important;
    }
    
    h1 {
        padding-bottom: 20px;
        margin-bottom: 50px;
        border-bottom: none !important;
    }
    
    /* Remove default red highlight line */
    div[data-baseweb="tab-highlight"] {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_and_prep_data():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "Nassau Candy Distributor.csv")
    if not os.path.exists(data_path):
        return None
    df = load_data(data_path)
    if df is not None:
        df = clean_data(df)
        if df.empty:
            return None
        df = feature_engineering(df)
        if df.empty:
            return None
    return df

df = load_and_prep_data()

if df is None:
    st.error("Data file not found or could not be loaded. Please check the data directory.")
else:
    # Sidebar
    st.sidebar.title("Filters")
    
    # Date Range Filter
    min_date = df['Order Date'].min()
    max_date = df['Order Date'].max()
    start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
    
    # Division Filter
    division = st.sidebar.multiselect("Select Division", options=df['Division'].unique(), default=df['Division'].unique())

    # Product Category Filter
    if 'Product Category' in df.columns:
        product_category = st.sidebar.multiselect("Select Product Category", options=df['Product Category'].unique(), default=df['Product Category'].unique())
    else:
        product_category = []

    # Customer Segment Filter
    if 'Customer Segment' in df.columns:
        customer_segment = st.sidebar.multiselect("Select Customer Segment", options=df['Customer Segment'].unique(), default=df['Customer Segment'].unique())
    else:
        customer_segment = []
    
    # Margin Threshold Slider
    margin_threshold = st.sidebar.slider("Min Gross Margin (%)", min_value=float(df['Gross Margin (%)'].min()), max_value=float(df['Gross Margin (%)'].max()), value=0.0)
    
    # Filter data
    # Create mask for filtering
    mask = (
        (df['Division'].isin(division)) & 
        (df['Order Date'] >= pd.to_datetime(start_date)) & 
        (df['Order Date'] <= pd.to_datetime(end_date)) &
        (df['Gross Margin (%)'] >= margin_threshold)
    )
    
    if product_category:
        mask = mask & (df['Product Category'].isin(product_category))

    if customer_segment:
        mask = mask & (df['Customer Segment'].isin(customer_segment))

    filtered_df = df[mask]
    
    # Main Dashboard
    st.title("Product Line Profitability Analysis")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
    col2.metric("Total Profit", f"${filtered_df['Gross Profit'].sum():,.2f}")
    col3.metric("Total Units", f"{filtered_df['Units'].sum():,.0f}")
    col4.metric("Avg Margin", f"{filtered_df['Gross Margin (%)'].mean():.2f}%")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs(["Overview", "Product Analysis", "Division Performance", "Profit Concentration", "Cost Diagnostics", "Temporal Trends", "Geospatial Insights", "Customer Insights", "Forecasting", "Scenario Planning", "Reports"])
    
    with tab1:
        st.subheader("Profitability Overview")
        # Scatter plot Sales vs Profit
        fig = px.scatter(
            filtered_df, 
            x='Sales', 
            y='Gross Profit', 
            color='Division', 
            hover_data=['Product Name', 'Gross Margin (%)'],
            title="Sales vs Gross Profit",
            color_discrete_sequence=COLOR_SEQUENCE
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        st.subheader("Product Analysis")
        
        # Product Search
        search_term = st.text_input("Search Product", "", placeholder="Search here...")
        if search_term:
            product_view = filtered_df[filtered_df['Product Name'].str.contains(search_term, case=False)]
        else:
            product_view = filtered_df
            
        product_stats = get_product_profitability(product_view)
        st.dataframe(product_stats.head(20).style.format({'Sales': '${:,.2f}', 'Gross Profit': '${:,.2f}', 'Gross Margin (%)': '{:.2f}%', 'Profit per Unit': '${:,.2f}'}))
        
    with tab3:
        st.subheader("Division Performance")
        division_stats = get_division_performance(filtered_df)
        fig = px.bar(
            division_stats, 
            x='Division', 
            y='Gross Profit', 
            color='Division',
            title="Total Gross Profit by Division",
            hover_data=['Sales', 'Gross Margin (%)'],
            color_discrete_sequence=COLOR_SEQUENCE
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with tab4:
        st.subheader("Pareto Analysis")
        if not filtered_df.empty:
            pareto_df = get_pareto_data(filtered_df)
            top_n = min(20, len(pareto_df))
            pareto_subset = pareto_df.head(top_n)
            
            # Create figure with secondary y-axis
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Add traces
            fig.add_trace(
                go.Bar(x=pareto_subset['Product Name'], y=pareto_subset['Gross Profit'], name="Gross Profit", marker_color=COLOR_SEQUENCE[0]),
                secondary_y=False,
            )

            fig.add_trace(
                go.Scatter(x=pareto_subset['Product Name'], y=pareto_subset['Cumulative Percentage'], name="Cumulative %", mode='lines+markers', line=dict(color=COLOR_SEQUENCE[2], width=2)),
                secondary_y=True,
            )

            # Add figure title
            fig.update_layout(
                title_text=f"Top {top_n} Products - Pareto Chart"
            )

            # Set x-axis title
            fig.update_xaxes(title_text="Product Name")

            # Set y-axes titles
            fig.update_yaxes(title_text="Gross Profit", secondary_y=False)
            fig.update_yaxes(title_text="Cumulative %", secondary_y=True)
            
            # Add 80% line
            fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="80% Threshold", secondary_y=True)

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for Pareto Analysis with current filters.")

    with tab5:
        st.subheader("Cost Structure Diagnostics")
        if not filtered_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Cost vs Margin")
                fig = px.scatter(
                    filtered_df, 
                    x='Cost', 
                    y='Gross Margin (%)', 
                    color='Division', 
                    size='Sales', 
                    hover_data=['Product Name'],
                    title="Cost vs Gross Margin (%)",
                    color_discrete_sequence=COLOR_SEQUENCE
                )
                fig.add_hline(y=0, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Cost Components Breakdown (Simulated)")
                cost_breakdown = get_cost_breakdown(filtered_df)
                fig = px.pie(
                    cost_breakdown, 
                    values='Total Cost', 
                    names='Cost Component', 
                    title="Total Cost Breakdown",
                    color_discrete_sequence=COLOR_SEQUENCE
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### High Cost, Low Margin Products")
            high_cost_low_margin = filtered_df[(filtered_df['Cost'] > filtered_df['Cost'].median()) & (filtered_df['Gross Margin (%)'] < 10)]
            st.dataframe(high_cost_low_margin[['Product Name', 'Division', 'Cost', 'Sales', 'Gross Margin (%)']].drop_duplicates().head(10))
        else:
            st.info("No data available.")

    with tab6:
        st.subheader("Temporal Trends (Monthly)")
        if not filtered_df.empty:
            monthly_trends = get_monthly_trends(filtered_df)
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(x=monthly_trends['Month'].astype(str), y=monthly_trends['Sales'], name="Total Sales", marker_color=COLOR_SEQUENCE[0]),
                secondary_y=False
            )
            
            fig.add_trace(
                go.Scatter(x=monthly_trends['Month'].astype(str), y=monthly_trends['Gross Margin (%)'], name="Gross Margin (%)", marker_color=COLOR_SEQUENCE[2], mode='lines+markers'),
                secondary_y=True
            )
            
            fig.update_layout(title_text="Monthly Sales and Gross Margin Trends")
            fig.update_yaxes(title_text="Total Sales ($)", secondary_y=False)
            fig.update_yaxes(title_text="Gross Margin (%)", secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data to display trends.")

    with tab7:
        st.subheader("Geospatial Insights (By State)")
        if not filtered_df.empty:
            state_performance = get_state_performance(filtered_df)
            
            fig = px.bar(
                state_performance.head(10), 
                x='Gross Profit', 
                y='State/Province', 
                orientation='h',
                color='Gross Profit',
                title="Top 10 States by Gross Profit",
                hover_data=['Sales', 'Gross Margin (%)'],
                color_continuous_scale='Viridis'
            )
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
            
            st.write("Full State Performance Data:")
            st.dataframe(state_performance.style.format({'Sales': '${:,.2f}', 'Gross Profit': '${:,.2f}', 'Gross Margin (%)': '{:.2f}%'}))
        else:
            st.info("No data available.")

    with tab8:
        st.subheader("Customer Profitability (Simulated)")
        if not filtered_df.empty:
            cust_stats = get_customer_profitability(filtered_df)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### Top 15 Customers by Profit")
                fig = px.bar(
                    cust_stats.head(15),
                    x='Customer ID',
                    y='Gross Profit',
                    title="Top 15 Customers by Profit",
                    hover_data=['Sales', 'Gross Margin (%)'],
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig, use_container_width=True)
                
            with col2:
                st.markdown("#### Customer Metrics")
                st.metric("Total Customers", f"{cust_stats['Customer ID'].nunique():,.0f}")
                st.metric("Avg Profit per Customer", f"${cust_stats['Gross Profit'].mean():,.2f}")
                
            st.markdown("#### Detailed Customer Data")
            st.dataframe(cust_stats.head(50).style.format({'Sales': '${:,.2f}', 'Gross Profit': '${:,.2f}', 'Gross Margin (%)': '{:.2f}%'}))
        else:
            st.info("No data available.")

    # Sidebar Data Export
    st.sidebar.markdown("---")
    st.sidebar.download_button(
        label="Download Filtered Data",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name='filtered_profitability_data.csv',
        mime='text/csv',
    )
    
    with tab9:
        st.subheader("Sales & Profit Forecasting (6 Months)")
        if not filtered_df.empty:
            forecast_df = generate_forecast(filtered_df, periods=6)
            
            # Metric Card for Forecasted Totals
            forecast_only = forecast_df[forecast_df['Type'] == 'Forecast']
            total_forecast_sales = forecast_only['Sales'].sum()
            total_forecast_profit = forecast_only['Gross Profit'].sum()
            
            c1, c2 = st.columns(2)
            c1.metric("Forecasted Sales (Next 6 Months)", f"${total_forecast_sales:,.2f}")
            c2.metric("Forecasted Profit (Next 6 Months)", f"${total_forecast_profit:,.2f}")
            
            # Plot
            fig = px.line(
                forecast_df, 
                x='Order Date', 
                y='Sales', 
                color='Type', 
                title="Sales Forecast",
                color_discrete_sequence=[COLOR_SEQUENCE[0], COLOR_SEQUENCE[2]] # Blue for history, Orange for forecast
            )
            st.plotly_chart(fig, use_container_width=True)
            
            fig2 = px.line(
                forecast_df, 
                x='Order Date', 
                y='Gross Profit', 
                color='Type', 
                title="Gross Profit Forecast",
                color_discrete_sequence=[COLOR_SEQUENCE[1], COLOR_SEQUENCE[3]] # Green for history, Red for forecast
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No data available for forecasting.")

    with tab10:
        st.subheader("Scenario Planning (What-If Analysis)")
        st.markdown("Adjust the parameters below to see the impact on profitability.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            mfg_change = st.slider("Mfg Cost Change (%)", -20.0, 20.0, 0.0, 0.5)
        with c2:
            ship_change = st.slider("Shipping Cost Change (%)", -20.0, 20.0, 0.0, 0.5)
        with c3:
            price_change = st.slider("Sales Price Change (%)", -20.0, 20.0, 0.0, 0.5)
            
        if st.button("Run Simulation"):
            if not filtered_df.empty:
                results = run_scenario(filtered_df, mfg_change, ship_change, price_change)
                
                # Display Results
                st.divider()
                st.markdown("### Simulation Results")
                
                m1, m2, m3 = st.columns(3)
                m1.metric(
                    "Projected Profit", 
                    f"${results['New Profit']:,.2f}", 
                    f"{results['Profit Change']:,.2f}",
                    delta_color="normal"
                )
                m2.metric(
                    "Projected Margin", 
                    f"{results['New Margin']:.2f}%", 
                    f"{results['Margin Change']:.2f}%",
                    delta_color="normal"
                )
                m3.metric(
                    "Projected Sales", 
                    f"${results['New Sales']:,.2f}", 
                    f"${results['New Sales'] - results['Original Sales']:,.2f}",
                    delta_color="normal"
                )
                
                # Comparison Chart
                scenario_data = pd.DataFrame({
                    'Metric': ['Total Profit', 'Total Profit'],
                    'Scenario': ['Original', 'New'],
                    'Value': [results['Original Profit'], results['New Profit']]
                })
                
                fig = px.bar(
                    scenario_data, 
                    x='Metric', 
                    y='Value', 
                    color='Scenario', 
                    barmode='group',
                    title="Profit Comparison",
                    color_discrete_sequence=[COLOR_SEQUENCE[0], COLOR_SEQUENCE[2]]
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available to simulate.")


    with tab11:
        st.subheader("Generate Reports")
        st.markdown("Download detailed analysis reports based on current filters.")
        
        if not filtered_df.empty:
            # 1. Excel Report Generator
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                # Sheet 1: Filtered Raw Data
                filtered_df.to_excel(writer, sheet_name='Raw Data', index=False)
                
                # Sheet 2: Product Performance
                product_stats = get_product_profitability(filtered_df)
                product_stats.to_excel(writer, sheet_name='Product Performance', index=False)
                
                # Sheet 3: Division Performance
                division_stats = get_division_performance(filtered_df)
                division_stats.to_excel(writer, sheet_name='Division Performance', index=False)
                
                # Sheet 4: Monthly Trends
                monthly_trends = get_monthly_trends(filtered_df)
                monthly_trends.to_excel(writer, sheet_name='Monthly Trends', index=False)
                
            buffer.seek(0)
            
            st.download_button(
                label="Download Comprehensive Excel Report",
                data=buffer,
                file_name="Profitability_Analysis_Report.xlsx",
                mime="application/vnd.ms-excel"
            )
            
            st.markdown("### Report Contents:")
            st.markdown("""
            - **Raw Data**: The complete dataset allowing for your own custom analysis.
            - **Product Performance**: Sales, Profit, and Margin metrics by Product.
            - **Division Performance**: Aggregated metrics by Division.
            - **Monthly Trends**: Time-series data for Sales and Profit.
            """)
            
        else:
            st.info("No data available to generate reports.")                
