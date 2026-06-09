/**
 * @fileoverview API client with Firebase ID token injection.
 * All requests to the backend automatically include the Authorization header.
 */
import { auth } from './firebase';

/** Base URL for API requests */
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/** Response wrapper for API calls */
interface ApiResponse<T> {
  data: T;
  status: number;
}

/** Error response from the API */
interface ApiError {
  message: string;
  status: number;
  details?: Record<string, unknown>;
}

/**
 * Custom error class for API errors
 */
export class ApiRequestError extends Error {
  public status: number;
  public details?: Record<string, unknown>;

  constructor(message: string, status: number, details?: Record<string, unknown>) {
    super(message);
    this.name = 'ApiRequestError';
    this.status = status;
    this.details = details;
  }
}

/**
 * Get the current user's Firebase ID token.
 * @returns The ID token string, or null if not authenticated.
 */
async function getIdToken(): Promise<string | null> {
  const user = auth.currentUser;
  if (!user) return null;
  try {
    return await user.getIdToken();
  } catch {
    return null;
  }
}

/**
 * Build request headers with optional auth token.
 * @returns Headers object with Content-Type and optional Authorization.
 */
async function buildHeaders(): Promise<Record<string, string>> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  const token = await getIdToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  return headers;
}

/**
 * Make an API request with automatic auth token injection.
 * @param endpoint - API endpoint path (e.g., '/activities')
 * @param options - Fetch options
 * @returns Parsed response data
 */
async function request<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<ApiResponse<T>> {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers = await buildHeaders();

  const response = await fetch(url, {
    ...options,
    headers: {
      ...headers,
      ...(options.headers as Record<string, string> | undefined),
    },
  });

  if (!response.ok) {
    let errorData: ApiError | undefined;
    try {
      errorData = (await response.json()) as ApiError;
    } catch {
      // Response body may not be JSON
    }

    throw new ApiRequestError(
      errorData?.message || `API request failed with status ${response.status}`,
      response.status,
      errorData?.details,
    );
  }

  const data = (await response.json()) as T;
  return { data, status: response.status };
}

/** API client with convenience methods */
export const api = {
  /**
   * GET request
   * @param endpoint - API endpoint path
   */
  get: <T>(endpoint: string) => request<T>(endpoint, { method: 'GET' }),

  /**
   * POST request
   * @param endpoint - API endpoint path
   * @param body - Request body
   */
  post: <T>(endpoint: string, body: unknown) =>
    request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  /**
   * PUT request
   * @param endpoint - API endpoint path
   * @param body - Request body
   */
  put: <T>(endpoint: string, body: unknown) =>
    request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body),
    }),

  /**
   * PATCH request
   * @param endpoint - API endpoint path
   * @param body - Request body
   */
  patch: <T>(endpoint: string, body: unknown) =>
    request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(body),
    }),

  /**
   * DELETE request
   * @param endpoint - API endpoint path
   */
  delete: <T>(endpoint: string) => request<T>(endpoint, { method: 'DELETE' }),
} as const;
