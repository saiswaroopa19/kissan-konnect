import React, { useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"
import api from "../api/client"

export default function ResetPassword() {
  const location = useLocation()
  const navigate = useNavigate()

  // Get token from state (if navigated from ForgotPassword)
  const presetToken = location.state?.token || ""

  const [token, setToken] = useState(presetToken)
  const [newPassword, setNewPassword] = useState("")
  const [message, setMessage] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.post("/auth/reset-password", { token, new_password: newPassword })
      alert("Password reset successful! Please login with your new password.")
      navigate("/login")
    } catch (err) {
      setMessage("Invalid or expired token")
    }
  }

  return (
    <div className="container card">
      <h2>Reset Password</h2>
      <form onSubmit={handleSubmit} className="grid" style={{ gap: "12px" }}>
        <input
          className="input"
          placeholder="Reset Token"
          value={token}
          onChange={(e) => setToken(e.target.value)}
          required
        />
        <input
          className="input"
          type="password"
          placeholder="New Password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          required
        />
        <button className="btn" type="submit">Reset Password</button>
      </form>
      {message && <p style={{ marginTop: "12px", color: "red" }}>{message}</p>}
    </div>
  )
}
