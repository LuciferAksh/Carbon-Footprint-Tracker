import { describe, it, expect, vi, beforeEach } from 'vitest';
import { api, ApiRequestError } from '../lib/api';

vi.mock('../lib/firebase', () => ({
  auth: {
    currentUser: {
      getIdToken: vi.fn().mockResolvedValue('test-token'),
    },
  },
}));

describe('api client', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('should make GET requests with token injection', async () => {
    const mockResponse = { data: 'test-data' };
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => mockResponse,
    });
    globalThis.fetch = mockFetch;

    const res = await api.get('/test-endpoint');
    expect(res.data).toEqual(mockResponse);
    expect(mockFetch).toHaveBeenCalledWith(
      '/api/v1/test-endpoint',
      expect.objectContaining({
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer test-token',
        },
      }),
    );
  });

  it('should handle request errors correctly', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 400,
      json: async () => ({ message: 'Bad request' }),
    });
    globalThis.fetch = mockFetch;

    await expect(api.get('/error-endpoint')).rejects.toThrow(ApiRequestError);
  });
});
