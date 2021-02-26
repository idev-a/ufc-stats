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
  name: "game",
  state: {
    selectedContestId: '',
  },
  getters: {
    selectedContestId: state => state.selectedContestId,
  },
  actions: {
    setContestId({commit}, payload) {
      commit('setSnack', payload)
    },
  },
  mutations: {
    setContestId(state, payload) {
      state.selectedContestId = payload
    },
  },
};