import pandas as pd
import copy
from typing import Dict, Any

def run_scenario(df: pd.DataFrame, mfg_cost_change_pct: float, shipping_cost_change_pct: float, price_change_pct: float) -> Dict[str, Any]:
    """
    Calculates the impact of cost and price changes on profitability.
    
    Args:
        df (pd.DataFrame): Input dataframe.
        mfg_cost_change_pct (float): Percentage change in manufacturing cost (e.g., 5.0 for +5%).
        shipping_cost_change_pct (float): Percentage change in shipping cost.
        price_change_pct (float): Percentage change in sales price.
        
    Returns:
        Dict[str, Any]: A dictionary containing key metrics for the scenario. Returns default zero-values dict if error occurs.
    """
    try:
        # Work on a copy to avoid modifying the original dataframe in session state
        scenario_df = df.copy()
        
        # Apply changes
        # 1. Price Change
        if price_change_pct != 0:
            scenario_df['Sales'] = scenario_df['Sales'] * (1 + price_change_pct / 100)
        
        # 2. Cost Changes
        # Assuming 'Manufacturing Cost' and 'Shipping Cost' columns exist from feature engineering
        if 'Manufacturing Cost' in scenario_df.columns:
            scenario_df['Manufacturing Cost'] = scenario_df['Manufacturing Cost'] * (1 + mfg_cost_change_pct / 100)
        else:
            # Fallback if detailed components are missing (approx 70% of total cost)
            if 'Cost' in scenario_df.columns:
                scenario_df['Manufacturing Cost'] = scenario_df['Cost'] * 0.7 * (1 + mfg_cost_change_pct / 100)
            
        if 'Shipping Cost' in scenario_df.columns:
            scenario_df['Shipping Cost'] = scenario_df['Shipping Cost'] * (1 + shipping_cost_change_pct / 100)
        else:
            # Fallback (approx 20% of total cost)
            if 'Cost' in scenario_df.columns:
                 scenario_df['Shipping Cost'] = scenario_df['Cost'] * 0.2 * (1 + shipping_cost_change_pct / 100)
            
        # Recalculate Total Cost (Manufacturing + Shipping + Overhead (assume fixed))
        # Note: Overhead might not be in the df if it was just created in get_cost_breakdown, 
        # but feature_engineering adds it.
        if 'Overhead Cost' not in scenario_df.columns and 'Cost' in scenario_df.columns:
             scenario_df['Overhead Cost'] = scenario_df['Cost'] * 0.1
             
        if 'Manufacturing Cost' in scenario_df.columns and 'Shipping Cost' in scenario_df.columns and 'Overhead Cost' in scenario_df.columns:
            scenario_df['New Cost'] = scenario_df['Manufacturing Cost'] + scenario_df['Shipping Cost'] + scenario_df['Overhead Cost']
        elif 'Cost' in scenario_df.columns:
            # Simplistic fallback if breakdown completely failed
            scenario_df['New Cost'] = scenario_df['Cost']
        else:
            scenario_df['New Cost'] = 0
        
        # Recalculate Profit
        if 'New Cost' in scenario_df.columns:
            scenario_df['New Gross Profit'] = scenario_df['Sales'] - scenario_df['New Cost']
        else:
            scenario_df['New Gross Profit'] = scenario_df['Gross Profit'] # No change if no cost info
        
        # Aggregated Metrics
        original_sales = df['Sales'].sum()
        original_profit = df['Gross Profit'].sum()
        original_margin = (original_profit / original_sales) * 100 if original_sales else 0
        
        new_sales = scenario_df['Sales'].sum()
        new_profit = scenario_df['New Gross Profit'].sum()
        new_margin = (new_profit / new_sales) * 100 if new_sales else 0
        
        return {
            'Original Sales': original_sales,
            'Original Profit': original_profit,
            'Original Margin': original_margin,
            'New Sales': new_sales,
            'New Profit': new_profit,
            'New Margin': new_margin,
            'Profit Change': new_profit - original_profit,
            'Margin Change': new_margin - original_margin
        }
    except Exception as e:
        print(f"Error in run_scenario: {e}")
        return {
            'Original Sales': 0, 'Original Profit': 0, 'Original Margin': 0,
            'New Sales': 0, 'New Profit': 0, 'New Margin': 0,
            'Profit Change': 0, 'Margin Change': 0
        }
