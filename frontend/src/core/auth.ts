export type UserRole = "user" | "runner" | "admin";

const TOKEN_KEY = "gofer_token";
const ROLE_KEY = "gofer_role";
const USER_ID_KEY = "gofer_user_id";
const USER_PHONE_KEY = "gofer_user_phone";

export const getToken = () => localStorage.getItem(TOKEN_KEY);

export const getRole = () => localStorage.getItem(ROLE_KEY) as UserRole | null;

export const getUserId = () => localStorage.getItem(USER_ID_KEY);

export const getUserPhone = () => localStorage.getItem(USER_PHONE_KEY);

export const setAuth = (role: UserRole, token = "mock-token", userId?: string, phone?: string) => {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(ROLE_KEY, role);
  if (userId) localStorage.setItem(USER_ID_KEY, userId);
  else localStorage.removeItem(USER_ID_KEY);
  if (phone) localStorage.setItem(USER_PHONE_KEY, phone);
  else localStorage.removeItem(USER_PHONE_KEY);
};

export const clearAuth = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(ROLE_KEY);
  localStorage.removeItem(USER_ID_KEY);
  localStorage.removeItem(USER_PHONE_KEY);
};

