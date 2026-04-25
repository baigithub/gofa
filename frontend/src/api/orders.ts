import { http, unwrap, type ApiResult } from "./index";

export type BackendOrderItem = {
  id: string;
  user_id: string;
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

export type CreateOrderPayload = {
  user_id: string;
  order_type: "pickup" | "buy" | "errand";
  pickup_address?: string | null;
  delivery_address?: string | null;
  contact_phone: string;
  remark?: string | null;
  amount_cents: number;
};

export const fetchOrders = async (userId?: string) => {
  const { data } = await http.get<ApiResult<BackendOrderItem[]>>("/orders", {
    params: userId ? { user_id: userId } : undefined,
  });
  return unwrap(data);
};

export const fetchOrderById = async (orderId: string) => {
  const { data } = await http.get<ApiResult<BackendOrderItem>>(`/orders/${encodeURIComponent(orderId)}`);
  return unwrap(data);
};

export const createOrder = async (payload: CreateOrderPayload) => {
  const { data } = await http.post<ApiResult<BackendOrderItem>>("/orders", payload);
  return unwrap(data);
};

export const createPayment = async (orderId: string) => {
  const { data } = await http.post<ApiResult<{ id: string; order_id: string; status: string }>>("/payments/create", {
    order_id: orderId,
  });
  return unwrap(data);
};

export const mockPaySuccess = async (orderId: string) => {
  const { data } = await http.post<ApiResult<{ success: boolean }>>(`/payments/${encodeURIComponent(orderId)}/mock-success`);
  return unwrap(data);
};

