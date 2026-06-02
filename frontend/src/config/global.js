const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const WS_URL = import.meta.env.VITE_WS_URL || API.replace('https', 'wss').replace('http', 'ws');

window.API = API;
window.WS_URL = WS_URL;
window.DEPLOYED = import.meta.env.VITE_PROD === 'true';

export { API, WS_URL, DEPLOYED };