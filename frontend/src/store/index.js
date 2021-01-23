import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import { Cookies } from "quasar";

Vue.use(Vuex);

// Axios config
const frontendUrl =
  process.env.NODE_ENV === "development" ? "http://localhost:8080" : "";
const backendUrl =
  process.env.NODE_ENV === "development" ? "http://localhost:5000" : "";

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
    currentUser: {},
    userExists: false
  },
  getters: {
    getSignedIn(state) {
      return state.userExists;
    }
  },
  mutations: {
    auth_request(state) {
      state.status = "loading";
    },
    auth_success(state, authObj) {
      state.status = "success";
      state.currentUser = authObj.user;
      state.userExists = true;
    },
    auth_error(state) {
      state.status = "error";
    },
    logout(state) {
      state.status = "";
      state.currentUser = {};
      state.userExists = false;
    },
    set_user(state, user) {
      state.currentUser = user;
      state.userExists = true;
    }
  },
  actions: {
    login({ commit }, loginBody) {
      return new Promise((resolve, reject) => {
        commit("auth_request");
        AXIOS.post(
          "/auth/login",
          { email: loginBody.email, token: loginBody.token },
          { withCredentials: true }
        )
          .then(resp => {
            const user = resp.data.user;
            commit("auth_success", { user });
            resolve(resp);
          })
          .catch(err => {
            commit("auth_error");
            reject(err);
          });
      });
    },
    logout({ commit }) {
      return new Promise((resolve, reject) => {
        AXIOS.post("/auth/logout", null, {
          headers: {
            "X-CSRF-TOKEN": Cookies.get("csrf_access_token")
          },
          withCredentials: true
        })
          .then(resp => {
            commit("logout");
            resolve(resp);
          })
          .catch(err => {
            reject(err);
          });
      });
    },
    setUser({ commit }, user) {
      commit("set_user", user);
    }
  },
  modules: {},

  // enable strict mode (adds overhead!)
  // for dev mode only
  strict: process.env.DEV
});

export default Store;
