import axios, { AxiosError } from "axios";
import { clearAuth, getToken } from "../core/auth";

export const http = axios.create({
  baseURL: "/api/v1",
  timeout: 10000,
});

export class ApiError extends Error {
  code: string;
  status?: number;

  constructor(message: string, code = "UNKNOWN_ERROR", status?: number) {
    super(message);
    this.name = "ApiError";
    this.code = code;
    this.status = status;
  }
}

http.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

http.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ code?: string; message?: string }>) => {
    if (!error.response) {
      return Promise.reject(new ApiError("网络异常，请稍后重试", "NETWORK_ERROR"));
    }

    const { status, data } = error.response;
    if (status === 401) {
      clearAuth();
      return Promise.reject(new ApiError("登录已过期，请重新登录", "UNAUTHORIZED", status));
    }

    const message = data?.message || "请求失败，请稍后重试";
    const code = data?.code || "REQUEST_FAILED";
    return Promise.reject(new ApiError(message, code, status));
  },
);

export type ApiResult<T> = {
  code: number;
  message: string;
  data: T;
};

export const unwrap = <T>(result: ApiResult<T>) => result.data;
