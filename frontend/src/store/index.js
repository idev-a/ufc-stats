import Vue from 'vue'
import Vuex from 'vuex'
import moment from 'moment'

Vue.use(Vuex)

import auth from './auth'
import password from './password';
import signup from './signup';
import snackbar from './snackbar';
import chat from './chat';
import game from './game';
// import socket from './socket';

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
    lastLeft: _lastLeft(),
    socket: {},
    event: {},
    notifications: [],
    countdown: null
  },
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
    },
    SOCKET_ONOPEN (state, event)  {
      Vue.prototype.$socket = event.currentTarget
      state.socket.isConnected = true
    },
    SOCKET_ONCLOSE (state, event)  {
      state.socket.isConnected = false
    },
    SOCKET_ONERROR (state, event)  {
      console.error(state, event)
    },
    // default handler called for all methods
    SOCKET_ONMESSAGE (state, message)  {
      state.socket.message = message
      if (message.type == 'test-notify') {
        console.log(message)
      }
      else if (message.type == 'chat_message') {
        
      } else {
        if (message) {
          if (message.event) {
            state.event = {
             ...state.event,
             ...message.event
            }
          }
          if (message.refresh) {
            snackbar.state.refresh = true
          }
          snackbar.state.snack = true
          snackbar.state.status = 'red lighten-1'
          snackbar.state.message = message.message

          state.notifications.push({
            msg: message.message,
            time: moment().format('mm:ss')
          })
        }
      }

    },
    // mutations for reconnect methods
    SOCKET_RECONNECT(state, count) {
      console.info('--- reconnect')
    },
    SOCKET_RECONNECT_ERROR(state) {
      state.socket.reconnectError = true;
    },
    SET_EVENT (state, payload) {
      state.event = payload
    },
    UPDATE_COUNTDOWN(state, payload) {
      state.countdown = payload
    }
  },
  actions: {
  },
  modules: { 
    auth,
    password,
    signup,
    snackbar,
    chat,
    game
  },
})
