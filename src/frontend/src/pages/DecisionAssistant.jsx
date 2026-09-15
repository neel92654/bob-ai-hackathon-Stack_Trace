import React, { useState } from 'react';
import { 
  MessageSquare, 
  Send, 
  Sparkles, 
  User, 
  CheckCircle2, 
  Info, 
  ArrowRight,
  ShieldAlert,
  Cpu,
  CornerDownRight,
  Bot
} from 'lucide-react';
import { queryDecisionAssistant } from '../services/api';

const SAMPLE_QUERIES = [
  "Show critical bottlenecks",
  "Find highest-risk supplier",
  "Why is CVD-03 critical?",
  "What happens if SUP-002 becomes unavailable for 14 days?",
  "Show affected production lots",
  "Give executive summary"
];

export function DecisionAssistant() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      direct_answer: "Hello, I am the Nexora Decision Support Assistant for IBM Bob. I analyze fab equipment WIP queues, single-source supplier risks, ML delivery projections, and disruption simulations.",
      supporting_facts: [
        "Live tracking 28 fab tools across 10 manufacturing stages.",
        "Monitoring 22 suppliers with SPoF and geopolitical scoring.",
        "Trained RandomForest model predicting lot delivery delay."
      ],
      reasoning: "I only answer questions using verified telemetry within the local Nexora database.",
      recommended_action: "Select a sample prompt below or ask any question regarding fab bottlenecks, suppliers, or what-if scenarios."
    }
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSend(text = null) {
    const q = text || inputQuery;
    if (!q.trim() || loading) return;

    const userMsg = { role: 'user', content: q };
    setMessages(prev => [...prev, userMsg]);
    if (!text) setInputQuery('');
    setLoading(true);

    try {
      const res = await queryDecisionAssistant(q);
      const assistantMsg = {
        role: 'assistant',
        ...res.data
      };
      setMessages(prev => [...prev, assistantMsg]);
    } catch (err) {
      console.error("Assistant error:", err);
      setMessages(prev => [...prev, {
        role: 'assistant',
        direct_answer: "Failed to communicate with Nexora query engine. Please check backend status.",
        supporting_facts: [],
        reasoning: "Network error or backend timeout.",
        recommended_action: "Ensure Flask API server is running on port 5001."
      }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', maxWidth: '1000px', margin: '0 auto' }}>
      
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
            Decision Assistant
          </h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            Ask Nexora about operational risk, bottlenecks, suppliers, production impact, or scenarios.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="status-badge badge-purple">IBM BOB ADVISOR</span>
          <span className="status-badge badge-neutral">Grounded Fact Reasoning</span>
        </div>
      </div>

      {/* Suggested Quick Prompt Chips */}
      <div>
        <span style={{ fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '0.04em', display: 'block', marginBottom: '8px' }}>
          Suggested Operations Queries
        </span>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {SAMPLE_QUERIES.map((sq, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(sq)}
              className="btn-secondary"
              style={{
                padding: '6px 12px',
                borderRadius: 'var(--radius-full)',
                fontSize: '0.78rem',
                fontWeight: 500
              }}
            >
              <Sparkles size={12} color="var(--primary-brand)" />
              <span>{sq}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Conversation Stream */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {messages.map((m, idx) => {
          const isUser = m.role === 'user';

          if (isUser) {
            return (
              <div
                key={idx}
                style={{
                  alignSelf: 'flex-end',
                  maxWidth: '80%',
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '10px'
                }}
              >
                <div style={{
                  padding: '12px 16px',
                  borderRadius: '12px 12px 2px 12px',
                  background: 'var(--primary-brand)',
                  color: '#ffffff',
                  fontSize: '0.875rem',
                  fontWeight: 500,
                  boxShadow: 'var(--shadow-sm)'
                }}>
                  {m.content}
                </div>
                <div style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  background: 'var(--surface-subtle)',
                  border: '1px solid var(--border-light)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'var(--text-secondary)',
                  flexShrink: 0
                }}>
                  <User size={16} />
                </div>
              </div>
            );
          }

          // Assistant Message
          return (
            <div
              key={idx}
              style={{
                alignSelf: 'flex-start',
                maxWidth: '92%',
                width: '100%',
                display: 'flex',
                alignItems: 'flex-start',
                gap: '12px'
              }}
            >
              <div style={{
                width: '34px',
                height: '34px',
                borderRadius: '8px',
                background: 'var(--primary-brand)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#ffffff',
                flexShrink: 0,
                boxShadow: '0 2px 6px rgba(0, 98, 255, 0.3)',
                marginTop: '2px'
              }}>
                <Cpu size={18} />
              </div>

              <div className="enterprise-card" style={{ padding: '18px 20px', flex: 1, display: 'flex', flexDirection: 'column', gap: '14px' }}>
                {/* Direct Answer */}
                <div>
                  <span style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--primary-brand)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                    Direct Diagnostic Answer
                  </span>
                  <p style={{ fontSize: '0.9rem', color: 'var(--text-primary)', marginTop: '4px', lineHeight: 1.5, fontWeight: 500 }}>
                    {m.direct_answer}
                  </p>
                </div>

                {/* Supporting Facts Cards */}
                {m.supporting_facts && m.supporting_facts.length > 0 && (
                  <div>
                    <span style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em', display: 'block', marginBottom: '6px' }}>
                      Verified Grounded Telemetry Facts
                    </span>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                      {m.supporting_facts.map((fact, fIdx) => (
                        <div
                          key={fIdx}
                          style={{
                            padding: '8px 12px',
                            borderRadius: 'var(--radius-sm)',
                            background: 'var(--surface-subtle)',
                            border: '1px solid var(--border-light)',
                            fontSize: '0.8rem',
                            color: 'var(--text-secondary)',
                            display: 'flex',
                            alignItems: 'flex-start',
                            gap: '8px'
                          }}
                        >
                          <CheckCircle2 size={14} color="var(--low)" style={{ marginTop: '2px', flexShrink: 0 }} />
                          <span>{fact}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Algorithmic Reasoning */}
                {m.reasoning && (
                  <div style={{
                    padding: '10px 14px',
                    borderRadius: 'var(--radius-sm)',
                    background: 'var(--info-bg)',
                    border: '1px solid var(--info-border)',
                    fontSize: '0.8rem',
                    color: 'var(--info-text)'
                  }}>
                    <strong>Algorithmic Reasoning: </strong>{m.reasoning}
                  </div>
                )}

                {/* Prescribed Action */}
                {m.recommended_action && (
                  <div style={{
                    padding: '10px 14px',
                    borderRadius: 'var(--radius-sm)',
                    background: 'var(--primary-light)',
                    border: '1px solid var(--primary-border)',
                    fontSize: '0.8rem',
                    color: 'var(--primary-brand)',
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '8px'
                  }}>
                    <CornerDownRight size={14} style={{ marginTop: '3px', flexShrink: 0 }} />
                    <div>
                      <strong>Recommended Operational Action: </strong>
                      <span style={{ color: 'var(--text-secondary)' }}>{m.recommended_action}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {/* Loading Bubble */}
        {loading && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '34px',
              height: '34px',
              borderRadius: '8px',
              background: 'var(--primary-brand)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#ffffff'
            }}>
              <Cpu size={18} />
            </div>
            <div className="enterprise-card" style={{ padding: '12px 18px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div className="animate-spin" style={{ width: '16px', height: '16px', border: '2px solid var(--primary-brand)', borderTopColor: 'transparent', borderRadius: '50%' }} />
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Querying Nexora Telemetry Engine...</span>
            </div>
          </div>
        )}
      </div>

      {/* Input Box Bar */}
      <div className="enterprise-card" style={{ padding: '8px 12px', display: 'flex', alignItems: 'center', gap: '10px', boxShadow: 'var(--shadow-md)' }}>
        <input
          type="text"
          placeholder="Ask about fab tool bottlenecks, SPoF suppliers, wafer delays, or disruption scenarios..."
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') handleSend();
          }}
          className="form-input"
          style={{ border: 'none', boxShadow: 'none', padding: '8px 4px', fontSize: '0.875rem' }}
        />
        <button
          className="btn-primary"
          onClick={() => handleSend()}
          disabled={loading || !inputQuery.trim()}
          style={{ padding: '8px 16px' }}
        >
          <Send size={15} />
          <span>Ask</span>
        </button>
      </div>
    </div>
  );
}
