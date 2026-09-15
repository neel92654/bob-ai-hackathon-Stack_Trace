"""
Nexora — Synthetic Fab & Supply Chain Data Generator
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)

Generates a realistic, deterministic demonstration dataset (Seed: 42)
for fab bottleneck intelligence, supply chain risk analysis, and delivery prediction.
"""

import os
import random
import csv
import json
from datetime import datetime, timedelta

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Process Routes (Sequential Fab Process Stages)
PROCESS_ROUTES = [
    {"step_seq": 1, "process_id": "PRC-01", "name": "Wafer Prep & Clean", "nominal_cycle_time_hr": 3.5, "predecessor_id": None},
    {"step_seq": 2, "process_id": "PRC-02", "name": "Oxidation & Thermal", "nominal_cycle_time_hr": 6.0, "predecessor_id": "PRC-01"},
    {"step_seq": 3, "process_id": "PRC-03", "name": "Photolithography (EUV/DUV)", "nominal_cycle_time_hr": 8.0, "predecessor_id": "PRC-02"},
    {"step_seq": 4, "process_id": "PRC-04", "name": "Plasma & Reactive Etch", "nominal_cycle_time_hr": 5.5, "predecessor_id": "PRC-03"},
    {"step_seq": 5, "process_id": "PRC-05", "name": "Ion Implantation", "nominal_cycle_time_hr": 4.5, "predecessor_id": "PRC-04"},
    {"step_seq": 6, "process_id": "PRC-06", "name": "Chemical Vapor Deposition (CVD)", "nominal_cycle_time_hr": 7.0, "predecessor_id": "PRC-05"},
    {"step_seq": 7, "process_id": "PRC-07", "name": "Physical Vapor Deposition (PVD)", "nominal_cycle_time_hr": 5.0, "predecessor_id": "PRC-06"},
    {"step_seq": 8, "process_id": "PRC-08", "name": "Chemical Mechanical Polishing (CMP)", "nominal_cycle_time_hr": 4.0, "predecessor_id": "PRC-07"},
    {"step_seq": 9, "process_id": "PRC-09", "name": "In-line Metrology & Defect Scan", "nominal_cycle_time_hr": 3.0, "predecessor_id": "PRC-08"},
    {"step_seq": 10, "process_id": "PRC-10", "name": "Wafer Test & Final Packaging", "nominal_cycle_time_hr": 6.5, "predecessor_id": "PRC-09"},
]

