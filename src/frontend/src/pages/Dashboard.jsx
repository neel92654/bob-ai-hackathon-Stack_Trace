import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, 
  Factory, 
  Globe2, 
  Boxes, 
  AlertTriangle, 
  ArrowRight,
  TrendingUp, 
  Sliders, 
  Lightbulb, 
  CheckCircle2, 
  ChevronRight,
  ExternalLink,
  Zap,
  Activity
} from 'lucide-react';
import { fetchDashboardSummary } from '../services/api';
import { MetricCard } from '../components/MetricCard';
import { RiskBadge } from '../components/RiskBadge';
import { ExplainabilityModal } from '../components/ExplainabilityModal';

export function Dashboard({ setActiveTab, onSimulateSupplier, onSimulateTool }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedAuditItem, setSelectedAuditItem] = useState(null);
  const [auditType, setAuditType] = useState('bottleneck');

  useEffect(() => {
    loadSummary();
  }, []);

  async function loadSummary() {
    try {
      setLoading(true);
      const res = await fetchDashboardSummary();
      setSummary(res);
      setError(null);
    } catch (err) {
      console.error("Dashboard load failed:", err);
      setError("Failed to load dashboard summary from backend.");
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div style={{ padding: '60px 20px', textAlign: 'center', color: 'var(--text-muted)' }}>
        <div className="animate-spin" style={{ display: 'inline-block', width: '32px', height: '32px', border: '3px solid var(--border-light)', borderTopColor: 'var(--primary-brand)', borderRadius: '50%' }} />
        <p style={{ marginTop: '14px', fontSize: '0.9rem', fontWeight: 500 }}>Ingesting fab operational telemetry...</p>
      </div>
    );
  }

  if (error || !summary) {
    return (
      <div className="enterprise-card p-8 text-center" style={{ margin: '40px auto', maxWidth: '560px', padding: '32px' }}>
        <AlertTriangle size={36} color="var(--critical)" style={{ margin: '0 auto 12px' }} />
        <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--text-primary)' }}>Telemetry Ingestion Error</h3>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '6px' }}>{error}</p>
        <button className="btn-primary" style={{ marginTop: '16px' }} onClick={loadSummary}>
          Retry Connection
        </button>
      </div>
    );
  }

  const { kpi_metrics, distributions, critical_alerts, top_bottlenecks, top_suppliers, top_recommendations } = summary;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* 4 Top KPI Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px' }}>
        <MetricCard
          title="Overall Operational Risk"
          value={`${kpi_metrics?.overall_risk_score || 78}/100`}
          subtitle="Aggregated queue & supply exposure"
          icon={Activity}
          accentColor="critical"
          badgeText="HIGH RISK"
          badgeType="critical"
          trend="+4.2 pts"
          trendType="up-bad"
        />

        <MetricCard
          title="Critical Bottlenecks"
          value={kpi_metrics?.critical_bottlenecks_count || 4}
          subtitle="Tools operating >100% capacity"
          icon={Factory}
          accentColor="high"
          badgeText={`${distributions?.bottlenecks?.CRITICAL || 2} Critical`}
          badgeType="high"
          onClick={() => setActiveTab('bottlenecks')}
        />

        <MetricCard
          title="High-Risk Suppliers"
          value={kpi_metrics?.high_risk_suppliers_count || 3}
          subtitle="Single-source dependencies detected"
          icon={Globe2}
          accentColor="purple"
          badgeText="3 SPoF"
          badgeType="purple"
          onClick={() => setActiveTab('supply')}
        />

        <MetricCard
          title="At-Risk Production Lots"
          value={kpi_metrics?.delayed_lots_count || 42}
          subtitle={`Avg projected delay: +${kpi_metrics?.average_predicted_delay_hours || 18.4}h`}
          icon={Boxes}
          accentColor="cyan"
          badgeText="200 Active"
          badgeType="info"
          onClick={() => setActiveTab('lots')}
        />
      </div>

      {/* Critical Operational Alert Callout */}
      {critical_alerts && critical_alerts.length > 0 && (
        <div style={{
          background: 'var(--critical-bg)',
          border: '1px solid var(--critical-border)',
          borderRadius: 'var(--radius-md)',
          padding: '14px 18px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '12px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '28px',
              height: '28px',
              borderRadius: 'var(--radius-sm)',
              background: '#ffffff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--critical)',
              boxShadow: 'var(--shadow-xs)'
            }}>
              <ShieldAlert size={16} />
            </div>
            <div>
              <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--critical-text)' }}>
                {critical_alerts[0]?.title}: {critical_alerts[0]?.message}
              </span>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
                Tool operating at 153.3% rated capacity. 23 wafer lots queued creating downstream starvation.
              </div>
            </div>
          </div>
          <button
            className="btn-outline-danger"
            onClick={() => onSimulateTool('CVD-03')}
          >
            <Sliders size={13} />
            <span>Simulate Tool Outage</span>
          </button>
        </div>
      )}

      {/* Grid: Left (Critical Bottlenecks) | Right (Supplier Risk & SPoF) */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(480px, 1fr))', gap: '24px' }}>
        
        {/* Left: Critical Fab Bottlenecks */}
        <div className="enterprise-card" style={{ padding: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Factory size={18} color="var(--primary-brand)" />
                <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                  Critical Fab Bottlenecks
                </h3>
              </div>
              <button
                className="btn-secondary"
                style={{ padding: '4px 10px', fontSize: '0.72rem' }}
                onClick={() => setActiveTab('bottlenecks')}
              >
                View All Tools ({summary?.distributions?.bottlenecks?.total || 28})
                <ChevronRight size={12} />
              </button>
            </div>

            <div className="enterprise-table-container">
              <table className="enterprise-table">
                <thead>
                  <tr>
                    <th>Tool ID</th>
                    <th>Process Stage</th>
                    <th>Utilization</th>
                    <th>WIP / Cap</th>
                    <th>Risk</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {(top_bottlenecks || []).slice(0, 4).map(b => (
                    <tr key={b.tool_id}>
                      <td style={{ fontWeight: 700, fontFamily: 'monospace', color: 'var(--text-primary)' }}>
                        {b.tool_id}
                      </td>
                      <td style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                        {b.process_name}
                      </td>
                      <td style={{ minWidth: '120px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <span style={{ fontSize: '0.78rem', fontWeight: 700, minWidth: '45px', color: b.utilization_pct >= 120 ? 'var(--critical-text)' : (b.utilization_pct >= 100 ? 'var(--high-text)' : 'var(--text-primary)') }}>
                            {b.utilization_pct}%
                          </span>
                          <div className="progress-track" style={{ flex: 1, height: '6px' }}>
                            <div
                              className="progress-fill"
                              style={{
                                width: `${Math.min(100, b.utilization_pct)}%`,
                                background: b.utilization_pct >= 120 ? 'var(--critical)' : (b.utilization_pct >= 100 ? 'var(--high)' : 'var(--low)')
                              }}
                            />
                          </div>
                        </div>
                      </td>
                      <td style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                        {b.current_wip} / {b.nominal_capacity}
                      </td>
                      <td>
                        <RiskBadge level={b.risk_level} size="sm" />
                      </td>
                      <td>
                        <button
                          className="btn-secondary"
                          style={{ padding: '3px 8px', fontSize: '0.7rem' }}
                          onClick={() => {
                            setSelectedAuditItem(b);
                            setAuditType('bottleneck');
                          }}
                        >
                          Audit
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right: Supplier Risk & SPoFs */}
        <div className="enterprise-card" style={{ padding: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Globe2 size={18} color="var(--purple)" />
                <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                  Supplier Risk & SPoFs
                </h3>
              </div>
              <button
                className="btn-secondary"
                style={{ padding: '4px 10px', fontSize: '0.72rem' }}
                onClick={() => setActiveTab('supply')}
              >
                View All Suppliers (22)
                <ChevronRight size={12} />
              </button>
            </div>

            <div className="enterprise-table-container">
              <table className="enterprise-table">
                <thead>
                  <tr>
                    <th>Supplier</th>
                    <th>Material</th>
                    <th>Score</th>
                    <th>Dependency</th>
                    <th>SPoF</th>
                    <th>Simulate</th>
                  </tr>
                </thead>
                <tbody>
                  {(top_suppliers || []).slice(0, 4).map(s => (
                    <tr key={s.supplier_id}>
                      <td style={{ fontWeight: 700, fontFamily: 'monospace', color: 'var(--text-primary)' }}>
                        {s.supplier_id}
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontWeight: 400 }}>{s.name}</div>
                      </td>
                      <td style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                        {s.material}
                      </td>
                      <td>
                        <span style={{ fontWeight: 700, color: s.supplier_risk_score >= 80 ? 'var(--critical-text)' : (s.supplier_risk_score >= 60 ? 'var(--high-text)' : 'var(--low-text)') }}>
                          {s.supplier_risk_score}
                        </span>
                      </td>
                      <td style={{ fontSize: '0.8rem', fontWeight: 600 }}>
                        {s.market_dependency_pct}%
                      </td>
                      <td>
                        {s.is_single_point_of_failure ? (
                          <span className="status-badge badge-critical" style={{ fontSize: '0.65rem' }}>
                            SPoF
                          </span>
                        ) : (
                          <span className="status-badge badge-low" style={{ fontSize: '0.65rem' }}>
                            DUAL
                          </span>
                        )}
                      </td>
                      <td>
                        <button
                          className="btn-secondary"
                          style={{ padding: '3px 8px', fontSize: '0.7rem' }}
                          onClick={() => onSimulateSupplier(s.supplier_id)}
                        >
                          Simulate
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      {/* Downstream Production Impact & Priority Recommendations */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(480px, 1fr))', gap: '24px' }}>
        
        {/* Downstream Production Impact */}
        <div className="enterprise-card" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Boxes size={18} color="var(--info-text)" />
              <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                Downstream Production Lot Impact
              </h3>
            </div>
            <button
              className="btn-secondary"
              style={{ padding: '4px 10px', fontSize: '0.72rem' }}
              onClick={() => setActiveTab('lots')}
            >
              View All 200 Lots
              <ChevronRight size={12} />
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <div style={{
              padding: '12px 14px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-light)',
              background: 'var(--surface-subtle)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between'
            }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontWeight: 700, fontFamily: 'monospace' }}>LOT-8001</span>
                  <span className="status-badge badge-critical" style={{ fontSize: '0.65rem' }}>HIGH PRIORITY</span>
                </div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
                  AI Accelerator (Tier-1 Auto) • Stage: CVD Thin Film (CVD-03)
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--critical-text)' }}>
                  +28.4h Delay
                </span>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>ML Forecast</div>
              </div>
            </div>

            <div style={{
              padding: '12px 14px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-light)',
              background: 'var(--surface-subtle)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between'
            }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontWeight: 700, fontFamily: 'monospace' }}>LOT-8004</span>
                  <span className="status-badge badge-high" style={{ fontSize: '0.65rem' }}>MEDIUM PRIORITY</span>
                </div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
                  Server GPU (Enterprise) • Stage: Plasma Etch (ETCH-01)
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--high-text)' }}>
                  +19.2h Delay
                </span>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>ML Forecast</div>
              </div>
            </div>
          </div>
        </div>

        {/* Priority Recommended Actions */}
        <div className="enterprise-card" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Lightbulb size={18} color="var(--warning)" />
              <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                Recommended Operational Actions
              </h3>
            </div>
            <button
              className="btn-secondary"
              style={{ padding: '4px 10px', fontSize: '0.72rem' }}
              onClick={() => setActiveTab('recommendations')}
            >
              View All Protocols
              <ChevronRight size={12} />
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {(top_recommendations || []).slice(0, 2).map((rec, idx) => (
              <div
                key={idx}
                style={{
                  padding: '12px 14px',
                  borderRadius: 'var(--radius-md)',
                  border: `1px solid ${rec.priority === 'CRITICAL' ? 'var(--critical-border)' : 'var(--high-border)'}`,
                  background: rec.priority === 'CRITICAL' ? 'var(--critical-bg)' : 'var(--high-bg)'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '3px' }}>
                  <span style={{ fontSize: '0.825rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {rec.title}
                  </span>
                  <RiskBadge level={rec.priority} size="sm" />
                </div>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', lineHeight: 1.35 }}>
                  {rec.recommended_action}
                </p>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px', fontWeight: 500 }}>
                  Target: {rec.affected_entity_id} • Expected: {rec.expected_impact}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Explainability Audit Modal */}
      <ExplainabilityModal
        isOpen={!!selectedAuditItem}
        onClose={() => setSelectedAuditItem(null)}
        data={selectedAuditItem}
        type={auditType}
      />
    </div>
  );
}
