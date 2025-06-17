import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health check
  healthCheck: () => api.get('/health'),
  
  // Get EEG types
  getEEGTypes: () => api.get('/eeg/types'),
  
  // Get ECG types
  getECGTypes: () => api.get('/ecg/types'),
  
  // Generate EEG
  generateEEG: (data) => api.post('/generate/eeg', data),
  
  // Generate ECG
  generateECG: (data) => api.post('/generate/ecg', data),
  
  // Download files
  downloadFile: (sessionId, fileType) => 
    api.get(`/download/${sessionId}/${fileType}`, { responseType: 'blob' }),
  
  // Get session files
  getSessionFiles: (sessionId) => api.get(`/session/${sessionId}/files`),
};

export default api; 