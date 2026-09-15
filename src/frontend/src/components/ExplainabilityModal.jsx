import React from 'react';
import { X, Info, ShieldAlert, CheckCircle2, TrendingUp, AlertTriangle, Cpu, Globe2 } from 'lucide-react';
import { RiskBadge } from './RiskBadge';

export function ExplainabilityModal({ isOpen, onClose, data, type = 'bottleneck' }) {
  if (!isOpen || !data) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
        {/* Modal Header */}
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
              <span className="status-badge badge-neutral" style={{ fontSize: '0.68rem' }}>
                {type === 'bottleneck' ? 'EQUIPMENT AUDIT' : 'SUPPLIER RISK AUDIT'}
              </span>
              <RiskBadge level={data.risk_level || 'HIGH'} score={data.risk_score || data.supplier_risk_score} />
            </div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '4px' }}>
              {type === 'bottleneck' ? `${data.tool_id} — ${data.name}` : `${data.supplier_id} — ${data.name}`}
            </h3>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              borderRadius: 'var(--radius-sm)',
              color: 'var(--text-muted)',
              padding: '6px',
              cursor: 'pointer'
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Modal Body */}
        <div style={{ padding: '24px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '18px' }}>
          {/* Explanation Callout */}
          <div style={{
            padding: '14px 16px',
            borderRadius: 'var(--radius-md)',
            background: 'var(--info-bg)',
            border: '1px solid var(--info-border)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
              <Info size={16} color="var(--info-text)" />
              <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--info-text)', textTransform: 'uppercase' }}>
                Algorithmic Assessment
              </span>
            </div>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.45 }}>
              {data.explanation}
            </p>
          </div>

          {/* Metric Breakdown */}
          {type === 'bottleneck' ? (
            <div>
              <h4 style={{ fontSize: '0.825rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '10px' }}>
                Equipment Telemetry & Queue Health
              </h4>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px' }}>
                <div style={{ padding: '12px', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-md)', background: 'var(--surface-subtle)' }}>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>WIP / Capacity</span>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '2px' }}>
                    {data.current_wip} / {data.nominal_capacity} wafers
                  </div>
                  <div className="progress-track" style={{ marginTop: '8px' }}>
                    <div
                      className="progress-fill"
                      style={{
                        width: `${Math.min(100, data.utilization_pct)}%`,
                        background: data.utilization_pct >= 120 ? 'var(--critical)' : (data.utilization_pct >= 100 ? 'var(--high)' : 'var(--low)')
                      }}
                    />
                  </div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px', textAlign: 'right' }}>
                    {data.utilization_pct}% utilization
                  </div>
                </div>

                <div style={{ padding: '12px', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-md)', background: 'var(--surface-subtle)' }}>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Chamber Health</span>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '2px' }}>
                    {data.chamber_health}%
                  </div>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px', display: 'block' }}>
                    Service due in {data.maintenance_due_hours}h
                  </span>
                </div>
              </div>

              {/* Queued Lots Preview */}
              {data.queued_lots && data.queued_lots.length > 0 && (
                <div style={{ marginTop: '16px' }}>
                  <h4 style={{ fontSize: '0.825rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '8px' }}>
                    Queued Production Lots ({data.queued_lots.length})
                  </h4>
                  <div className="enterprise-table-container" style={{ maxHeight: '180px', overflowY: 'auto' }}>
                    <table className="enterprise-table">
                      <thead>
                        <tr>
                          <th>Lot ID</th>
                          <th>Product</th>
                          <th>Priority</th>
                          <th>ML Delay Forecast</th>
                        </tr>
                      </thead>
                      <tbody>
                        {data.queued_lots.map(l => (
                          <tr key={l.lot_id}>
                            <td style={{ fontWeight: 600, fontFamily: 'monospace' }}>{l.lot_id}</td>
                            <td>{l.product_family}</td>
                            <td>
                              <span className={`status-badge badge-${l.lot_priority === 'HIGH' ? 'high' : 'neutral'}`} style={{ fontSize: '0.65rem' }}>
                                {l.lot_priority}
                              </span>
                            </td>
                            <td style={{ fontWeight: 600, color: 'var(--high-text)' }}>
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
          ) : (
            <div>
              <h4 style={{ fontSize: '0.825rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '10px' }}>
                5-Factor Weighted Risk Scoring Breakdown
              </h4>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '10px' }}>
                <div style={{ padding: '10px 12px', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-md)', background: 'var(--surface-subtle)' }}>
                  <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>1. Fab Dependency (30%)</span>
                  <div style={{ fontSize: '1rem', fontWeight: 700, color: data.market_dependency_pct >= 75 ? 'var(--critical)' : 'var(--text-primary)' }}>
                    {data.market_dependency_pct}%
                  </div>
                </div>

                <div style={{ padding: '10px 12px', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-md)', background: 'var(--surface-subtle)' }}>
                  <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>2. Lead Time (25%)</span>
                  <div style={{ fontSize: '1rem', fontWeight: 700, color: data.lead_time_days >= 40 ? 'var(--high)' : 'var(--text-primary)' }}>
                    {data.lead_time_days} Days
                  </div>
                </div>

                <div style={{ padding: '10px 12px', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-md)', background: 'var(--surface-subtle)' }}>
                  <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>3. Material Criticality (20%)</span>
                  <div style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {data.criticality_rating || 'HIGH'}
                  </div>
                </div>

                <div style={{ padding: '10px 12px', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-md)', background: 'var(--surface-subtle)' }}>
                  <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>4. Backup Suppliers (10%)</span>
                  <div style={{ fontSize: '1rem', fontWeight: 700, color: data.backup_supplier_count === 0 ? 'var(--critical)' : 'var(--low)' }}>
                    {data.backup_supplier_count} Available {data.backup_supplier_count === 0 && '(SPoF)'}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div style={{
          padding: '14px 24px',
          borderTop: '1px solid var(--border-light)',
          background: 'var(--surface-subtle)',
          display: 'flex',
          justifyContent: 'flex-end'
        }}>
          <button className="btn-secondary" onClick={onClose}>
            Close Audit
          </button>
        </div>
      </div>
    </div>
  );
}
