import axios from 'axios';

const state = {
  status: '',
};

const getters = {
  authStatus: state => state.status,
};

const actions = {
  async register({ commit }, user) {
    commit('auth_request');
    try {
      await axios.post('/register', user);
      commit('auth_success');
    } catch (err) {
      commit('auth_error', err);
    }
  },
  async login({ commit }, user) {
    commit('auth_request');
    try {
      await axios.post('/login', user);
      commit('auth_success');
    } catch (err) {
      commit('auth_error', err);
    }
  },
};

const mutations = {
  auth_request(state) {
    state.status = 'loading';
  },
  auth_success(state) {
    state.status = 'success';
  },
  auth_error(state) {
    state.status = 'error';
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
