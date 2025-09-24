import React, { useState } from "react"
import api from "../api/client"
import { useNavigate } from "react-router-dom"

export default function ForgotPassword() {
  const [email, setEmail] = useState("")
  const [message, setMessage] = useState(null)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await api.post("/auth/forgot-password", { email })
      setMessage(res.data.msg)

      // For demo, show the token
      if (res.data.token) {
        alert(`Your reset token: ${res.data.token}`)
        // Navigate to reset page and pass token in state
        navigate("/reset-password", { state: { token: res.data.token } })
      }
    } catch (err) {
      setMessage("Something went wrong")
    }
  }

  return (
    <div className="container card">
      <h2>Forgot Password</h2>
      <form onSubmit={handleSubmit} className="grid" style={{ gap: "12px" }}>
        <input
          className="input"
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button className="btn" type="submit">Request Reset</button>
      </form>
      {message && <p style={{ marginTop: "12px" }}>{message}</p>}
    </div>
  )
}
