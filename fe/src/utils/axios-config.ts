import axios from 'axios';

// Create axios instance with default config
const instance = axios.create({
  baseURL: 'http://192.168.0.179:5000',
  timeout: 10000, // 10 seconds
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add request interceptor if needed (optional)
instance.interceptors.request.use(
  (config) => {
    // You could add auth tokens here if needed
    // config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor if needed (optional)
instance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle errors globally
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default instance;