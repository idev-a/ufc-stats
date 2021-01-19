const getDefaultState = () => {
  return {
    snack: false,
    message: '',
    status: 'success',
    refresh: false
  };
};

export default {
  namespaced: true,
  name: "snackbar",
  state: {
    snack: false,
    message: '',
    status: 'success',
    refresh: false
  },
  getters: {
    snack: state => state.snack,
    message: state => state.message,
    status: state => state.status,
    refresh: state => state.refresh,
  },
  actions: {
    setSnack({commit}, payload) {
      commit('setSnack', payload)
    },
    showSnack({commit}, payload) {
      commit('showSnack', payload)
    }
  },
  mutations: {
    setSnack(state, payload) {
      state.snack = payload.snack
      state.message = payload.message
      state.status = payload.status
    },
    showSnack(state, payload=true) {
      state.snack = payload
    },
    resetState(state) {
      Object.assign(state, getDefaultState());
    }
  },
};