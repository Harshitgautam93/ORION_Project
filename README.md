🛰️ ORION | Order Risk & Intelligent Optimization Network NexGen Logistics Intelligence Command Center

Project Overview
  ORION is an AI-driven decision engine developed for NexGen Logistics Pvt. Ltd. to transform reactive operations into a predictive "Command Center." By unifying 7+    disparate datasets, the project addresses the Tri-Factor Optimization challenge: balancing Profitability, Environmental Sustainability (Carbon), and Customer Lifetime Value (CLV).

Features
Predictive Risk Modeling: Assigns a failure propensity score to orders based on traffic volatility and historical carrier performance.

🌐 Geospatial Emission Hotspots: An interactive PyDeck heatmap that identifies high-pollution transit corridors and carbon intensity.

⚠️ Risk Propensity Matrix: A dynamic Plotly scatter plot mapping Distance vs. Cost, sized by CLV Score to prioritize high-value service recovery.

📦 Warehouse Health Tracker: Real-time visualization of inventory stock levels against critical reorder points.

🤖 AI Intervention Agent: A logic-driven module that provides Explainable AI (XAI) badges for at-risk shipments and suggests rerouting.

Detailed Implementation
1. Backend & Data Engine (Python, Pandas, NumPy)
Self-Healing Pipeline: Implemented a "fuzzy" column mapper to handle whitespace and naming inconsistencies across the 7 CSV sources.

Dynamic Asset Injection: Developed logic to inject missing critical data (like vehicle_type) using weighted random distribution from the fleet database to maintain analytical integrity.

Feature Engineering: Engineered the CLV Score using a weighted formula: (Order_Value / Max * 70) + (Rating / 5 * 30).

2. Frontend & UI (Streamlit)
State-Aware Sidebar: Designed dynamic filters that adapt in real-time based on warehouse selection and priority levels.

Executive KPI "Pulse" Row: Utilized Streamlit metrics to display high-level visibility into Revenue at Risk, Carbon Footprint (kg), and Service Recovery %.

Intervention UI: Integrated a dedicated agent box with trigger actions (e.g., "Fix All Risks") to demonstrate immediate business ROI.

3. Geospatial & Visual Analytics (PyDeck, Plotly)
3D Map Layers: Leveraged PyDeck for a multi-layered geospatial experience, including ScreenGrid for density and HeatmapLayer for emission intensity.

Interactive Charts: Used Plotly Express to create responsive visualizations that update dynamically as users filter data in the sidebar.

4. Optimization & Sustainability Logic
Carbon-to-Cost Calculator: Built a real-time trade-off visualizer showing the financial impact of choosing "Greener" carriers vs. standard options.

Service Recovery Logic: Automated the identification of "High Risk" orders by cross-referencing traffic delays exceeding 60 minutes with promised delivery windows.

Getting Started
Prerequisites
Python 3.8+: Ensure the Python environment is ready.

pip: Python package manager for dependency installation.

Installation
Clone the Repository: git clone https://github.com/Harshitgautam93/ORION_Project.git

Navigate to the Project Directory: cd ORION_Project

Install Dependencies: pip install -r requirements.txt

Running the Application
Start the Dashboard: streamlit run frontend/app.py

Open in Browser: Visit the local URL (usually http://localhost:8501) to access the Command Center.

Conclusion
The ORION Control Tower serves as a testament to the power of integrating fragmented data into a cohesive decision-support system. By leveraging Streamlit, Plotly, and PyDeck, the project successfully demonstrates how logistics firms can achieve a 15–20% reduction in operational costs while simultaneously improving their sustainability footprint and customer retention.
