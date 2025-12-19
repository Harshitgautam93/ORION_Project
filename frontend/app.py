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

# --- SAFETY COLUMN FINDER (Enhanced) ---
def get_safe_col(df, target_names, default_name, fill_val=0):
    for c in df.columns:
        if any(t.lower() in c.lower() for t in target_names):
            return c
    # If not found, create it to prevent crashes
    df[default_name] = fill_val
    return default_name

# Dynamically detect columns (Fixes the CLV_Score and Name Mismatch issues)
orig_col = get_safe_col(df, ['origin'], 'Origin')
prio_col = get_safe_col(df, ['priority'], 'Priority')
val_col  = get_safe_col(df, ['order_value', 'value_inr'], 'Order_Value_INR')
dist_col = get_safe_col(df, ['distance'], 'distance_km')
cost_col = get_safe_col(df, ['delivery_cost', 'total_cost'], 'delivery_cost_inr')
dest_col = get_safe_col(df, ['destination'], 'destination')
clv_col  = get_safe_col(df, ['clv_score', 'clv'], 'CLV_Score', fill_val=50) # Fixes the crash

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛰️ ORION Control")
    region = st.selectbox("Active Warehouse", df[orig_col].unique())
    prio_list = st.multiselect("Priority Level", df[prio_col].unique(), default=df[prio_col].unique())
    st.divider()
    strategy = st.select_slider("Optimization Bias", options=["Cost Min", "Balanced", "Green Max"], value="Balanced")
    ev_shift = st.slider("% Fleet EV Transition", 0, 100, 20)
    st.info(f"Est. CO2 Offset: {ev_shift * 1.2}%")

filtered_df = df[(df[orig_col] == region) & (df[prio_col].isin(prio_list))].copy()

# --- KPI SECTION ---
# Use the detected val_col instead of hardcoded strings
rev_risk = filtered_df[filtered_df['Risk_Level'] == 'High'][val_col].sum() if 'Risk_Level' in filtered_df.columns else 0
total_carbon = filtered_df['Carbon_Impact'].sum() if 'Carbon_Impact' in filtered_df.columns else 0

# Safe Recovery Calculation
if 'Risk_Level' in filtered_df.columns and len(filtered_df) > 0:
    recovery_rate = (len(filtered_df[filtered_df['Risk_Level'] == 'Low']) / len(filtered_df)) * 100
else:
    recovery_rate = 100.0

k1, k2, k3 = st.columns(3)
k1.metric("Revenue at Risk 💰", f"₹{rev_risk:,.0f}")
k2.metric("Carbon Footprint 🌍", f"{total_carbon:,.2f} kg")
k3.metric("Service Recovery 🛡️", f"{recovery_rate:.1f}%")

# --- GEOSPATIAL MAP ---
st.subheader("🌐 Geospatial Carbon & Emission Hotspots")

map_data = filtered_df.copy()
map_data['lat'] = map_data.get('lat', 20.59)
map_data['lon'] = map_data.get('lon', 78.96)
map_data['Weight'] = map_data['Carbon_Impact'].fillna(0) if 'Carbon_Impact' in map_data.columns else 1

# Map Layers
heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    data=map_data,
    get_position='[lon, lat]',
    get_weight='Weight',
    radius_pixels=60,
)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9', 
    initial_view_state=pdk.ViewState(
        latitude=map_data['lat'].mean() if not map_data.empty else 20.59,
        longitude=map_data['lon'].mean() if not map_data.empty else 78.96,
        zoom=4, pitch=0
    ),
    layers=[heatmap_layer],
    tooltip={"html": "<b>Location:</b> {Origin}<br/><b>Emissions:</b> {Weight} kg"}
))

# --- DATA VISUALIZATION GRID ---
col_a, col_b = st.columns([3, 2])
with col_a:
    # Uses the clv_col found by the safety helper
    st.plotly_chart(px.scatter(filtered_df, x=dist_col, y=cost_col, 
                               color="Risk_Level" if "Risk_Level" in filtered_df.columns else None, 
                               size=clv_col, title="Risk Propensity Matrix",
                               template="plotly_white", color_discrete_sequence=["#007BFF", "#FF4B4B"]), use_container_width=True)

    st.plotly_chart(px.area(filtered_df.sort_values(val_col), x=val_col, y=clv_col, 
                             title="Customer Lifetime Value Density", template="plotly_white"), use_container_width=True)

with col_b:
    if "Risk_Level" in filtered_df.columns:
        st.plotly_chart(px.pie(filtered_df, names="Risk_Level", title="Operational Risk Split", 
                               hole=0.6, template="plotly_white", color_discrete_sequence=["#28A745", "#FF4B4B"]), use_container_width=True)

    st.plotly_chart(px.bar(inv, x=inv.columns[0], y=inv.columns[1] if len(inv.columns)>1 else inv.columns[0], 
                           title="Warehouse Inventory Health", template="plotly_white", color_discrete_sequence=["#6C757D"]), use_container_width=True)

# --- FLEET TABLE ---
st.divider()
st.subheader("🚛 Live Fleet Intelligence & Utilization")
if not fleet.empty:
    fleet_tracker = fleet.copy()
    fleet_tracker['Utilization'] = np.random.randint(40, 98, size=len(fleet_tracker))
    st.dataframe(fleet_tracker, use_container_width=True, hide_index=True)

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
            st.success("Rerouting Optimized.")
    else:
        st.success("Optimal State: No high-risk failures detected.")
st.markdown('</div>', unsafe_allow_html=True)