# 2. Equipment Tools (28 Tools across 10 processes)
EQUIPMENT_DATA = [
    # Lithography
    {"tool_id": "LITH-01", "name": "ASML EUV Stepper Alpha", "process_id": "PRC-03", "nominal_capacity": 40, "current_wip": 48, "status": "RUNNING", "chamber_health": 88, "maintenance_due_hours": 120, "mtbf_hours": 720},
    {"tool_id": "LITH-02", "name": "ASML DUV Scanner Beta", "process_id": "PRC-03", "nominal_capacity": 50, "current_wip": 42, "status": "RUNNING", "chamber_health": 94, "maintenance_due_hours": 340, "mtbf_hours": 850},
    {"tool_id": "LITH-03", "name": "Nikon Immersion Scanner", "process_id": "PRC-03", "nominal_capacity": 35, "current_wip": 46, "status": "MAINTENANCE_WARNING", "chamber_health": 74, "maintenance_due_hours": 24, "mtbf_hours": 600},
    # CVD
    {"tool_id": "CVD-01", "name": "Applied Materials Centura CVD", "process_id": "PRC-06", "nominal_capacity": 45, "current_wip": 38, "status": "RUNNING", "chamber_health": 92, "maintenance_due_hours": 210, "mtbf_hours": 900},
    {"tool_id": "CVD-02", "name": "Lam Vector PECVD", "process_id": "PRC-06", "nominal_capacity": 40, "current_wip": 36, "status": "RUNNING", "chamber_health": 86, "maintenance_due_hours": 180, "mtbf_hours": 820},
    {"tool_id": "CVD-03", "name": "Tokyo Electron Telindy ALD/CVD", "process_id": "PRC-06", "nominal_capacity": 30, "current_wip": 46, "status": "RUNNING", "chamber_health": 68, "maintenance_due_hours": 18, "mtbf_hours": 650},
    # Etch
    {"tool_id": "ETCH-01", "name": "Lam Kiyo Dielectric Etcher", "process_id": "PRC-04", "nominal_capacity": 50, "current_wip": 35, "status": "RUNNING", "chamber_health": 95, "maintenance_due_hours": 400, "mtbf_hours": 1100},
    {"tool_id": "ETCH-02", "name": "Applied Materials Producer Etch", "process_id": "PRC-04", "nominal_capacity": 45, "current_wip": 52, "status": "RUNNING", "chamber_health": 79, "maintenance_due_hours": 48, "mtbf_hours": 750},
    {"tool_id": "ETCH-03", "name": "TEL Tactras ICP Etcher", "process_id": "PRC-04", "nominal_capacity": 35, "current_wip": 28, "status": "RUNNING", "chamber_health": 91, "maintenance_due_hours": 290, "mtbf_hours": 950},
    # CMP
    {"tool_id": "CMP-01", "name": "Applied Materials Reflexion LK", "process_id": "PRC-08", "nominal_capacity": 50, "current_wip": 44, "status": "RUNNING", "chamber_health": 85, "maintenance_due_hours": 160, "mtbf_hours": 700},
    {"tool_id": "CMP-02", "name": "Ebara Planarization System", "process_id": "PRC-08", "nominal_capacity": 40, "current_wip": 32, "status": "RUNNING", "chamber_health": 90, "maintenance_due_hours": 310, "mtbf_hours": 800},
    # Ion Implantation
    {"tool_id": "IMP-01", "name": "Axcelis Purion H High-Current", "process_id": "PRC-05", "nominal_capacity": 35, "current_wip": 39, "status": "RUNNING", "chamber_health": 81, "maintenance_due_hours": 95, "mtbf_hours": 680},
    {"tool_id": "IMP-02", "name": "Varian VIISta Medium-Current", "process_id": "PRC-05", "nominal_capacity": 40, "current_wip": 25, "status": "RUNNING", "chamber_health": 93, "maintenance_due_hours": 420, "mtbf_hours": 1000},
    # PVD
    {"tool_id": "PVD-01", "name": "Applied Materials Endura PVD", "process_id": "PRC-07", "nominal_capacity": 45, "current_wip": 39, "status": "RUNNING", "chamber_health": 87, "maintenance_due_hours": 250, "mtbf_hours": 850},
    {"tool_id": "PVD-02", "name": "Evatec Sputter System", "process_id": "PRC-07", "nominal_capacity": 30, "current_wip": 26, "status": "RUNNING", "chamber_health": 89, "maintenance_due_hours": 190, "mtbf_hours": 780},
    # Metrology
    {"tool_id": "MET-01", "name": "KLA Archer Optical CD/Overlay", "process_id": "PRC-09", "nominal_capacity": 60, "current_wip": 45, "status": "RUNNING", "chamber_health": 96, "maintenance_due_hours": 500, "mtbf_hours": 1200},
    {"tool_id": "MET-02", "name": "Hitachi High-Tech CD-SEM", "process_id": "PRC-09", "nominal_capacity": 40, "current_wip": 34, "status": "RUNNING", "chamber_health": 90, "maintenance_due_hours": 280, "mtbf_hours": 900},
    {"tool_id": "MET-03", "name": "Applied Materials SEMVision Defect", "process_id": "PRC-09", "nominal_capacity": 35, "current_wip": 41, "status": "RUNNING", "chamber_health": 78, "maintenance_due_hours": 60, "mtbf_hours": 620},
    # Wafer Prep / Clean
    {"tool_id": "CLN-01", "name": "DNS Wet Station Clean 300", "process_id": "PRC-01", "nominal_capacity": 70, "current_wip": 48, "status": "RUNNING", "chamber_health": 97, "maintenance_due_hours": 600, "mtbf_hours": 1400},
    {"tool_id": "CLN-02", "name": "Tokyo Electron Celius Single-Wafer", "process_id": "PRC-01", "nominal_capacity": 65, "current_wip": 50, "status": "RUNNING", "chamber_health": 92, "maintenance_due_hours": 450, "mtbf_hours": 1300},
    # Oxidation
    {"tool_id": "THM-01", "name": "TEL Vertical Furnace Alpha", "process_id": "PRC-02", "nominal_capacity": 55, "current_wip": 40, "status": "RUNNING", "chamber_health": 94, "maintenance_due_hours": 380, "mtbf_hours": 1150},
    {"tool_id": "THM-02", "name": "Kokusai Electric Diffusion Furnace", "process_id": "PRC-02", "nominal_capacity": 50, "current_wip": 37, "status": "RUNNING", "chamber_health": 88, "maintenance_due_hours": 220, "mtbf_hours": 980},
    # Packaging / Test
    {"tool_id": "PKG-01", "name": "Advantest V93000 Wafer Prober", "process_id": "PRC-10", "nominal_capacity": 60, "current_wip": 42, "status": "RUNNING", "chamber_health": 91, "maintenance_due_hours": 300, "mtbf_hours": 1050},
    {"tool_id": "PKG-02", "name": "Teradyne UltraFLEX Test System", "process_id": "PRC-10", "nominal_capacity": 55, "current_wip": 38, "status": "RUNNING", "chamber_health": 95, "maintenance_due_hours": 480, "mtbf_hours": 1250},
    {"tool_id": "PKG-03", "name": "DISCO Ultra-Thin Wafer Dicer", "process_id": "PRC-10", "nominal_capacity": 45, "current_wip": 31, "status": "RUNNING", "chamber_health": 87, "maintenance_due_hours": 170, "mtbf_hours": 890},
    {"tool_id": "PKG-04", "name": "BESI Flip-Chip Die Bonder", "process_id": "PRC-10", "nominal_capacity": 40, "current_wip": 29, "status": "RUNNING", "chamber_health": 93, "maintenance_due_hours": 350, "mtbf_hours": 1100},
    # Extra CVD & Litho for high load
    {"tool_id": "CVD-04", "name": "Kokusai Atomic Layer Deposition", "process_id": "PRC-06", "nominal_capacity": 30, "current_wip": 22, "status": "RUNNING", "chamber_health": 91, "maintenance_due_hours": 320, "mtbf_hours": 850},
    {"tool_id": "ETCH-04", "name": "Hitachi M-600 Micro-Wave Etcher", "process_id": "PRC-04", "nominal_capacity": 35, "current_wip": 20, "status": "RUNNING", "chamber_health": 96, "maintenance_due_hours": 510, "mtbf_hours": 1300},
]

