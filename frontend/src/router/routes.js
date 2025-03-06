const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("src/pages/DasboardPage.vue") },
      { path: "query", component: () => import("pages/QueryPage.vue") },
      {
        path: "documents",
        component: () => import("pages/DocumentsPage.vue"),
      },
      {
        path: "topics",
        component: () => import("pages/TopicsPage.vue"),
      },
      {
        path: "profile",
        component: () => import("pages/ProfilePage.vue"),
      },
    ],
  },
  {
    path: "/login",
    component: () => import("layouts/LoginLayout.vue"),
    children: [{ path: "", component: () => import("pages/LoginPage.vue") }],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
