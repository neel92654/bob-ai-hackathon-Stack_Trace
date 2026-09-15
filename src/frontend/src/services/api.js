/**
 * API Service Layer for Nexora Frontend
 * Communicates with Flask REST backend endpoints with robust error handling.
 */

const API_BASE = (typeof window !== 'undefined' && (window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost'))
  ? 'http://127.0.0.1:5001/api'
  : '/api';


export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
  return res.json();
}

export async function fetchDashboardSummary() {
  const res = await fetch(`${API_BASE}/dashboard/summary`);
  if (!res.ok) throw new Error(`Dashboard summary failed: ${res.statusText}`);
  return res.json();
}

export async function fetchBottlenecks() {
  const res = await fetch(`${API_BASE}/bottlenecks`);
  if (!res.ok) throw new Error(`Fetch bottlenecks failed: ${res.statusText}`);
  return res.json();
}

export async function fetchBottleneckDetails(toolId) {
  const res = await fetch(`${API_BASE}/bottlenecks/${toolId}`);
  if (!res.ok) throw new Error(`Fetch bottleneck details failed: ${res.statusText}`);
  return res.json();
}

export async function fetchSuppliers() {
  const res = await fetch(`${API_BASE}/suppliers`);
  if (!res.ok) throw new Error(`Fetch suppliers failed: ${res.statusText}`);
  return res.json();
}

export async function fetchSupplierDetails(supplierId) {
  const res = await fetch(`${API_BASE}/suppliers/${supplierId}`);
  if (!res.ok) throw new Error(`Fetch supplier details failed: ${res.statusText}`);
  return res.json();
}

export async function fetchGeopoliticalConcentration() {
  const res = await fetch(`${API_BASE}/suppliers/geopolitical-concentration`);
  if (!res.ok) throw new Error(`Fetch geopolitical data failed: ${res.statusText}`);
  return res.json();
}

export async function fetchProductionLots(filters = {}) {
  const params = new URLSearchParams();
  if (filters.priority) params.append('priority', filters.priority);
  if (filters.process) params.append('process', filters.process);
  if (filters.tool) params.append('tool', filters.tool);
  
  const url = `${API_BASE}/production/lots${params.toString() ? '?' + params.toString() : ''}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Fetch lots failed: ${res.statusText}`);
  return res.json();
}

export async function runSimulation(scenarioType, params) {
  const res = await fetch(`${API_BASE}/simulation/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scenario_type: scenarioType, params })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.message || `Simulation failed: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchRecommendations(filters = {}) {
  const params = new URLSearchParams();
  if (filters.category) params.append('category', filters.category);
  if (filters.priority) params.append('priority', filters.priority);

  const url = `${API_BASE}/recommendations${params.toString() ? '?' + params.toString() : ''}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Fetch recommendations failed: ${res.statusText}`);
  return res.json();
}

export async function queryDecisionAssistant(query) {
  const res = await fetch(`${API_BASE}/assistant/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.message || `Assistant query failed: ${res.statusText}`);
  }
  return res.json();
}