# 3. Suppliers Data (22 Suppliers with Single-Point-of-Failure cases and geopolitical concentration)
SUPPLIERS_DATA = [
    {
        "supplier_id": "SUP-001",
        "name": "Shin-Etsu Chemical Co.",
        "material": "High-Purity Silicon Wafers (300mm)",
        "country": "Japan",
        "lead_time_days": 28,
        "dependency_pct": 58,
        "criticality": "HIGH",
        "alternate_supplier": "SUMCO Corp.",
        "alternate_lead_time_days": 35,
        "alternate_capacity_pct": 45,
        "geo_risk_factor": 1.1,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-01,PRC-02"
    },
    {
        "supplier_id": "SUP-002",
        "name": "Global Gallium Refining Ltd.",
        "material": "High-Purity Gallium / GaAs Substrates",
        "country": "China",
        "lead_time_days": 45,
        "dependency_pct": 91,
        "criticality": "CRITICAL",
        "alternate_supplier": "None",
        "alternate_lead_time_days": 0,
        "alternate_capacity_pct": 0,
        "geo_risk_factor": 1.8,
        "status": "ALERT",
        "single_point_of_failure": 1,
        "affected_process_ids": "PRC-02,PRC-05,PRC-06"
    },
    {
        "supplier_id": "SUP-003",
        "name": "Tokyo Ohka Kogyo (TOK)",
        "material": "EUV Photoresist Polymer",
        "country": "Japan",
        "lead_time_days": 30,
        "dependency_pct": 74,
        "criticality": "CRITICAL",
        "alternate_supplier": "JSR Micro",
        "alternate_lead_time_days": 42,
        "alternate_capacity_pct": 30,
        "geo_risk_factor": 1.15,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-03"
    },
    {
        "supplier_id": "SUP-004",
        "name": "Ingas Purification Corp.",
        "material": "Ultra-Pure Neon Gas (Excimer Laser)",
        "country": "Ukraine",
        "lead_time_days": 60,
        "dependency_pct": 82,
        "criticality": "CRITICAL",
        "alternate_supplier": "Cryoin Engineering (Partial)",
        "alternate_lead_time_days": 90,
        "alternate_capacity_pct": 15,
        "geo_risk_factor": 1.95,
        "status": "CRITICAL_WATCH",
        "single_point_of_failure": 1,
        "affected_process_ids": "PRC-03"
    },
    {
        "supplier_id": "SUP-005",
        "name": "Merck Electronics KGaA",
        "material": "Advanced CMP Slurry & Pads",
        "country": "Germany",
        "lead_time_days": 18,
        "dependency_pct": 45,
        "criticality": "MEDIUM",
        "alternate_supplier": "Cabot Microelectronics",
        "alternate_lead_time_days": 21,
        "alternate_capacity_pct": 55,
        "geo_risk_factor": 1.05,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-08"
    },
    {
        "supplier_id": "SUP-006",
        "name": "Entegris Inc.",
        "material": "Ultra-Pure Liquid Chemical Precursors (TEOS/Silane)",
        "country": "United States",
        "lead_time_days": 14,
        "dependency_pct": 38,
        "criticality": "MEDIUM",
        "alternate_supplier": "Versum Materials",
        "alternate_lead_time_days": 18,
        "alternate_capacity_pct": 60,
        "geo_risk_factor": 1.0,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-06,PRC-07"
    },
    {
        "supplier_id": "SUP-007",
        "name": "BASF SE Electronic Materials",
        "material": "Electronic-Grade Hydrofluoric Acid (HF)",
        "country": "Germany",
        "lead_time_days": 22,
        "dependency_pct": 52,
        "criticality": "HIGH",
        "alternate_supplier": "Stella Chemifa",
        "alternate_lead_time_days": 30,
        "alternate_capacity_pct": 40,
        "geo_risk_factor": 1.05,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-01,PRC-04"
    },
    {
        "supplier_id": "SUP-008",
        "name": "Umicore Noble Metals",
        "material": "Palladium & Platinum Sputtering Targets",
        "country": "Belgium",
        "lead_time_days": 35,
        "dependency_pct": 68,
        "criticality": "HIGH",
        "alternate_supplier": "Materion Corp.",
        "alternate_lead_time_days": 40,
        "alternate_capacity_pct": 35,
        "geo_risk_factor": 1.08,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-07"
    },
    {
        "supplier_id": "SUP-009",
        "name": "Norilsk Specialty Metallics",
        "material": "Refined Palladium Precursors",
        "country": "Russia",
        "lead_time_days": 55,
        "dependency_pct": 79,
        "criticality": "CRITICAL",
        "alternate_supplier": "None",
        "alternate_lead_time_days": 0,
        "alternate_capacity_pct": 0,
        "geo_risk_factor": 1.9,
        "status": "HIGH_RISK",
        "single_point_of_failure": 1,
        "affected_process_ids": "PRC-07"
    },
    {
        "supplier_id": "SUP-010",
        "name": "Kyocera Fine Ceramics",
        "material": "Ceramic Electrostatic Chucks (ESC)",
        "country": "Japan",
        "lead_time_days": 42,
        "dependency_pct": 62,
        "criticality": "HIGH",
        "alternate_supplier": "NGK Spark Plug",
        "alternate_lead_time_days": 50,
        "alternate_capacity_pct": 38,
        "geo_risk_factor": 1.12,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-04,PRC-06"
    },
    {
        "supplier_id": "SUP-011",
        "name": "GlobalWafers Co., Ltd.",
        "material": "Silicon Epitaxial Wafers",
        "country": "Taiwan",
        "lead_time_days": 25,
        "dependency_pct": 48,
        "criticality": "HIGH",
        "alternate_supplier": "Siltronic AG",
        "alternate_lead_time_days": 32,
        "alternate_capacity_pct": 45,
        "geo_risk_factor": 1.35,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-01,PRC-02"
    },
    {
        "supplier_id": "SUP-012",
        "name": "Linde Gas Asia",
        "material": "Ultra-High Purity Nitrogen & Argon",
        "country": "Singapore",
        "lead_time_days": 7,
        "dependency_pct": 30,
        "criticality": "LOW",
        "alternate_supplier": "Air Liquide",
        "alternate_lead_time_days": 10,
        "alternate_capacity_pct": 70,
        "geo_risk_factor": 1.0,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-01,PRC-02,PRC-06,PRC-07"
    },
    {
        "supplier_id": "SUP-013",
        "name": "DuPont Interconnect Solutions",
        "material": "Polyimide Dielectric Coatings",
        "country": "United States",
        "lead_time_days": 20,
        "dependency_pct": 42,
        "criticality": "MEDIUM",
        "alternate_supplier": "Toray Industries",
        "alternate_lead_time_days": 26,
        "alternate_capacity_pct": 50,
        "geo_risk_factor": 1.0,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-10"
    },
    {
        "supplier_id": "SUP-014",
        "name": "SK Siltron CSS",
        "material": "Silicon Carbide (SiC) Substrates",
        "country": "South Korea",
        "lead_time_days": 38,
        "dependency_pct": 65,
        "criticality": "HIGH",
        "alternate_supplier": "Wolfspeed Inc.",
        "alternate_lead_time_days": 45,
        "alternate_capacity_pct": 35,
        "geo_risk_factor": 1.2,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-01,PRC-02"
    },
    {
        "supplier_id": "SUP-015",
        "name": "Zeon Corporation",
        "material": "C4F8 / Fluorocarbon Etch Specialty Gases",
        "country": "Japan",
        "lead_time_days": 24,
        "dependency_pct": 54,
        "criticality": "HIGH",
        "alternate_supplier": "Solvay Special Chem",
        "alternate_lead_time_days": 30,
        "alternate_capacity_pct": 40,
        "geo_risk_factor": 1.1,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-04"
    },
    {
        "supplier_id": "SUP-016",
        "name": "Resonac Holdings (Showa Denko)",
        "material": "High-Purity Ammonia (NH3)",
        "country": "Japan",
        "lead_time_days": 19,
        "dependency_pct": 49,
        "criticality": "MEDIUM",
        "alternate_supplier": "Tongwei Co.",
        "alternate_lead_time_days": 25,
        "alternate_capacity_pct": 45,
        "geo_risk_factor": 1.1,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-06"
    },
    {
        "supplier_id": "SUP-017",
        "name": "JX Nippon Mining & Metals",
        "material": "High-Purity Copper Sputtering Targets (99.9999%)",
        "country": "Japan",
        "lead_time_days": 26,
        "dependency_pct": 57,
        "criticality": "HIGH",
        "alternate_supplier": "Honeywell Electronic Materials",
        "alternate_lead_time_days": 32,
        "alternate_capacity_pct": 40,
        "geo_risk_factor": 1.1,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-07"
    },
    {
        "supplier_id": "SUP-018",
        "name": "SoulBrain Co., Ltd.",
        "material": "Ultra-High Purity Phosphoric Acid",
        "country": "South Korea",
        "lead_time_days": 16,
        "dependency_pct": 36,
        "criticality": "MEDIUM",
        "alternate_supplier": "Arkema",
        "alternate_lead_time_days": 22,
        "alternate_capacity_pct": 60,
        "geo_risk_factor": 1.15,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-04"
    },
    {
        "supplier_id": "SUP-019",
        "name": "Nata Optoelectronic Material",
        "material": "Trimethylaluminum (TMA) ALD Precursor",
        "country": "China",
        "lead_time_days": 35,
        "dependency_pct": 84,
        "criticality": "CRITICAL",
        "alternate_supplier": "UP Chemical (Partial)",
        "alternate_lead_time_days": 48,
        "alternate_capacity_pct": 16,
        "geo_risk_factor": 1.75,
        "status": "ALERT",
        "single_point_of_failure": 1,
        "affected_process_ids": "PRC-06"
    },
    {
        "supplier_id": "SUP-020",
        "name": "Tanaka Kikinzoku Kogyo",
        "material": "Gold & Silver Bonding Wire",
        "country": "Japan",
        "lead_time_days": 21,
        "dependency_pct": 46,
        "criticality": "MEDIUM",
        "alternate_supplier": "Heraeus Electronics",
        "alternate_lead_time_days": 24,
        "alternate_capacity_pct": 50,
        "geo_risk_factor": 1.1,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-10"
    },
    {
        "supplier_id": "SUP-021",
        "name": "Microchem Corp.",
        "material": "EBR (Edge Bead Removal) Solvent",
        "country": "United States",
        "lead_time_days": 12,
        "dependency_pct": 25,
        "criticality": "LOW",
        "alternate_supplier": "Avantor Performance",
        "alternate_lead_time_days": 15,
        "alternate_capacity_pct": 75,
        "geo_risk_factor": 1.0,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-03"
    },
    {
        "supplier_id": "SUP-022",
        "name": "Adeka Corporation",
        "material": "High-k Hafnium Dielectric Precursor",
        "country": "Japan",
        "lead_time_days": 32,
        "dependency_pct": 63,
        "criticality": "HIGH",
        "alternate_supplier": "Air Liquide Electronics",
        "alternate_lead_time_days": 38,
        "alternate_capacity_pct": 37,
        "geo_risk_factor": 1.12,
        "status": "ACTIVE",
        "single_point_of_failure": 0,
        "affected_process_ids": "PRC-06"
    },
]

