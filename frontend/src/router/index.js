import Vue from "vue";
import VueRouter from "vue-router";

import routes from "./routes";
import Store from "../store/index";

Vue.use(VueRouter);

// Axios config
// const frontendUrl = config.build.host + ":" + config.build.port;
// const backendUrl = config.build.backendHost + ":" + config.build.backendPort;

// var AXIOS = axios.create({
//   baseURL: backendUrl,
//   headers: {
//     "Access-Control-Allow-Origin": frontendUrl,
//     "Content-Type": "application/json"
//   }
// });

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default function(/* { store, ssrContext } */) {
  const Router = new VueRouter({
    scrollBehavior: () => ({ x: 0, y: 0 }),
    routes,

    // Leave these as they are and change in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    mode: process.env.VUE_ROUTER_MODE,
    base: process.env.VUE_ROUTER_BASE
  });

  Router.beforeEach((to, _from, next) => {
    let requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    let isAuthorized = Store.state.userExists;

    if (requiresAuth && !isAuthorized) {
      next({
        path: "/",
        query: { redirect: to.fullPath }
      });
    } else {
      next();
    }
  });

  return Router;
}
