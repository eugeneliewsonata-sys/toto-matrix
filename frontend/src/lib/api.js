import axios from 'axios';

const BACKEND = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND}/api`;

export const api = axios.create({ baseURL: API });

api.interceptors.request.use((cfg) => {
  const t = localStorage.getItem('lottoluxe_token');
  if (t) cfg.headers.Authorization = `Bearer ${t}`;
  return cfg;
});

export const ZODIACS = [
  'Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'
];

export function formatDate(iso) {
  try {
    const d = new Date(iso);
    return d.toLocaleDateString('en-MY', { day:'2-digit', month:'short', year:'numeric' }) + ' · ' +
      d.toLocaleTimeString('en-MY', { hour:'2-digit', minute:'2-digit' });
  } catch { return iso; }
}