# 4. Generate Production Lots (200 active lots)
def generate_lots():
    lots = []
    base_date = datetime(2026, 9, 15, 8, 0, 0)
    customer_tiers = ["Tier-1 Automotive", "Tier-1 Hyperscale AI", "Mobile Flagship", "Industrial IoT", "Aerospace Defense"]
    priorities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    priority_weights = [0.15, 0.35, 0.35, 0.15]
    
    # Map process_id to tools
    process_tools = {}
    for eq in EQUIPMENT_DATA:
        pid = eq["process_id"]
        if pid not in process_tools:
            process_tools[pid] = []
        process_tools[pid].append(eq["tool_id"])

    for i in range(1, 201):
        lot_id = f"LOT-{i:04d}"
        
        # Determine process index (distributed across 10 stages)
        # Weight slightly toward bottleneck stages (PRC-03 Litho, PRC-06 CVD, PRC-04 Etch)
        weights = [0.08, 0.08, 0.18, 0.15, 0.08, 0.18, 0.08, 0.07, 0.05, 0.05]
        proc_idx = random.choices(range(len(PROCESS_ROUTES)), weights=weights)[0]
        curr_route = PROCESS_ROUTES[proc_idx]
        current_process_id = curr_route["process_id"]
        
        # Next process
        if proc_idx + 1 < len(PROCESS_ROUTES):
            next_process_id = PROCESS_ROUTES[proc_idx + 1]["process_id"]
        else:
            next_process_id = "COMPLETED"
            
        # Assigned tool
        avail_tools = process_tools.get(current_process_id, ["LITH-01"])
        assigned_tool = random.choice(avail_tools)
        
        qty = random.choice([25, 50, 75, 100, 125, 150]) # Wafers per lot
        priority = random.choices(priorities, weights=priority_weights)[0]
        customer = random.choice(customer_tiers)
        
        due_offset_days = random.randint(2, 14) if priority != "CRITICAL" else random.randint(1, 4)
        due_date = base_date + timedelta(days=due_offset_days, hours=random.randint(0, 23))
        
        status = random.choices(["IN_QUEUE", "PROCESSING", "HOLD_METROLOGY", "EXPEDITED"], weights=[0.55, 0.35, 0.05, 0.05])[0]
        if priority == "CRITICAL" and status == "IN_QUEUE" and random.random() < 0.4:
            status = "EXPEDITED"
            
        wafer_val = 1200 if "Hyperscale" in customer else (950 if "Automotive" in customer else 650)
        lot_value_usd = qty * wafer_val

        lots.append({
            "lot_id": lot_id,
            "product_family": f"NEX-{random.choice(['AI-ACCEL', 'MCU-AUTO', 'RF-TRANS', 'MEM-HBM', 'PMIC-CORE'])}",
            "customer_tier": customer,
            "current_process_id": current_process_id,
            "current_process_name": curr_route["name"],
            "next_process_id": next_process_id,
            "assigned_tool_id": assigned_tool,
            "wafer_quantity": qty,
            "lot_value_usd": lot_value_usd,
            "priority": priority,
            "status": status,
            "entry_time": (base_date - timedelta(hours=random.randint(4, 96))).strftime("%Y-%m-%d %H:%M:%S"),
            "due_date": due_date.strftime("%Y-%m-%d %H:%M:%S"),
            "steps_completed": proc_idx,
            "total_steps": len(PROCESS_ROUTES)
        })
    return lots

