export type UserRole = "user" | "runner" | "admin";

const TOKEN_KEY = "gofer_token";
const ROLE_KEY = "gofer_role";
const USER_ID_KEY = "gofer_user_id";

export const getToken = () => localStorage.getItem(TOKEN_KEY);

export const getRole = () => localStorage.getItem(ROLE_KEY) as UserRole | null;

export const getUserId = () => localStorage.getItem(USER_ID_KEY);

export const setAuth = (role: UserRole, token = "mock-token", userId?: string) => {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(ROLE_KEY, role);
  if (userId) localStorage.setItem(USER_ID_KEY, userId);
  else localStorage.removeItem(USER_ID_KEY);
};

export const clearAuth = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(ROLE_KEY);
  localStorage.removeItem(USER_ID_KEY);
};

