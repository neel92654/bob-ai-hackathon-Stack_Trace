import React from 'react';
import { ArrowRight, AlertTriangle, CheckCircle2, ShieldAlert } from 'lucide-react';

const PROCESS_STEPS = [
  { seq: 1, id: 'PRC-01', name: 'Wafer Clean' },
  { seq: 2, id: 'PRC-02', name: 'Oxidation' },
  { seq: 3, id: 'PRC-03', name: 'Photolithography' },
  { seq: 4, id: 'PRC-04', name: 'Plasma Etch' },
  { seq: 5, id: 'PRC-05', name: 'Ion Implantation' },
  { seq: 6, id: 'PRC-06', name: 'CVD Thin Film' },
  { seq: 7, id: 'PRC-07', name: 'PVD Metal' },
  { seq: 8, id: 'PRC-08', name: 'CMP Polish' },
  { seq: 9, id: 'PRC-09', name: 'Metrology' },
  { seq: 10, id: 'PRC-10', name: 'Packaging' },
];

export function ProcessFlow({ activeProcessId = 'PRC-06', activeToolId = 'CVD-03', riskLevel = 'CRITICAL' }) {
  const activeStep = PROCESS_STEPS.find(s => s.id === activeProcessId) || PROCESS_STEPS[5];
  const activeSeq = activeStep.seq;

  return (
    <div className="enterprise-card" style={{ padding: '20px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px', flexWrap: 'wrap', gap: '10px' }}>
        <div>
          <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-primary)' }}>
            Sequential Fab Process Dependency Flow
          </h4>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            Tracking queue propagation and downstream process stage starvation
          </p>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px', fontSize: '0.75rem' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px', color: 'var(--critical-text)', fontWeight: 600 }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--critical)' }} />
            Bottleneck Tool
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px', color: 'var(--high-text)', fontWeight: 600 }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--high)' }} />
            Starvation Risk
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px', color: 'var(--low-text)', fontWeight: 600 }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--low)' }} />
            Nominal Flow
          </span>
        </div>
      </div>

      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        overflowX: 'auto',
        paddingBottom: '8px',
        paddingTop: '4px'
      }}>
        {PROCESS_STEPS.map((step, idx) => {
          const isBottleneck = step.id === activeProcessId;
          const isDownstream = step.seq > activeSeq;
          const isUpstream = step.seq < activeSeq;

          let cardBorder = 'var(--border-light)';
          let cardBg = '#ffffff';
          let textColor = 'var(--text-secondary)';
          let seqColor = 'var(--text-muted)';
          let icon = <CheckCircle2 size={13} color="var(--low)" />;

          if (isBottleneck) {
            cardBorder = riskLevel === 'CRITICAL' ? 'var(--critical-border)' : 'var(--high-border)';
            cardBg = riskLevel === 'CRITICAL' ? 'var(--critical-bg)' : 'var(--high-bg)';
            textColor = riskLevel === 'CRITICAL' ? 'var(--critical-text)' : 'var(--high-text)';
            seqColor = textColor;
            icon = <ShieldAlert size={14} color="var(--critical)" />;
          } else if (isDownstream) {
            cardBorder = 'var(--high-border)';
            cardBg = 'var(--high-bg)';
            textColor = 'var(--high-text)';
            seqColor = 'var(--high)';
            icon = <AlertTriangle size={13} color="var(--high)" />;
          }

          return (
            <React.Fragment key={step.id}>
              <div
                style={{
                  minWidth: '120px',
                  padding: '10px 12px',
                  borderRadius: 'var(--radius-md)',
                  border: `1px solid ${cardBorder}`,
                  background: cardBg,
                  flexShrink: 0,
                  boxShadow: isBottleneck ? 'var(--shadow-sm)' : 'none'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
                  <span style={{ fontSize: '0.68rem', fontWeight: 700, color: seqColor }}>
                    STAGE {step.seq < 10 ? `0${step.seq}` : step.seq}
                  </span>
                  {icon}
                </div>
                <div style={{ fontSize: '0.8rem', fontWeight: 700, color: textColor, lineHeight: 1.25 }}>
                  {step.name}
                </div>
                <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)', marginTop: '4px', fontFamily: 'monospace' }}>
                  {step.id}
                </div>
              </div>

              {idx < PROCESS_STEPS.length - 1 && (
                <ArrowRight 
                  size={14} 
                  color={isBottleneck || isDownstream ? 'var(--high)' : 'var(--border-strong)'} 
                  style={{ flexShrink: 0 }} 
                />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
}
