// Centralized API Configuration
// Uses env var VITE_API_URL, falls back dynamically depending on environment

const API = import.meta.env.VITE_API_URL || 
  (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000'
    : 'https://dmcashield-agency.vercel.app');

const WS_URL = API.replace(/^http/, 'ws');
const IS_PROD = import.meta.env.PROD;

export { API, WS_URL, IS_PROD };
export default API;