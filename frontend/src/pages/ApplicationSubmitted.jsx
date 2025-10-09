import React from "react";
import { useNavigate } from "react-router-dom";

export default function ApplicationSubmitted() {
  const navigate = useNavigate(); // ✅ This line is missing in your file

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h2>🎉 Application Submitted Successfully!</h2>
      <p>Your subsidy application has been received and is under review.</p>

      <button
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          backgroundColor: "#4CAF50",
          color: "#fff",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
        }}
        onClick={() => navigate("/")} // ✅ now it works
      >
        Go to Dashboard
      </button>
    </div>
  );
}
