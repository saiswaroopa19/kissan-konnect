import React, { useEffect, useState } from 'react'
import Header from '../components/Header'
import api from '../api/client'

export default function AdminConsole(){
  const [filter,setFilter] = useState('')
  const [items,setItems] = useState([])

  async function load(){
    const qs = new URLSearchParams()
    if(filter) qs.set('status', filter)
    const {data} = await api.get(`/applications/admin/list?${qs.toString()}`)
    setItems(data)
  }
  useEffect(()=>{ load() },[filter])

  async function setStatus(id, status){
    await api.post(`/applications/admin/${id}/status`, { status })
    load()
  }

  return (<>
    <Header/>
    <div className="container">
      <div className="card">
        <h2>Admin Console</h2>
        <div style={{display:'flex',gap:8,alignItems:'center'}}>
          <label>Status filter:
            <select className="input" value={filter} onChange={e=>setFilter(e.target.value)}>
              <option value="">All</option>
              <option>pending</option><option>under_review</option><option>approved</option><option>rejected</option>
            </select>
          </label>
        </div>
      </div>
      <div className="card">
        <table className="table">
          <thead><tr><th>ID</th><th>User</th><th>Program</th><th>Acreage</th><th>Season</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody>
            {items.map(x=>(
              <tr key={x.id}>
                <td>#{x.id}</td>
                <td>{x.user_id}</td>
                <td>{x.program_id}</td>
                <td>{x.acreage}</td>
                <td>{x.season}</td>
                <td>{x.status}</td>
                <td style={{display:'flex',gap:6}}>
                  <button className="btn secondary" onClick={()=>setStatus(x.id,'under_review')}>Review</button>
                  <button className="btn" onClick={()=>setStatus(x.id,'approved')}>Approve</button>
                  <button className="btn" style={{background:'#a00'}} onClick={()=>setStatus(x.id,'rejected')}>Reject</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  </>)
}
