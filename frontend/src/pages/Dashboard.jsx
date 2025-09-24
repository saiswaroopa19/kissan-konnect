import React from 'react'
import Header from '../components/Header'
import { useAuth } from '../auth/AuthContext'
import { Link } from 'react-router-dom'

export default function Dashboard(){
  const { user } = useAuth()
  return (
    <>
      <Header/>
      <div className="container">

        {/* Hero Banner */}
        <div className="hero">
          <div>
            <h2 style={{margin:'0 0 8px'}}>Welcome, {user?.name} 👩‍🌾</h2>
            <p>Discover eligible schemes, apply in minutes, and track approvals.</p>
            <div style={{marginTop:12, display:'flex', gap:8}}>
              <Link className="btn" to="/programs">Browse Programs</Link>
              <Link className="btn secondary" to="/applications">My Applications</Link>
            </div>
          </div>
        </div>

        {/* Add spacing between hero and grid */}
        <div style={{ marginTop: '24px' }} className="grid cols-2">
          <div className="card">
            <h3>Quick Links</h3>
            <nav className="tabs">
              <Link to="/programs">All Programs</Link>
              <Link to="/applications">Application Status</Link>
              {user?.role==='admin' && <Link to="/admin">Admin Console</Link>}
            </nav>
            <p className="badge">Tip: Use crop filters to quickly find relevant subsidies.</p>
          </div>

          <div className="card">
            <h3>Announcements</h3>
            <ul>
              <li>Portal open 24/7. Average response under 3 seconds.</li>
              <li>Protect your data—never share your password with anyone.</li>
            </ul>
          </div>
        </div>

        <footer>
          © {new Date().getFullYear()} Kissan Konnect • A demo portal for farmer subsidies
        </footer>
      </div>
    </>
  )
}
