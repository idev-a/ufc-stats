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
import snackbar from './snackbar';

const _lastLeft = () => {
  let left =  localStorage.getItem('lastLeft') || 5
  left = Math.min(left, window.innerWidth-360)
  return left
}

export default new Vuex.Store({
  state: {
    barColor: 'rgba(0, 0, 0, .8), rgba(0, 0, 0, .8)',
    barImage: 'https://demos.creative-tim.com/material-dashboard-pro/assets/img/sidebar-1.jpg',
    drawer: null,
    lastLeft: _lastLeft()
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
    SET_LASTLEFT (state, payload) {
      state.lastLeft = Math.min(window.innerWidth-360, payload)
      localStorage.setItem('lastLeft', state.lastLeft)
    }
  },
  actions: {
  },
  modules: { 
    auth,
    password,
    signup,
    snackbar
  },
})
