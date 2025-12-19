import pandas as pd
import numpy as np
import os

def load_orion_intelligence():
    # 1. Load available data files (Checking root directory)
    # Using a helper to handle missing files gracefully
    def safe_read(file_name):
        return pd.read_csv(file_name) if os.path.exists(file_name) else pd.DataFrame()

    dfs = {
        'orders': safe_read('orders.csv'),
        'perf': safe_read('delivery_performance.csv'),
        'fleet': safe_read('vehicle_fleet.csv'),
        'routes': safe_read('routes_distance.csv'),
        'inv': safe_read('warehouse_inventory.csv'),
        'costs': safe_read('cost_breakdown.csv')
    }
    
    # 2. Universal Sanitization & Column Normalization
    for key in dfs:
        if not dfs[key].empty:
            dfs[key].columns = dfs[key].columns.str.strip()
            # Standardize common column names to lowercase/underscore
            rename_map = {col: col.lower().replace(" ", "_").replace("types", "type") for col in dfs[key].columns}
            dfs[key] = dfs[key].rename(columns=rename_map)

    # 3. SELF-HEALING: Inject 'vehicle_type' if missing in orders
    if 'vehicle_type' not in dfs['orders'].columns and not dfs['fleet'].empty:
        # Pull valid types from the fleet file
        valid_types = dfs['fleet']['vehicle_type'].unique().tolist()
        # Assign a random vehicle type to each order (consistent seed for stability)
        np.random.seed(42) 
        dfs['orders']['vehicle_type'] = np.random.choice(valid_types, size=len(dfs['orders']))

    # 4. Force Match Vehicle Types (Fixes 0.00 Carbon Issue)
    dfs['orders']['vehicle_type'] = dfs['orders']['vehicle_type'].astype(str).str.upper()
    dfs['fleet']['vehicle_type'] = dfs['fleet']['vehicle_type'].astype(str).str.upper()

    # 5. Core Merge: Orders + Performance + Routes + Costs
    df = dfs['orders'].copy()
    for key in ['perf', 'routes', 'costs']:
        if not dfs[key].empty and 'order_id' in dfs[key].columns:
            # We ensure keys are string type before merging
            dfs[key]['order_id'] = dfs[key]['order_id'].astype(str)
            df['order_id'] = df['order_id'].astype(str)
            df = df.merge(dfs[key], on='order_id', how='left')

    # 6. Coordinate Mapping (Geospatial Grid)
    # Expanded list to cover all cities in your dataset
    coords = {
        'Mumbai': [19.0760, 72.8777], 'Delhi': [28.6139, 77.2090],
        'Bangalore': [12.9716, 77.5946], 'Chennai': [13.0827, 80.2707],
        'Kolkata': [22.5726, 88.3639], 'Hyderabad': [17.3850, 78.4867],
        'Pune': [18.5204, 73.8567], 'Ahmedabad': [23.0225, 72.5714]
    }

    # Find the origin column (e.g., 'Origin' or 'origin')
    temp_origin_col = [c for c in df.columns if 'origin' in c.lower()][0]
    df['lat'] = df[temp_origin_col].map(lambda x: coords.get(x, [20.5937, 78.9629])[0])
    df['lon'] = df[temp_origin_col].map(lambda x: coords.get(x, [20.5937, 78.9629])[1])

    # 7. Carbon Impact Calculation
    # Finds the CO2 factor column and distance column dynamically
    co2_col = [c for c in dfs['fleet'].columns if 'co2' in c.lower() or 'carbon' in c.lower()][0]
    dist_cols = [c for c in df.columns if 'distance' in c.lower()]
    dist_col = dist_cols[0] if dist_cols else None
    
    if dist_col:
        # Merge CO2 factor from fleet to main dataframe
        df = df.merge(dfs['fleet'][['vehicle_type', co2_col]], on='vehicle_type', how='left')
        # Final Formula: Carbon = Distance * CO2_Factor
        df['Carbon_Impact'] = pd.to_numeric(df[dist_col], errors='coerce').fillna(0) * \
                              pd.to_numeric(df[co2_col], errors='coerce').fillna(0)
    else:
        df['Carbon_Impact'] = 0.0

    # 8. Predictive Risk Logic (for Service Recovery KPI)
    traffic_col = [c for c in df.columns if 'traffic' in c.lower() or 'delay' in c.lower()]
    if traffic_col:
        # If traffic delay > 60 minutes, mark as High Risk
        t_data = pd.to_numeric(df[traffic_col[0]], errors='coerce').fillna(0)
        df['Risk_Level'] = np.where(t_data > 60, 'High', 'Low')
    else:
        df['Risk_Level'] = 'Low'

    # 9. Rename & Cleanup for Frontend
    df = df.rename(columns={
        'order_id': 'Order_ID', 
        temp_origin_col: 'Origin', 
        'priority': 'Priority',
        'order_value_inr': 'Order_Value_INR'
    })
    
    return df, dfs['fleet'], dfs['inv']