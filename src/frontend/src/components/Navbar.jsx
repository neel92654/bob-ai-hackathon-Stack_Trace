import React, { useState } from 'react';
import { 
  LayoutDashboard, 
  Factory, 
  Network, 
  Boxes, 
  FlaskConical, 
  Lightbulb, 
  MessageSquare,
  Activity,
  Cpu,
  ShieldCheck,
  Menu,
  X,
  ExternalLink,
  ChevronRight
} from 'lucide-react';

export function Navbar({ activeTab, setActiveTab, healthStatus = 'ONLINE' }) {
  const [mobileOpen, setMobileOpen] = useState(false);

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, badge: null },
    { id: 'bottlenecks', label: 'Fab Bottlenecks', icon: Factory, badge: '4 Alert' },
    { id: 'supply', label: 'Supply Chain & SPoF', icon: Network, badge: '3 SPoF' },
    { id: 'lots', label: 'Production Lots', icon: Boxes, badge: null },
    { id: 'simulator', label: 'What-If Simulation', icon: FlaskConical, badge: 'Scenario' },
    { id: 'recommendations', label: 'Recommendations', icon: Lightbulb, badge: 'Action' },
    { id: 'assistant', label: 'Decision Assistant', icon: MessageSquare, badge: 'IBM Bob' },
  ];

  return (
    <>
      {/* Mobile Header Bar */}
      <div className="mobile-header" style={{
        display: 'none',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '12px 16px',
        background: 'var(--bg-sidebar)',
        color: '#ffffff',
        borderBottom: '1px solid var(--border-light)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{
            width: '28px',
            height: '28px',
            borderRadius: '6px',
            background: 'var(--primary-brand)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Cpu size={16} color="#ffffff" />
          </div>
          <span style={{ fontWeight: 800, letterSpacing: '-0.02em', fontSize: '1.1rem' }}>NEXORA</span>
        </div>
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          style={{ background: 'transparent', border: 'none', color: '#ffffff', cursor: 'pointer' }}
        >
          {mobileOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Persistent Left Sidebar */}
      <aside
        className={`app-sidebar ${mobileOpen ? 'mobile-open' : ''}`}
        style={{
          width: '260px',
          background: 'var(--bg-sidebar)',
          color: '#ffffff',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          flexShrink: 0,
          borderRight: '1px solid #1e293b',
          zIndex: 50
        }}
      >
        <div>
          {/* Brand Header */}
          <div style={{
            padding: '24px 20px 20px',
            borderBottom: '1px solid rgba(255, 255, 255, 0.08)'
          }}>
            <div 
              style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}
              onClick={() => { setActiveTab('dashboard'); setMobileOpen(false); }}
            >
              <div style={{
                width: '36px',
                height: '36px',
                borderRadius: '8px',
                background: 'var(--primary-brand)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 2px 8px rgba(0, 98, 255, 0.4)',
                flexShrink: 0
              }}>
                <Cpu size={20} color="#ffffff" />
              </div>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span style={{ fontSize: '1.2rem', fontWeight: 800, letterSpacing: '-0.03em', color: '#ffffff' }}>
                    NEXORA
                  </span>
                  <span style={{
                    fontSize: '0.62rem',
                    fontWeight: 700,
                    background: 'rgba(0, 98, 255, 0.25)',
                    color: '#60a5fa',
                    border: '1px solid rgba(96, 165, 250, 0.3)',
                    padding: '1px 5px',
                    borderRadius: '4px'
                  }}>
                    S2 ADVISOR
                  </span>
                </div>
                <p style={{ fontSize: '0.68rem', color: '#94a3b8', marginTop: '2px', lineHeight: 1.2 }}>
                  Operational Risk & Supply Intelligence
                </p>
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <nav style={{ padding: '16px 12px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <div style={{
              fontSize: '0.65rem',
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: '0.08em',
              color: '#64748b',
              padding: '6px 12px 4px'
            }}>
              Core Intelligence
            </div>

            {navItems.map(item => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveTab(item.id);
                    setMobileOpen(false);
                  }}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    width: '100%',
                    padding: '9px 12px',
                    borderRadius: '6px',
                    border: 'none',
                    background: isActive ? 'var(--primary-brand)' : 'transparent',
                    color: isActive ? '#ffffff' : '#cbd5e1',
                    fontSize: '0.825rem',
                    fontWeight: isActive ? 600 : 500,
                    cursor: 'pointer',
                    transition: 'all 0.15s ease',
                    textAlign: 'left'
                  }}
                  onMouseEnter={(e) => {
                    if (!isActive) e.currentTarget.style.background = 'rgba(255, 255, 255, 0.06)';
                  }}
                  onMouseLeave={(e) => {
                    if (!isActive) e.currentTarget.style.background = 'transparent';
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <Icon size={17} color={isActive ? '#ffffff' : '#94a3b8'} />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span style={{
                      fontSize: '0.65rem',
                      fontWeight: 600,
                      background: isActive ? 'rgba(255, 255, 255, 0.2)' : 'rgba(255, 255, 255, 0.08)',
                      color: isActive ? '#ffffff' : '#94a3b8',
                      padding: '2px 6px',
                      borderRadius: '4px'
                    }}>
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Sidebar Footer Info */}
        <div style={{
          padding: '16px 16px 20px',
          borderTop: '1px solid rgba(255, 255, 255, 0.08)',
          background: 'rgba(0, 0, 0, 0.15)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#22c55e', display: 'inline-block' }} />
            <span style={{ fontSize: '0.72rem', fontWeight: 600, color: '#e2e8f0' }}>Telemetry Stream Active</span>
          </div>
          <div style={{ fontSize: '0.68rem', color: '#94a3b8', lineHeight: 1.4 }}>
            IBM Bobathon 2026<br />
            ML Model R² = 0.954 • SQLite Local
          </div>
        </div>
      </aside>
    </>
  );
}
