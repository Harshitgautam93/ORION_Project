ORION              Report - https://drive.google.com/file/d/1-a7rT1aoyycETYqz6l1OHbHelT3imSNx/view?usp=sharing

Order Risk & Intelligent Optimization Network
NexGen Logistics Pvt. Ltd. | Internship Case-Study Assignment

1. Project Overview

ORION is an AI-driven Logistics Decision Intelligence platform built for NexGen Logistics Pvt. Ltd., a mid-sized logistics company operating across India with international hubs in Singapore, Dubai, Hong Kong, and Bangkok.

The platform acts as a predictive Command Center, transforming reactive logistics operations into proactive, data-driven decision-making through Tri-Factor Optimization:

Profitability

Carbon Footprint

Customer Lifetime Value (CLV)

ORION is implemented using Python and Streamlit, combining analytics, optimization heuristics, and explainable AI to support executive and operational decisions.

2. Tech Stack

Core Logic: Python (Pandas, NumPy, Scikit-learn / ML)

Frontend Interface: Streamlit

Visualizations: Plotly, Matplotlib, PyDeck, Folium

Optimization Layer: Rule-based heuristics + predictive modeling

Data Source: CSV-based operational datasets

3. Business Context & Problem Statement

Despite steady growth, NexGen Logistics faces multiple operational challenges:

Delivery Delays: Actual delivery timelines frequently exceed promised windows

Rising Costs: Fuel, labor, and fleet maintenance overheads

Sustainability Blind Spot: No visibility into CO₂ emissions

Data Silos: Operational data scattered across 7+ CSV files with integrity issues

Business Goal:
Reduce operational costs by 15–20% while improving customer satisfaction through intelligent, data-driven logistics optimization.

4. Data Integrity Audit (OFI – Opportunities for Improvement)

The initial audit identified critical data quality issues:

File	Key Issues	Business Impact
orders.csv	76% missing Special_Handling, order value outliers	Risk to fragile goods
delivery_performance.csv	Gap between promised vs actual delivery	Reduced CLV
routes_distance.csv	70% missing weather impact, zero tolls for international routes	Incorrect profit & risk
warehouse_inventory.csv	Stock below reorder points (Industrial goods)	Stockouts / dead stock
vehicle_fleet.csv	Refrigerated fleet mismatch with food orders	Perishable goods risk

ORION addresses these issues through self-healing data pipelines.

5. Solution Overview: ORION Capabilities
I. Predictive Decision Engine

Failure Propensity Modeling: Assigns a probability-of-failure score per order using traffic, weather, and carrier history

Tri-Factor Scoring: Balances profit, carbon emissions, and customer value

CLV-Based Prioritization: High-value customers are auto-flagged for premium shipping lanes

II. Sustainability & Transparency

Carbon-to-Cost Calculator: Visualizes cost trade-offs of greener carriers

Eco-Optimized Fleet Pairing: Matches orders to low-emission vehicles (EVs / Euro-6)

III. Advanced UI/UX (Streamlit Command Center)

Dynamic Sidebar Filters: Context-aware warehouse and priority filters

Executive KPI Pulse Row: Revenue at Risk, Carbon Intensity, Fleet Utilization

Explainable AI Badges: Plain-English explanations for AI decisions

IV. Implemented Intelligence Features

Risk Propensity Matrix: Visualizes risk level vs delivery cost and customer value

Fleet Ranking System: Normalized scoring of fuel efficiency, vehicle age, CO₂ emissions, and utilization

Geospatial Carbon Tracking: PyDeck heatmaps of emission hotspots

Self-Healing Data Engine: Automatically injects simulated values when CSV columns are missing

6. System Architecture

ORION follows a clean, decoupled architecture:

Backend – data_engine.py

Data ingestion and sanitization

Fuzzy column mapping (case/whitespace tolerant)

Self-healing schema injection

Feature engineering and scoring logic (Risk, CLV, Carbon)

Frontend – app.py

Streamlit-based executive dashboard

Custom enterprise-grade CSS styling

Interactive charts, maps, and ranking tables

Data Layer

CSV datasets for orders, fleet, inventory, routes, and performance

7. Key Analytics & Engineering Techniques

Schema Integration: Multi-way left joins on order_id

Feature Engineering:

Total_Order_Cost

Delay_Days = Actual – Promised

Profit = Order_Value – Total_Cost

Data Normalization: Metrics scaled to a unified 0–100 range

Path Handling: Robust backend imports using sys.path.append

8. User Workflow & Decision Support
Feature	Purpose
KPI Metrics	Executive overview of risk, carbon, and recovery
Fleet Intelligence	Optimization bias: Cost / Balanced / Green
AI Intervention Agent	Flags high-risk, high-value orders
“Fix All Risks”	Simulates automated rerouting decisions
9. Project Deliverables

app.py – Main Streamlit dashboard

data_engine.py – Backend analytics engine

requirements.txt – Python dependencies

README.md – Project documentation

Interactive Visuals:

Risk vs Reward Scatter

Fleet Ranking Tables

Warehouse Health Indicators

Carbon Emission Heatmaps

10. Future Roadmap

AI Agent (NLP): Natural language queries (e.g., “What happens if Delhi orders switch carriers?”)

Predictive Maintenance: Alerts when fuel efficiency drops >10%

What-if Simulations: Fuel price hikes, carbon tax scenarios

Service Scheduling: Days-to-service prediction using vehicle age & distance

Live Data Integration: SQL databases, telematics APIs, real-time feeds

11. Outcome

ORION demonstrates how AI-driven decision intelligence can unify cost optimization, sustainability, and customer value into a single operational platform—positioning NexGen Logistics for scalable, resilient, and future-ready operations.

<img width="1827" height="716" alt="Screenshot 2025-12-19 122237" src="https://github.com/user-attachments/assets/c514ce12-07ba-4c9a-a89d-3379e167c68e" />
<img width="1882" height="719" alt="Screenshot 2025-12-19 122208" src="https://github.com/user-attachments/assets/63ff2016-2b42-4777-8427-26f3c9f912d3" />
<img width="1829" height="702" alt="Screenshot 2025-12-19 122133" src="https://github.com/user-attachments/assets/e1827cae-6692-40f8-bc0b-a1b848eb5b1c" />
<img width="1818" height="720" alt="Screenshot 2025-12-19 122104" src="https://github.com/user-attachments/assets/c79a8876-acc3-4177-add3-57220711023d" />
<img width="9432" height="3626" alt="ORION - ARCHITECTURE DIAGRAM" src="https://github.com/user-attachments/assets/d229cda7-c6c0-459a-81bf-1b1447f5fa7a" />

