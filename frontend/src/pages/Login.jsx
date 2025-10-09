import React, { useState } from "react";
import { useAuth } from "../auth/AuthContext";
import { useNavigate, Link } from "react-router-dom";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password);
      navigate("/"); // redirect to dashboard
    } catch (err) {
      setError("Invalid email or password. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundImage:
        "url('/images/farmers1.jpg')", // 🌾 farmland photo
        backgroundSize: "cover",
        backgroundPosition: "center",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "20px",
      }}
    >
      <div
        style={{
          display: "flex",
          backgroundColor: "rgba(255, 255, 255, 0.9)",
          borderRadius: "20px",
          maxWidth: "900px",
          width: "100%",
          boxShadow: "0 10px 25px rgba(0,0,0,0.2)",
          overflow: "hidden",
        }}
      >
        {/* Left Side - Info Section */}
        <div
          style={{
            flex: 1,
            background:
              "linear-gradient(135deg, #4CAF50 0%, #81C784 100%)",
            color: "white",
            padding: "40px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
          }}
        >
          <h1 style={{ fontSize: "2.5rem", marginBottom: "20px" }}>
            🌾 Kissan Konnect
          </h1>
          <p style={{ fontSize: "1.2rem", lineHeight: "1.6" }}>
            Empowering farmers with easy access to government subsidies and
            support programs. <br />
            Login to manage your crops, apply for schemes, and track your
            applications — all in one place!
          </p>
        </div>

        {/* Right Side - Login Form */}
        <div style={{ flex: 1, padding: "40px" }}>
          <h2 style={{ textAlign: "center", marginBottom: "30px" }}>
            👨‍🌾 Farmer / Admin Login
          </h2>
          {error && (
            <p
              style={{
                color: "red",
                textAlign: "center",
                marginBottom: "20px",
              }}
            >
              {error}
            </p>
          )}
          <form
            onSubmit={handleSubmit}
            style={{ display: "flex", flexDirection: "column", gap: "15px" }}
          >
            <input
              type="email"
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              style={{
                padding: "12px",
                borderRadius: "8px",
                border: "1px solid #ccc",
                fontSize: "16px",
              }}
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{
                padding: "12px",
                borderRadius: "8px",
                border: "1px solid #ccc",
                fontSize: "16px",
              }}
            />
            <button
              type="submit"
              disabled={loading}
              style={{
                padding: "12px",
                borderRadius: "8px",
                backgroundColor: "#4CAF50",
                color: "white",
                fontSize: "18px",
                border: "none",
                cursor: "pointer",
                transition: "0.3s",
              }}
              onMouseOver={(e) =>
                (e.target.style.backgroundColor = "#45a049")
              }
              onMouseOut={(e) =>
                (e.target.style.backgroundColor = "#4CAF50")
              }
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>

          <p style={{ marginTop: "20px", textAlign: "center" }}>
            Don’t have an account? <Link to="/register">Register</Link>
          </p>

          <p style={{ marginTop: "10px", textAlign: "center" }}>
            <Link to="/forgot-password">Forgot Password?</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
