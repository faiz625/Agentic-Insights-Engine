import React, { useState } from "react";
import { runOrchestrator } from "./api";
import InsightCard from "./components/InsightCard";
import Chart from "./components/Chart";

export default function App() {
  const [sql, setSql] = useState("");
  const [limit, setLimit] = useState(1000);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const onRun = async () => {
    setLoading(true);
    try {
      const data = await runOrchestrator({ sql: sql || null, limit });
      setResult(data);
    } catch (e) {
      console.error(e);
      alert("Failed to run orchestrator. Check console.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 1100, padding: 24, margin: "0 auto", fontFamily: "Inter, system-ui, Arial" }}>
      <h1>Agentic Insights Engine — Exec Dashboard</h1>
      <p style={{ color: "#6b7280" }}>Run the multi-agent pipeline and review insights.</p>

      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 120px 140px",
        gap: 12,
        marginBottom: 16
      }}>
        <textarea
          placeholder="Optional SQL (BigQuery)"
          value={sql}
          onChange={(e) => setSql(e.target.value)}
          rows={4}
          style={{ width: "100%", padding: 12, borderRadius: 8, border: "1px solid #e5e7eb" }}
        />
        <input
          type="number"
          value={limit}
          onChange={(e) => setLimit(Number(e.target.value))}
          style={{ width: "100%", padding: 12, borderRadius: 8, border: "1px solid #e5e7eb" }}
        />
        <button
          onClick={onRun}
          disabled={loading}
          style={{
            width: "100%", padding: 12, borderRadius: 8, border: "1px solid #111827",
            background: "#111827", color: "white", cursor: "pointer"
          }}
        >
          {loading ? "Running..." : "Run Orchestrator"}
        </button>
      </div>

      {result && (
        <>
          <InsightCard title="Narrative Summary">
            <p>{result.narrative}</p>
          </InsightCard>

          <InsightCard title="Training Metrics">
            <pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(result.training_metrics, null, 2)}</pre>
          </InsightCard>

          <InsightCard title="Top Features (mean |SHAP|)">
            <table style={{ width: "100%" }}>
              <thead>
                <tr><th align="left">Feature</th><th align="right">Importance</th></tr>
              </thead>
              <tbody>
                {result.feature_importance?.map(([f, v]) => (
                  <tr key={f}>
                    <td>{f}</td><td align="right">{v.toFixed(4)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </InsightCard>

          <InsightCard title="Anomalies (preview)">
            <pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(result.anomalies?.slice(0, 10), null, 2)}</pre>
          </InsightCard>

          <InsightCard title="Charts">
            {result.charts?.length ? result.charts.map((c, idx) => (
              <div key={idx} style={{ marginBottom: 16 }}>
                <Chart payload={c} />
              </div>
            )) : <p>No charts generated for this dataset.</p>}
          </InsightCard>

          <InsightCard title="Sample Rows">
            <pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(result.sample?.slice(0, 10), null, 2)}</pre>
          </InsightCard>
        </>
      )}
    </div>
  );
}
