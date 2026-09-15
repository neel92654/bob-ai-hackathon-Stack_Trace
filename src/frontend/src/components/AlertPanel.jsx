import React from 'react';
import { ShieldAlert, AlertTriangle, Radio, BellRing } from 'lucide-react';

export function AlertPanel({ alerts = [], onSelectAlert = null }) {
  if (!alerts || alerts.length === 0) {
    return (
      <div className="enterprise-card p-5 text-center" style={{ padding: '24px', color: 'var(--text-muted)' }}>
        <p>No critical operational alerts currently active.</p>
      </div>
    );
  }

  return (
    <div className="enterprise-card" style={{ padding: '20px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{
            width: '28px',
            height: '28px',
            borderRadius: 'var(--radius-sm)',
            background: 'var(--critical-bg)',
            border: '1px solid var(--critical-border)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--critical)'
          }}>
            <BellRing size={16} />
          </div>
          <div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-primary)' }}>
              Real-Time Critical Alerts
            </h4>
          </div>
        </div>
        <span className="status-badge badge-critical">
          {alerts.length} Active
        </span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {alerts.map((a, idx) => {
          let badgeClass = 'badge-critical';
          let borderCol = 'var(--critical-border)';
          let bgCol = 'var(--critical-bg)';
          let Icon = ShieldAlert;
          let iconCol = 'var(--critical)';

          if (a.severity === 'HIGH') {
            badgeClass = 'badge-high';
            borderCol = 'var(--high-border)';
            bgCol = 'var(--high-bg)';
            Icon = AlertTriangle;
            iconCol = 'var(--high)';
          } else if (a.type === 'DISRUPTION') {
            badgeClass = 'badge-purple';
            borderCol = 'var(--purple-border)';
            bgCol = 'var(--purple-bg)';
            Icon = Radio;
            iconCol = 'var(--purple)';
          }

          return (
            <div
              key={idx}
              onClick={() => onSelectAlert && onSelectAlert(a)}
              style={{
                padding: '12px 14px',
                borderRadius: 'var(--radius-md)',
                border: `1px solid ${borderCol}`,
                background: bgCol,
                display: 'flex',
                alignItems: 'flex-start',
                gap: '12px',
                cursor: onSelectAlert ? 'pointer' : 'default',
                transition: 'box-shadow var(--transition-fast)'
              }}
            >
              <div style={{ marginTop: '2px', color: iconCol }}>
                <Icon size={16} />
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2px' }}>
                  <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {a.title}
                  </span>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                    {a.time}
                  </span>
                </div>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', lineHeight: 1.4 }}>
                  {a.message}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
