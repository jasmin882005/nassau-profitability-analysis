import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from typing import List, Optional

def generate_forecast(df: pd.DataFrame, periods: int = 6) -> pd.DataFrame:
    """
    Generates a sales and profit forecast for the specified number of months.
    
    Args:
        df (pd.DataFrame): The input dataframe containing 'Order Date', 'Sales', and 'Gross Profit'.
        periods (int): Number of months to forecast.
        
    Returns:
        pd.DataFrame: A DataFrame containing historical and forecasted data. Returns original reshaped data if forecast fails.
    """
    # Prepare data
    df_copy = df.copy()
    if 'Order Date' not in df_copy.columns:
         return df_copy
         
    df_copy['Order Date'] = pd.to_datetime(df_copy['Order Date'])
    monthly_data = df_copy.groupby(pd.Grouper(key='Order Date', freq='M')).agg({
        'Sales': 'sum',
        'Gross Profit': 'sum'
    }).reset_index()
    
    # Ensure regular frequency
    monthly_data.set_index('Order Date', inplace=True)
    monthly_data.index.freq = 'M'
    
    forecast_results: List[pd.DataFrame] = []
    
    for col in ['Sales', 'Gross Profit']:
        try:
            # Fit Holt-Winters model (Trend + Seasonality)
            # Use 'add' (additive) trend/seasonal if no zeros/negatives, otherwise might need care.
            # Sales/Profit can be high, additive is usually safe for this scale.
            model = ExponentialSmoothing(
                monthly_data[col],
                trend='add',
                seasonal='add',
                seasonal_periods=12
            ).fit()
            
            # Forecast
            forecast = model.forecast(periods)
            
            # Create a localized dataframe for this metric's forecast
            fc_df = pd.DataFrame({
                'Order Date': forecast.index,
                f'{col}': forecast.values,
                'Type': 'Forecast'
            })
            
            # Add to results
            if not forecast_results:
                forecast_results.append(fc_df)
            else:
                forecast_results[0][col] = fc_df[col]
                
        except Exception as e:
            print(f"Forecasting error for {col}: {e}")
            # Fallback: Simple Moving Average or Naive
            if not monthly_data.empty:
                last_value = monthly_data[col].iloc[-1]
                if not monthly_data.index.empty:
                    start_date = monthly_data.index[-1] + pd.DateOffset(months=1)
                else:
                    start_date = pd.Timestamp.now()
                    
                dates = pd.date_range(start=start_date, periods=periods, freq='M')
                fc_df = pd.DataFrame({
                    'Order Date': dates,
                    f'{col}': [last_value] * periods,
                    'Type': 'Forecast'
                })
                if not forecast_results:
                    forecast_results.append(fc_df)
                else:
                    forecast_results[0][col] = fc_df[col]
            else:
                # If truly empty, create dummy
                pass

    # Combine History and Forecast
    history = monthly_data.reset_index()
    history['Type'] = 'Historical'
    
    if forecast_results:
        forecast_final = forecast_results[0]
        combined = pd.concat([history, forecast_final], ignore_index=True)
        return combined
    else:
        return history
