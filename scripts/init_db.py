"""
Nexora — SQLite Database Initializer
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)

Initializes SQLite database and ingests synthetic CSV tables into src/backend/database/nexora.db
"""

import os
import sqlite3
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "src", "data")
DB_DIR = os.path.join(BASE_DIR, "src", "backend", "database")
DB_PATH = os.path.join(DB_DIR, "nexora.db")

os.makedirs(DB_DIR, exist_ok=True)

SCHEMA_SQL = """
DROP TABLE IF EXISTS process_routes;
CREATE TABLE process_routes (
    step_seq INTEGER PRIMARY KEY,
    process_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    nominal_cycle_time_hr REAL NOT NULL,
    predecessor_id TEXT
);

DROP TABLE IF EXISTS equipment;
CREATE TABLE equipment (
    tool_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    process_id TEXT NOT NULL,
    nominal_capacity INTEGER NOT NULL,
    current_wip INTEGER NOT NULL,
    status TEXT NOT NULL,
    chamber_health INTEGER NOT NULL,
    maintenance_due_hours INTEGER NOT NULL,
    mtbf_hours INTEGER NOT NULL,
    FOREIGN KEY(process_id) REFERENCES process_routes(process_id)
);

DROP TABLE IF EXISTS suppliers;
CREATE TABLE suppliers (
    supplier_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    material TEXT NOT NULL,
    country TEXT NOT NULL,
    lead_time_days INTEGER NOT NULL,
    dependency_pct INTEGER NOT NULL,
    criticality TEXT NOT NULL,
    alternate_supplier TEXT NOT NULL,
    alternate_lead_time_days INTEGER NOT NULL,
    alternate_capacity_pct INTEGER NOT NULL,
    geo_risk_factor REAL NOT NULL,
    status TEXT NOT NULL,
    single_point_of_failure INTEGER NOT NULL,
    affected_process_ids TEXT NOT NULL
);

DROP TABLE IF EXISTS production_lots;
CREATE TABLE production_lots (
    lot_id TEXT PRIMARY KEY,
    product_family TEXT NOT NULL,
    customer_tier TEXT NOT NULL,
    current_process_id TEXT NOT NULL,
    current_process_name TEXT NOT NULL,
    next_process_id TEXT NOT NULL,
    assigned_tool_id TEXT NOT NULL,
    wafer_quantity INTEGER NOT NULL,
    lot_value_usd REAL NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    entry_time TEXT NOT NULL,
    due_date TEXT NOT NULL,
    steps_completed INTEGER NOT NULL,
    total_steps INTEGER NOT NULL,
    FOREIGN KEY(current_process_id) REFERENCES process_routes(process_id),
    FOREIGN KEY(assigned_tool_id) REFERENCES equipment(tool_id)
);

DROP TABLE IF EXISTS historical_delays;
CREATE TABLE historical_delays (
    record_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    process_id TEXT NOT NULL,
    tool_nominal_capacity INTEGER NOT NULL,
    wip_queue_size INTEGER NOT NULL,
    tool_utilization_pct REAL NOT NULL,
    downstream_queue_size INTEGER NOT NULL,
    wafer_quantity INTEGER NOT NULL,
    lot_priority_num INTEGER NOT NULL,
    remaining_stages INTEGER NOT NULL,
    nominal_cycle_time_hr REAL NOT NULL,
    chamber_health INTEGER NOT NULL,
    has_active_disruption INTEGER NOT NULL,
    actual_delay_hours REAL NOT NULL
);

DROP TABLE IF EXISTS disruptions;
CREATE TABLE disruptions (
    disruption_id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    target_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    target_name TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    start_time TEXT NOT NULL,
    estimated_duration_days INTEGER NOT NULL,
    description TEXT NOT NULL,
    impact_summary TEXT NOT NULL,
    recommended_mitigation TEXT NOT NULL
);
"""

def load_csv(cursor, table_name, filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} does not exist.")
        return 0
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            return 0
        cols = list(rows[0].keys())
        placeholders = ", ".join(["?"] * len(cols))
        col_names = ", ".join(cols)
        query = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"
        cursor.executemany(query, [[r[c] for c in cols] for r in rows])
        print(f"Loaded {len(rows)} rows into {table_name}")
        return len(rows)

def init_db():
    print(f"Initializing SQLite database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(SCHEMA_SQL)
    
    load_csv(cursor, "process_routes", "process_routes.csv")
    load_csv(cursor, "equipment", "equipment.csv")
    load_csv(cursor, "suppliers", "suppliers.csv")
    load_csv(cursor, "production_lots", "production_lots.csv")
    load_csv(cursor, "historical_delays", "historical_delays.csv")
    load_csv(cursor, "disruptions", "disruptions.csv")
    
    conn.commit()
    conn.close()
    print("Database initialization complete successfully!")

if __name__ == "__main__":
    init_db()
