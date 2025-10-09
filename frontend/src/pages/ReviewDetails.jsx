import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import api from "../api/client";

export default function ReviewDetails() {
  const navigate = useNavigate();
  const location = useLocation();
  const selectedProgram = location.state?.program;
  const [user, setUser] = useState(null);
  const [consent, setConsent] = useState(false);
  const [loading, setLoading] = useState(false);

  // ✅ NEW state variables
  const [selectedCropId, setSelectedCropId] = useState("");
  const [acreage, setAcreage] = useState("");

  // ✅ Fetch user data
  useEffect(() => {
    const u = JSON.parse(localStorage.getItem("kk_user"));
    if (u) setUser(u);
  }, []);

  const handleChange = (e) => {
    setUser({ ...user, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    if (!consent) {
      alert("Please agree to data storage terms before proceeding.");
      return;
    }
    if (!selectedCropId || !acreage) {
      alert("Please select a crop and enter acreage before applying.");
      return;
    }

    setLoading(true);
    try {
      // ✅ Update user info
      const { id, ...updatedUser } = user;
      await api.put(`/users/${id}`, updatedUser);

      // ✅ Submit application
      await api.post(
  "/applications",
  {
    program_id: selectedProgram.id,
    crop_id: parseInt(selectedCropId),
    acreage: parseFloat(acreage),
    season: selectedProgram?.season || "Any",
  },
  {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("kk_access")}`,
    },
  }
);


      navigate("/application-submitted");
    } catch (err) {
      console.error(err);
      alert("Something went wrong while submitting your application.");
    } finally {
      setLoading(false);
    }
  };

  if (!user) return <p>Loading user info...</p>;

  return (
    <div
      style={{
        maxWidth: "700px",
        margin: "50px auto",
        padding: "30px",
        background: "#fff",
        borderRadius: "12px",
        boxShadow: "0px 0px 15px rgba(0,0,0,0.1)",
      }}
    >
      <h2>📄 Review Your Details</h2>
      <p>
        Please confirm and update your details before submitting your
        application for <strong>{selectedProgram?.title}</strong>.
      </p>

      <div style={{ display: "grid", gap: "15px", marginTop: "20px" }}>
        <label>
          Name:
          <input name="name" value={user.name || ""} onChange={handleChange} />
        </label>
        <label>
          Email:
          <input name="email" value={user.email || ""} onChange={handleChange} />
        </label>
        <label>
          Phone:
          <input name="phone" value={user.phone || ""} onChange={handleChange} />
        </label>
        <label>
          State:
          <input name="state" value={user.state || ""} onChange={handleChange} />
        </label>
        <label>
          District:
          <input
            name="district"
            value={user.district || ""}
            onChange={handleChange}
          />
        </label>
        <label>
          Aadhaar:
          <input
            name="aadhar"
            value={user.aadhar || ""}
            onChange={handleChange}
          />
        </label>

        {/* 🌾 New Crop Selection */}
        <label>
          Select Crop:
          <select
            value={selectedCropId}
            onChange={(e) => setSelectedCropId(e.target.value)}
            required
          >
            <option value="">-- Select Crop --</option>
            <option value="1">Rice</option>
            <option value="2">Wheat</option>
            <option value="3">Maize</option>
            <option value="4">Cotton</option>
            <option value="5">Sugarcane</option>
            <option value="6">Pulses</option>
          </select>
        </label>

        {/* 🌱 New Acreage Input */}
        <label>
          Land Size (in acres):
          <input
            type="number"
            placeholder="Enter acreage"
            value={acreage}
            onChange={(e) => setAcreage(e.target.value)}
            required
          />
        </label>
      </div>

      <div style={{ marginTop: "20px" }}>
        <label style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <input
            type="checkbox"
            checked={consent}
            onChange={(e) => setConsent(e.target.checked)}
          />
          I agree that Kissan Konnect may store and use my personal information
          for subsidy application processing.
        </label>
      </div>

      <button
        style={{
          marginTop: "30px",
          padding: "12px",
          backgroundColor: consent ? "#4CAF50" : "#ccc",
          color: "white",
          border: "none",
          borderRadius: "8px",
          cursor: consent ? "pointer" : "not-allowed",
        }}
        onClick={handleSubmit}
        disabled={!consent || loading}
      >
        {loading ? "Submitting..." : "Submit Application"}
      </button>
    </div>
  );
}
