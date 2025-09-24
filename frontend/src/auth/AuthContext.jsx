import React, {createContext, useContext, useEffect, useState} from 'react'
import api from '../api/client'

const Ctx = createContext(null)

export function AuthProvider({children}){
  const [user,setUser] = useState(null)
  useEffect(()=>{
    const u = localStorage.getItem('kk_user')
    if(u) setUser(JSON.parse(u))
  },[])
  const login = async (email,password)=>{
    const {data} = await api.post('/auth/login',{email,password})
    localStorage.setItem('kk_access', data.access_token)
    localStorage.setItem('kk_refresh', data.refresh_token)
    localStorage.setItem('kk_user', JSON.stringify(data.user))
    setUser(data.user)
  }
 const register = async (payload) => {
  try {
    const { data } = await api.post('/auth/register', payload)
    await login(payload.email, payload.password)
    return data
  } catch (err) {
    console.error("❌ Register failed:", {
      message: err.message,
      status: err.response?.status,
      data: err.response?.data,
    })
    throw err
  }
}


  const logout = ()=>{
    localStorage.removeItem('kk_access');localStorage.removeItem('kk_refresh');localStorage.removeItem('kk_user')
    setUser(null)
  }
  return <Ctx.Provider value={{user,login,register,logout}}>{children}</Ctx.Provider>
}
export const useAuth = ()=> useContext(Ctx)
