import Vue from "vue";
import axios from "axios";
import config from "../config";
import Store from "../store";
import Router from "../router";
import { Cookies } from "quasar";

// Axios config
const frontendUrl = config.build.host + ":" + config.build.port;
const backendUrl = config.build.backendHost + ":" + config.build.backendPort;

Vue.prototype.$axios = axios.create({
  baseURL: backendUrl,
  headers: {
    "Access-Control-Allow-Origin": frontendUrl,
    "Content-Type": "application/json"
  },
  withCredentials: true
});

// set up interceptor to handle expired access tokens
Vue.prototype.$axios.interceptors.response.use(
  function(response) {
    return response;
  },
  function(error) {
    if (error.response.status === 401) {
      // get user with stored token
      this.$axios
        .get("/auth/current-user", null, {
          headers: {
            "X-CSRF-TOKEN": Cookies.get("csrf_refresh_token")
          }
        })
        .then(resp => {
          Store.commit("set_user", resp.data.user);
        })
        .catch(() => {
          // token is invalid
          Store.dispatch("logout").then(Router.push({ path: "/" }));
        });
    } else {
      Router.push({ path: "/" });
    }
  }
);
