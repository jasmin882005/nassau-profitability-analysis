import pandas as pd
import numpy as np
import os
from typing import Optional

def load_data(filepath: str) -> Optional[pd.DataFrame]:
    """
    Loads data from a CSV file.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: The loaded dataframe, or None if an error occurs.
    """
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataframe by handling dates, numeric conversions, and missing values.

    Args:
        df (pd.DataFrame): The raw dataframe.

    Returns:
        pd.DataFrame: The cleaned dataframe. Returns empty dataframe if error occurs.
    """
    try:
        # Date conversion
        date_cols = ['Order Date', 'Ship Date']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], format='%d-%m-%Y', errors='coerce')

        # Numeric conversion (just in case)
        numeric_cols = ['Sales', 'Units', 'Gross Profit', 'Cost']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows with critical missing values
        df.dropna(subset=['Sales', 'Units', 'Gross Profit'], inplace=True)
        
        # Sort by Order Date
        if 'Order Date' in df.columns:
            df.sort_values(by='Order Date', inplace=True)

        return df
    except Exception as e:
        print(f"Error cleaning data: {e}")
        return pd.DataFrame()

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds calculated columns to the dataframe, including margin percentages and simulated data.

    Args:
        df (pd.DataFrame): The cleaned dataframe.

    Returns:
        pd.DataFrame: The dataframe with added features. Returns original df if error occurs.
    """
    try:
        # Gross Margin Percentage
        # Avoid division by zero
        df['Gross Margin (%)'] = df.apply(lambda row: (row['Gross Profit'] / row['Sales'] * 100) if row['Sales'] != 0 else 0, axis=1)
        
        # Profit per Unit
        df['Profit per Unit'] = df.apply(lambda row: (row['Gross Profit'] / row['Units']) if row['Units'] != 0 else 0, axis=1)

        # --- Data Simulation for Analytical Depth ---
        np.random.seed(42) # For reproducibility
        
        # 1. Simulate Customer ID
        # Assume repeat customers exist. Generate 500 unique customer IDs.
        customer_ids = [f"CUST-{i:04d}" for i in range(1, 501)]
        df['Customer ID'] = np.random.choice(customer_ids, size=len(df))
        
        # 2. Simulate Customer Segment
        # Randomly assign segments
        segments = ['Wholesale', 'Retail', 'Online', 'Corporate']
        df['Customer Segment'] = np.random.choice(segments, size=len(df), p=[0.4, 0.3, 0.2, 0.1])

        # 3. Simulate Product Category
        # Randomly assign categories
        categories = ['Sweets', 'Chocolates', 'Savory', 'Beverages', 'Gifts']
        df['Product Category'] = np.random.choice(categories, size=len(df))

        # 4. Simulate Cost Components (Manufacturing ~70%, Shipping ~20%, Overhead ~10%)
        # Add some random variation
        if 'Cost' in df.columns:
            df['Manufacturing Cost'] = df['Cost'] * np.random.uniform(0.65, 0.75, size=len(df))
            df['Shipping Cost'] = df['Cost'] * np.random.uniform(0.15, 0.25, size=len(df))
            df['Overhead Cost'] = df['Cost'] - df['Manufacturing Cost'] - df['Shipping Cost']
            
            # Ensure no negative costs due to rounding/subtraction
            df['Overhead Cost'] = df['Overhead Cost'].apply(lambda x: max(x, 0))

        return df
    except Exception as e:
        print(f"Error in feature engineering: {e}")
        return df

if __name__ == "__main__":
    # Test execution
    # Use relative path from the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "data", "Nassau Candy Distributor.csv")
    
    print(f"Looking for data at: {data_path}")

    if os.path.exists(data_path):
        df = load_data(data_path)
        if df is not None:
            print("Data loaded successfully.")
            print(f"Initial shape: {df.shape}")
            
            df = clean_data(df)
            print("Data cleaned.")
            
            df = feature_engineering(df)
            print("Features engineered.")
            print(f"Final shape: {df.shape}")
            print(df.head())
        else:
            print("Failed to load dataframe.")
    else:
        print("File not found.")
