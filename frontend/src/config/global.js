const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';
const WS_URL = API.replace('https', 'wss').replace('http', 'ws');
export { API, WS_URL };
export default API;