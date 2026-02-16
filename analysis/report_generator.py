import sys
import os
import pandas as pd
import numpy as np

# Add analysis directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analysis.data_processing import load_data, clean_data, feature_engineering

def generate_report_stats():
    # Load Data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "data", "Nassau Candy Distributor.csv")
    output_path = os.path.join(script_dir, "report_stats.txt")
    
    df = load_data(data_path)
    if df is None:
        print("Failed to load data")
        return

    df = clean_data(df)
    df = feature_engineering(df)
    
    # Import analysis functions
    from analysis.insights import (
        get_product_profitability, 
        get_division_performance, 
        get_pareto_data, 
        get_monthly_trends, 
        get_state_performance, 
        get_cost_breakdown, 
        get_customer_profitability
    )

    with open(output_path, "w") as f:
        # 1. Overall Metrics
        f.write("--- Executive Summary Metrics ---\n")
        f.write(f"Total Sales: ${df['Sales'].sum():,.2f}\n")
        f.write(f"Total Gross Profit: ${df['Gross Profit'].sum():,.2f}\n")
        f.write(f"Overall Gross Margin: {(df['Gross Profit'].sum() / df['Sales'].sum() * 100):.2f}%\n")
        f.write(f"Total Units: {df['Units'].sum():,.0f}\n\n")
        
        # 2. Product Performance
        prod_stats = get_product_profitability(df)
        f.write("--- Product Performance ---\n")
        f.write(f"Top Product: {prod_stats.iloc[0]['Product Name']} (${prod_stats.iloc[0]['Gross Profit']:,.2f})\n")
        f.write(f"Bottom Product: {prod_stats.iloc[-1]['Product Name']} (${prod_stats.iloc[-1]['Gross Profit']:,.2f})\n\n")
        
        # 3. Division Analysis
        div_stats = get_division_performance(df)
        f.write("--- Division Performance ---\n")
        f.write(div_stats.to_string() + "\n\n")
        
        # 4. Pareto Analysis
        pareto_df = get_pareto_data(df)
        total_profit = df['Gross Profit'].sum()
        count_80 = pareto_df[pareto_df['Cumulative Percentage'] <= 80].shape[0]
        total_products = df['Product Name'].nunique()
        f.write("--- Pareto Analysis ---\n")
        f.write(f"Products for 80% Profit: {count_80} out of {total_products} ({count_80/total_products*100:.1f}%)\n\n")
        
        # 5. Cost Diagnostics
        f.write("--- Cost Diagnostics ---\n")
        f.write(f"Cost-Margin Correlation: {df['Cost'].corr(df['Gross Margin (%)']):.4f}\n")
        
        cost_breakdown = get_cost_breakdown(df)
        f.write("\nSimulated Cost Breakdown:\n")
        f.write(cost_breakdown.to_string() + "\n\n")

        # 6. Temporal Trends
        monthly = get_monthly_trends(df)
        f.write("--- Temporal Trends ---\n")
        f.write(monthly.to_string() + "\n\n")

        # 7. Geospatial Insights
        state_stats = get_state_performance(df)
        f.write("--- Top 5 States ---\n")
        f.write(state_stats.head(5).to_string() + "\n\n")

        # 8. Customer Insights
        cust_stats = get_customer_profitability(df)
        f.write("--- Customer Insights ---\n")
        f.write(f"Total Customers: {len(cust_stats)}\n")
        f.write(f"Avg Profit/Customer: ${cust_stats['Gross Profit'].mean():,.2f}\n")
        f.write(f"Top 5 Customers:\n{cust_stats.head(5).to_string()}\n")

    print(f"Report generated at {output_path}")

if __name__ == "__main__":
    generate_report_stats()