# 5. Generate Historical Delays (650 records for ML training)
def generate_historical_delays(lots):
    records = []
    base_date = datetime(2026, 1, 1, 0, 0, 0)
    proc_cycle_map = {r["process_id"]: r["nominal_cycle_time_hr"] for r in PROCESS_ROUTES}
    
    for i in range(1, 651):
        record_id = f"HIST-{i:05d}"
        proc_idx = random.randint(0, len(PROCESS_ROUTES) - 1)
        proc_route = PROCESS_ROUTES[proc_idx]
        proc_id = proc_route["process_id"]
        
        tool_capacity = random.choice([30, 35, 40, 45, 50, 60, 70])
        utilization = round(random.uniform(45.0, 175.0), 1)
        wip_queue_size = int(round(tool_capacity * (utilization / 100.0)))
        
        downstream_queue_size = random.randint(15, 95)
        lot_qty = random.choice([25, 50, 75, 100, 125, 150])
        priority_val = random.choices([1, 2, 3, 4], weights=[0.15, 0.35, 0.35, 0.15])[0]
        remaining_stages = len(PROCESS_ROUTES) - proc_idx
        nominal_cycle = proc_cycle_map.get(proc_id, 5.0)
        
        chamber_health = random.randint(65, 99)
        active_disruption_flag = 1 if (random.random() < 0.12) else 0
        
        queue_excess = max(0.0, utilization - 100.0)
        base_delay = (queue_excess * 0.42) + (wip_queue_size * 0.28) + (downstream_queue_size * 0.12)
        priority_discount = (priority_val - 1) * 2.2
        health_penalty = max(0.0, (85 - chamber_health) * 0.35)
        disruption_penalty = active_disruption_flag * random.uniform(8.0, 22.0)
        
        noise = random.gauss(0, 1.8)
        actual_delay_hr = max(0.0, round(base_delay - priority_discount + health_penalty + disruption_penalty + noise, 2))
        
        records.append({
            "record_id": record_id,
            "timestamp": (base_date + timedelta(days=random.randint(0, 250), hours=random.randint(0, 23))).strftime("%Y-%m-%d %H:%M:%S"),
            "process_id": proc_id,
            "tool_nominal_capacity": tool_capacity,
            "wip_queue_size": wip_queue_size,
            "tool_utilization_pct": utilization,
            "downstream_queue_size": downstream_queue_size,
            "wafer_quantity": lot_qty,
            "lot_priority_num": priority_val,
            "remaining_stages": remaining_stages,
            "nominal_cycle_time_hr": nominal_cycle,
            "chamber_health": chamber_health,
            "has_active_disruption": active_disruption_flag,
            "actual_delay_hours": actual_delay_hr
        })
    return records

