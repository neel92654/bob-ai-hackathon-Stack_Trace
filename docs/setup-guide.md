# Setup Guide: Nexora Platform

> **This setup guide provides exact, tested step-by-step instructions to run Nexora locally from scratch.**

---

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [ ] **Python 3.11+** (Verify with `python3 --version`)
- [ ] **Node.js 18+ & npm 9+** (Verify with `node --version` and `npm --version`)
- [ ] **Git** (Verify with `git --version`)

---

## Environment Configuration

Copy `src/.env.example` to `src/.env` (optional, default fallbacks are pre-configured):

```bash
cp src/.env.example src/.env
```

| Variable | Description | Default | Required |
|---|---|---|---|
| `APP_PORT` | Port for Flask backend REST API | `5001` | No |
| `FLASK_DEBUG` | Enable Flask debug mode | `False` | No |
| `DATABASE_URL` | SQLite database connection path | `src/backend/database/nexora.db` | No |

---

## Step-by-Step Installation

### 1. Clone the Repository
```bash
git clone https://github.com/neel92654/bob-ai-hackathon-Stack_Trace.git
cd bob-ai-hackathon-Stack_Trace
```


### 2. Install Dependencies
```bash
# Backend dependencies
pip install -r src/backend/requirements.txt

# MCP Server dependencies
pip install -r mcp-server/requirements.txt
```

### 3. Generate Synthetic Demonstration Dataset (Seed: 42)
```bash
python3 scripts/generate_data.py
```
*Outputs:* `process_routes.csv`, `equipment.csv`, `suppliers.csv`, `production_lots.csv`, `historical_delays.csv`, `disruptions.csv` into `src/data/`.

### 4. Initialize SQLite Database
```bash
python3 scripts/init_db.py
```
*Outputs:* Creates and populates `src/backend/database/nexora.db`.

### 5. Train the ML Delivery Prediction Model
```bash
python3 src/backend/ml/train_delivery_model.py
```
*Outputs:* Trains `RandomForestRegressor` ($R^2 = 0.954$) and saves `delivery_model.joblib` and `model_metrics.json`.

### 6. Run Automated Test Suite (52 Tests)
```bash
pytest tests/ -v
```
*Expected Output:* `52 passed in ~3.2s` (covers API endpoints, calculations, ML predictions, What-If simulations, and all 8 MCP tools).

### 7. Install Frontend Dependencies
```bash
cd src/frontend
npm install
cd ../..
```

---

## Running the Application

### Option A: Standard Full-Stack Web Platform

#### Start Backend API Server (Terminal 1)
```bash
python3 src/backend/app.py
```
*The backend API will start on: `http://127.0.0.1:5001`*  
*Health check URL: `http://127.0.0.1:5001/api/health`*

#### Start Frontend Application (Terminal 2)
```bash
cd src/frontend
npm run dev
```
*The React + Vite application will be available at: `http://localhost:5173`*

---

### Option B: Running the Nexora MCP Server for IBM Bob

The Nexora MCP server exposes 8 native tools over local STDIO transport without requiring open external network ports or remote API keys.

#### 1. Start / Verify the MCP Server Directly:
```bash
python3 mcp-server/server.py
```

#### 2. IBM Bob Client Configuration:
Configure IBM Bob using the included `.bob/mcp.json` file:

```json
{
  "mcpServers": {
    "nexora": {
      "command": "python3",
      "args": ["mcp-server/server.py"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

#### 3. Test Prompts in IBM Bob:
Once connected, IBM Bob will automatically discover and invoke Nexora's operational tools:

| Prompt in IBM Bob | Expected MCP Tool Invoked |
|---|---|
| *"Show me the top three fab bottlenecks."* | `get_fab_bottlenecks` |
| *"Why is the most critical bottleneck a risk?"* | `get_bottleneck_details(tool_id='CVD-03')` |
| *"Which supplier represents the largest single point of failure?"* | `get_supplier_risk` |
| *"Show me the production lots most affected by current bottlenecks."* | `get_production_impact` |
| *"Simulate a 14-day disruption of the highest-risk supplier."* | `run_disruption_simulation` |
| *"What changes after the supplier disruption?"* | `run_disruption_simulation` |
| *"What should operations prioritize right now?"* | `get_recommendations` |
| *"Give me an executive summary of Nexora's operational risk."* | `get_executive_summary` |

---

## 3-Minute Quick Demo Walkthrough

1. **Executive Dashboard (`http://localhost:5173`):** Review the Overall Fab Risk score, active bottleneck count, high-risk suppliers, and real-time alerts.
2. **Fab Bottlenecks Tab:** View equipment utilization meters. Click **"Drilldown & Lots"** on `CVD-03` to inspect its 153% queue utilization and assigned wafer lots.
3. **Supply Chain & SPoF Tab:** Inspect the critical Single-Point-of-Failure alert banner for `SUP-002` (Gallium, 91% dependency).
4. **What-If Simulator Tab:** Select **"1. Supplier Disruption"**, pick `SUP-002` with a 14-day outage, and click **"RUN DISRUPTION SIMULATION"** to observe the Before vs. After delay drift, financial SLA exposure, and recommended mitigation protocol.
5. **Decision Assistant Tab:** Click the prompt *"Why is CVD-03 critical?"* or *"What happens if SUP-002 becomes unavailable for 14 days?"* to view grounded, explainable operational reasoning.

---

## Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| `ModuleNotFoundError: No module named 'flask'` | Backend packages not installed | Run `pip install -r src/backend/requirements.txt`. |
| `ModuleNotFoundError: No module named 'mcp'` | MCP SDK packages not installed | Run `pip install -r mcp-server/requirements.txt`. |
| `Database file not found` | SQLite database not initialized | Run `python3 scripts/init_db.py`. |
| `ML model artifact not found` | Model training script was not executed | Run `python3 src/backend/ml/train_delivery_model.py`. (The system will also automatically use the deterministic physics fallback). |
| `Port 5001 already in use` | Another process is using port 5001 | Set `APP_PORT=5002` in `src/.env` or terminate the existing process. |
| `npm run dev fails` | Node modules missing | Run `cd src/frontend && npm install`. |

