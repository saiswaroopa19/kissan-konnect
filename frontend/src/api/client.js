import axios from 'axios'

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const api = axios.create({ baseURL })

api.interceptors.request.use(cfg => {
  const t = localStorage.getItem('kk_access')
  if (t) cfg.headers.Authorization = `Bearer ${t}`
  return cfg
})

api.interceptors.response.use(
  r => r,
  async err => {
    if (err.response?.status === 401) {
      const rt = localStorage.getItem('kk_refresh')
      if (rt) {
        try{
          const { data } = await axios.post(`${baseURL}/auth/refresh`, { refresh_token: rt })
          localStorage.setItem('kk_access', data.access_token)
          localStorage.setItem('kk_refresh', data.refresh_token)
          err.config.headers.Authorization = `Bearer ${data.access_token}`
          return api.request(err.config)
        }catch(e){ /* fallthrough */ }
      }
    }
    return Promise.reject(err)
  }
)

export default api
