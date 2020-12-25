import Vue from 'vue'
import Vuex from 'vuex'
// import createPersistedState from 'vuex-persistedstate';
import VuexPersistence from 'vuex-persist';
import localForage from 'localforage';

Vue.use(Vuex)

const vuexLocal = new VuexPersistence({
  key: 'issuer-vuex',
  storage: window.localStorage,
  modules: ['auth', 'password', 'signup'],
})

import auth from './auth'
import password from './password';
import signup from './signup';
// import snackbar from './snackbar';

export default new Vuex.Store({
  state: {
    barColor: 'rgba(0, 0, 0, .8), rgba(0, 0, 0, .8)',
    barImage: 'https://demos.creative-tim.com/material-dashboard-pro/assets/img/sidebar-1.jpg',
    drawer: null,
  },
  // plugins: [vuexLocal.plugin],
  mutations: {
    SET_BAR_IMAGE (state, payload) {
      state.barImage = payload
    },
    SET_DRAWER (state, payload) {
      state.drawer = payload
    },
    SET_SCRIM (state, payload) {
      state.barColor = payload
    },
  },
  actions: {
  },
  modules: { 
    auth,
    password,
    signup
  },
})
