import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import './styles.css'
import { AuthProvider, useAuth } from './auth/AuthContext'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Programs from './pages/Programs'
import Apply from './pages/Apply'
import Applications from './pages/Applications'
import AdminConsole from './pages/AdminConsole'
import ForgotPassword from "./pages/ForgotPassword"
import ResetPassword from "./pages/ResetPassword"
import ReviewDetails from "./pages/ReviewDetails";
import ApplicationSubmitted from "./pages/ApplicationSubmitted";



function RequireAuth({ children, admin=false }){
  const { user } = useAuth()
  if(!user) return <Navigate to="/login" replace />
  if(admin && user.role!=='admin') return <Navigate to="/" replace />
  return children
}

function App(){
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login/>} />
        <Route path="/register" element={<Register/>} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/" element={<RequireAuth><Dashboard/></RequireAuth>} />
        <Route path="/programs" element={<RequireAuth><Programs/></RequireAuth>} />
        <Route path="/apply/:programId" element={<RequireAuth><Apply/></RequireAuth>} />
        <Route path="/applications" element={<RequireAuth><Applications/></RequireAuth>} />
        <Route path="/admin" element={<RequireAuth admin={true}><AdminConsole/></RequireAuth>} />
        <Route path="/review-details" element={<ReviewDetails />} />
        <Route path="/application-submitted" element={<ApplicationSubmitted />} />
       <Route path="/" element={<RequireAuth><Dashboard/></RequireAuth>} />


      </Routes>
    </BrowserRouter>
  )
}

createRoot(document.getElementById('root')).render(
  <AuthProvider><App/></AuthProvider>
)
