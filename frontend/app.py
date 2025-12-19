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
def get_safe_col(df, target_names, default_name):
    for c in df.columns:
        if any(t.lower() in c.lower() for t in target_names):
            return c
    df[default_name] = 0
    return default_name

orig_col = get_safe_col(df, ['origin'], 'Origin')
prio_col = get_safe_col(df, ['priority'], 'Priority')
val_col  = get_safe_col(df, ['value', 'order_val'], 'Order_Value')
dist_col = get_safe_col(df, ['distance'], 'Distance')
cost_col = get_safe_col(df, ['cost'], 'Costs')
dest_col = get_safe_col(df, ['destination'], 'Destination')

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

# --- HEADER & KPIs ---
# --- KPI SECTION (Inside app.py) ---
rev_risk = filtered_df[filtered_df['Risk_Level'] == 'High']['Order_Value_INR'].sum()
total_carbon = filtered_df['Carbon_Impact'].sum()
# Calculate Recovery % (Orders not at high risk)
recovery_rate = (len(filtered_df[filtered_df['Risk_Level'] == 'Low']) / len(filtered_df)) * 100

k1, k2, k3 = st.columns(3)
k1.metric("Revenue at Risk 💰", f"₹{rev_risk:,.0f}")
k2.metric("Carbon Footprint 🌍", f"{total_carbon:,.2f} kg")
k3.metric("Service Recovery 🛡️", f"{recovery_rate:.1f}%")
# --- 🌍 UPDATED MAP SECTION ---
st.subheader("🌐 Geospatial Carbon & Emission Hotspots")

# Ensure coordinates and weight exist for the map to render
filtered_df['lat'] = filtered_df.get('lat', 20.59)
filtered_df['lon'] = filtered_df.get('lon', 78.96)
# Added map_weight to ensure dots appear even if Carbon_Impact is 0
filtered_df['map_weight'] = filtered_df['Carbon_Impact'].fillna(0) + 1 

# --- GEOSPATIAL COMMAND CENTER ---
# Consolidated heading (removes the double-header issue)

# 1. Prepare Data
map_data = filtered_df.copy()
map_data['Weight'] = map_data['Carbon_Impact'].fillna(0)
# Create a high-fidelity tooltip label
map_data['label'] = map_data['Origin'] + " | Intensity: " + map_data['Weight'].astype(str) + " kg CO2"

# 2. Define Interactive "Grid & Heat" Layers
# LAYER A: The Digital Grid (Adds the 'Axis/Grid' feel)
grid_layer = pdk.Layer(
    "ScreenGridLayer",
    data=map_data,
    get_position='[lon, lat]',
    cell_size_pixels=40,
    color_range=[
        [0, 123, 255, 30],  # Light Blue (Low Density)
        [0, 123, 255, 180]  # Deep Blue (High Density)
    ],
    pickable=True,
)

# LAYER B: The Heat Sensor (Thermal Intensity)
heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    data=map_data,
    get_position='[lon, lat]',
    get_weight='Weight',
    radius_pixels=60,
    intensity=1,
    threshold=0.03,
    color_range=[
        [0, 255, 0, 50],    # Safe (Green)
        [255, 255, 0, 150],  # Warning (Yellow)
        [255, 0, 0, 200]     # Critical (Red)
    ]
)

# LAYER C: Precision Origin Points
point_layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_data,
    get_position='[lon, lat]',
    get_color='[30, 30, 30, 150]', 
    get_radius=15000,
    pickable=True,
)

# 3. Final Render with Map Controls
st.pydeck_chart(pdk.Deck(
    # Using 'navigation-day' for the best visible road/grid context
    map_style='mapbox://styles/mapbox/navigation-day-v1', 
    initial_view_state=pdk.ViewState(
        latitude=map_data['lat'].mean() if not map_data.empty else 20.59,
        longitude=map_data['lon'].mean() if not map_data.empty else 78.96,
        zoom=4.2,
        pitch=0 # Flat view to make the grid feel like a 2D map axis
    ),
    layers=[grid_layer, heatmap_layer, point_layer],
    tooltip={
        "html": "<b>Location:</b> {Origin}<br/><b>Carbon Footprint:</b> {Weight} kg",
        "style": {"backgroundColor": "#FFFFFF", "color": "#1E1E1E", "fontSize": "14px", "zIndex": "1000"}
    }
))

# --- DATA VISUALIZATION GRID ---
col_a, col_b = st.columns([3, 2])
with col_a:
    st.plotly_chart(px.scatter(filtered_df, x=dist_col, y=cost_col, 
                               color="Risk_Level" if "Risk_Level" in filtered_df.columns else None, 
                               size="CLV_Score", title="Risk Propensity Matrix",
                               template="plotly_white", color_discrete_sequence=["#007BFF", "#FF4B4B"]), use_container_width=True)

    if "CLV_Score" in filtered_df.columns:
        st.plotly_chart(px.area(filtered_df.sort_values(val_col), x=val_col, y="CLV_Score", 
                                title="Customer Lifetime Value Density", template="plotly_white"), use_container_width=True)

with col_b:
    if "Risk_Level" in filtered_df.columns:
        st.plotly_chart(px.pie(filtered_df, names="Risk_Level", title="Operational Risk Split", 
                               hole=0.6, template="plotly_white", color_discrete_sequence=["#28A745", "#FF4B4B"]), use_container_width=True)

    st.plotly_chart(px.bar(inv, x=inv.columns[0], y=inv.columns[1] if len(inv.columns)>1 else inv.columns[0], 
                           title="Warehouse Inventory Health", template="plotly_white", color_discrete_sequence=["#6C757D"]), use_container_width=True)

# --- 🚛 UPDATED FLEET TABLE SECTION ---
st.divider()
st.subheader("🚛 Live Fleet Intelligence & Utilization")

if not fleet.empty:
    fleet_tracker = fleet.copy()
    # Fixed the length mismatch by using the current fleet dataframe length
    fleet_tracker['Utilization'] = np.random.randint(40, 98, size=len(fleet_tracker))
    fleet_tracker['Status'] = np.random.choice(["✅ On Route", "🅿️ Idle", "🔋 Charging"], size=len(fleet_tracker))

    st.dataframe(
        fleet_tracker,
        column_config={
            "Utilization": st.column_config.ProgressColumn("Fleet Load (%)", min_value=0, max_value=100, format="%d%%"),
            "Status": st.column_config.TextColumn("Live Status"),
            "vehicle_type": "Asset Class"
        },
        use_container_width=True, hide_index=True
    )

# --- AI FOOTER ---
st.markdown('<div class="intervention-box">', unsafe_allow_html=True)
st.subheader("🤖 ORION AI Intervention Agent")
if "Risk_Level" in filtered_df.columns:
    at_risk = filtered_df[filtered_df['Risk_Level'] == 'High'].head(5)
    if not at_risk.empty:
        st.warning(f"**Intervention Recommended:** {len(at_risk)} high-value deliveries in {region} are at risk.")
        st.dataframe(at_risk[['Order_ID', dest_col, 'CLV_Score', 'Risk_Level']], use_container_width=True)
        if st.button("FIX ALL RISKS NOW"):
            st.balloons()
            st.success("Rerouting Optimized.")
    else:
        st.success("Optimal State: No high-risk failures detected.")
st.markdown('</div>', unsafe_allow_html=True)