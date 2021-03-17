import axios from 'axios';
import { TOKEN_STORAGE_KEY } from '@/store/types'

const CSRF_COOKIE_NAME = 'csrftoken';
const CSRF_HEADER_NAME = 'X-CSRFToken';

const session = axios.create({
  xsrfCookieName: CSRF_COOKIE_NAME,
  xsrfHeaderName: CSRF_HEADER_NAME,
  baseURL: process.env.VUE_APP_BACKEND_URL
})

delete session.defaults.headers.Authorization;

const token = localStorage.getItem(TOKEN_STORAGE_KEY)
// console.log(session.defaults.headers)
if (token && token != 'null') {
  session.defaults.headers.Authorization = `Token ${token}`;
} else {
  delete session.defaults.headers.Authorization;
}

session.interceptors.request.use(function (config) {
    // Do something before request is sent
    // console.log(config)
    return config;
  }, function (error) {
    // Do something with request error
    return Promise.reject(error);
  });

// session.interceptors.response.use(function (response) {
//     // Do something with response data
//     return response;
//   }, function (error) {
//     // Do something with response error
//     return Promise.resolve(error.response);
//   });

export default session;
