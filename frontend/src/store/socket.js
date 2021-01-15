import Vue from 'vue'

const initialState = {
 	connect: false,
  message: null
}

const mutations = {
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
  SOCKET_CONNECT (state,  status ) {
    console.log('store', status)
    state.connect = true;
  },
  SOCKET_MESSAGE (state,  message) {
    console.log('store', message)
    state.message = message;
  },
  SOCKET_ONMESSAGE (state, message) {
    console.log(message)
  },
  SOCKET_UFC: (state,  message) => {
    console.log('store', message)
    state.message = message;
  },
  SOCKET_RECONNECT(state, count) {
    console.info(state, count)
  },
  SOCKET_RECONNECT_ERROR(state) {
    state.socket.reconnectError = true;
  },
}
const actions = {
  otherAction: (context, type) => {
    return true;
  },
  socket_ufc: (context, message) => {
    console.log('message', message)
  },
  socket_message: (context, message) => {
    console.log('message', message)
    context.dispatch('newMessage', message);
    context.commit('NEW_MESSAGE_RECEIVED', message);
    if (message.is_important) {
      context.dispatch('alertImportantMessage', message);
    }
  }
}

export default {
  namespaced: true,
  state: initialState,
  actions,
  mutations,
};
