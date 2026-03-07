import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Add root directory to path to import insights
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from analysis.data_processing import load_data, clean_data, feature_engineering
from analysis.insights import (
    get_product_profitability, 
    get_division_performance, 
    get_pareto_data, 
    get_monthly_trends, 
    get_state_performance, 
    get_cost_breakdown, 
    get_customer_profitability
)

def generate_figures():
    # Load and prep data
    data_path = "data/Nassau Candy Distributor.csv"
    if not os.path.exists(data_path):
        print(f"Data not found at {data_path}")
        return
    
    df = load_data(data_path)
    df = clean_data(df)
    df = feature_engineering(df)
    
    # Create figures directory
    output_dir = "research-paper/figures"
    os.makedirs(output_dir, exist_ok=True)
    
    # Set style
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)
    
    # 1. Sales vs Gross Profit (Scatter)
    plt.figure()
    sns.scatterplot(data=df, x='Sales', y='Gross Profit', hue='Division', palette='viridis', s=60, alpha=0.7)
    plt.title("Sales vs Gross Profit by Division", fontsize=15, pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "sales_vs_profit.png"), dpi=300)
    plt.close()
    
    # 2. Pareto Chart
    pareto_df = get_pareto_data(df).head(20)
    fig, ax1 = plt.subplots()
    ax1.bar(pareto_df['Product Name'], pareto_df['Gross Profit'], color='C0')
    ax1.set_ylabel('Gross Profit ($)', color='C0', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='C0')
    plt.xticks(rotation=45, ha='right')
    
    ax2 = ax1.twinx()
    ax2.plot(pareto_df['Product Name'], pareto_df['Cumulative Percentage'], color='C1', marker='o', linewidth=2)
    ax2.set_ylabel('Cumulative %', color='C1', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='C1')
    ax2.axhline(y=80, color='r', linestyle='--', alpha=0.5)
    
    plt.title("Pareto Analysis: Product Profit Concentration", fontsize=15, pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "pareto_chart.png"), dpi=300)
    plt.close()
    
    # 3. Division Performance
    div_stats = get_division_performance(df)
    plt.figure()
    sns.barplot(data=div_stats, x='Division', y='Gross Profit', palette='magma')
    plt.title("Gross Profit by Division", fontsize=15, pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "division_performance.png"), dpi=300)
    plt.close()
    
    # 4. Monthly Trends
    monthly = get_monthly_trends(df)
    fig, ax1 = plt.subplots()
    ax1.bar(monthly['Month'], monthly['Sales'], color='skyblue', alpha=0.6, label='Sales')
    ax1.set_ylabel('Total Sales ($)', fontsize=12)
    plt.xticks(rotation=45)
    
    ax2 = ax1.twinx()
    ax2.plot(monthly['Month'], monthly['Gross Margin (%)'], color='orange', marker='s', linewidth=2, label='Margin %')
    ax2.set_ylabel('Gross Margin (%)', fontsize=12)
    
    plt.title("Monthly Sales and Margin Trends", fontsize=15, pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "monthly_trends.png"), dpi=300)
    plt.close()
    
    # 5. Top 10 States
    state_stats = get_state_performance(df).head(10)
    plt.figure()
    sns.barplot(data=state_stats, x='Gross Profit', y='State/Province', palette='viridis')
    plt.title("Top 10 States by Gross Profit", fontsize=15, pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "state_performance.png"), dpi=300)
    plt.close()
    
    # 6. Cost Breakdown
    cost_data = get_cost_breakdown(df)
    plt.figure()
    plt.pie(cost_data['Total Cost'], labels=cost_data['Cost Component'], autopct='%1.1f%%', colors=sns.color_palette('pastel'))
    plt.title("Total Cost Component Breakdown", fontsize=15, pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "cost_breakdown.png"), dpi=300)
    plt.close()
    
    # 7. Customer Profitability
    cust_stats = get_customer_profitability(df).head(15)
    plt.figure()
    sns.barplot(data=cust_stats, x='Gross Profit', y='Customer ID', palette='rocket')
    plt.title("Top 15 Customers by Gross Profit", fontsize=15, pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "customer_profitability.png"), dpi=300)
    plt.close()
    
    print(f"All 7 figures generated in {output_dir}")

if __name__ == "__main__":
    generate_figures()
