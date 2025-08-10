import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (username, email, password) => api.post('/auth/register', { username, email, password }),
  getProfile: () => api.get('/auth/me'),
  logout: () => api.post('/auth/logout')
}

// Query API
export const queryAPI = {
  parse: (query, includeVisualization = false) => 
    api.post('/queries/parse', { query, includeVisualization }),
  getHistory: (page = 1, limit = 20) => 
    api.get(`/queries/history?page=${page}&limit=${limit}`),
  getQuery: (queryId) => api.get(`/queries/${queryId}`),
  addFeedback: (queryId, rating, comment) => 
    api.post(`/queries/${queryId}/feedback`, { rating, comment }),
  deleteQuery: (queryId) => api.delete(`/queries/${queryId}`)
}

// User API
export const userAPI = {
  getProfile: () => api.get('/users/profile'),
  updateProfile: (data) => api.put('/users/profile', data),
  changePassword: (currentPassword, newPassword) => 
    api.put('/users/change-password', { currentPassword, newPassword }),
  deactivateAccount: () => api.delete('/users/account')
}

// Analytics API
export const analyticsAPI = {
  getDashboard: (days = 30) => api.get(`/analytics/dashboard?days=${days}`),
  getSystemAnalytics: (days = 30) => api.get(`/analytics/system?days=${days}`)
}

export default api
