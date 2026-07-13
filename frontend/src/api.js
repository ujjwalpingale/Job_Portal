import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: (email, password) => {
    return api.post('/login', { email, password });
  },
  register: (userData) => api.post('/register', userData),
};

export const userAPI = {
  getProfile: () => api.get('/profile'),
  updateProfile: (profileData) => api.put('/profile', profileData),
  uploadResume: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/resume', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export const jobAPI = {
  getJobs: () => api.get('/jobs'),
  createJob: (jobData) => api.post('/jobs', jobData),
  updateJob: (id, jobData) => api.put(`/jobs/${id}`, jobData),
  deleteJob: (id) => api.delete(`/jobs/${id}`),
};

export const applicationAPI = {
  applyForJob: (jobId) => api.post(`/jobs/${jobId}/apply`),
  getApplications: () => api.get('/applications'),
  updateStatus: (id, status) => api.patch(`/applications/${id}`, { status }),
};

export default api;
