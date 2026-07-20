# AI-Powered Computational Architecture Core Engine

An end-to-end autonomous architecture ecosystem designed to automate real estate development workflows—from raw municipal zoning law analysis to generative 2D spatial programming and climate-responsive form optimization.

## 🎯 The Core Vision
Traditional architectural feasibility and early-stage programming take weeks of manual drafting, cross-referencing, and spreadsheet calculations. This multi-phase project showcases an autonomous pipeline that reduces a **2-week workflow into less than 5 seconds** with 0% human error, maximizing commercial and environmental efficiency.

---

## 🏗️ Phase 1: Autonomous Zoning Law & 3D Envelope Auditor
Located in the `01_Zoning_and_Massing/` directory, this sub-agent extracts structural limits from raw, human-written city council texts and translates them into architectural geometry.

### How It Works:
1. **The Brain:** Utilizes `OpenRouter/GPT-4o` to parse complex zoning legal codes and extract FAR (Floor Area Ratio), setbacks, and plot limits into a structured JSON payload.
2. **The Cloud 3D Engine:** Injects that JSON payload directly into a vector engine to dynamically render the maximum legal 3D boundary envelope of the building.
3. **The Auditor:** Compares the designed area against regional caps, issuing an automated compliance certificate (`APPROVED` / `REJECTED`).

---

## 📐 Phase 2: Generative Space Programming & Presentation Diagram
Located in the `02_Space_Programming/` directory, this sub-agent operates *inside* the approved volume from Phase 1, automating the internal brief breakdown.

### How It Works:
1. **The Allocator:** Takes a raw client brief and programmatically breaks it down into individual room metrics based on international residential standards (e.g., 150 sqm cap).
2. **The Vector Layout:** Calculates room dimensions ($\sqrt{Area}$) and plots a presentation-ready architectural bubble diagram with a curated studio pastel palette.
3. **Circulation Mapper:** Automates network graph nodes to draw critical circulation routes and spatial relationships between public and private zones.

---

## ☀️ Phase 3: Climate-Responsive Form Optimization Agent
Located in the `03_Climate_Optimization/` directory, this sub-agent optimizes the building geometry against environmental factors to reduce HVAC energy loads.

### How It Works:
1. **Solar Vector Simulation:** Models real-time sun angles and calculates directional heat radiation across building facades.
2. **Automated Orientation Search:** Iterates through 3D rotational coordinates ($0^\circ$ to $90^\circ$) to find the orientation that yields the lowest heat absorption index.
3. **Environmental Envelope Plot:** Renders a 3D massing model overlaying the optimal roof vector and directional solar ray.

---

## 🛠️ Tech Stack & Skills Showcased
- **AI Agent Engineering:** Advanced prompt engineering, structured JSON extraction via OpenRouter API.
- **Computational Geometry:** Cloud-based 3D/2D spatial rendering using `Matplotlib`, `NumPy`, and Python.
- **Microclimate Analytics:** Algorithmic form-finding based on environmental vectors.
- **Architectural Automation:** End-to-end integration combining algorithmic design logic with data pipelines.
