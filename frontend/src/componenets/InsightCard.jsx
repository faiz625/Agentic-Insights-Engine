import React from "react";

export default function InsightCard({ title, children }) {
  return (
    <div style={{
      border: "1px solid #e5e7eb",
      borderRadius: 12,
      padding: 16,
      marginBottom: 16,
      boxShadow: "0 2px 10px rgba(0,0,0,0.04)"
    }}>
      <h3 style={{ marginTop: 0 }}>{title}</h3>
      <div>{children}</div>
    </div>
  );
}
