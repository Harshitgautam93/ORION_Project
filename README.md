🛰️ ORION | Order Risk & Intelligent Optimization Network
NexGen Logistics Intelligence Command Center
ORION is an AI-driven decision engine designed to transform reactive logistics into a predictive "Command Center." Built for NexGen Logistics Pvt. Ltd., it unifies 7+ fragmented datasets to solve the Tri-Factor Optimization challenge: Balancing Profitability, Sustainability (Carbon), and Customer Lifetime Value (CLV).

📌 Business Context & Problem Statement
NexGen Logistics operates across India and international hubs (Singapore, Dubai, etc.), but faces critical threats:

Performance Gaps: Actual delivery times consistently exceed promised windows.

Cost Pressures: High overheads in fuel, labor, and maintenance.

The "Data Silo" Effect: Information is scattered across inconsistent CSV files, leading to "invisible" revenue at risk.

ORION bridges these gaps by identifying at-risk customers and suggesting interventions before the delivery failure occurs.

🛠️ Innovation: The "Self-Healing" Pipeline
Real-world data is messy. ORION’s backend includes a Data Integrity Audit layer that handles:

Fuzzy Column Mapping: Automatically resolves whitespace, casing, and naming inconsistencies (e.g., "CO2 Emissions" vs "carbon_kg").

Schema Integration: Uses multi-way left joins to ensure "In-Transit" orders are preserved, reflecting true operational state.

Feature Engineering:

CLV Score: (Order_Value / Max) * 0.7 + (Rating / 5) * 0.3.

Failure Propensity: Dynamic risk scoring based on traffic volatility and carrier history.

Carbon-to-Cost Calculator: Shows the real-time financial trade-off for choosing "Green" carriers.

📊 Dashboard Features
1. Geospatial Carbon & Emission Hotspots
Using PyDeck, ORION visualizes "Emission Hotspots." The heatmap density is driven by Carbon_Impact, allowing managers to pinpoint where the fleet is most carbon-intensive.

2. Risk Propensity Matrix
An interactive Plotly scatter plot:

X-Axis: Distance | Y-Axis: Cost.

Bubble Size: CLV_Score (Prioritizes high-value customers).

Color: Risk_Level (Flags orders delayed by traffic/weather).

3. Warehouse Inventory "Health" Tracker
Monitors stock levels against reorder points to prevent stockouts of high-demand 'Industrial' goods.

4. AI Intervention Agent
A logic-driven module that scans for "High Risk" orders and provides Explainable AI (XAI) Badges (e.g., "Prioritized due to high churn risk").

🏗️ Technical Architecture
Core Logic: Python (Pandas, NumPy).

Interface: Streamlit (Dynamic Web Framework).

Visualizations: Plotly, PyDeck.

Data: 7-Layered CSV Ecosystem (Orders, Performance, Routes, Fleet, Inventory, Costs, Feedback).

📈 Business Impact
15–20% Cost Reduction: Through identification of cost leakage and optimized vehicle-to-order matching.

Sustainability Transparency: Real-time CO2 tracking for "Green Max" optimization.

Revenue Protection: Proactive intervention for high-CLV customers who are at risk of late delivery.

🚀 Installation & Setup
Clone: git clone https://github.com/Harshitgautam93/ORION_Project

Install: pip install -r requirements.txt

Run: streamlit run frontend/app.py

🗺️ Roadmap
Predictive Maintenance: Automated alerts when fuel efficiency drops by >10%.

What-if Sandboxes: Simulation sliders for fuel price hikes or carbon tax impacts.

NLP AI Agent: Ask "What is the revenue impact of switching Delhi orders to BlueDart?"

Developed as a Strategic Decision Support System for NexGen Logistics.

- <img width="1870" height="757" alt="Screenshot 2025-12-19 104857" src="https://github.com/user-attachments/assets/51678000-0650-4f05-9db7-31c652defbcc" />
<img width="1896" height="810" alt="Screenshot 2025-12-19 104833" src="https://github.com/user-attachments/assets/2b78b9d2-a646-49b1-90a9-044c7658964e" />
<img width="1355" height="695" alt="Screenshot 2025-12-19 104738" src="https://github.com/user-attachments/assets/a04f09fb-b7e8-4ba4-bf36-657decb88e8d" />
<img width="1866" height="736" alt="Screenshot 2025-12-19 104724" src="https://github.com/user-attachments/assets/21f9b50f-82e7-4380-9531-b9d8da0f05aa" />
<img width="1817" height="758" alt="Screenshot 2025-12-19 104702" src="https://github.com/user-attachments/assets/6eb9e550-b084-4149-84cf-fc4dc71b67c2" />
<img width="1358" height="646" alt="Screenshot 2025-12-19 102337" src="https://github.com/user-attachments/assets/049824e5-983f-484d-b411-1243e107c4d4" />
