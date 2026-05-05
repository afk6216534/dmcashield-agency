// Centralized API Configuration
// Uses env var VITE_API_URL for production, Vercel URL for deployed version

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';
const WS_URL = API.replace('https', 'wss').replace('http', 'ws');
const IS_PROD = import.meta.env.PROD;

export { API, WS_URL, IS_PROD };
export default API;