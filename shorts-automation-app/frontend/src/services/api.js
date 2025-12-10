import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Channels API
export const channelsAPI = {
  list: () => api.get('/channels'),
  get: (id) => api.get(`/channels/${id}`),
  create: (data) => api.post('/channels', data),
  update: (id, data) => api.put(`/channels/${id}`, data),
  delete: (id) => api.delete(`/channels/${id}`),
  getStats: (id) => api.get(`/channels/${id}/stats`),
};

// Ideas API
export const ideasAPI = {
  list: (params) => api.get('/ideas', { params }),
  get: (id) => api.get(`/ideas/${id}`),
  create: (data) => api.post('/ideas', data),
  updateStatus: (id, status) => api.put(`/ideas/${id}/status`, null, { params: { status } }),
  delete: (id) => api.delete(`/ideas/${id}`),
};

// Videos API
export const videosAPI = {
  list: (params) => api.get('/videos', { params }),
  get: (id) => api.get(`/videos/${id}`),
  create: (data) => api.post('/videos', data),
  delete: (id) => api.delete(`/videos/${id}`),
};

// Workflow API
export const workflowAPI = {
  start: (data) => api.post('/workflow/start', data),
  generateIdeas: (channelId, numIdeas) =>
    api.post(`/workflow/generate-ideas/${channelId}`, null, { params: { num_ideas: numIdeas } }),
  createScript: (ideaId) => api.post(`/workflow/create-script/${ideaId}`),
  generateAudio: (ideaId) => api.post(`/workflow/generate-audio/${ideaId}`),
  renderVideo: (ideaId, audioPath) =>
    api.post(`/workflow/render-video/${ideaId}`, null, { params: { audio_path: audioPath } }),
  uploadYoutube: (videoId) => api.post(`/workflow/upload-youtube/${videoId}`),
  getStatus: (channelId) => api.get(`/workflow/status/${channelId}`),
  getLogs: (channelId, params) => api.get(`/workflow/logs/${channelId}`, { params }),
};

export default api;
