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
    login({ commit }, user) {
      return new Promise((resolve, reject) => {
        const token = user.getId();
        const email = "jane@moveuptoday.org"; // user.getEmail();
        localStorage.setItem("token", token);
        commit("auth_request");
        AXIOS.get("/mentors/email/" + email)
          .then((resp, token) => {
            if (resp.data.name) {
              const user = resp.data.name;
              axios.defaults.headers.common["Authorization"] = token;
              commit("auth_success", { token, user });
              resolve(resp);
            } else {
              localStorage.removeItem("token");
            }
          })
          .catch(err => {
            commit("auth_error");
            localStorage.removeItem("token");
            reject(err);
          });
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
