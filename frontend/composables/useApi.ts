export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase

  return {
    get: <T>(path: string) =>
      $fetch<T>(`${baseURL}${path}`),

    post: <T>(path: string, body?: any, token?: string) =>
      $fetch<T>(`${baseURL}${path}`, {
        method: 'POST',
        body,
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      }),

    put: <T>(path: string, body?: any, token?: string) =>
      $fetch<T>(`${baseURL}${path}`, {
        method: 'PUT',
        body,
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      }),

    del: <T>(path: string, token?: string) =>
      $fetch<T>(`${baseURL}${path}`, {
        method: 'DELETE',
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      }),

    upload: <T>(path: string, formData: FormData, token?: string) =>
      $fetch<T>(`${baseURL}${path}`, {
        method: 'POST',
        body: formData,
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      }),
  }
}
