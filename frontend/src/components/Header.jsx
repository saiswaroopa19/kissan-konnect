import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

export default function Header(){
  const { user, logout } = useAuth()
  return (
    <header>
      <img src="/src/assets/logo.svg" alt="logo"/>
      <h1>Kissan Konnect</h1>
      <nav style={{marginLeft:'auto',display:'flex',gap:12}}>
        {user && <>
          <Link to="/">Dashboard</Link>
          <Link to="/programs">Programs</Link>
          <Link to="/applications">My Applications</Link>
          {user.role==='admin' && <Link to="/admin">Admin</Link>}
          <button className="btn secondary" onClick={logout}>Logout</button>
        </>}
      </nav>
    </header>
  )
}
