import React, { useEffect, useState } from 'react'
import Header from '../components/Header'
import api from '../api/client'
import { Link } from 'react-router-dom'

export default function Programs(){
  const [items,setItems] = useState([])
  const [cropId,setCropId] = useState('')
  const [season,setSeason] = useState('Any')
  const [loading,setLoading] = useState(true)

  useEffect(()=>{ load() },[])

  async function load(){
    setLoading(true)
    const qs = new URLSearchParams()
    if(cropId) qs.set('crop_id', cropId)
    if(season) qs.set('season', season)
    const { data } = await api.get(`/programs?${qs.toString()}`)
    setItems(data); setLoading(false)
  }

  return (<>
    <Header/>
    <div className="container">
      <div className="card">
        <h2>Government Programs</h2>
        <div className="grid cols-2">
          <select className="input" value={cropId} onChange={e=>setCropId(e.target.value)}>
            <option value="">All Crops</option>
            <option value="1">Rice</option>
            <option value="2">Wheat</option>
            <option value="3">Maize</option>
            <option value="4">Cotton</option>
            <option value="5">Sugarcane</option>
            <option value="6">Pulses</option>
          </select>
          <select className="input" value={season} onChange={e=>setSeason(e.target.value)}>
            <option>Any</option><option>Kharif</option><option>Rabi</option><option>Zaid</option>
          </select>
          <button className="btn" onClick={load}>Apply Filters</button>
        </div>
      </div>

      {loading ? <div className="card">Loading…</div> : items.map(p=>(
        <div key={p.id} className="card">
          <h3 style={{marginTop:0}}>{p.title} <span className="badge">{p.season||'Any'}</span></h3>
          <p>{p.description}</p>
          <div style={{display:'flex',gap:8,alignItems:'center'}}>
            <span className="badge">Authority: {p.authority}</span>
            <span className="badge">Land: {(p.min_land_size ?? 0)} - {(p.max_land_size ?? 'No limit')} acres</span>
            <Link className="btn" to="/review-details" state={{ program: p }}>Apply</Link>

          </div>
        </div>
      ))}
    </div>
  </>)
}
