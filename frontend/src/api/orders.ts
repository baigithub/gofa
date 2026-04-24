import { http, unwrap, type ApiResult } from "./index";

export type BackendOrderItem = {
  id: string;
  order_type: "pickup" | "buy" | "errand";
  status: "pending_pay" | "pending_take" | "accepted" | "delivering" | "completed" | "cancelled";
  pickup_address: string | null;
  delivery_address: string | null;
  amount_cents: number;
  created_at: string;
};

export const fetchOrders = async (userId?: string) => {
  const { data } = await http.get<ApiResult<BackendOrderItem[]>>("/orders", {
    params: userId ? { user_id: userId } : undefined,
  });
  return unwrap(data);
};

