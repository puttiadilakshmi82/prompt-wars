# 🏛️ CivicPulse AI — Predictive Community Problem Resolution & Urban Intelligence

> An AI-driven municipal intelligence platform bridging the gap between citizens and city administration by transforming reactive civic complaints into proactive, predictive infrastructure stewardship.

---

## 🌟 Why CivicPulse AI?

Traditional municipal grievance portals (like 311 systems) suffer from major systemic bottlenecks:
1. **System Flooding & Duplication:** When an urgent event occurs (e.g. a burst water main or dangerous road cave-in), dozens of residents report the same localized incident, overwhelming dispatch staff with duplicate tickets.
2. **Reactive Rather than Predictive:** City departments only learn about infrastructure failures after catastrophic breakdowns happen, leading to emergency repair costs that are 4x–8x higher than preventative maintenance.
3. **Piecemeal Resource Dispatch:** Work crews are dispatched to individual scattered complaints rather than grouped along high-density geospatial clusters, wasting municipal transit hours and fuel.
4. **Lack of Resident Feedback Loops:** Citizens rarely receive transparent tracking or confirmation of action.

**CivicPulse AI** solves this through **semantic deduplication**, **unsupervised geospatial clustering (DBSCAN)**, **multi-factor urgency scoring**, and **predictive infrastructure deterioration forecasting**.

---

## 🚀 Key Modules & Architecture

```
civicpulse/
├── app.py                      # Main Streamlit command center and multi-view portal
├── config.py                   # City geometry, wards, categories, SLA rules & risk weights
├── data/
│   ├── sample_data.py          # Realistic seed generator & persistent JSON storage
│   └── civic_data.json         # Real-time municipal ticket database
├── models/
│   ├── deduplication.py        # TF-IDF + Haversine spatial deduplication engine
│   ├── clustering.py           # DBSCAN geospatial hotspot & macro-incident detector
│   ├── urgency_scoring.py      # Multi-factor priority score (0–100) & risk evaluator
│   └── predictive_engine.py    # Infrastructure failure & degradation forecaster
├── services/
│   ├── ai_assistant.py         # PulseAssistant RAG Analyst (natural language queries)
│   └── dispatch_router.py      # Automated department routing & SLA lifecycle tracker
├── components/
│   ├── ui_styles.py            # Glassmorphism UI styling, cards, and status badges
│   ├── maps.py                 # PyDeck 3D scatter, cluster rings, and hexagon density layers
│   └── charts.py               # Altair analytics & ward vulnerability charts
└── run_civicpulse.bat          # One-click Windows application launcher
```

---

## 💡 Core Features

### 1. 📝 Smart Citizen Reporting & Real-Time Deduplication
- As the user types their complaint headline and description, the engine checks for semantic hazard triggers (`live wire`, `sinkhole`, `flooding`, `toxic`).
- **Composite Deduplication**: Evaluates existing reports within a 400m radius using Haversine distance and TF-IDF Cosine Similarity.
- If a match is detected (e.g. 92% similarity 140m away), it alerts the citizen and provides a **"👍 Upvote & Confirm Existing Ticket"** button instead of flooding the city with duplicate records.

### 2. 🗺️ Geospatial Command Center & Unsupervised Clustering (DBSCAN)
- Interactive **PyDeck 3D map** with color-coded severity:
  - 🔴 **Critical (Urgency ≥ 80)**
  - 🟠 **High (60–79)**
  - 🟡 **Medium (40–59)**
  - 🟢 **Low (<40)**
- **Density-Based Spatial Clustering (DBSCAN)**: Automatically aggregates dozens of individual complaints into unified **Macro-Incident Hotspots** with centroid coordinates, affected radius, and consolidated work orders.

### 3. 🔮 Predictive Infrastructure Degradation Forecaster
- **Forecasting Cascading Failures (7-day & 14-day Window)**: Analyzes localized micro-leak frequencies, electrical transformer spikes, and road degradation signatures.
- **Actionable Preventative Engineering Directives**: e.g. *"Deploy mobile acoustic leak inspection van and throttle pressure regulators by 15% during off-peak hours before monsoon."*
- **Fiscal Savings Metric**: Computes estimated municipal repair expenditure saved (e.g. `+$115,000+` in averted damages).

### 4. 📋 Operations Kanban & SLA Dispatch Board
- Live operational board with columns: `Reported` ➔ `Triaged` ➔ `Dispatched` ➔ `In Progress` ➔ `Resolved`.
- Real-time SLA compliance indicators with countdown timers and automated department routing (PWD, Water Supply Board, Electric Utility, Solid Waste Management).

### 5. 🤖 PulseAssistant: Municipal RAG & AI Analyst
- City administrators can ask natural language questions grounded directly in the municipal database:
  - *"Which ward has the highest water contamination risk?"*
  - *"Summarize road grievances along Tech Corridor North."*
  - *"Give me a daily executive briefing."*
  - *"What is our 7-day predictive risk forecast?"*

---

## 🛠️ How to Run

### Option 1: One-Click Batch Launcher
Double-click `run_civicpulse.bat` in the project root.

### Option 2: Terminal Command
Run via PowerShell or Command Prompt:
```bash
python -m streamlit run civicpulse/app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Real-Time Simulation
Click the **"🚨 Simulate New Incident Event"** button in the sidebar to inject simulated real-time community grievances and watch the AI priority scoring, deduplication, and geospatial maps update dynamically.
