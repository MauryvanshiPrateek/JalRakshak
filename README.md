# 🌊 JalRakshak

**Dam Break Inundation Modelling & Flood Risk Visualization Platform**

Smart India Hackathon 2026 — Problem Statement **SIH26161**  
Theme: Disaster Management | Category: Software | Team: VisionSix

## 1. Overview

JalRakshak is a reusable, open-source prototype for simulating dam-break flood scenarios and generating location-specific flood-risk maps.

The prototype combines:
- DEM/elevation data
- River and dam geometry
- Configurable breach scenarios
- Physics-based hydrodynamic modelling with ANUGA
- GIS processing
- Interactive flood-depth and flood-extent maps
- Exposure/risk analysis for settlements and infrastructure
- Time-based flood propagation visualization

> **Prototype scope:** Start with one selected dam/river and a bounded downstream study area. The architecture is designed so additional locations can be added later.

## 2. Core Workflow

```text
Dam/River + DEM + Scenario
            ↓
       GIS preprocessing
            ↓
     Computational domain
            ↓
     Breach / inflow setup
            ↓
          ANUGA
            ↓
 Water depth + velocity + extent
            ↓
       GIS risk analysis
            ↓
 Interactive dashboard + warnings
```

## 3. Prototype Features

### MVP
1. Select a demo dam/river.
2. Display the study area on an interactive map.
3. Configure breach parameters.
4. Run a hydrodynamic simulation.
5. Visualize flood extent and water depth.
6. Show simulation statistics.
7. Identify potentially affected settlements/roads.
8. Classify flood risk.

### Demo Enhancements
- Time slider / flood animation
- Scenario presets: Small, Medium, Severe
- Population/exposure statistics
- Infrastructure markers
- Export flood layers
- Simulation history

## 4. Important Scientific Principle

ANUGA should be the simulation engine for the real prototype. Do not replace actual simulation outputs with hard-coded numbers in the final demonstration. During early UI development, a mock simulation adapter may be used, but it must be clearly separated from the real ANUGA adapter.

## 5. Suggested Project Structure

```text
JalRakshak/
├── app/
│   ├── main.py
│   ├── components/
│   └── pages/
├── simulation/
│   ├── anuga_runner.py
│   ├── breach_model.py
│   └── simulation_service.py
├── gis/
│   ├── dem.py
│   ├── layers.py
│   └── risk.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
├── outputs/
├── config/
│   └── scenarios.yaml
├── tests/
├── docs/
├── scripts/
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

## 6. Running Locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app/main.py
```

## 7. Docker

```bash
docker build -t jalrakshak .
docker run --rm -p 8501:8501 jalrakshak
```

Open `http://localhost:8501`.

## 8. Safety / Interpretation

JalRakshak is a decision-support prototype. Simulation outputs depend on terrain, hydraulic assumptions, breach parameters, boundary conditions and data quality. Prototype warnings must not be presented as official emergency instructions.

## 9. Development Principle

Keep the system modular:

```text
UI → Simulation Service → ANUGA Adapter
UI → GIS Service → Raster/Vector Processing
UI → Risk Service → Exposure Analysis
```

This makes it possible to replace sample data with real datasets without rewriting the dashboard.
