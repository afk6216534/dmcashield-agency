// Centralized API Configuration
// Uses env var VITE_API_URL for production, localhost for dev

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const WS_URL = API.replace('http', 'ws');
const IS_PROD = import.meta.env.PROD;

export { API, WS_URL, IS_PROD };
export default API;