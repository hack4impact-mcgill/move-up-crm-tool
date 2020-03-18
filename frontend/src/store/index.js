import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

// Axios config
const frontendUrl = "http://127.0.0.1:8080/";
const backendUrl = "http://127.0.0.1:5000";

var AXIOS = axios.create({
  baseURL: backendUrl,
  headers: {
    "Access-Control-Allow-Origin": frontendUrl,
    "Content-Type": "application/json"
  }
});

const Store = new Vuex.Store({
  state: {
    status: "",
    token: localStorage.getItem("token") || "",
    currentUser: {},
    userExists: false
  },
  mutations: {
    auth_request(state) {
      state.status = "loading";
    },
    auth_success(state, authObj) {
      state.status = "success";
      state.token = authObj.token;
      state.currentUser = authObj.user;
      state.userExists = true;
    },
    auth_error(state) {
      state.status = "error";
    },
    logout(state) {
      state.status = "";
      state.token = "";
      state.currentUser = {};
      state.userExists = false;
    }
  },
  actions: {
    async login({ commit }, user) {
      const token = user.getId();
      const email = user.getEmail();
      commit("auth_request");
      await AXIOS.get("/mentors/email/" + email).then(resp => {
        if (resp.data.name) {
          user = resp.data.name;
          localStorage.setItem("token", token);
          axios.defaults.headers.common["Authorization"] = token;
          commit("auth_success", { token, user });
          return;
        } else {
          localStorage.removeItem("token");
          commit("auth_error");
          return;
        }
      });
    },
    logout({ commit }) {
      return new Promise(resolve => {
        commit("logout");
        localStorage.removeItem("token");
        delete axios.defaults.headers.common["Authorization"];
        resolve();
      });
    }
  },
  modules: {},

  // enable strict mode (adds overhead!)
  // for dev mode only
  strict: process.env.DEV
});

export default Store;