# 6. Generate Disruptions
def generate_disruptions():
    disruptions = [
        {
            "disruption_id": "DISR-2026-001",
            "type": "GEOPOLITICAL_EXPORT_RESTRICTION",
            "target_type": "SUPPLIER",
            "target_id": "SUP-002",
            "target_name": "Global Gallium Refining Ltd.",
            "severity": "CRITICAL",
            "status": "ACTIVE",
            "start_time": "2026-09-10 06:00:00",
            "estimated_duration_days": 21,
            "description": "Export quota restriction on high-purity Gallium substrates from primary supplier hub.",
            "impact_summary": "Affects 3 process routes (PRC-02, PRC-05, PRC-06) with 91% dependency and zero immediate second source.",
            "recommended_mitigation": "Immediately allocate reserve safety stock, qualify secondary supplier, and prioritize Tier-1 automotive lots."
        },
        {
            "disruption_id": "DISR-2026-002",
            "type": "EQUIPMENT_CHAMBER_DEGRADATION",
            "target_type": "EQUIPMENT",
            "target_id": "CVD-03",
            "target_name": "Tokyo Electron Telindy ALD/CVD",
            "severity": "HIGH",
            "status": "ACTIVE",
            "start_time": "2026-09-14 14:30:00",
            "estimated_duration_days": 2,
            "description": "Chamber RF match drift causing 153% WIP accumulation and queue back-pressure.",
            "impact_summary": "18 active production lots queued; downstream PVD and CMP processes facing starvation.",
            "recommended_mitigation": "Reallocate 40% batch volume to CVD-01 / CVD-04 and expedite scheduled preventive maintenance."
        },
        {
            "disruption_id": "DISR-2026-003",
            "type": "RAW_MATERIAL_LOGISTICS_DELAY",
            "target_type": "SUPPLIER",
            "target_id": "SUP-004",
            "target_name": "Ingas Purification Corp.",
            "severity": "CRITICAL",
            "status": "ACTIVE",
            "start_time": "2026-09-08 00:00:00",
            "estimated_duration_days": 30,
            "description": "Regional transit disruptions constraining neon gas supply shipments.",
            "impact_summary": "EUV/DUV laser uptime buffer reduced to 12 days safety threshold.",
            "recommended_mitigation": "Initiate air-freight contingency protocol with Cryoin backup supply channel."
        },
        {
            "disruption_id": "DISR-2026-004",
            "type": "UNSCHEDULED_STEPPER_CALIBRATION",
            "target_type": "EQUIPMENT",
            "target_id": "LITH-03",
            "target_name": "Nikon Immersion Scanner",
            "severity": "MEDIUM",
            "status": "MONITORING",
            "start_time": "2026-09-12 18:00:00",
            "estimated_duration_days": 1,
            "description": "Lens heating compensation drift under investigation.",
            "impact_summary": "Throughput derated by 15% pending optical re-baseline.",
            "recommended_mitigation": "Reroute non-critical layers to LITH-02."
        }
    ]
    return disruptions

def save_csv(filename, data):
    filepath = os.path.join(OUTPUT_DIR, filename)
    if not data:
        return
    keys = data[0].keys()
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Generated {filepath} ({len(data)} rows)")

def main():
    print("=" * 60)
    print("Generating Nexora Synthetic Demonstration Dataset (Seed: 42)...")
    print("=" * 60)
    
    lots = generate_lots()
    hist_delays = generate_historical_delays(lots)
    disruptions = generate_disruptions()
    
    save_csv("process_routes.csv", PROCESS_ROUTES)
    save_csv("equipment.csv", EQUIPMENT_DATA)
    save_csv("suppliers.csv", SUPPLIERS_DATA)
    save_csv("production_lots.csv", lots)
    save_csv("historical_delays.csv", hist_delays)
    save_csv("disruptions.csv", disruptions)
    
    print("=" * 60)
    print("Synthetic dataset successfully generated!")
    print("=" * 60)

if __name__ == "__main__":
    main()
