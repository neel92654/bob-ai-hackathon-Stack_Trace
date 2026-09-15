import React, { useState, useEffect } from 'react';
import { 
  Factory, 
  Search, 
  Filter, 
  AlertTriangle, 
  Info, 
  Sliders, 
  ArrowRight, 
  Wrench, 
  Activity, 
  CheckCircle2, 
  X,
  ChevronRight,
  Boxes
} from 'lucide-react';
import { fetchBottlenecks, fetchBottleneckDetails } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';
import { ProcessFlow } from '../components/ProcessFlow';

export function Bottlenecks({ onSimulateTool }) {
  const [bottlenecks, setBottlenecks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedProcess, setSelectedProcess] = useState('ALL');
  const [selectedRisk, setSelectedRisk] = useState('ALL');
  const [selectedToolDetails, setSelectedToolDetails] = useState(null);
  const [detailsLoading, setDetailsLoading] = useState(false);

  useEffect(() => {
    loadBottlenecks();
  }, []);

  async function loadBottlenecks() {
    try {
      setLoading(true);
      const res = await fetchBottlenecks();
      setBottlenecks(res.data || []);
    } catch (err) {
      console.error("Failed to load bottlenecks:", err);
    } finally {
      setLoading(false);
    }
  }

  async function handleOpenDetails(toolId) {
    try {
      setDetailsLoading(true);
      const res = await fetchBottleneckDetails(toolId);
      setSelectedToolDetails(res.data);
    } catch (err) {
      console.error("Failed to fetch tool details:", err);
    } finally {
      setDetailsLoading(false);
    }
  }

  const filteredTools = bottlenecks.filter(tool => {
    const matchesSearch = tool.tool_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          tool.process_name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesProcess = selectedProcess === 'ALL' || tool.process_id === selectedProcess;
    const matchesRisk = selectedRisk === 'ALL' || tool.risk_level === selectedRisk;
    return matchesSearch && matchesProcess && matchesRisk;
  });

  const uniqueProcesses = Array.from(new Set(bottlenecks.map(b => b.process_id)));
  const criticalCount = bottlenecks.filter(b => b.risk_level === 'CRITICAL').length;
  const highCount = bottlenecks.filter(b => b.risk_level === 'HIGH').length;
  const mediumCount = bottlenecks.filter(b => b.risk_level === 'MEDIUM').length;
  const lowCount = bottlenecks.filter(b => b.risk_level === 'LOW').length;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Page Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
            Fab Bottleneck Intelligence
          </h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            Identify equipment and process stages constraining production throughput across 10 sequential fab operations.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          <span className="status-badge badge-critical">{criticalCount} Critical</span>
          <span className="status-badge badge-high">{highCount} High</span>
          <span className="status-badge badge-medium">{mediumCount} Medium</span>
          <span className="status-badge badge-low">{lowCount} Nominal</span>
        </div>
      </div>

      {/* Sequential Process Flow Visualizer */}
      <ProcessFlow 
        activeProcessId={selectedToolDetails?.process_id || 'PRC-06'} 
        activeToolId={selectedToolDetails?.tool_id || 'CVD-03'} 
        riskLevel={selectedToolDetails?.risk_level || 'CRITICAL'} 
      />

      {/* Filter Ribbon */}
      <div className="enterprise-card" style={{ padding: '14px 18px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        
        {/* Search */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', minWidth: '260px' }}>
          <Search size={16} color="var(--text-muted)" />
          <input
            type="text"
            className="form-input"
            placeholder="Search by tool ID, name, process..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ padding: '6px 10px', fontSize: '0.825rem' }}
          />
        </div>

        {/* Filters */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Process:</span>
            <select
              className="form-select"
              value={selectedProcess}
              onChange={(e) => setSelectedProcess(e.target.value)}
              style={{ padding: '5px 10px', fontSize: '0.8rem' }}
            >
              <option value="ALL">All Process Stages</option>
              {uniqueProcesses.map(p => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Risk Level:</span>
            <select
              className="form-select"
              value={selectedRisk}
              onChange={(e) => setSelectedRisk(e.target.value)}
              style={{ padding: '5px 10px', fontSize: '0.8rem' }}
            >
              <option value="ALL">All Risk Tiers</option>
              <option value="CRITICAL">CRITICAL (&gt;120%)</option>
              <option value="HIGH">HIGH (100-120%)</option>
              <option value="MEDIUM">MEDIUM (80-100%)</option>
              <option value="LOW">LOW (&lt;80%)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Equipment Bottleneck Table */}
      <div className="enterprise-table-container">
        <table className="enterprise-table">
          <thead>
            <tr>
              <th>Tool ID</th>
              <th>Equipment Name</th>
              <th>Process Stage</th>
              <th>Utilization Rate</th>
              <th>WIP Queue</th>
              <th>Rated Capacity</th>
              <th>Risk Severity</th>
              <th>Chamber Health</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredTools.map(tool => {
              const util = tool.utilization_pct;
              let utilColor = 'var(--low)';
              if (util >= 120) utilColor = 'var(--critical)';
              else if (util >= 100) utilColor = 'var(--high)';
              else if (util >= 80) utilColor = 'var(--medium)';

              return (
                <tr key={tool.tool_id}>
                  <td style={{ fontWeight: 700, fontFamily: 'monospace', color: 'var(--text-primary)' }}>
                    {tool.tool_id}
                  </td>
                  <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                    {tool.name}
                  </td>
                  <td style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    {tool.process_name}
                  </td>
                  <td style={{ minWidth: '150px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontSize: '0.825rem', fontWeight: 700, minWidth: '50px', color: utilColor }}>
                        {util}%
                      </span>
                      <div className="progress-track" style={{ flex: 1, height: '7px' }}>
                        <div
                          className="progress-fill"
                          style={{
                            width: `${Math.min(100, util)}%`,
                            background: utilColor
                          }}
                        />
                      </div>
                    </div>
                  </td>
                  <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                    {tool.current_wip} wafers
                  </td>
                  <td style={{ color: 'var(--text-secondary)' }}>
                    {tool.nominal_capacity} / shift
                  </td>
                  <td>
                    <RiskBadge level={tool.risk_level} score={tool.risk_score} size="sm" />
                  </td>
                  <td>
                    <span style={{
                      fontSize: '0.78rem',
                      fontWeight: 600,
                      color: tool.chamber_health < 75 ? 'var(--critical-text)' : 'var(--text-secondary)'
                    }}>
                      {tool.chamber_health}%
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <button
                        className="btn-secondary"
                        style={{ padding: '4px 8px', fontSize: '0.72rem' }}
                        onClick={() => handleOpenDetails(tool.tool_id)}
                      >
                        Drilldown
                      </button>
                      <button
                        className="btn-secondary"
                        style={{ padding: '4px 8px', fontSize: '0.72rem' }}
                        onClick={() => onSimulateTool(tool.tool_id)}
                      >
                        Simulate
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Tool Detail Slide-Over / Dialog */}
      {selectedToolDetails && (
        <div className="modal-backdrop" onClick={() => setSelectedToolDetails(null)}>
          <div className="modal-dialog" style={{ maxWidth: '720px' }} onClick={(e) => e.stopPropagation()}>
            <div style={{
              padding: '18px 24px',
              borderBottom: '1px solid var(--border-light)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              background: 'var(--surface-subtle)'
            }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className="status-badge badge-neutral">EQUIPMENT TELEMETRY</span>
                  <RiskBadge level={selectedToolDetails.risk_level} score={selectedToolDetails.risk_score} />
                </div>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '4px' }}>
                  {selectedToolDetails.tool_id} — {selectedToolDetails.name}
                </h3>
              </div>
              <button
                onClick={() => setSelectedToolDetails(null)}
                style={{ background: 'transparent', border: 'none', cursor: 'pointer', color: 'var(--text-muted)' }}
              >
                <X size={20} />
              </button>
            </div>

            <div style={{ padding: '24px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '18px' }}>
              {/* Algorithmic Reason */}
              <div style={{
                padding: '14px 16px',
                borderRadius: 'var(--radius-md)',
                background: 'var(--info-bg)',
                border: '1px solid var(--info-border)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
                  <Info size={16} color="var(--info-text)" />
                  <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--info-text)', textTransform: 'uppercase' }}>
                    Bottleneck Diagnostic Reason
                  </span>
                </div>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.45 }}>
                  {selectedToolDetails.explanation}
                </p>
              </div>

              {/* KPI Cards */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px' }}>
                <div style={{ padding: '12px', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-md)', background: 'var(--surface-subtle)' }}>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Utilization Rate</span>
                  <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--critical-text)' }}>
                    {selectedToolDetails.utilization_pct}%
                  </div>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>{selectedToolDetails.current_wip} / {selectedToolDetails.nominal_capacity} wafers</span>
                </div>

                <div style={{ padding: '12px', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-md)', background: 'var(--surface-subtle)' }}>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Chamber Health</span>
                  <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {selectedToolDetails.chamber_health}%
                  </div>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Service due in {selectedToolDetails.maintenance_due_hours}h</span>
                </div>

                <div style={{ padding: '12px', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-md)', background: 'var(--surface-subtle)' }}>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Process Stage</span>
                  <div style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {selectedToolDetails.process_name}
                  </div>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>ID: {selectedToolDetails.process_id}</span>
                </div>
              </div>

              {/* Queued Lots Table */}
              {selectedToolDetails.queued_lots && selectedToolDetails.queued_lots.length > 0 && (
                <div>
                  <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '8px' }}>
                    Queued Production Lots ({selectedToolDetails.queued_lots.length})
                  </h4>
                  <div className="enterprise-table-container" style={{ maxHeight: '180px', overflowY: 'auto' }}>
                    <table className="enterprise-table">
                      <thead>
                        <tr>
                          <th>Lot ID</th>
                          <th>Product Family</th>
                          <th>Customer</th>
                          <th>Priority</th>
                          <th>ML Predicted Delay</th>
                        </tr>
                      </thead>
                      <tbody>
                        {selectedToolDetails.queued_lots.map(l => (
                          <tr key={l.lot_id}>
                            <td style={{ fontWeight: 700, fontFamily: 'monospace' }}>{l.lot_id}</td>
                            <td>{l.product_family}</td>
                            <td>{l.customer_tier}</td>
                            <td>
                              <span className={`status-badge badge-${l.lot_priority === 'HIGH' ? 'high' : 'neutral'}`} style={{ fontSize: '0.65rem' }}>
                                {l.lot_priority}
                              </span>
                            </td>
                            <td style={{ fontWeight: 700, color: 'var(--critical-text)' }}>
                              +{l.predicted_delay_hours}h
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>

            <div style={{
              padding: '14px 24px',
              borderTop: '1px solid var(--border-light)',
              background: 'var(--surface-subtle)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <button
                className="btn-primary"
                onClick={() => {
                  const id = selectedToolDetails.tool_id;
                  setSelectedToolDetails(null);
                  onSimulateTool(id);
                }}
              >
                <Sliders size={14} />
                <span>Simulate Outage on {selectedToolDetails.tool_id}</span>
              </button>
              <button className="btn-secondary" onClick={() => setSelectedToolDetails(null)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
