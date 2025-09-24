import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Header from '../components/Header'
import api from '../api/client'

export default function Apply(){
  const { programId } = useParams()
  const nav = useNavigate()
  const [program,setProgram] = useState(null)
  const [form,setForm] = useState({crop_id:1, acreage:1, season:'Any'})
  const [msg,setMsg] = useState('')

  useEffect(()=>{ (async()=>{
    const {data} = await api.get(`/programs/${programId}`)
    setProgram(data)
  })() },[programId])

  async function submit(e){
    e.preventDefault()
    setMsg('')
    try{
      await api.post('/applications', { program_id:Number(programId), ...form })
      setMsg('Application submitted!')
      setTimeout(()=> nav('/applications'), 700)
    }catch(err){
      setMsg(err.response?.data?.detail || 'Failed to submit')
    }
  }

  if(!program) return (<><Header/><div className="container"><div className="card">Loading…</div></div></>)

  return (<>
    <Header/>
    <div className="container">
      <div className="card">
        <h2>Apply: {program.title}</h2>
        <form onSubmit={submit} className="grid cols-2">
          <label>Crop
            <select className="input" value={form.crop_id} onChange={e=>setForm({...form, crop_id:Number(e.target.value)})}>
              <option value="1">Rice</option><option value="2">Wheat</option><option value="3">Maize</option>
              <option value="4">Cotton</option><option value="5">Sugarcane</option><option value="6">Pulses</option>
            </select>
          </label>
          <label>Acreage
            <input className="input" type="number" min="0.1" step="0.1" value={form.acreage} onChange={e=>setForm({...form, acreage:Number(e.target.value)})}/>
          </label>
          <label>Season
            <select className="input" value={form.season} onChange={e=>setForm({...form, season:e.target.value})}>
              <option>Any</option><option>Kharif</option><option>Rabi</option><option>Zaid</option>
            </select>
          </label>
          <button className="btn" style={{gridColumn:'1/-1'}}>Submit Application</button>
        </form>
        {msg && <p className="badge" style={{marginTop:8}}>{msg}</p>}
      </div>
    </div>
  </>)
}
