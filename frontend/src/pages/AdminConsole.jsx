import React, { useEffect, useState } from 'react'
import Header from '../components/Header'
import api from '../api/client'

export default function AdminConsole(){
  const [filter,setFilter] = useState('')
  const [items,setItems] = useState([])

  // Review panel state
  const [openReview, setOpenReview] = useState(false)
  const [details, setDetails] = useState(null)
  const [remarks, setRemarks] = useState('')

  async function load(){
    const qs = new URLSearchParams()
    if(filter) qs.set('status', filter)
    const {data} = await api.get(`/applications/admin/list?${qs.toString()}`)
    setItems(data)
  }
  useEffect(()=>{ load() },[filter])

  async function setStatus(id, status, remarkText){
    await api.post(`/applications/admin/${id}/status`, { status, remarks: remarkText ?? null })
    await load()
  }

  async function openReviewFor(id){
    // mark "under_review" and fetch details
    try {
      await setStatus(id, 'under_review', 'Admin started manual verification')
    } catch(e) {
      // ignore if already under_review, continue to details
    }
    const {data} = await api.get(`/applications/admin/${id}/details`)
    setDetails(data)
    setRemarks('')
    setOpenReview(true)
  }

  function closeReview(){
    setOpenReview(false)
    setDetails(null)
    setRemarks('')
  }

  async function approve(){
    if(!details) return
    try{
      await setStatus(details.application.id, 'approved', remarks || 'Approved after manual verification')
      alert('Application approved')
      closeReview()
    }catch(err){
      const msg = err?.response?.data?.detail || 'Approval failed'
      alert(msg)
    }
  }

  async function reject(){
    if(!details) return
    const message = remarks?.trim()
    if(!message){
      alert('Please add remarks explaining the reason for rejection.')
      return
    }
    try{
      await setStatus(details.application.id, 'rejected', message)
      alert('Application rejected')
      closeReview()
    }catch(err){
      const msg = err?.response?.data?.detail || 'Rejection failed'
      alert(msg)
    }
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
                  <button className="btn secondary" onClick={()=>openReviewFor(x.id)}>Review</button>
                  <button className="btn" onClick={()=>setStatus(x.id,'approved','Approved from list view')}>Approve</button>
                  <button className="btn" style={{background:'#a00'}} onClick={async ()=>{
                    const r = prompt('Reason for rejection (shown to farmer):')
                    if(r) await setStatus(x.id,'rejected', r)
                  }}>Reject</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Review Panel / Modal */}
      {openReview && details && (
        <div style={{
          position:'fixed', inset:0, background:'rgba(0,0,0,0.35)',
          display:'flex', alignItems:'center', justifyContent:'center', padding:16, zIndex:1000
        }}>
          <div className="card" style={{maxWidth:900, width:'100%', maxHeight:'90vh', overflow:'auto', padding:24}}>
            <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:12}}>
              <h3>Manual Verification – Application #{details.application.id}</h3>
              <button className="btn secondary" onClick={closeReview}>Close</button>
            </div>

            <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:16}}>
              <section className="card" style={{padding:16}}>
                <h4>User</h4>
                <p><b>Name:</b> {details.user.name}</p>
                <p><b>Aadhar:</b> {details.user.aadhar || '—'}</p>
                <p><b>Phone:</b> {details.user.phone || '—'}</p>
                <p><b>Address:</b> {details.user.state}, {details.user.district}</p>
              </section>

              <section className="card" style={{padding:16}}>
                <h4>Program</h4>
                <p><b>Title:</b> {details.program.title}</p>
                <p><b>Authority:</b> {details.program.authority}</p>
                <p><b>Season:</b> {details.program.season || 'Any'}</p>
                <p><b>Land size limits:</b> {details.program.min_land_size ?? '—'} to {details.program.max_land_size ?? '—'} acres</p>
              </section>

              <section className="card" style={{padding:16}}>
                <h4>Application</h4>
                <p><b>Crop:</b> {details.crop.name}</p>
                <p><b>Acreage:</b> {details.application.acreage} acres</p>
                <p><b>Season:</b> {details.application.season}</p>
                <p><b>Status:</b> {details.application.status}</p>
                {details.application.remarks && <p><b>Previous remarks:</b> {details.application.remarks}</p>}
              </section>

              <section className="card" style={{padding:16}}>
                <h4>Documents</h4>
                {details.documents.length === 0 ? (
                  <p>No documents uploaded.</p>
                ) : (
                  <ul>
                    {details.documents.map(d=>(
                      <li key={d.id}>
                        <b>{d.kind}:</b> <span style={{wordBreak:'break-all'}}>{d.file_path}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </section>
            </div>

            <div className="card" style={{marginTop:16, padding:16}}>
              <label style={{display:'block', marginBottom:8}}>
                <b>Verification Notes (shown to farmer on approve/reject):</b>
              </label>
              <textarea
                className="input"
                rows={4}
                value={remarks}
                onChange={e=>setRemarks(e.target.value)}
                placeholder="Add notes about your manual verification..."
                style={{width:'100%'}}
              />
              <div style={{display:'flex', gap:8, marginTop:12}}>
                <button className="btn" onClick={approve}>✅ Approve</button>
                <button className="btn" style={{background:'#a00'}} onClick={reject}>❌ Reject</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  </>)
}
