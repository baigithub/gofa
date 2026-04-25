import { http, unwrap, type ApiResult } from "./index";

export type UserRoleCode = "user" | "runner" | "admin" | string;
export type UserItem = {
  id: string;
  phone: string;
  nickname: string | null;
  role: UserRoleCode;
  is_enabled: boolean;
  created_at: string;
};
export type RoleItem = {
  id: string;
  code: string;
  name: string;
  description: string | null;
  is_enabled: boolean;
  created_at: string;
  updated_at: string;
};
export type AdminOrderItem = {
  order_id: string;
  order_content: string;
  initiator: string;
  runner: string;
  status: string;
  created_at: string;
  completed_at: string | null;
  required_completed_at: string | null;
};

export type RunnerVerificationItem = {
  id: string;
  user_id: string;
  phone: string;
  student_no: string | null;
  credential_images: string[];
  verification_status: "pending" | "approved" | "rejected" | string;
  rejection_reason: string | null;
  reviewed_by: string | null;
  reviewed_at: string | null;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
};

export const fetchUsers = async (adminUserId: string) => {
  const { data } = await http.get<ApiResult<UserItem[]>>("/admin/users", {
    params: { admin_user_id: adminUserId },
  });
  return unwrap(data);
};

export const setUserRole = async (adminUserId: string, userId: string, role: UserRoleCode) => {
  const { data } = await http.post<ApiResult<{ success: boolean }>>(
    `/admin/users/${encodeURIComponent(userId)}/role`,
    { role },
    { params: { admin_user_id: adminUserId } },
  );
  return unwrap(data);
};

export const setUserEnabled = async (adminUserId: string, userId: string, isEnabled: boolean) => {
  const { data } = await http.post<ApiResult<{ success: boolean }>>(
    `/admin/users/${encodeURIComponent(userId)}/enabled`,
    { is_enabled: isEnabled },
    { params: { admin_user_id: adminUserId } },
  );
  return unwrap(data);
};

export const resetUserPassword = async (adminUserId: string, userId: string) => {
  const { data } = await http.post<ApiResult<{ success: boolean; temp_password: string }>>(
    `/admin/users/${encodeURIComponent(userId)}/reset-password`,
    {},
    { params: { admin_user_id: adminUserId } },
  );
  return unwrap(data);
};

export const fetchAdminOrders = async (adminUserId: string) => {
  const { data } = await http.get<ApiResult<AdminOrderItem[]>>("/admin/orders", {
    params: { admin_user_id: adminUserId },
  });
  return unwrap(data);
};

export const fetchRoles = async (adminUserId: string) => {
  const { data } = await http.get<ApiResult<RoleItem[]>>("/admin/roles", {
    params: { admin_user_id: adminUserId },
  });
  return unwrap(data);
};

export const createRole = async (adminUserId: string, payload: { code: string; name: string; description?: string }) => {
  const { data } = await http.post<ApiResult<RoleItem>>("/admin/roles", payload, {
    params: { admin_user_id: adminUserId },
  });
  return unwrap(data);
};

export const updateRole = async (
  adminUserId: string,
  roleId: string,
  payload: { name: string; description?: string },
) => {
  const { data } = await http.put<ApiResult<RoleItem>>(`/admin/roles/${encodeURIComponent(roleId)}`, payload, {
    params: { admin_user_id: adminUserId },
  });
  return unwrap(data);
};

export const setRoleEnabled = async (adminUserId: string, roleId: string, isEnabled: boolean) => {
  const { data } = await http.post<ApiResult<RoleItem>>(
    `/admin/roles/${encodeURIComponent(roleId)}/enabled`,
    { is_enabled: isEnabled },
    { params: { admin_user_id: adminUserId } },
  );
  return unwrap(data);
};

export const deleteRole = async (adminUserId: string, roleId: string) => {
  const { data } = await http.delete<ApiResult<{ success: boolean }>>(`/admin/roles/${encodeURIComponent(roleId)}`, {
    params: { admin_user_id: adminUserId },
  });
  return unwrap(data);
};

export const fetchRunnerVerifications = async (adminUserId: string) => {
  const { data } = await http.get<ApiResult<RunnerVerificationItem[]>>("/admin/runner-verifications", {
    params: { admin_user_id: adminUserId },
  });
  const items = unwrap(data);
  console.info("[gofer] admin.runner-verifications.response", {
    count: items.length,
    items,
  });
  return items;
};

export const submitRunnerVerification = async (
  payload: { user_id: string; student_no?: string | null; credential_images: string[] },
) => {
  const { data } = await http.post<ApiResult<RunnerVerificationItem>>("/admin/runner-verifications/submit", payload);
  return unwrap(data);
};

export const reviewRunnerVerification = async (
  adminUserId: string,
  profileId: string,
  payload: { approve: boolean; rejection_reason?: string | null },
) => {
  const { data } = await http.post<ApiResult<RunnerVerificationItem>>(
    `/admin/runner-verifications/${encodeURIComponent(profileId)}/review`,
    { ...payload, admin_user_id: adminUserId },
  );
  return unwrap(data);
};

