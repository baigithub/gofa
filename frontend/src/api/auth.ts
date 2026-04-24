import { http, unwrap, type ApiResult } from "./index";

type LoginPayload = {
  phone: string;
  code: string;
};

type LoginResponse = {
  token: string;
  role: "user" | "runner" | "admin";
  user_id: string;
};

export const sendCode = async (phone: string) => {
  const { data } = await http.post<ApiResult<{ success: boolean }>>("/auth/send-code", {
    phone,
  });
  return unwrap(data);
};

export const login = async (payload: LoginPayload) => {
  const { data } = await http.post<ApiResult<LoginResponse>>("/auth/login", payload);
  const result = unwrap(data);
  return { token: result.token, role: result.role, userId: result.user_id };
};

