🛰️ ORION | Order Risk & Intelligent Optimization Network
NexGen Logistics Intelligence Command Center
📌 1. Project Overview & Problem Statement
The Mission: To transform NexGen Logistics from reactive operations to a predictive "Command Center."

The Core Problem: * Data Silos: Logistics data is scattered across 7+ inconsistent CSV files.

Performance Gaps: Significant delays between "Promised" vs. "Actual" delivery dates.

Sustainability Blindness: High operational costs paired with a lack of CO2 emission transparency.

Revenue Risk: High-value customers (High CLV) are often impacted by unmonitored traffic and weather delays.

⚙️ 2. The "Self-Healing" Data Pipeline
To handle real-world data inconsistencies, ORION uses a robust backend engine featuring:

Fuzzy Column Mapping: Automatically resolves naming mismatches (e.g., "order_val" vs "Order_Value_INR") and handles whitespace/casing issues.

Dynamic Asset Injection: If a dataset is missing a vehicle_type, the engine uses a weighted random distribution from the fleet database to maintain integrity.

Multi-Way Schema Integration: Performs complex Left Joins on Order_ID to ensure recent "In-Transit" orders are included in the analysis.

Automated Sanitization: Cleans outliers in order values and fills missing coordinates for geospatial mapping.

🧬 3. Advanced Feature Engineering
ORION creates three proprietary metrics to drive decision-making:

Tri-Factor Optimization Score: A balanced metric weighing Profit, Carbon Footprint, and Time.

Dynamic CLV Score: * Formula: (Order_Value / Max_Value * 70) + (Customer_Rating / 5 * 30).

Purpose: Identifies high-priority customers for "White-Glove" service recovery.

Carbon Impact Tracker: * Formula: Distance_KM * CO2_Factor_per_Vehicle_Type.

Purpose: Provides real-time visibility into the environmental cost of every delivery.

📊 4. Interactive Dashboard Features
🌐 Geospatial Emission Hotspots: A PyDeck-powered heatmap identifying high-pollution transit corridors.

⚠️ Risk Propensity Matrix: A Plotly scatter plot mapping Distance vs. Cost, sized by CLV Score and colored by Risk Level.

📦 Warehouse Health Tracker: Visualizes inventory stock levels against reorder points to prevent stockouts of critical industrial goods.

🤖 AI Intervention Agent: * Scans for "High Risk" deliveries.

Provides Explainable AI (XAI) Badges explaining why an order is flagged (e.g., "High Traffic + Fragile Cargo").

Includes a "Fix All Risks" optimization trigger.

💻 5. Technical Stack
Language: Python 3.8+

Framework: Streamlit (Web Interface)

Data Science: Pandas (Wrangling), NumPy (Calculations)

Visualization: Plotly (Interactive Charts), PyDeck (Mapping), Mapbox (Satellite Layer)

📈 6. Business Impact & ROI
Cost Reduction: Targets a 15–20% decrease in operational overhead through optimized vehicle-to-order matching.

Revenue Protection: Proactively saves high-value orders from failure, reducing churn.

Sustainability: Enables a data-driven transition to EVs by highlighting the highest CO2-producing routes.

Operational Speed: Consolidates 7 separate reports into a single, real-time "Pulse" KPI row.

🛠️ 7. Installation & Setup
Clone Repository: ```bash git clone https://github.com/Harshitgautam93/ORION_Project

Install Requirements: ```bash pip install -r requirements.txt

Launch App: ```bash streamlit run frontend/app.py


🗺️ 8. Future Roadmap
NLP AI Agent: Integration to allow queries like "What is the revenue impact of a 10% fuel hike?"

Predictive Maintenance: Automated alerts when a vehicle's fuel efficiency drops below the fleet average.

What-if Sandboxes: Simulation sliders for testing the impact of new carbon taxes or labor cost changes.

Developed for the ORION Logistics Intelligence Challenge.
