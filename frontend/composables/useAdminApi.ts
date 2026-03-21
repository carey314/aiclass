import { useAuthStore } from '~/stores/auth'

export const useAdminApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase

  const getHeaders = () => {
    const authStore = useAuthStore()
    return {
      Authorization: `Bearer ${authStore.token}`,
    }
  }

  return {
    get: <T>(path: string) =>
      $fetch<T>(`${baseURL}${path}`, { headers: getHeaders() }),

    post: <T>(path: string, body?: any) =>
      $fetch<T>(`${baseURL}${path}`, {
        method: 'POST',
        body,
        headers: getHeaders(),
      }),

    put: <T>(path: string, body?: any) =>
      $fetch<T>(`${baseURL}${path}`, {
        method: 'PUT',
        body,
        headers: getHeaders(),
      }),

    del: <T>(path: string) =>
      $fetch<T>(`${baseURL}${path}`, {
        method: 'DELETE',
        headers: getHeaders(),
      }),

    upload: <T>(path: string, formData: FormData) =>
      $fetch<T>(`${baseURL}${path}`, {
        method: 'POST',
        body: formData,
        headers: getHeaders(),
      }),
  }
}
