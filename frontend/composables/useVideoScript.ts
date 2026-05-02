/**
 * useVideoScript — 视频脚本生成器 API 封装
 *
 * 核心：generate 用 fetch + ReadableStream 解析 SSE 流，
 * 边生成边把累积的JSON文本吐给前端展示。
 *
 * 数据流：
 *   用户输入主题
 *     → POST /generate (fetch with stream:true)
 *     → 持续读取 ReadableStream
 *     → 解析 SSE event/data
 *     → 调 onChunk(text) 让 UI 实时显示
 *     → 收到 done → 调 onDone(id)
 *     → 收到 error → 调 onError(detail, kind)
 */

export interface JimengPrompt {
  subject: string
  scene: string
  motion: string
  camera: string
  mood: string
  style: string
}

export interface ScriptTemplate {
  topic: string
  titles: string[]
  hook: string
  voiceover: string
  estimated_duration: string
  jimeng_prompt: JimengPrompt
  reference_image_guide: string
  hashtags: string[]
  shooting_tips: string
}

export interface VideoScriptListItem {
  id: number
  topic: string
  created_at: string
}

export interface VideoScriptDetail {
  id: number
  topic: string
  template: ScriptTemplate
  model_used: string
  generation_ms: number | null
  created_at: string
}

export interface GenerateCallbacks {
  onChunk: (chunk: string, accumulated: string) => void
  onDone: (id: number, generation_ms: number) => void
  onError: (detail: string, kind: string) => void
}

export const useVideoScript = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase
  const auth = useAuthStore()

  /**
   * 上传音频转文字
   */
  const transcribe = async (audioBlob: Blob): Promise<{ text: string; duration_ms: number }> => {
    const formData = new FormData()
    // Blob 没有 name，必须给一个文件名让后端识别格式
    const ext = audioBlob.type.includes('webm') ? 'webm' : 'wav'
    formData.append('audio', audioBlob, `recording.${ext}`)

    const res = await $fetch<{ text: string; duration_ms: number }>(
      `${baseURL}/video_script/transcribe`,
      {
        method: 'POST',
        body: formData,
        headers: { Authorization: `Bearer ${auth.token}` },
      }
    )
    return res
  }

  /**
   * 流式生成脚本
   * 返回一个 abort 函数，用户可以中断
   */
  const generateStream = (
    topic: string,
    callbacks: GenerateCallbacks,
    referenceHints?: string[]
  ): { abort: () => void } => {
    const controller = new AbortController()

    const run = async () => {
      let accumulated = ''
      try {
        const response = await fetch(`${baseURL}/video_script/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${auth.token}`,
            Accept: 'text/event-stream',
          },
          body: JSON.stringify({ topic, reference_hints: referenceHints }),
          signal: controller.signal,
        })

        if (!response.ok) {
          const errText = await response.text()
          callbacks.onError(errText || `HTTP ${response.status}`, 'http_error')
          return
        }

        if (!response.body) {
          callbacks.onError('浏览器不支持流式响应', 'no_stream')
          return
        }

        const reader = response.body.getReader()
        const decoder = new TextDecoder('utf-8')
        let buffer = ''

        while (true) {
          const { done, value } = await reader.read()
          if (done) break
          buffer += decoder.decode(value, { stream: true })

          // 按 \n\n 切分 SSE 事件
          const events = buffer.split('\n\n')
          buffer = events.pop() || ''  // 最后一个可能不完整，留着

          for (const eventText of events) {
            if (!eventText.trim()) continue
            const lines = eventText.split('\n')
            let eventName = 'message'
            let data = ''
            for (const line of lines) {
              if (line.startsWith('event:')) eventName = line.slice(6).trim()
              else if (line.startsWith('data:')) data += line.slice(5).trim()
            }
            if (!data) continue

            try {
              const parsed = JSON.parse(data)
              if (eventName === 'token') {
                accumulated += parsed.chunk
                callbacks.onChunk(parsed.chunk, accumulated)
              } else if (eventName === 'done') {
                callbacks.onDone(parsed.id, parsed.generation_ms)
              } else if (eventName === 'error') {
                callbacks.onError(parsed.detail, parsed.kind)
              }
            } catch (e) {
              console.error('SSE parse error:', e, data)
            }
          }
        }
      } catch (e: any) {
        if (e.name === 'AbortError') {
          callbacks.onError('已取消', 'aborted')
        } else {
          callbacks.onError(e.message || '网络错误', 'network')
        }
      }
    }

    run()
    return { abort: () => controller.abort() }
  }

  /**
   * 历史列表
   */
  const fetchHistory = async (page: number = 1, pageSize: number = 20) => {
    return await $fetch<{
      items: VideoScriptListItem[]
      total: number
      page: number
      page_size: number
    }>(`${baseURL}/video_script/history?page=${page}&page_size=${pageSize}`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    })
  }

  /**
   * 历史详情
   */
  const fetchDetail = async (id: number): Promise<VideoScriptDetail> => {
    return await $fetch<VideoScriptDetail>(`${baseURL}/video_script/${id}`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    })
  }

  /**
   * 删除
   */
  const deleteScript = async (id: number) => {
    await $fetch(`${baseURL}/video_script/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${auth.token}` },
    })
  }

  return {
    transcribe,
    generateStream,
    fetchHistory,
    fetchDetail,
    deleteScript,
  }
}
