import React, { useState, useEffect } from 'react';
import { 
  Globe2, 
  ShieldAlert, 
  Search, 
  Filter, 
  AlertTriangle, 
  Info, 
  Sliders, 
  MapPin, 
  CheckCircle2, 
  Truck,
  Building2,
  Package,
  X
} from 'lucide-react';
import { fetchSuppliers, fetchGeopoliticalConcentration } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';
import { ExplainabilityModal } from '../components/ExplainabilityModal';

export function SupplyChain({ onSimulateSupplier }) {
  const [suppliers, setSuppliers] = useState([]);
  const [geopolitical, setGeopolitical] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRisk, setSelectedRisk] = useState('ALL');
  const [selectedCountry, setSelectedCountry] = useState('ALL');
  const [selectedSupplierForAudit, setSelectedSupplierForAudit] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      setLoading(true);
      const [suppRes, geoRes] = await Promise.all([
        fetchSuppliers(),
        fetchGeopoliticalConcentration()
      ]);
      setSuppliers(suppRes.data || []);
      setGeopolitical(geoRes.data || []);
    } catch (err) {
      console.error("Failed to load supply chain intelligence:", err);
    } finally {
      setLoading(false);
    }
  }

  const spofList = suppliers.filter(s => s.is_single_point_of_failure);

  const filteredSuppliers = suppliers.filter(s => {
    const matchesSearch = s.supplier_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          s.material.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          s.country.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesRisk = selectedRisk === 'ALL' || s.risk_level === selectedRisk;
    const matchesCountry = selectedCountry === 'ALL' || s.country === selectedCountry;
    return matchesSearch && matchesRisk && matchesCountry;
  });

  const uniqueCountries = Array.from(new Set(suppliers.map(s => s.country)));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Page Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
            Supply Chain Risk & Single-Point-of-Failure Advisor
          </h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            5-factor weighted supplier scoring (0–100), single-point-of-failure (SPoF) alerts, and geopolitical concentration.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="status-badge badge-critical">{spofList.length} SPoF Suppliers</span>
          <span className="status-badge badge-purple">{geopolitical.length} Sourcing Regions</span>
        </div>
      </div>

      {/* Top 4 Supply Risk KPI Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
        <div className="enterprise-card" style={{ padding: '16px', borderLeft: '4px solid var(--critical)' }}>
          <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
            Highest-Risk Supplier
          </span>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '4px' }}>
            SUP-002
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--critical-text)', fontWeight: 600, marginTop: '2px' }}>
            Gallium (91% dependency, 0 backup)
          </p>
        </div>

        <div className="enterprise-card" style={{ padding: '16px', borderLeft: '4px solid var(--high)' }}>
          <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
            Single Points of Failure
          </span>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '4px' }}>
            {spofList.length} Suppliers
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>
            Zero qualified alternate sources
          </p>
        </div>

        <div className="enterprise-card" style={{ padding: '16px', borderLeft: '4px solid var(--purple)' }}>
          <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
            Highest Dependency Share
          </span>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '4px' }}>
            91.0%
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>
            Exceeds 75% critical threshold
          </p>
        </div>

        <div className="enterprise-card" style={{ padding: '16px', borderLeft: '4px solid var(--info-border)' }}>
          <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
            Top Sourcing Concentration
          </span>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '4px' }}>
            Taiwan (32%)
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>
            Followed by Japan (23%), Germany (18%)
          </p>
        </div>
      </div>

      {/* SPoF Dedicated Alert Banner */}
      {spofList.length > 0 && (
        <div style={{
          padding: '16px 20px',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--critical-border)',
          background: 'var(--critical-bg)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '14px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: 'var(--radius-sm)',
              background: '#ffffff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--critical)',
              boxShadow: 'var(--shadow-xs)'
            }}>
              <ShieldAlert size={18} />
            </div>
            <div>
              <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--critical-text)' }}>
                Critical Single-Point-of-Failure (SPoF) Vulnerability Detected
              </h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
                Supplier <strong>SUP-002 (Gallium)</strong> supplies 91% of fab raw chemical demand with <strong>0 backup suppliers</strong> and a 56-day replenishment lead time.
              </p>
            </div>
          </div>
          <button
            className="btn-outline-danger"
            onClick={() => onSimulateSupplier('SUP-002')}
          >
            <Sliders size={14} />
            <span>Simulate 14-Day Embargo</span>
          </button>
        </div>
      )}

      {/* Filter Ribbon */}
      <div className="enterprise-card" style={{ padding: '14px 18px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        
        {/* Search */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', minWidth: '260px' }}>
          <Search size={16} color="var(--text-muted)" />
          <input
            type="text"
            className="form-input"
            placeholder="Search by supplier, material, country..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ padding: '6px 10px', fontSize: '0.825rem' }}
          />
        </div>

        {/* Filters */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Region:</span>
            <select
              className="form-select"
              value={selectedCountry}
              onChange={(e) => setSelectedCountry(e.target.value)}
              style={{ padding: '5px 10px', fontSize: '0.8rem' }}
            >
              <option value="ALL">All Countries</option>
              {uniqueCountries.map(c => (
                <option key={c} value={c}>{c}</option>
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
              <option value="CRITICAL">CRITICAL (&gt;80)</option>
              <option value="HIGH">HIGH (60-80)</option>
              <option value="MEDIUM">MEDIUM (40-60)</option>
              <option value="LOW">LOW (&lt;40)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Supplier Intelligence Table */}
      <div className="enterprise-table-container">
        <table className="enterprise-table">
          <thead>
            <tr>
              <th>Supplier ID</th>
              <th>Supplier Name</th>
              <th>Material Supplied</th>
              <th>Risk Score</th>
              <th>Fab Dependency</th>
              <th>Backup Sources</th>
              <th>Lead Time</th>
              <th>Country</th>
              <th>SPoF Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredSuppliers.map(s => {
              const score = s.supplier_risk_score;
              let scoreColor = 'var(--low)';
              if (score >= 80) scoreColor = 'var(--critical)';
              else if (score >= 60) scoreColor = 'var(--high)';
              else if (score >= 40) scoreColor = 'var(--medium)';

              return (
                <tr key={s.supplier_id}>
                  <td style={{ fontWeight: 700, fontFamily: 'monospace', color: 'var(--text-primary)' }}>
                    {s.supplier_id}
                  </td>
                  <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                    {s.name}
                  </td>
                  <td style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    {s.material}
                  </td>
                  <td style={{ minWidth: '130px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontSize: '0.825rem', fontWeight: 700, minWidth: '30px', color: scoreColor }}>
                        {score}
                      </span>
                      <div className="progress-track" style={{ flex: 1, height: '6px' }}>
                        <div
                          className="progress-fill"
                          style={{
                            width: `${score}%`,
                            background: scoreColor
                          }}
                        />
                      </div>
                    </div>
                  </td>
                  <td style={{ fontWeight: 600, color: s.market_dependency_pct >= 75 ? 'var(--critical-text)' : 'var(--text-primary)' }}>
                    {s.market_dependency_pct}%
                  </td>
                  <td>
                    {s.backup_supplier_count === 0 ? (
                      <span style={{ color: 'var(--critical-text)', fontWeight: 700 }}>0 (SPoF)</span>
                    ) : (
                      <span style={{ color: 'var(--text-secondary)' }}>{s.backup_supplier_count} available</span>
                    )}
                  </td>
                  <td style={{ color: 'var(--text-secondary)' }}>
                    {s.lead_time_days} days
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.8rem' }}>
                      <MapPin size={12} color="var(--text-muted)" />
                      <span>{s.country}</span>
                    </div>
                  </td>
                  <td>
                    {s.is_single_point_of_failure ? (
                      <span className="status-badge badge-critical" style={{ fontSize: '0.65rem' }}>
                        SPoF
                      </span>
                    ) : (
                      <span className="status-badge badge-low" style={{ fontSize: '0.65rem' }}>
                        DUAL-SOURCED
                      </span>
                    )}
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <button
                        className="btn-secondary"
                        style={{ padding: '4px 8px', fontSize: '0.72rem' }}
                        onClick={() => setSelectedSupplierForAudit(s)}
                      >
                        Audit
                      </button>
                      <button
                        className="btn-secondary"
                        style={{ padding: '4px 8px', fontSize: '0.72rem' }}
                        onClick={() => onSimulateSupplier(s.supplier_id)}
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

      {/* Explainability Audit Modal */}
      <ExplainabilityModal
        isOpen={!!selectedSupplierForAudit}
        onClose={() => setSelectedSupplierForAudit(null)}
        data={selectedSupplierForAudit}
        type="supplier"
      />
    </div>
  );
}
