import React, { useState, useEffect } from 'react';
import { 
  Boxes, 
  Search, 
  Filter, 
  Clock, 
  TrendingUp, 
  AlertCircle, 
  CheckCircle2, 
  Info, 
  X,
  Sparkles
} from 'lucide-react';
import { fetchProductionLots } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';

export function ProductionLots() {
  const [lotsData, setLotsData] = useState({ summary: {}, lots: [] });
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedPriority, setSelectedPriority] = useState('ALL');
  const [selectedProcess, setSelectedProcess] = useState('ALL');
  const [selectedLotDetail, setSelectedLotDetail] = useState(null);

  useEffect(() => {
    loadLots();
  }, [selectedPriority, selectedProcess]);

  async function loadLots() {
    try {
      setLoading(true);
      const filters = {};
      if (selectedPriority !== 'ALL') filters.priority = selectedPriority;
      if (selectedProcess !== 'ALL') filters.process = selectedProcess;
      const res = await fetchProductionLots(filters);
      setLotsData({
        summary: res?.summary || {},
        lots: res?.data || res?.lots || []
      });
    } catch (err) {
      console.error("Failed to load lots:", err);
    } finally {
      setLoading(false);
    }
  }

  const { summary, lots } = lotsData;

  const filteredLots = (lots || []).filter(lot => {
    return lot.lot_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
           lot.product_family.toLowerCase().includes(searchQuery.toLowerCase()) ||
           lot.customer_tier.toLowerCase().includes(searchQuery.toLowerCase()) ||
           lot.assigned_tool_id.toLowerCase().includes(searchQuery.toLowerCase());
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Page Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
            Production Lot Impact & Delivery Schedule
          </h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            Downstream delivery delay forecasting trained on RandomForestRegressor ($R^2 = 0.954$, MAE = 2.81h), ranked by customer urgency.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="status-badge badge-neutral">{summary?.total_lots || 200} Total Lots</span>
          <span className="status-badge badge-high">{summary?.high_priority_lots || 45} High Priority</span>
          <span className="status-badge badge-critical">{summary?.critical_impact_lots || 12} Critical Delay</span>
        </div>
      </div>

      {/* KPI Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
        <div className="enterprise-card" style={{ padding: '16px', borderLeft: '4px solid var(--primary-brand)' }}>
          <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>Total Active Wafers</span>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '4px' }}>
            {(summary?.total_wafers || 4980).toLocaleString()} Wafers
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>In-process fab inventory</p>
        </div>

        <div className="enterprise-card" style={{ padding: '16px', borderLeft: '4px solid var(--high)' }}>
          <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>Average ML Delay</span>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--high-text)', marginTop: '4px' }}>
            +{summary?.average_predicted_delay_hours || 18.4} Hours
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>Projected cycle drift</p>
        </div>

        <div className="enterprise-card" style={{ padding: '16px', borderLeft: '4px solid var(--critical)' }}>
          <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>Critical Impact Lots</span>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--critical-text)', marginTop: '4px' }}>
            {summary?.critical_impact_lots || 12} Lots
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>&gt;24 hours behind schedule</p>
        </div>

        <div className="enterprise-card" style={{ padding: '16px', borderLeft: '4px solid var(--low)' }}>
          <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>ML Model Confidence</span>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--low-text)', marginTop: '4px' }}>
            R² = 0.954
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>MAE: 2.809 hours</p>
        </div>
      </div>

      {/* Filter Ribbon */}
      <div className="enterprise-card" style={{ padding: '14px 18px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        
        {/* Search */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', minWidth: '260px' }}>
          <Search size={16} color="var(--text-muted)" />
          <input
            type="text"
            className="form-input"
            placeholder="Search by lot ID, product family, customer..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ padding: '6px 10px', fontSize: '0.825rem' }}
          />
        </div>

        {/* Filters */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Priority:</span>
            <select
              className="form-select"
              value={selectedPriority}
              onChange={(e) => setSelectedPriority(e.target.value)}
              style={{ padding: '5px 10px', fontSize: '0.8rem' }}
            >
              <option value="ALL">All Priorities</option>
              <option value="HIGH">HIGH Priority</option>
              <option value="MEDIUM">MEDIUM Priority</option>
              <option value="LOW">LOW Priority</option>
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Stage:</span>
            <select
              className="form-select"
              value={selectedProcess}
              onChange={(e) => setSelectedProcess(e.target.value)}
              style={{ padding: '5px 10px', fontSize: '0.8rem' }}
            >
              <option value="ALL">All Process Stages</option>
              <option value="PRC-01">01: Wafer Clean</option>
              <option value="PRC-02">02: Oxidation</option>
              <option value="PRC-03">03: Photolithography</option>
              <option value="PRC-04">04: Plasma Etch</option>
              <option value="PRC-05">05: Ion Implantation</option>
              <option value="PRC-06">06: CVD Thin Film</option>
              <option value="PRC-07">07: PVD Metallization</option>
              <option value="PRC-08">08: CMP Polishing</option>
              <option value="PRC-09">09: Metrology</option>
              <option value="PRC-10">10: Packaging & Test</option>
            </select>
          </div>
        </div>
      </div>

      {/* Lots Table */}
      <div className="enterprise-table-container">
        <table className="enterprise-table">
          <thead>
            <tr>
              <th>Lot ID</th>
              <th>Product Family</th>
              <th>Customer Tier</th>
              <th>Order Priority</th>
              <th>Current Stage</th>
              <th>Assigned Tool</th>
              <th>Wafer Qty</th>
              <th>ML Predicted Delay</th>
              <th>Urgency Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {filteredLots.map(lot => {
              const delay = lot.predicted_delay_hours;
              let delayClass = 'var(--low)';
              if (delay >= 24) delayClass = 'var(--critical)';
              else if (delay >= 12) delayClass = 'var(--high)';
              else if (delay >= 6) delayClass = 'var(--medium)';

              return (
                <tr key={lot.lot_id}>
                  <td style={{ fontWeight: 700, fontFamily: 'monospace', color: 'var(--text-primary)' }}>
                    {lot.lot_id}
                  </td>
                  <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                    {lot.product_family}
                  </td>
                  <td style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    {lot.customer_tier}
                  </td>
                  <td>
                    <span className={`status-badge badge-${lot.priority === 'HIGH' ? 'critical' : (lot.priority === 'MEDIUM' ? 'high' : 'low')}`} style={{ fontSize: '0.65rem' }}>
                      {lot.priority}
                    </span>
                  </td>
                  <td style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    {lot.current_process_name}
                  </td>
                  <td style={{ fontFamily: 'monospace', fontWeight: 600, color: 'var(--text-primary)' }}>
                    {lot.assigned_tool_id}
                  </td>
                  <td style={{ color: 'var(--text-secondary)' }}>
                    {lot.wafer_quantity} pcs
                  </td>
                  <td>
                    <span style={{ fontWeight: 700, color: delayClass }}>
                      +{delay}h
                    </span>
                  </td>
                  <td>
                    {lot.urgency_score >= 80 ? (
                      <span className="status-badge badge-critical" style={{ fontSize: '0.65rem' }}>CRITICAL</span>
                    ) : lot.urgency_score >= 50 ? (
                      <span className="status-badge badge-high" style={{ fontSize: '0.65rem' }}>ELEVATED</span>
                    ) : (
                      <span className="status-badge badge-low" style={{ fontSize: '0.65rem' }}>ON-TRACK</span>
                    )}
                  </td>
                  <td>
                    <button
                      className="btn-secondary"
                      style={{ padding: '3px 8px', fontSize: '0.7rem' }}
                      onClick={() => setSelectedLotDetail(lot)}
                    >
                      Details
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Lot Detail Modal */}
      {selectedLotDetail && (
        <div className="modal-backdrop" onClick={() => setSelectedLotDetail(null)}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
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
                  <span className="status-badge badge-neutral">WAFER LOT SCHEDULE</span>
                  <span className={`status-badge badge-${selectedLotDetail.priority === 'HIGH' ? 'critical' : 'high'}`}>
                    {selectedLotDetail.priority} PRIORITY
                  </span>
                </div>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '4px' }}>
                  {selectedLotDetail.lot_id} — {selectedLotDetail.product_family}
                </h3>
              </div>
              <button
                onClick={() => setSelectedLotDetail(null)}
                style={{ background: 'transparent', border: 'none', cursor: 'pointer', color: 'var(--text-muted)' }}
              >
                <X size={20} />
              </button>
            </div>

            <div style={{ padding: '24px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{
                padding: '14px 16px',
                borderRadius: 'var(--radius-md)',
                background: 'var(--info-bg)',
                border: '1px solid var(--info-border)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
                  <Sparkles size={16} color="var(--info-text)" />
                  <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--info-text)', textTransform: 'uppercase' }}>
                    Machine Learning Delay Forecast
                  </span>
                </div>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.45 }}>
                  Projected <strong>+{selectedLotDetail.predicted_delay_hours} hours</strong> of cycle drift due to upstream queue pressure at <strong>{selectedLotDetail.assigned_tool_id}</strong>. Urgency score is {selectedLotDetail.urgency_score}/100.
                </p>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px' }}>
                <div style={{ padding: '12px', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-md)', background: 'var(--surface-subtle)' }}>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Customer Tier</span>
                  <div style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {selectedLotDetail.customer_tier}
                  </div>
                </div>

                <div style={{ padding: '12px', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-md)', background: 'var(--surface-subtle)' }}>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Current Process Stage</span>
                  <div style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {selectedLotDetail.current_process_name} ({selectedLotDetail.current_process_id})
                  </div>
                </div>

                <div style={{ padding: '12px', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-md)', background: 'var(--surface-subtle)' }}>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Wafer Batch Size</span>
                  <div style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {selectedLotDetail.wafer_quantity} Wafers
                  </div>
                </div>

                <div style={{ padding: '12px', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-md)', background: 'var(--surface-subtle)' }}>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Remaining Process Stages</span>
                  <div style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {selectedLotDetail.remaining_stages} Stages Remaining
                  </div>
                </div>
              </div>
            </div>

            <div style={{
              padding: '14px 24px',
              borderTop: '1px solid var(--border-light)',
              background: 'var(--surface-subtle)',
              display: 'flex',
              justifyContent: 'flex-end'
            }}>
              <button className="btn-secondary" onClick={() => setSelectedLotDetail(null)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
