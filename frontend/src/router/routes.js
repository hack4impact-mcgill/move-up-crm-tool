const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("pages/Index.vue") }]
  },
  { path: "/signin", component: () => import("components/SignIn.vue") },
  {
    path: "/protected",
    component: () => import("components/EssentialLink.vue"),
    props: { title: "Protected Page" },
    beforeEnter: (to, from, next) => {
      next("/signin");
      next();
    }
  }
];

// Always leave this as last one
if (process.env.MODE !== "ssr") {
  routes.push({
    path: "*",
    component: () => import("pages/Error404.vue")
  });
}

export default routes;
