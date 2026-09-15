import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

export function MetricCard({
  title,
  value,
  subtitle,
  icon: Icon,
  trend = null,
  trendType = 'neutral',
  accentColor = 'primary',
  badgeText = null,
  badgeType = 'neutral',
  onClick = null
}) {
  const accentColors = {
    primary: 'var(--primary-brand)',
    teal: 'var(--teal-operational)',
    critical: 'var(--critical)',
    high: 'var(--high)',
    medium: 'var(--medium)',
    low: 'var(--low)',
    purple: 'var(--purple)',
    cyan: '#0284c7',
    amber: '#d97706',
    emerald: '#16a34a',
    red: '#dc2626',
    blue: '#0062ff'
  };

  const selectedBorder = accentColors[accentColor] || accentColors.primary;

  return (
    <div
      onClick={onClick}
      className={`enterprise-card p-5 ${onClick ? 'cursor-pointer' : ''}`}
      style={{
        padding: '20px',
        borderLeft: `4px solid ${selectedBorder}`,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        cursor: onClick ? 'pointer' : 'default',
        position: 'relative'
      }}
    >
      <div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
          <span style={{ 
            fontSize: '0.75rem', 
            fontWeight: 600, 
            color: 'var(--text-muted)', 
            textTransform: 'uppercase', 
            letterSpacing: '0.04em' 
          }}>
            {title}
          </span>
          {Icon && (
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: 'var(--radius-md)',
              background: 'var(--surface-subtle)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: selectedBorder
            }}>
              <Icon size={18} />
            </div>
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px' }}>
          <h3 style={{ 
            fontSize: '1.85rem', 
            fontWeight: 700, 
            color: 'var(--text-primary)', 
            letterSpacing: '-0.02em',
            lineHeight: 1.1 
          }}>
            {value}
          </h3>
          {badgeText && (
            <span className={`status-badge badge-${badgeType}`} style={{ fontSize: '0.68rem', padding: '2px 6px' }}>
              {badgeText}
            </span>
          )}
        </div>
      </div>

      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between', 
        marginTop: '14px',
        paddingTop: '10px',
        borderTop: '1px solid var(--border-subtle)',
        fontSize: '0.78rem'
      }}>
        {subtitle && (
          <span style={{ color: 'var(--text-muted)' }}>
            {subtitle}
          </span>
        )}

        {trend && (
          <span style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '3px',
            fontWeight: 600,
            fontSize: '0.75rem',
            color: trendType === 'up-bad' || trendType === 'down-bad' ? 'var(--critical)' : (trendType === 'good' ? 'var(--low)' : 'var(--text-muted)')
          }}>
            {trendType === 'up-bad' && <TrendingUp size={13} />}
            {trendType === 'good' && <TrendingDown size={13} />}
            {trendType === 'neutral' && <Minus size={13} />}
            {trend}
          </span>
        )}
      </div>
    </div>
  );
}
