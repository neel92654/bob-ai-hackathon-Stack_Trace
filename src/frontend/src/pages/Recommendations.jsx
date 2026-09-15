import React, { useState, useEffect } from 'react';
import { 
  CheckSquare, 
  Filter, 
  ShieldAlert, 
  Factory, 
  Globe2, 
  Wrench, 
  CheckCircle2, 
  Sparkles, 
  Sliders, 
  ArrowRight,
  Lightbulb
} from 'lucide-react';
import { fetchRecommendations } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';

export function Recommendations({ onNavigateToSimulator }) {
  const [recommendationsData, setRecommendationsData] = useState({ recommendations: [] });
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [selectedPriority, setSelectedPriority] = useState('ALL');

  useEffect(() => {
    loadRecommendations();
  }, [selectedCategory, selectedPriority]);

  async function loadRecommendations() {
    try {
      setLoading(true);
      const filters = {};
      if (selectedCategory !== 'ALL') filters.category = selectedCategory;
      if (selectedPriority !== 'ALL') filters.priority = selectedPriority;
      const res = await fetchRecommendations(filters);
      setRecommendationsData(res.data || { recommendations: [] });
    } catch (err) {
      console.error("Failed to load recommendations:", err);
    } finally {
      setLoading(false);
    }
  }

  const { recommendations = [], critical_count = 0, high_count = 0 } = recommendationsData;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Page Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
            Prioritized Operational Recommendations
          </h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            Prescriptive mitigation protocols generated deterministically from live queue overloads, single-point-of-failure vulnerabilities, and active disruption events.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="status-badge badge-critical">{critical_count} Critical Mitigations</span>
          <span className="status-badge badge-high">{high_count} High Priority</span>
        </div>
      </div>

      {/* Filter Ribbon */}
      <div className="enterprise-card" style={{ padding: '14px 18px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Category:</span>
            <select
              className="form-select"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              style={{ padding: '5px 10px', fontSize: '0.8rem' }}
            >
              <option value="ALL">All Categories</option>
              <option value="DISRUPTION_MITIGATION">Active Disruption</option>
              <option value="FAB_BOTTLENECK">Fab Tool Bottleneck</option>
              <option value="PREVENTIVE_MAINTENANCE">Preventive Maintenance</option>
              <option value="SUPPLY_CHAIN_SPOF">Single Point of Failure (SPoF)</option>
              <option value="SUPPLY_CHAIN_RISK">Supply Chain Risk</option>
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Priority:</span>
            <select
              className="form-select"
              value={selectedPriority}
              onChange={(e) => setSelectedPriority(e.target.value)}
              style={{ padding: '5px 10px', fontSize: '0.8rem' }}
            >
              <option value="ALL">All Priorities</option>
              <option value="CRITICAL">CRITICAL</option>
              <option value="HIGH">HIGH</option>
              <option value="MEDIUM">MEDIUM</option>
            </select>
          </div>
        </div>

        <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
          Showing {recommendations.length} action items
        </span>
      </div>

      {/* Recommendations Cards Grid */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        {recommendations.map((rec, idx) => {
          const isCritical = rec.priority === 'CRITICAL';
          const isHigh = rec.priority === 'HIGH';

          let borderAccent = 'var(--border-light)';
          let badgeType = 'neutral';
          if (isCritical) {
            borderAccent = 'var(--critical)';
            badgeType = 'critical';
          } else if (isHigh) {
            borderAccent = 'var(--high)';
            badgeType = 'high';
          } else {
            borderAccent = 'var(--medium)';
            badgeType = 'medium';
          }

          return (
            <div
              key={idx}
              className="enterprise-card"
              style={{
                padding: '20px',
                borderLeft: `4px solid ${borderAccent}`,
                display: 'flex',
                flexDirection: 'column',
                gap: '12px'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <RiskBadge level={rec.priority} />
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase' }}>
                      {rec.category.replace(/_/g, ' ')}
                    </span>
                  </div>
                  <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '4px' }}>
                    {rec.title}
                  </h3>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{
                    padding: '3px 8px',
                    borderRadius: 'var(--radius-sm)',
                    background: 'var(--surface-subtle)',
                    border: '1px solid var(--border-light)',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    fontFamily: 'monospace'
                  }}>
                    Target: {rec.affected_entity_id}
                  </span>
                  <button
                    className="btn-secondary"
                    style={{ padding: '4px 10px', fontSize: '0.72rem' }}
                    onClick={() => onNavigateToSimulator(rec.affected_entity_id)}
                  >
                    <Sliders size={12} />
                    <span>Simulate</span>
                  </button>
                </div>
              </div>

              {/* Action Callout */}
              <div style={{
                padding: '12px 14px',
                borderRadius: 'var(--radius-md)',
                background: isCritical ? 'var(--critical-bg)' : (isHigh ? 'var(--high-bg)' : 'var(--surface-subtle)'),
                border: `1px solid ${isCritical ? 'var(--critical-border)' : (isHigh ? 'var(--high-border)' : 'var(--border-light)')}`
              }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 700, color: isCritical ? 'var(--critical-text)' : (isHigh ? 'var(--high-text)' : 'var(--text-secondary)'), textTransform: 'uppercase', marginBottom: '2px' }}>
                  Prescribed Action Protocol
                </div>
                <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                  {rec.recommended_action}
                </div>
              </div>

              {/* Justification & Expected Impact */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '12px', fontSize: '0.8rem' }}>
                <div>
                  <span style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>Operational Reason: </span>
                  <span style={{ color: 'var(--text-muted)' }}>{rec.reason}</span>
                </div>
                <div>
                  <span style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>Expected Benefit: </span>
                  <span style={{ color: 'var(--low-text)', fontWeight: 600 }}>{rec.expected_impact}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
