const routes = [
  {
    path: "/",
    meta: { requiresAuth: false },
    component: () => import("pages/SignInPage.vue"),
  },
  {
    path: "/home",
    component: () => import("layouts/MainLayout.vue"),
    meta: { requiresAuth: true },
    children: [{ path: "", component: () => import("pages/Dashboard.vue") }]
  },
  {
    path: "/clients",
    component: () => import("layouts/MainLayout.vue"),
    meta: { requiresAuth: true },
    children: [{ path: "", component: () => import("pages/Clients.vue") }]
  },
  {
    path: "/donors",
    component: () => import("layouts/MainLayout.vue"),
    meta: { requiresAuth: true },
    children: [{ path: "", component: () => import("pages/Donors.vue") }]
  },
  {
    path: "/volunteers",
    component: () => import("layouts/MainLayout.vue"),
    meta: { requiresAuth: true },
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
