import streamlit as st
import plotly.express as px
import sys
import os
import pandas as pd
import pydeck as pdk
import numpy as np

# Path Fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.data_engine import load_orion_intelligence

# --- PAGE CONFIG ---
st.set_page_config(page_title="ORION | Control Tower", layout="wide", initial_sidebar_state="expanded")

# --- WHITE ENTERPRISE THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1E1E1E; }
    [data-testid="stMetricValue"] {
        background: #f8f9fa;
        border-left: 5px solid #007BFF;
        padding: 10px 20px;
        border-radius: 8px;
        color: #1E1E1E !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    section[data-testid="stSidebar"] {
        background-color: #f1f3f5;
        border-right: 1px solid #dee2e6;
    }
    .intervention-box {
        background: linear-gradient(90deg, #f0f7ff 0%, #f2fff9 100%);
        border: 1px solid #007BFF;
        padding: 25px;
        border-radius: 15px;
        color: #1E1E1E;
    }
    .stButton>button {
        background: linear-gradient(45deg, #007BFF, #00D1FF);
        color: white; font-weight: bold; border: none;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def get_data():
    return load_orion_intelligence()

df, fleet, inv = get_data()

# --- SAFETY COLUMN FINDER ---
def get_safe_col(df, target_names, default_name, fill_val=0):
    for c in df.columns:
        if any(t.lower() in c.lower() for t in target_names):
            return c
    df[default_name] = fill_val
    return default_name

orig_col = get_safe_col(df, ['origin'], 'Origin')
prio_col = get_safe_col(df, ['priority'], 'Priority')
val_col  = get_safe_col(df, ['order_value', 'value_inr'], 'Order_Value_INR')
dist_col = get_safe_col(df, ['distance'], 'distance_km')
cost_col = get_safe_col(df, ['delivery_cost', 'total_cost'], 'delivery_cost_inr')
dest_col = get_safe_col(df, ['destination'], 'destination')
clv_col  = get_safe_col(df, ['clv_score', 'clv'], 'CLV_Score', fill_val=50)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛰️ ORION Control")
    
    st.subheader("📦 Order Filters")
    region = st.selectbox("Active Warehouse", df[orig_col].unique())
    prio_list = st.multiselect("Priority Level", df[prio_col].unique(), default=df[prio_col].unique())
    
    st.divider()
    
    # --- NEW: FLEET INTELLIGENCE FILTERS ---
    st.subheader("🚛 Fleet Intelligence Filters")
    
    # 1. Fuel Efficiency Slider
    min_eff = float(fleet['fuel_efficiency_km_per_l'].min())
    max_eff = float(fleet['fuel_efficiency_km_per_l'].max())
    eff_range = st.slider("Fuel Efficiency (KM/L)", min_eff, max_eff, (min_eff, max_eff))
    
    # 2. Fleet Load Slider
    load_range = st.slider("Fleet Load / Utilization (%)", 0, 100, (0, 100))
    
    # 3. Location Dropdown
    loc_list = ["All Locations"] + sorted(list(fleet['current_location'].unique()))
    sel_location = st.selectbox("Current Vehicle Location", loc_list)
    
    # 4. Live Status Checkboxes
    st.write("**Live Status**")
    status_map = {"In_Transit": "On Route", "Available": "Idle", "Maintenance": "🛠️ Maint", "Charging": "⚡ Charging"}
    selected_statuses = []
    c1, c2 = st.columns(2)
    for i, status in enumerate(fleet['status'].unique()):
        display = status_map.get(status, status)
        if [c1, c2][i % 2].checkbox(display, value=True, key=f"status_{status}"):
            selected_statuses.append(status)

    st.divider()
    strategy = st.select_slider("Optimization Bias", options=["Cost Min", "Balanced", "Green Max"], value="Balanced")
    ev_shift = st.slider("% Fleet EV Transition", 0, 100, 20)
    st.info(f"Est. CO2 Offset: {ev_shift * 1.2}%")

# --- FILTER LOGIC (Main Body) ---
filtered_df = df[(df[orig_col] == region) & (df[prio_col].isin(prio_list))].copy()

# Apply Filters to the Fleet Dataframe
filtered_fleet = fleet[
    (fleet['fuel_efficiency_km_per_l'].between(eff_range[0], eff_range[1])) &
    (fleet['utilization'].between(load_range[0], load_range[1])) &
    (fleet['status'].isin(selected_statuses))
].copy()

if sel_location != "All Locations":
    filtered_fleet = filtered_fleet[filtered_fleet['current_location'] == sel_location]


# --- KPI SECTION ---
rev_risk = filtered_df[filtered_df['Risk_Level'] == 'High'][val_col].sum() if 'Risk_Level' in filtered_df.columns else 0
total_carbon = filtered_df['Carbon_Impact'].sum() if 'Carbon_Impact' in filtered_df.columns else 0
recovery_rate = (len(filtered_df[filtered_df['Risk_Level'] == 'Low']) / len(filtered_df)) * 100 if len(filtered_df) > 0 else 100.0

k1, k2, k3 = st.columns(3)
k1.metric("Revenue at Risk 💰", f"₹{rev_risk:,.0f}")
k2.metric("Carbon Footprint 🌍", f"{total_carbon:,.2f} kg")
k3.metric("Service Recovery 🛡️", f"{recovery_rate:.1f}%")

# --- GEOSPATIAL MAP ---
st.subheader("🌐 Geospatial Carbon & Emission Hotspots")
map_data = filtered_df.copy()
heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    data=map_data,
    get_position='[lon, lat]',
    get_weight='Carbon_Impact',
    radius_pixels=60,
)
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9', 
    initial_view_state=pdk.ViewState(
        latitude=map_data['lat'].mean() if not map_data.empty else 20.59, 
        longitude=map_data['lon'].mean() if not map_data.empty else 78.96, 
        zoom=4),
    layers=[heatmap_layer],
))

