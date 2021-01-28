import auth from '../api/auth';
import session from '../api/session';

import {
  ACTIVATION_BEGIN,
  ACTIVATION_CLEAR,
  ACTIVATION_FAILURE,
  ACTIVATION_SUCCESS,
  REGISTRATION_BEGIN,
  REGISTRATION_CLEAR,
  REGISTRATION_FAILURE,
  REGISTRATION_SUCCESS,
  TOKEN_STORAGE_KEY,
} from './types';

export default {
  namespaced: true,
  state: {
    activationCompleted: false,
    activationError: false,
    activationLoading: false,
    registrationCompleted: false,
    registrationError: '',
    registrationLoading: false,
    launchRegister: false
  },
  getters: {
    launchRegister: state => state.launchRegister,
  },
  actions: {
    createAccount({ commit }, payload) {
      commit(REGISTRATION_BEGIN);
      return auth.createAccount(payload)
        .then(({data}) => commit(REGISTRATION_SUCCESS, data.key))
        .catch((err) => commit(REGISTRATION_FAILURE, err));
    },
    activateAccount({ commit }, { key }) {
      commit(ACTIVATION_BEGIN);
      return auth.verifyAccountEmail(key)
        .then(() => commit(ACTIVATION_SUCCESS))
        .catch(() => commit(ACTIVATION_FAILURE));
    },
    clearRegistrationStatus({ commit }) {
      commit(REGISTRATION_CLEAR);
    },
    clearActivationStatus({ commit }) {
      commit(ACTIVATION_CLEAR);
    },
    referralCallback({ rootState, commit, dispatch, state }, {id}) {
      // show signup dialog
      if (!!rootState.auth.token && rootState.auth.token != 'null') {
        window.location.href = '/'
      } else {
        state.launchRegister = true
      }
    },
  },
  mutations: {
    [ACTIVATION_BEGIN](state) {
      state.activationLoading = true;
    },
    [ACTIVATION_CLEAR](state) {
      state.activationCompleted = false;
      state.activationError = false;
      state.activationLoading = false;
    },
    [ACTIVATION_FAILURE](state) {
      state.activationError = true;
      state.activationLoading = false;
    },
    [ACTIVATION_SUCCESS](state) {
      state.activationCompleted = true;
      state.activationError = false;
      state.activationLoading = false;
    },
    [REGISTRATION_BEGIN](state) {
      state.registrationLoading = true;
    },
    [REGISTRATION_CLEAR](state) {
      state.registrationCompleted = false;
      state.registrationError = '';
      state.registrationLoading = false;
    },
    [REGISTRATION_FAILURE](state, error) {
      let errorMsg = ''
      for(let err in error.response.data) {
        if (error.response.data[err].length) {
          errorMsg += error.response.data[err].join('') + '\n'
        }
      }
      state.registrationError = errorMsg;
      state.registrationLoading = false;
    },
    [REGISTRATION_SUCCESS](state, token) {
      state.registrationCompleted = true;
      state.registrationError = '';
      state.registrationLoading = false;
      state.launchRegister = false;

      localStorage.setItem(TOKEN_STORAGE_KEY, token);
      session.defaults.headers.Authorization = `Token ${token}`;
    },
    showRegisterDlg(state, payload=true) {
      state.launchRegister = payload
    }
  },
};
