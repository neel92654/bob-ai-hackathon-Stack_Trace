import React, { useState, useEffect } from 'react';
import { 
  Sliders, 
  Play, 
  RefreshCw, 
  ShieldAlert, 
  ArrowRight, 
  Clock, 
  DollarSign, 
  Boxes, 
  Sparkles, 
  Factory, 
  Globe2, 
  CheckCircle2,
  TrendingUp,
  Activity,
  AlertTriangle,
  Info
} from 'lucide-react';
import { runSimulation, fetchSuppliers, fetchBottlenecks } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';

export function WhatIfSimulator({ preselectedSupplier = null, preselectedTool = null }) {
  const [scenarioType, setScenarioType] = useState('SUPPLIER_DISRUPTION');
  
  // Dynamic options
  const [supplierOptions, setSupplierOptions] = useState([]);
  const [equipmentOptions, setEquipmentOptions] = useState([]);
  
  // Scenario Params
  const [supplierId, setSupplierId] = useState(preselectedSupplier || 'SUP-002');
  const [supplierDuration, setSupplierDuration] = useState(14);
  
  const [toolId, setToolId] = useState(preselectedTool || 'CVD-03');
  const [toolFailureHours, setToolFailureHours] = useState(24);
  
  const [capToolId, setCapToolId] = useState('LITH-01');
  const [capacityReductionPct, setCapacityReductionPct] = useState(30);
  const [capacityDurationDays, setCapacityDurationDays] = useState(7);
  
  const [demandSurgePct, setDemandSurgePct] = useState(25);
  const [demandWeeks, setDemandWeeks] = useState(4);

  // Results
  const [simulationResult, setSimulationResult] = useState(null);
  const [simulating, setSimulating] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadOptions();
  }, []);

  useEffect(() => {
    if (preselectedSupplier) {
      setScenarioType('SUPPLIER_DISRUPTION');
      setSupplierId(preselectedSupplier);
    } else if (preselectedTool) {
      setScenarioType('EQUIPMENT_FAILURE');
      setToolId(preselectedTool);
    }
  }, [preselectedSupplier, preselectedTool]);

  async function loadOptions() {
    try {
      const [suppRes, toolRes] = await Promise.all([
        fetchSuppliers(),
        fetchBottlenecks()
      ]);
      setSupplierOptions(suppRes.data || []);
      setEquipmentOptions(toolRes.data || []);
    } catch (err) {
      console.error("Failed to load options for simulator:", err);
    }
  }

  async function handleExecuteSimulation() {
    try {
      setSimulating(true);
      setError(null);
      let params = {};

      if (scenarioType === 'SUPPLIER_DISRUPTION') {
        params = { supplier_id: supplierId, duration_days: Number(supplierDuration) };
      } else if (scenarioType === 'EQUIPMENT_FAILURE') {
        params = { tool_id: toolId, failure_duration_hours: Number(toolFailureHours) };
      } else if (scenarioType === 'CAPACITY_REDUCTION') {
        params = { tool_id: capToolId, capacity_reduction_pct: Number(capacityReductionPct), duration_days: Number(capacityDurationDays) };
      } else if (scenarioType === 'DEMAND_INCREASE') {
        params = { demand_increase_pct: Number(demandSurgePct), duration_weeks: Number(demandWeeks) };
      }

      const res = await runSimulation(scenarioType, params);
      setSimulationResult(res.data);
    } catch (err) {
      console.error("Simulation error:", err);
      setError(err.message || "Failed to execute simulation.");
    } finally {
      setSimulating(false);
    }
  }

  const scenarioCards = [
    {
      id: 'SUPPLIER_DISRUPTION',
      title: '1. Supplier Disruption',
      desc: 'Simulate raw material embargo or vendor supply delay',
      icon: Globe2
    },
    {
      id: 'EQUIPMENT_FAILURE',
      title: '2. Equipment Outage',
      desc: 'Simulate unexpected unscheduled tool breakdown',
      icon: Factory
    },
    {
      id: 'CAPACITY_REDUCTION',
      title: '3. Capacity Loss',
      desc: 'Simulate chamber derating or maintenance reduction',
      icon: Sliders
    },
    {
      id: 'DEMAND_INCREASE',
      title: '4. Demand Surge',
      desc: 'Simulate incoming customer wafer wafer volume spike',
      icon: TrendingUp
    }
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Page Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
            What-If Disruption Simulator
          </h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            Simulate operational shocks, tool outages, and supplier embargos to evaluate downstream delay and financial exposure before taking action.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="status-badge badge-neutral">Interactive Scenario Engine</span>
        </div>
      </div>

      {/* Scenario Type Selection Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px' }}>
        {scenarioCards.map(sc => {
          const isSelected = scenarioType === sc.id;
          const Icon = sc.icon;
          return (
            <div
              key={sc.id}
              onClick={() => setScenarioType(sc.id)}
              style={{
                padding: '16px',
                borderRadius: 'var(--radius-md)',
                border: isSelected ? '2px solid var(--primary-brand)' : '1px solid var(--border-light)',
                background: isSelected ? 'var(--primary-light)' : '#ffffff',
                cursor: 'pointer',
                transition: 'all var(--transition-fast)',
                boxShadow: isSelected ? 'var(--shadow-sm)' : 'none'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
                <div style={{
                  width: '28px',
                  height: '28px',
                  borderRadius: 'var(--radius-sm)',
                  background: isSelected ? 'var(--primary-brand)' : 'var(--surface-subtle)',
                  color: isSelected ? '#ffffff' : 'var(--text-secondary)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <Icon size={16} />
                </div>
                <h4 style={{ fontSize: '0.875rem', fontWeight: 700, color: isSelected ? 'var(--primary-brand)' : 'var(--text-primary)' }}>
                  {sc.title}
                </h4>
              </div>
              <p style={{ fontSize: '0.75rem', color: isSelected ? 'var(--text-secondary)' : 'var(--text-muted)' }}>
                {sc.desc}
              </p>
            </div>
          );
        })}
      </div>

      {/* Scenario Configuration Form */}
      <div className="enterprise-card" style={{ padding: '24px' }}>
        <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '16px' }}>
          Configure Scenario Parameters
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '20px', marginBottom: '20px' }}>
          {scenarioType === 'SUPPLIER_DISRUPTION' && (
            <>
              <div>
                <label className="form-label">Target Supplier</label>
                <select
                  className="form-select"
                  style={{ width: '100%' }}
                  value={supplierId}
                  onChange={(e) => setSupplierId(e.target.value)}
                >
                  {supplierOptions.map(s => (
                    <option key={s.supplier_id} value={s.supplier_id}>
                      {s.supplier_id} — {s.name} ({s.material}) {s.is_single_point_of_failure ? '★ SPoF' : ''}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="form-label">Disruption Duration: {supplierDuration} Days</label>
                <input
                  type="range"
                  min="1"
                  max="60"
                  value={supplierDuration}
                  onChange={(e) => setSupplierDuration(e.target.value)}
                  style={{ width: '100%', accentColor: 'var(--primary-brand)', marginTop: '8px' }}
                />
              </div>
            </>
          )}

          {scenarioType === 'EQUIPMENT_FAILURE' && (
            <>
              <div>
                <label className="form-label">Target Equipment Tool</label>
                <select
                  className="form-select"
                  style={{ width: '100%' }}
                  value={toolId}
                  onChange={(e) => setToolId(e.target.value)}
                >
                  {equipmentOptions.map(t => (
                    <option key={t.tool_id} value={t.tool_id}>
                      {t.tool_id} — {t.name} ({t.process_name})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="form-label">Outage Duration: {toolFailureHours} Hours</label>
                <input
                  type="range"
                  min="1"
                  max="72"
                  value={toolFailureHours}
                  onChange={(e) => setToolFailureHours(e.target.value)}
                  style={{ width: '100%', accentColor: 'var(--primary-brand)', marginTop: '8px' }}
                />
              </div>
            </>
          )}

          {scenarioType === 'CAPACITY_REDUCTION' && (
            <>
              <div>
                <label className="form-label">Target Tool</label>
                <select
                  className="form-select"
                  style={{ width: '100%' }}
                  value={capToolId}
                  onChange={(e) => setCapToolId(e.target.value)}
                >
                  {equipmentOptions.map(t => (
                    <option key={t.tool_id} value={t.tool_id}>
                      {t.tool_id} — {t.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="form-label">Capacity Reduction: {capacityReductionPct}%</label>
                <input
                  type="range"
                  min="5"
                  max="75"
                  value={capacityReductionPct}
                  onChange={(e) => setCapacityReductionPct(e.target.value)}
                  style={{ width: '100%', accentColor: 'var(--primary-brand)', marginTop: '8px' }}
                />
              </div>

              <div>
                <label className="form-label">Duration: {capacityDurationDays} Days</label>
                <input
                  type="range"
                  min="1"
                  max="30"
                  value={capacityDurationDays}
                  onChange={(e) => setCapacityDurationDays(e.target.value)}
                  style={{ width: '100%', accentColor: 'var(--primary-brand)', marginTop: '8px' }}
                />
              </div>
            </>
          )}

          {scenarioType === 'DEMAND_INCREASE' && (
            <>
              <div>
                <label className="form-label">Demand Surge: +{demandSurgePct}%</label>
                <input
                  type="range"
                  min="10"
                  max="100"
                  value={demandSurgePct}
                  onChange={(e) => setDemandSurgePct(e.target.value)}
                  style={{ width: '100%', accentColor: 'var(--primary-brand)', marginTop: '8px' }}
                />
              </div>

              <div>
                <label className="form-label">Surge Horizon: {demandWeeks} Weeks</label>
                <input
                  type="range"
                  min="1"
                  max="12"
                  value={demandWeeks}
                  onChange={(e) => setDemandWeeks(e.target.value)}
                  style={{ width: '100%', accentColor: 'var(--primary-brand)', marginTop: '8px' }}
                />
              </div>
            </>
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-start', gap: '12px' }}>
          <button
            className="btn-primary"
            onClick={handleExecuteSimulation}
            disabled={simulating}
            style={{ padding: '10px 24px', fontSize: '0.9rem' }}
          >
            {simulating ? (
              <>
                <div className="animate-spin" style={{ width: '16px', height: '16px', border: '2px solid #ffffff', borderTopColor: 'transparent', borderRadius: '50%' }} />
                <span>Running Simulation...</span>
              </>
            ) : (
              <>
                <Play size={16} />
                <span>Run Disruption Simulation</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div style={{ padding: '14px', borderRadius: 'var(--radius-md)', background: 'var(--critical-bg)', border: '1px solid var(--critical-border)', color: 'var(--critical-text)' }}>
          {error}
        </div>
      )}

      {/* Simulation Results Section */}
      {simulationResult && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span className="status-badge badge-neutral">SIMULATION RESULTS</span>
            <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
              Scenario: {simulationResult.scenario_name || scenarioType}
            </span>
          </div>

          {/* Side-by-Side Comparison Metrics (BASELINE vs SIMULATED vs DELTA) */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
            
            {/* Risk Score Diff */}
            <div className="enterprise-card" style={{ padding: '18px', borderLeft: '4px solid var(--critical)' }}>
              <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                Operational Risk Score
              </span>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px', marginTop: '6px' }}>
                <span style={{ fontSize: '1.2rem', color: 'var(--text-muted)' }}>
                  {simulationResult.baseline?.risk_score || 78}
                </span>
                <ArrowRight size={14} color="var(--text-muted)" />
                <span style={{ fontSize: '1.6rem', fontWeight: 700, color: 'var(--critical-text)' }}>
                  {simulationResult.simulated?.risk_score || 94}
                </span>
              </div>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--critical-text)', marginTop: '4px' }}>
                +{simulationResult.delta?.risk_score_delta || 16} pts Increase
              </div>
            </div>

            {/* Affected Lots Diff */}
            <div className="enterprise-card" style={{ padding: '18px', borderLeft: '4px solid var(--high)' }}>
              <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                Affected Production Lots
              </span>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px', marginTop: '6px' }}>
                <span style={{ fontSize: '1.2rem', color: 'var(--text-muted)' }}>
                  {simulationResult.baseline?.affected_lots || 12}
                </span>
                <ArrowRight size={14} color="var(--text-muted)" />
                <span style={{ fontSize: '1.6rem', fontWeight: 700, color: 'var(--high-text)' }}>
                  {simulationResult.simulated?.affected_lots || 42}
                </span>
              </div>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--high-text)', marginTop: '4px' }}>
                +{simulationResult.delta?.affected_lots_delta || 30} Lots Impacted
              </div>
            </div>

            {/* Delay Drift Diff */}
            <div className="enterprise-card" style={{ padding: '18px', borderLeft: '4px solid var(--warning)' }}>
              <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                Total Schedule Delay Drift
              </span>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px', marginTop: '6px' }}>
                <span style={{ fontSize: '1.2rem', color: 'var(--text-muted)' }}>
                  {simulationResult.baseline?.total_delay_hours || 48}h
                </span>
                <ArrowRight size={14} color="var(--text-muted)" />
                <span style={{ fontSize: '1.6rem', fontWeight: 700, color: 'var(--warning-text)' }}>
                  {simulationResult.simulated?.total_delay_hours || 284.4}h
                </span>
              </div>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--warning-text)', marginTop: '4px' }}>
                +{simulationResult.delta?.delay_hours_delta || 236.4}h Drift
              </div>
            </div>

            {/* Financial SLA Exposure */}
            <div className="enterprise-card" style={{ padding: '18px', borderLeft: '4px solid var(--purple)' }}>
              <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                Estimated SLA Penalty Exposure
              </span>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px', marginTop: '6px' }}>
                <span style={{ fontSize: '1.2rem', color: 'var(--text-muted)' }}>
                  $0.4M
                </span>
                <ArrowRight size={14} color="var(--text-muted)" />
                <span style={{ fontSize: '1.6rem', fontWeight: 700, color: 'var(--purple-text)' }}>
                  ${simulationResult.financial_impact_millions || 2.4}M
                </span>
              </div>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--purple-text)', marginTop: '4px' }}>
                High Financial Urgency
              </div>
            </div>
          </div>

          {/* Operational Assessment & Recommended Mitigation Protocol */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '20px' }}>
            
            {/* Operational Impact */}
            <div className="enterprise-card" style={{ padding: '20px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                <AlertTriangle size={18} color="var(--high)" />
                <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                  Operational Impact Assessment
                </h4>
              </div>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.45 }}>
                {simulationResult.operational_impact_summary || 
                 `Disrupting ${supplierId || toolId} exhausts active buffer inventory in 4 days. Downstream process stages will experience immediate wafer queue starvation, leading to delivery schedule penalties.`}
              </p>
            </div>

            {/* Recommended Protocol */}
            <div className="enterprise-card" style={{ padding: '20px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                <Sparkles size={18} color="var(--primary-brand)" />
                <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                  Synthesized Mitigation Protocol
                </h4>
              </div>
              <div style={{
                padding: '12px 14px',
                borderRadius: 'var(--radius-md)',
                background: 'var(--primary-light)',
                border: '1px solid var(--primary-border)'
              }}>
                <div style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--primary-brand)' }}>
                  {simulationResult.mitigation_recommendation?.action || 'Activate Secondary Sourcing & Divert WIP Queues'}
                </div>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '4px', lineHeight: 1.35 }}>
                  {simulationResult.mitigation_recommendation?.detail || 'Engage alternate spot supplier immediately and reroute affected high-priority wafer lots to secondary fab chambers.'}
                </p>
              </div>

              {/* Supporting Response Directives */}
              {simulationResult.recommended_actions && simulationResult.recommended_actions.length > 0 && (
                <div style={{ marginTop: '12px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  <div style={{ fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)' }}>
                    Action Directives:
                  </div>
                  {simulationResult.recommended_actions.map((act, idx) => (
                    <div key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                      <CheckCircle2 size={14} color="var(--primary-brand)" style={{ flexShrink: 0, marginTop: '2px' }} />
                      <span><strong>{act.action}</strong> — <span style={{ color: 'var(--text-muted)' }}>{act.expected_benefit || act.reason}</span></span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
