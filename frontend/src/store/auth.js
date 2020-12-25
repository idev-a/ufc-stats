import auth from '../api/auth';
import session from '../api/session';
import {
  LOGIN_BEGIN,
  LOGIN_FAILURE,
  LOGIN_SUCCESS,
  LOGOUT,
  REMOVE_TOKEN,
  SET_TOKEN,
  TOKEN_STORAGE_KEY,
  SET_AUTH_USER,
  SET_USER_CONTEST_STATUS
} from './types';

const isProduction = process.env.NODE_ENV === 'production';

const getAuthUser = () => {
  let user = {}
  try {
    user = JSON.parse(localStorage.getItem('authUser'))
  } catch (e) {}
  return user
}

const initialState = {
  launchLogin: false,
  authenticating: false,
  authUser: getAuthUser(),
  userContestStatus: false,
  error: false,
  token: null,
};

const getters = {
  launchLogin: state => state.launchLogin,
  isAuthenticated: state => !!state.token && state.token != 'null',
};

const actions = {
  login({ commit }, { username, password }) {
    commit(LOGIN_BEGIN);
    return auth.login(username, password)
      .then(({ data }) => {
        commit(SET_TOKEN, data.key)

        auth.getAccountDetails()
          .then(({ data }) => {
            commit(SET_AUTH_USER, data)

            // check if user already took part in this contest
            auth.checkAlreadyTaken(data.pk)
            .then(({data}) => {
              commit(SET_USER_CONTEST_STATUS, data)
              commit(LOGIN_SUCCESS)
            })
          })
      })
      .catch(() => commit(LOGIN_FAILURE));
  },
  logout({ commit }) {
    return auth.logout()
      .then(() => commit(LOGOUT))
      .finally(() => commit(REMOVE_TOKEN));
  },
  initialize({ commit }) {
    const token = localStorage.getItem(TOKEN_STORAGE_KEY);

    // if (isProduction && token) {
    //   commit(REMOVE_TOKEN);
    // }
    commit(SET_TOKEN, token);
  },
};

const mutations = {
  [LOGIN_BEGIN](state) {
    state.authenticating = true;
    state.error = false;
  },
  [LOGIN_FAILURE](state) {
    state.authenticating = false;
    state.error = true;
  },
  [LOGIN_SUCCESS](state) {
    state.authenticating = false;
    state.error = false;
  },
  [LOGOUT](state) {
    state.authenticating = false;
    state.error = false;
  },
  [SET_TOKEN](state, token) {
    localStorage.setItem(TOKEN_STORAGE_KEY, token);
    session.defaults.headers.Authorization = `Token ${token}`;
    state.token = token 
  },
  [SET_AUTH_USER] (state, user) {
    localStorage.setItem('authUser', JSON.stringify(user))
    state.authUser = Object.assign({}, user)
  },
  [SET_USER_CONTEST_STATUS] (state, data) {
    state.userContestStatus = data.status
  },
  [REMOVE_TOKEN](state) {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    delete session.defaults.headers.Authorization;
    state.token = null
    window.location.href = '/'
  },
  showLoginDlg(state, payload=true) {
    state.launchLogin = payload
  }
};

export default {
  namespaced: true,
  state: initialState,
  getters,
  actions,
  mutations,
};
