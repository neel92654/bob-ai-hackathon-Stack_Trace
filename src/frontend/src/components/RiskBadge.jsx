import React from 'react';
import { AlertCircle, AlertTriangle, CheckCircle2, ShieldAlert } from 'lucide-react';

export function RiskBadge({ level = 'LOW', score = null, showIcon = true, size = 'md' }) {
  const normLevel = (level || 'LOW').toUpperCase();

  let badgeClass = 'badge-low';
  let Icon = CheckCircle2;

  if (normLevel === 'CRITICAL') {
    badgeClass = 'badge-critical';
    Icon = ShieldAlert;
  } else if (normLevel === 'HIGH') {
    badgeClass = 'badge-high';
    Icon = AlertTriangle;
  } else if (normLevel === 'MEDIUM') {
    badgeClass = 'badge-medium';
    Icon = AlertCircle;
  } else if (normLevel === 'INFO') {
    badgeClass = 'badge-info';
    Icon = AlertCircle;
  }

  const paddingStyle = size === 'sm' 
    ? { padding: '2px 6px', fontSize: '0.68rem', gap: '3px' } 
    : { padding: '3px 8px', fontSize: '0.72rem', gap: '5px' };

  return (
    <span className={`status-badge ${badgeClass}`} style={paddingStyle}>
      {showIcon && <Icon size={size === 'sm' ? 11 : 13} />}
      <span>{normLevel}</span>
      {score !== null && <span style={{ opacity: 0.9, fontWeight: 700 }}>({score})</span>}
    </span>
  );
}
