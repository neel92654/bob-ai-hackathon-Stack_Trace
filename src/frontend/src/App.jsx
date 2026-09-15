import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Dashboard } from './pages/Dashboard';
import { Bottlenecks } from './pages/Bottlenecks';
import { SupplyChain } from './pages/SupplyChain';
import { ProductionLots } from './pages/ProductionLots';
import { WhatIfSimulator } from './pages/WhatIfSimulator';
import { Recommendations } from './pages/Recommendations';
import { DecisionAssistant } from './pages/DecisionAssistant';
import { Info, Bell, RefreshCw, Sparkles, Sliders } from 'lucide-react';

export function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [preselectedSupplier, setPreselectedSupplier] = useState(null);
  const [preselectedTool, setPreselectedTool] = useState(null);

  function handleSimulateSupplier(supplierId) {
    setPreselectedSupplier(supplierId);
    setPreselectedTool(null);
    setActiveTab('simulator');
  }

  function handleSimulateTool(toolId) {
    setPreselectedTool(toolId);
    setPreselectedSupplier(null);
    setActiveTab('simulator');
  }

  function handleNavigateFromRec(targetId) {
    if (targetId.startsWith('SUP-')) {
      handleSimulateSupplier(targetId);
    } else {
      handleSimulateTool(targetId);
    }
  }

  const pageHeaders = {
    dashboard: {
      title: 'Operational Risk & Executive Overview',
      subtitle: 'Real-time equipment bottleneck tracking, supplier single-point-of-failure analysis, and production impact.'
    },
    bottlenecks: {
      title: 'Fab Bottleneck Intelligence',
      subtitle: 'Identify semiconductor fabrication equipment and process stages constraining line throughput.'
    },
    supply: {
      title: 'Supply Chain & SPoF Intelligence',
      subtitle: '5-factor supplier risk scoring, critical single points of failure, and country concentration metrics.'
    },
    lots: {
      title: 'Production Lot Impact & Delivery',
      subtitle: 'Machine learning delivery delay forecasting (RandomForest R² = 0.95) across active wafer lots.'
    },
    simulator: {
      title: 'What-If Disruption Simulator',
      subtitle: 'Proactively simulate supplier disruptions, tool outages, and demand surges before committing actions.'
    },
    recommendations: {
      title: 'Prioritized Mitigation Protocols',
      subtitle: 'Prescriptive, condition-driven operational responses synthesized from active fab risk telemetry.'
    },
    assistant: {
      title: 'Decision Assistant Console',
      subtitle: 'Grounded natural-language operational decision support interface for IBM Bob.'
    }
  };

  const currentHeader = pageHeaders[activeTab] || pageHeaders.dashboard;

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--bg-app)' }}>
      {/* Left Sidebar Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      {/* Main Content Area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0, overflowX: 'hidden' }}>
        
        {/* Top Header Bar */}
        <header style={{
          background: '#ffffff',
          borderBottom: '1px solid var(--border-light)',
          padding: '16px 32px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          position: 'sticky',
          top: 0,
          zIndex: 30,
          boxShadow: 'var(--shadow-xs)'
        }}>
          <div>
            <h1 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)' }}>
              {currentHeader.title}
            </h1>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px' }}>
              {currentHeader.subtitle}
            </p>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '5px 10px',
              background: 'var(--low-bg)',
              border: '1px solid var(--low-border)',
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.72rem',
              fontWeight: 600,
              color: 'var(--low-text)'
            }}>
              <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'var(--low)' }} />
              Live Telemetry
            </div>

            {activeTab !== 'simulator' && (
              <button
                className="btn-secondary"
                style={{ padding: '6px 12px', fontSize: '0.78rem' }}
                onClick={() => setActiveTab('simulator')}
              >
                <Sliders size={14} />
                <span>Simulate</span>
              </button>
            )}

            {activeTab !== 'assistant' && (
              <button
                className="btn-primary"
                style={{ padding: '6px 12px', fontSize: '0.78rem' }}
                onClick={() => setActiveTab('assistant')}
              >
                <Sparkles size={14} />
                <span>Assistant</span>
              </button>
            )}
          </div>
        </header>

        {/* Dynamic Page Content */}
        <main style={{ flex: 1, padding: '28px 32px', maxWidth: '1440px', width: '100%', margin: '0 auto' }}>
          {activeTab === 'dashboard' && (
            <Dashboard
              setActiveTab={setActiveTab}
              onSimulateSupplier={handleSimulateSupplier}
              onSimulateTool={handleSimulateTool}
            />
          )}
          {activeTab === 'bottlenecks' && (
            <Bottlenecks
              onSimulateTool={handleSimulateTool}
            />
          )}
          {activeTab === 'supply' && (
            <SupplyChain
              onSimulateSupplier={handleSimulateSupplier}
            />
          )}
          {activeTab === 'lots' && (
            <ProductionLots />
          )}
          {activeTab === 'simulator' && (
            <WhatIfSimulator
              preselectedSupplier={preselectedSupplier}
              preselectedTool={preselectedTool}
            />
          )}
          {activeTab === 'recommendations' && (
            <Recommendations
              onNavigateToSimulator={handleNavigateFromRec}
            />
          )}
          {activeTab === 'assistant' && (
            <DecisionAssistant />
          )}
        </main>

        {/* Clean Enterprise Footer */}
        <footer style={{
          borderTop: '1px solid var(--border-light)',
          background: '#ffffff',
          padding: '16px 32px',
          marginTop: 'auto'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '12px',
            fontSize: '0.75rem',
            color: 'var(--text-muted)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <strong style={{ color: 'var(--text-primary)' }}>NEXORA</strong>
              <span>•</span>
              <span>IBM Bob AI Innovation Hackathon 2026</span>
              <span>•</span>
              <span>Problem Statement S2: Fab Bottleneck & Supply Chain Advisor</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Info size={14} />
              <span>Synthetic fab telemetry demonstration dataset (Seed: 42).</span>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default App;
