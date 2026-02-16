import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_product_profitability(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates product-level profitability metrics.

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        pd.DataFrame: A dataframe containing Sales, Gross Profit, Units, Margin %, and Profit per Unit, ranked by Gross Profit.
    """
    try:
        product_stats = df.groupby('Product Name').agg({
            'Sales': 'sum',
            'Gross Profit': 'sum',
            'Units': 'sum'
        }).reset_index()
        
        product_stats['Gross Margin (%)'] = (product_stats['Gross Profit'] / product_stats['Sales'] * 100)
        product_stats['Profit per Unit'] = product_stats['Gross Profit'] / product_stats['Units']
        
        return product_stats.sort_values(by='Gross Profit', ascending=False)
    except Exception as e:
        print(f"Error in get_product_profitability: {e}")
        return pd.DataFrame()

def get_division_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates division-level performance metrics.

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        pd.DataFrame: A dataframe containing Sales, Gross Profit, Units, and Margin % by Division, ranked by Gross Profit.
    """
    try:
        division_stats = df.groupby('Division').agg({
            'Sales': 'sum',
            'Gross Profit': 'sum',
            'Units': 'sum'
        }).reset_index()
        
        division_stats['Gross Margin (%)'] = (division_stats['Gross Profit'] / division_stats['Sales'] * 100)
        
        return division_stats.sort_values(by='Gross Profit', ascending=False)
    except Exception as e:
        print(f"Error in get_division_performance: {e}")
        return pd.DataFrame()

def get_pareto_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs Pareto analysis on products based on Gross Profit.

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        pd.DataFrame: A dataframe with Cumulative Profit and Cumulative Percentage columns.
    """
    try:
        product_stats = df.groupby('Product Name').agg({'Gross Profit': 'sum'}).reset_index()
        product_stats = product_stats.sort_values(by='Gross Profit', ascending=False)
        
        product_stats['Cumulative Profit'] = product_stats['Gross Profit'].cumsum()
        product_stats['Cumulative Percentage'] = 100 * product_stats['Cumulative Profit'] / product_stats['Gross Profit'].sum()
        
        return product_stats
    except Exception as e:
        print(f"Error in get_pareto_data: {e}")
        return pd.DataFrame()

def get_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates sales and profit metrics by month.

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        pd.DataFrame: A dataframe with Monthly Sales, Gross Profit, and Gross Margin %.
    """
    try:
        # Ensure Order Date is datetime
        df['Month'] = df['Order Date'].dt.to_period('M')
        monthly_stats = df.groupby('Month').agg({
            'Sales': 'sum',
            'Gross Profit': 'sum'
        }).reset_index()
        
        monthly_stats['Month'] = monthly_stats['Month'].astype(str)
        monthly_stats['Gross Margin (%)'] = (monthly_stats['Gross Profit'] / monthly_stats['Sales'] * 100)
        
        return monthly_stats
    except Exception as e:
        print(f"Error in get_monthly_trends: {e}")
        return pd.DataFrame()

def get_state_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates performance metrics by State/Province.

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        pd.DataFrame: A dataframe containing Sales, Gross Profit, and Gross Margin % by State, ranked by Gross Profit.
    """
    try:
        state_stats = df.groupby('State/Province').agg({
            'Sales': 'sum',
            'Gross Profit': 'sum'
        }).reset_index()
        
        state_stats['Gross Margin (%)'] = (state_stats['Gross Profit'] / state_stats['Sales'] * 100)
        return state_stats.sort_values(by='Gross Profit', ascending=False)
    except Exception as e:
        print(f"Error in get_state_performance: {e}")
        return pd.DataFrame()

def get_cost_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarizes the total cost components (Manufacturing, Shipping, Overhead).

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        pd.DataFrame: A dataframe with 'Cost Component' and 'Total Cost' columns.
    """
    try:
        cost_cols = ['Manufacturing Cost', 'Shipping Cost', 'Overhead Cost']
        # Filter only existing columns
        existing_cols = [c for c in cost_cols if c in df.columns]
        if not existing_cols:
             return pd.DataFrame(columns=['Cost Component', 'Total Cost'])
             
        cost_summary = df[existing_cols].sum().reset_index()
        cost_summary.columns = ['Cost Component', 'Total Cost']
        return cost_summary
    except Exception as e:
        print(f"Error in get_cost_breakdown: {e}")
        return pd.DataFrame()

def get_customer_profitability(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates performance metrics by Customer ID (Simulated).

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        pd.DataFrame: A dataframe containing Sales, Gross Profit, Units, and Gross Margin % by Customer ID, ranked by Gross Profit.
    """
    try:
        if 'Customer ID' not in df.columns:
             return pd.DataFrame()
             
        cust_stats = df.groupby('Customer ID').agg({
            'Sales': 'sum',
            'Gross Profit': 'sum',
            'Units': 'sum'
        }).reset_index()
        
        cust_stats['Gross Margin (%)'] = (cust_stats['Gross Profit'] / cust_stats['Sales'] * 100)
        return cust_stats.sort_values(by='Gross Profit', ascending=False)
    except Exception as e:
        print(f"Error in get_customer_profitability: {e}")
        return pd.DataFrame()


