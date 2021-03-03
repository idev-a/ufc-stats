import auth from '../api/auth';
import session from '../api/session';
import router from '../router'

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
  token: localStorage.getItem('TOKEN_STORAGE_KEY'),
  selectedUserId: null,
  loading: false,
  profile: {}
};

const getters = {
  launchLogin: state => state.launchLogin,
  isAuthenticated: state => !!state.token && state.token != 'null',
  authUser: state => state.authUser,
  selectedUserId: state => state.selectedUserId,
};

const actions = {
  login({ commit, dispatch }, { username, password }) {
    commit(LOGIN_BEGIN);
    return auth.login(username, password)
      .then(({ data }) => {
        return dispatch('afterLogin', { data })
      })
      .catch((err) => commit(LOGIN_FAILURE, err));
  },
  twitterLogin({ commit }) {
    commit(LOGIN_BEGIN);
    return auth.twitterRequestToken()
      .then(({data}) => {
        commit(LOGIN_SUCCESS)
        window.location.href = data.twitter_redirect_url
        localStorage.setItem('return_url', window.location.href)
      })
      .catch((err) => commit(LOGIN_FAILURE, err))
  },
  twitterCallback({ commit, dispatch }, {oauth_token, oauth_verifier}) {
    commit(LOGIN_BEGIN);
    const url = `auth/twitter/callback/?oauth_token=${oauth_token}&oauth_verifier=${oauth_verifier}`
    auth.twitterCallback(url)
      .then(({ data }) => {
        dispatch('afterLogin', { data, popup:true })
      })
      .catch((err) => {
        commit(LOGIN_FAILURE, err)
        commit('showLoginDlg', false)
      })
  },
  afterLogin ({ commit }, { data, popup }) {
    commit(SET_TOKEN, data.key)

    return auth.getAccountDetails()
    .then(({ data }) => {
      commit(SET_AUTH_USER, data)

      commit(LOGIN_SUCCESS)

      commit('showLoginDlg', false)
      // return url
      if (localStorage.getItem('returnUrl')) {
        router.push({path: localStorage.getItem('returnUrl')})
      }

      // if (popup) {
      //   if (window.opener) {
      //     window.opener.location.href = '/'
      //     window.close('','_parent','')
      //   }
      //   const return_url = localStorage.getItem('return_url')
      //   window.location.href = return_url || '/'
      // }

      // check if user already took part in this contest
      // auth.checkAlreadyTaken(data.pk)
      // .then(({data}) => {
      // })
    })
  },
  updateUser({ commit }, payload) {
    commit(LOGIN_BEGIN);
    auth.updateAccount(payload)
      .then(({data}) => {
        commit(SET_AUTH_USER, data)
        commit(LOGIN_SUCCESS)
      })
      .catch((err) => commit(LOGIN_FAILURE, err));
  },
  loadProfile({ commit, state }, payload) {
    commit('setLoading', true)
    commit('setUserId', payload)
    auth.loadProfile(payload)
      .then(({data}) => {
        commit('setProfile', data)
        commit('setLoading', false)
      })
  },
  logout({ commit }) {
    localStorage.setItem('returnUrl', '')
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
  [LOGIN_FAILURE](state, error) {
    let errorMsg = ''
    for(let err in error.response.data) {
      if (error.response.data[err].length) {
        errorMsg += error.response.data[err].join('') + '\n'
      }
    }
    state.authenticating = false;
    state.error = errorMsg;
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
    if (token && token != 'null') {
      localStorage.setItem(TOKEN_STORAGE_KEY, token);
      session.defaults.headers.Authorization = `Token ${token}`;
      state.token = token 
    }
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
    localStorage.removeItem('authUser');
    delete session.defaults.headers.Authorization;
    state.token = null
    window.location.href = '/'
  },
  showLoginDlg(state, payload=true) {
    state.launchLogin = payload
  },
  setUserId(state, payload) {
    state.selectedUserId = payload
  },
  setLoading(state, payload=true) {
    state.loading = payload
  },
  setProfile(state, payload) {
    state.profile = payload
  }
};

export default {
  namespaced: true,
  state: initialState,
  getters,
  actions,
  mutations,
};
