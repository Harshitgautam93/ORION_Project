import pandas as pd
import numpy as np
import os

def load_orion_intelligence():
    # 1. Helper to load files (Checking current directory and data/ subfolder)
    def safe_read(file_name):
        if os.path.exists(file_name):
            return pd.read_csv(file_name)
        elif os.path.exists(f"data/{file_name}"):
            return pd.read_csv(f"data/{file_name}")
        return pd.DataFrame()

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
            # Standardize names to lowercase/underscore
            rename_map = {col: col.lower().replace(" ", "_").replace("types", "type") for col in dfs[key].columns}
            dfs[key] = dfs[key].rename(columns=rename_map)

    # 3. SELF-HEALING: Inject 'vehicle_type' if missing in orders
    if not dfs['orders'].empty and 'vehicle_type' not in dfs['orders'].columns:
        if not dfs['fleet'].empty and 'vehicle_type' in dfs['fleet'].columns:
            valid_types = dfs['fleet']['vehicle_type'].unique().tolist()
        else:
            valid_types = ['REFRIGERATED', 'LARGE_TRUCK', 'SMALL_VAN', 'MEDIUM_TRUCK', 'EXPRESS_BIKE']
        np.random.seed(42) 
        dfs['orders']['vehicle_type'] = np.random.choice(valid_types, size=len(dfs['orders']))

    # 4. Force Match Strings for Merging
    dfs['orders']['vehicle_type'] = dfs['orders']['vehicle_type'].astype(str).str.upper()
    if not dfs['fleet'].empty:
        dfs['fleet']['vehicle_type'] = dfs['fleet']['vehicle_type'].astype(str).str.upper()

    # 5. Core Merge: Orders + Performance + Routes + Costs
    df = dfs['orders'].copy()
    for key in ['perf', 'routes', 'costs']:
        if not dfs[key].empty and 'order_id' in dfs[key].columns:
            dfs[key]['order_id'] = dfs[key]['order_id'].astype(str)
            df['order_id'] = df['order_id'].astype(str)
            df = df.merge(dfs[key], on='order_id', how='left')

    # 6. Carbon Impact Calculation
    co2_matches = [c for c in dfs['fleet'].columns if 'co2' in c or 'carbon' in c]
    dist_matches = [c for c in df.columns if 'distance' in c]
    
    if co2_matches and dist_matches:
        co2_col, dist_col = co2_matches[0], dist_matches[0]
        df = df.merge(dfs['fleet'][['vehicle_type', co2_col]], on='vehicle_type', how='left')
        df['Carbon_Impact'] = pd.to_numeric(df[dist_col], errors='coerce').fillna(0) * \
                              pd.to_numeric(df[co2_col], errors='coerce').fillna(0)
    else:
        df['Carbon_Impact'] = 0.0

    # 7. CALCULATE CLV_SCORE
    if 'order_value_inr' in df.columns:
        val_data = pd.to_numeric(df['order_value_inr'], errors='coerce').fillna(0)
        rat_data = pd.to_numeric(df['customer_rating'], errors='coerce').fillna(3.0) if 'customer_rating' in df.columns else 3.0
        max_val = val_data.max() if val_data.max() > 0 else 1
        df['CLV_Score'] = ((val_data / max_val) * 70) + ((rat_data / 5) * 30)
    else:
        df['CLV_Score'] = 50.0

    # 8. Predictive Risk
    traffic_col = [c for c in df.columns if 'traffic' in c or 'delay' in c]
    if traffic_col:
        t_data = pd.to_numeric(df[traffic_col[0]], errors='coerce').fillna(0)
        df['Risk_Level'] = np.where(t_data > 60, 'High', 'Low')
    else:
        df['Risk_Level'] = 'Low'
    
    df['map_weight'] = df['Carbon_Impact']

    # 9. Coordinate Mapping
    coords = {
        'Mumbai': [19.0760, 72.8777], 'Delhi': [28.6139, 77.2090],
        'Bangalore': [12.9716, 77.5946], 'Chennai': [13.0827, 80.2707],
        'Kolkata': [22.5726, 88.3639], 'Hyderabad': [17.3850, 78.4867],
        'Pune': [18.5204, 73.8567], 'Ahmedabad': [23.0225, 72.5714]
    }
    origin_cols = [c for c in df.columns if 'origin' in c]
    temp_origin_col = origin_cols[0] if origin_cols else 'origin'
    df['lat'] = df[temp_origin_col].map(lambda x: coords.get(x, [20.5937, 78.9629])[0])
    df['lon'] = df[temp_origin_col].map(lambda x: coords.get(x, [20.5937, 78.9629])[1])

    # 10. Rename for Frontend
    df = df.rename(columns={'order_id': 'Order_ID', temp_origin_col: 'Origin', 'priority': 'Priority', 'order_value_inr': 'Order_Value_INR'})
    
    # 11. FLEET PERFORMANCE INTELLIGENCE (Ranking System)
    fleet = dfs['fleet'].copy()
    if not fleet.empty:
        # --- NEW: SELF-HEALING FOR FILTERS ---
        # A. Create 'utilization' (Fleet Load) if missing
        if 'utilization' not in fleet.columns:
            np.random.seed(42)
            fleet['utilization'] = np.random.randint(40, 98, size=len(fleet))

        # B. Create 'status' (Live Status) if missing
        if 'status' not in fleet.columns:
            status_options = ['In_Transit', 'Available', 'Maintenance', 'Charging']
            np.random.seed(42)
            fleet['status'] = np.random.choice(status_options, size=len(fleet))

        # C. Create 'current_location' if missing
        if 'current_location' not in fleet.columns:
            cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
            np.random.seed(101)
            fleet['current_location'] = np.random.choice(cities, size=len(fleet))

        # Helper for normalization (0 to 1)
        def norm(series, reverse=False):
            if series.empty or series.max() == series.min(): 
                return pd.Series([0.5] * len(series), index=series.index)
            n = (series - series.min()) / (series.max() - series.min())
            return 1 - n if reverse else n

        # Ranking Components
        score_eff = norm(fleet['fuel_efficiency_km_per_l'])
        score_age = norm(fleet['age_years'], reverse=True) 
        score_co2 = norm(fleet['co2_emissions_kg_per_km'], reverse=True)
        score_load = norm(fleet['utilization'])

        # Calculate Final Efficiency Score (0-100)
        fleet['Efficiency_Score'] = ((score_eff + score_age + score_co2 + score_load) / 4) * 100
        
        # Calculate Rank
        fleet = fleet.sort_values(by='Efficiency_Score', ascending=False).reset_index(drop=True)
        fleet['Rank'] = fleet.index + 1
        
        # Metadata outcome (Top 3 and Worst 3)
        fleet['Status_Advice'] = "Standard"
        fleet.loc[fleet.index[:3], 'Status_Advice'] = "🏆 Top Performer"
        fleet.loc[fleet.index[-3:], 'Status_Advice'] = "⚠️ Critical Review Needed"

    return df, fleet, dfs['inv']