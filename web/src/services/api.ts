const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1';

export const getAuthToken = (): string | null => {
  return localStorage.getItem('coopconnect_access_token');
};

export const setAuthToken = (token: string) => {
  localStorage.setItem('coopconnect_access_token', token);
};

export const clearAuthToken = () => {
  localStorage.removeItem('coopconnect_access_token');
  localStorage.removeItem('coopconnect_user');
};

export const apiFetch = async (endpoint: string, options: RequestInit = {}) => {
  const token = getAuthToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {})
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data?.error?.message || data?.detail || 'API request failed');
  }

  return data;
};
