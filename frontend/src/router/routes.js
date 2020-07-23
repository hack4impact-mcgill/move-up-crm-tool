const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [{ path: "", component: () => import("pages/Index.vue") }]
  },
  {
    path: "/home",
    component: () => import("layouts/MainLayout.vue"),
    // meta: { requiresAuth: true },
    children: [{ path: "", component: () => import("pages/Dashboard.vue") }]
  },
  {
    path: "/clients",
    component: () => import("layouts/MainLayout.vue"),
    // meta: { requiresAuth: true },
    children: [{ path: "", component: () => import("pages/Clients.vue") }]
  },
  {
    path: "/volunteers",
    component: () => import("layouts/MainLayout.vue"),
    // meta: { requiresAuth: true },
    children: [{ path: "", component: () => import("pages/Volunteers.vue") }]
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
