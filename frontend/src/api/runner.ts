import { http, unwrap, type ApiResult } from "./index";

export type CredentialImageUploadResult = {
  success: boolean;
  path: string;
  url: string;
  filename: string;
};

export type ChatMessageItem = {
  id: string;
  order_id: string;
  sender_user_id: string;
  sender_role: "user" | "runner" | "admin";
  content: string;
  created_at: string;
};

export type ReviewItem = {
  order_id: string;
  user_id: string;
  runner_id: string | null;
  rating: number;
  comment: string;
  created_at: string;
};

export type RunnerDashboardStats = {
  today_earnings_cents: number;
  available_order_count: number;
  verification_status: string;
  is_verified: boolean;
  rejection_reason: string | null;
};

export type RunnerOrderItem = {
  id: string;
  user_id: string;
  runner_id: string | null;
  order_type: "pickup" | "buy" | "errand";
  status: "pending_pay" | "pending_take" | "accepted" | "delivering" | "completed" | "cancelled";
  pickup_address: string | null;
  delivery_address: string | null;
  contact_phone: string;
  remark: string | null;
  amount_cents: number;
  created_at: string;
  updated_at: string;
};

export const fetchRunnerDashboardStats = async (runnerUserId: string) => {
  const { data } = await http.get<ApiResult<RunnerDashboardStats>>(`/runner/stats?runner_user_id=${encodeURIComponent(runnerUserId)}`);
  return unwrap(data);
};

export const uploadCredentialImage = async (file: File) => {
  const form = new FormData();
  form.append("file", file);
  const { data } = await http.post<ApiResult<CredentialImageUploadResult>>("/runner/credential-image", form);
  const result = unwrap(data);
  return {
    ...result,
    url: new URL(result.url, "http://127.0.0.1:8000").toString(),
  };
};

export const submitRunnerVerification = async (payload: {
  user_id: string;
  student_no?: string | null;
  credential_images: string[];
}) => {
  const { data } = await http.post<ApiResult<{ success: boolean; runner_profile_id: string }>>("/runner/verification/submit", payload);
  return unwrap(data);
};

export const fetchOrderChats = async (orderId: string) => {
  const { data } = await http.get<ApiResult<ChatMessageItem[]>>(`/runner/orders/${encodeURIComponent(orderId)}/chats`);
  return unwrap(data);
};

export const sendOrderChat = async (orderId: string, payload: { sender_user_id: string; sender_role: string; content: string }) => {
  const { data } = await http.post<ApiResult<ChatMessageItem>>(
    `/runner/orders/${encodeURIComponent(orderId)}/chats`,
    payload,
  );
  return unwrap(data);
};

export const fetchRunnerHistoryOrders = async (runnerUserId: string) => {
  const { data } = await http.get<ApiResult<RunnerOrderItem[]>>(`/runner/orders/history?runner_user_id=${encodeURIComponent(runnerUserId)}`);
  return unwrap(data);
};

export const fetchHallOrders = async () => {
  const { data } = await http.get<ApiResult<RunnerOrderItem[]>>("/runner/orders/hall");
  return unwrap(data);
};

export const acceptOrder = async (orderId: string, runnerUserId: string) => {
  const { data } = await http.post<ApiResult<{ success: boolean }>>(
    `/runner/orders/${encodeURIComponent(orderId)}/accept?runner_id=${encodeURIComponent(runnerUserId)}`,
  );
  return unwrap(data);
};

export const submitOrderReview = async (orderId: string, payload: { user_id: string; rating: number; comment: string }) => {
  const { data } = await http.post<ApiResult<ReviewItem>>(`/runner/orders/${encodeURIComponent(orderId)}/review`, payload);
  return unwrap(data);
};

export const fetchOrderReview = async (orderId: string) => {
  const { data } = await http.get<ApiResult<ReviewItem | null>>(`/runner/orders/${encodeURIComponent(orderId)}/review`);
  return unwrap(data);
};

