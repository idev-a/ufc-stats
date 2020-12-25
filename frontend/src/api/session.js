import axios from 'axios';
import { TOKEN_STORAGE_KEY } from '@/store/types'

const CSRF_COOKIE_NAME = 'csrftoken';
const CSRF_HEADER_NAME = 'X-CSRFToken';

const session = axios.create({
  xsrfCookieName: CSRF_COOKIE_NAME,
  xsrfHeaderName: CSRF_HEADER_NAME,
  baseURL: process.env.VUE_APP_BACKEND_URL
});

const token = localStorage.getItem(TOKEN_STORAGE_KEY)
// console.log(session.defaults.headers)
if (token && token != 'null') {
	session.defaults.headers.Authorization = `Token ${token}`;
} else {
	delete session.defaults.headers.Authorization;
}

export default session;