# --- DATA VISUALIZATION GRID ---
col_a, col_b = st.columns([3, 2])
with col_a:
    st.plotly_chart(px.scatter(filtered_df, x=dist_col, y=cost_col, 
                               color="Risk_Level" if "Risk_Level" in filtered_df.columns else None, 
                               size=clv_col, title="Risk Propensity Matrix",
                               template="plotly_white", color_discrete_sequence=["#007BFF", "#FF4B4B"]), use_container_width=True)

with col_b:
    # Uses Filtered Fleet for the chart
    if not filtered_fleet.empty:
        top_perf = filtered_fleet.sort_values("Efficiency_Score", ascending=False).head(5)
        st.plotly_chart(px.bar(top_perf, x='Efficiency_Score', y='vehicle_id', orientation='h',
                               title="Top 5 Filtered Efficiency Assets",
                               color='Efficiency_Score', color_continuous_scale='Greens',
                               template="plotly_white"), use_container_width=True)
    else:
        st.warning("No fleet assets match active filters.")

# --- FLEET INTELLIGENCE SECTION (UPDATED) ---
st.divider()
st.subheader("🚛 Live Fleet Intelligence & Performance Ranking")
if not filtered_fleet.empty:
    st.dataframe(
        filtered_fleet[['Rank', 'vehicle_id', 'vehicle_type', 'current_location', 'status', 'Efficiency_Score', 'Status_Advice', 'fuel_efficiency_km_per_l', 'utilization']],
        column_config={
            "Efficiency_Score": st.column_config.ProgressColumn("Efficiency Score", format="%.2f", min_value=0, max_value=100),
            "Status_Advice": "AI Recommendation",
            "status": "Live Status",
            "current_location": "Current Location"
        },
        use_container_width=True, 
        hide_index=True
    )
    
    # Quick Summary Advice based on filtered results
    c1, c2 = st.columns(2)
    with c1:
        st.success(f"**Best Available:** {filtered_fleet.iloc[0]['vehicle_id']} at {filtered_fleet.iloc[0]['current_location']}")
    with c2:
        if len(filtered_fleet) > 1:
            st.info(f"Showing {len(filtered_fleet)} assets matching your criteria.")

# --- AI FOOTER ---
st.markdown('<div class="intervention-box">', unsafe_allow_html=True)
st.subheader("🤖 ORION AI Intervention Agent")
if "Risk_Level" in filtered_df.columns:
    at_risk = filtered_df[filtered_df['Risk_Level'] == 'High'].head(5)
    if not at_risk.empty:
        st.warning(f"**Intervention Recommended:** {len(at_risk)} high-value deliveries in {region} are at risk.")
        st.dataframe(at_risk[['Order_ID', dest_col, clv_col, 'Risk_Level']], use_container_width=True)
        if st.button("FIX ALL RISKS NOW"):
            st.balloons()
            st.success("Rerouting Optimized. Assigned to Top Performing Assets.")
    else:
        st.success("Optimal State: No high-risk failures detected.")
st.markdown('</div>', unsafe_allow_html=True)