const getDefaultState = () => {
  return {};
};

const state = getDefaultState();
export default {
  namespaced: true,
  name: "snackbar",
  state: {
    snack: {}
  },
  mutations: {
    setSnack(state, showSnack) {
      state.snack = { ...showSnack };
    },
    resetState(state) {
      Object.assign(state, getDefaultState());
    }
  },
};