import { createRouter, createWebHistory } from "vue-router";
import { getRole, getToken, type UserRole } from "../core/auth";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/u/login" },
    { path: "/u/login", component: () => import("../views/U01LoginView.vue"), meta: { public: true } },
    {
      path: "/u/home",
      component: () => import("../views/U02HomeView.vue"),
      meta: { requiresAuth: true, role: "user" as UserRole },
    },
    { path: "/r/login", component: () => import("../views/R01RunnerLoginView.vue"), meta: { public: true } },
    {
      path: "/r/hall",
      component: () => import("../views/R02RunnerHallView.vue"),
      meta: { requiresAuth: true, role: "runner" as UserRole },
    },
  ],
});

router.beforeEach((to) => {
  console.info(`[gofer] route=${to.fullPath}`);
  if (to.meta.public) return true;

  const token = getToken();
  const role = getRole();
  const needRole = to.meta.role as UserRole | undefined;

  if (!token) return "/u/login";
  if (needRole && role !== needRole) return role === "runner" ? "/r/hall" : "/u/home";

  return true;
});

export default router;

