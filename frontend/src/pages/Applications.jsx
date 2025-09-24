import React, { useEffect, useState } from 'react'
import Header from '../components/Header'
import api from '../api/client'

const STATUS_COLORS = { pending:'#ffb703', under_review:'#118ab2', approved:'#2a9d8f', rejected:'#e76f51' }

export default function Applications(){
  const [items,setItems] = useState([])
  const [loading,setLoading] = useState(true)

  useEffect(()=>{ (async()=>{
    const {data} = await api.get('/applications')
    setItems(data); setLoading(false)
  })() },[])

  return (<>
    <Header/>
    <div className="container">
      <div className="card">
        <h2>My Applications</h2>
        {loading ? 'Loading…' :
        <table className="table">
          <thead><tr><th>ID</th><th>Program</th><th>Acreage</th><th>Season</th><th>Status</th></tr></thead>
          <tbody>
            {items.map(x=>(
              <tr key={x.id}>
                <td>#{x.id}</td>
                <td>{x.program_id}</td>
                <td>{x.acreage}</td>
                <td>{x.season}</td>
                <td><span className="badge" style={{background:'#fff',borderColor:'#ddd', color:STATUS_COLORS[x.status]}}>{x.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>}
      </div>
    </div>
  </>)
}
