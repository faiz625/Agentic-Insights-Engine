import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function runOrchestrator({ sql = null, limit = 1000 }) {
  const { data } = await axios.post(`${API_BASE}/run`, { sql, limit });
  return data;
}
