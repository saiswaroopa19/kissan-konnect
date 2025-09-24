import React, { useState } from 'react'
import { useAuth } from '../auth/AuthContext'
import api from '../api/client'
import { useNavigate } from 'react-router-dom'

const apDistricts = [
  "Anantapur", "Chittoor", "East Godavari", "Guntur", "Krishna",
  "Kurnool", "Nellore", "Prakasam", "Srikakulam", "Visakhapatnam",
  "Vizianagaram", "West Godavari", "YSR Kadapa"
]

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()

  const [form, setForm] = useState({
    name: "", email: "", password: "", phone: "",
    gender: "Male", dob: "", state: "Andhra Pradesh",
    district: "", aadhar: ""
  })
  const [doc, setDoc] = useState(null)

  const handleChange = e => setForm({...form, [e.target.name]: e.target.value})
  const handleFile = e => setDoc(e.target.files[0])

  const handleSubmit = async e => {
    e.preventDefault()

    // Validate Indian phone
    if(!/^[6-9]\d{9}$/.test(form.phone)) {
      alert("Invalid phone number. Must be 10 digits starting with 6-9.")
      return
    }

    let docPath = null
    if(doc){
      const fd = new FormData()
      fd.append("file", doc)
      const res = await api.post("/upload", fd, {
        headers: {"Content-Type":"multipart/form-data"}
      })
      docPath = res.data.path
    }

    try {
      await register({...form, doc_path: docPath})
      alert("✅ Registration successful! Please login.")
      navigate("/login")   // 🔥 redirect to login
    } catch (err) {
      console.error(err)
      alert("❌ Registration failed.")
    }
  }

  return (
    <div className="container card">
      <h2>Farmer Registration (AP Only)</h2>
      <form onSubmit={handleSubmit} className="grid">
        <input className="input" name="name" placeholder="Full Name" onChange={handleChange} />
        <input className="input" type="email" name="email" placeholder="Email" onChange={handleChange} />
        <input className="input" type="password" name="password" placeholder="Password" onChange={handleChange} />
        <input className="input" name="phone" placeholder="Phone Number" onChange={handleChange} />

        <select className="input" name="gender" onChange={handleChange}>
          <option>Male</option><option>Female</option><option>Other</option>
        </select>

        <input className="input" type="date" name="dob" onChange={handleChange} />
        <input className="input" value="Andhra Pradesh" readOnly />

        <select className="input" name="district" onChange={handleChange}>
          <option value="">Select District</option>
          {apDistricts.map(d => <option key={d}>{d}</option>)}
        </select>

        <input className="input" name="aadhar" placeholder="Aadhar ID" onChange={handleChange} />
        <label>Upload Govt ID (Aadhar, PAN, License)</label>
        <input type="file" onChange={handleFile} />

        <button className="btn" type="submit">Register</button>
      </form>
    </div>
  )
}
