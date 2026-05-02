<script setup lang="ts">
/**
 * VoiceRecorder — 按住录音组件
 *
 * 交互逻辑（仿微信"按住说话"）：
 *   touchstart/mousedown → 开始录音
 *   touchmove → 显示"上滑取消"提示
 *   touchend/mouseup → 停止录音
 *     如果手指上滑出按钮 → 取消
 *     否则 → 上传转文字
 *
 * 浏览器兼容：
 *   - MediaRecorder API（iOS 14.3+, Android Chrome）
 *   - 不支持时降级提示
 *
 * 状态机：
 *   idle → recording → uploading → idle
 *           ↓
 *         cancelled → idle
 */
import { ref, onUnmounted } from 'vue'

const emit = defineEmits<{
  /** 转写完成，返回识别出的文字 */
  (e: 'transcribed', text: string): void
  /** 录音中或转写中的状态变化 */
  (e: 'state', state: 'idle' | 'recording' | 'uploading'): void
  /** 错误（用户拒绝权限/不支持/识别失败） */
  (e: 'error', message: string): void
}>()

const state = ref<'idle' | 'recording' | 'uploading'>('idle')
const willCancel = ref(false)  // true时松手会取消
const recordSeconds = ref(0)
const errorMessage = ref('')

let mediaStream: MediaStream | null = null
let mediaRecorder: MediaRecorder | null = null
let chunks: Blob[] = []
let timerHandle: ReturnType<typeof setInterval> | null = null
let touchStartY = 0

const MAX_SECONDS = 30  // 最长录音时长

const isSupported = (() => {
  if (typeof window === 'undefined') return true  // SSR时假定支持
  return !!(
    navigator.mediaDevices &&
    typeof navigator.mediaDevices.getUserMedia === 'function' &&
    typeof window.MediaRecorder === 'function'
  )
})()

const updateState = (s: typeof state.value) => {
  state.value = s
  emit('state', s)
}

const startRecording = async (e: TouchEvent | MouseEvent) => {
  if (state.value !== 'idle') return
  if (!isSupported) {
    errorMessage.value = '此浏览器不支持录音，请在Chrome/Safari打开'
    emit('error', errorMessage.value)
    return
  }

  // 记录起始Y坐标（判断上滑取消）
  if ('touches' in e) touchStartY = e.touches[0].clientY
  else touchStartY = e.clientY

  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true })
  } catch (err: any) {
    errorMessage.value = '请允许使用麦克风（地址栏左侧的小图标）'
    emit('error', errorMessage.value)
    return
  }

  // 选择最佳格式
  const mimeType =
    MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
      ? 'audio/webm;codecs=opus'
      : MediaRecorder.isTypeSupported('audio/webm')
      ? 'audio/webm'
      : MediaRecorder.isTypeSupported('audio/mp4')
      ? 'audio/mp4'
      : ''

  try {
    mediaRecorder = mimeType
      ? new MediaRecorder(mediaStream, { mimeType })
      : new MediaRecorder(mediaStream)
  } catch (err: any) {
    errorMessage.value = '录音器初始化失败'
    emit('error', errorMessage.value)
    cleanupStream()
    return
  }

  chunks = []
  mediaRecorder.ondataavailable = (ev) => {
    if (ev.data.size > 0) chunks.push(ev.data)
  }
  mediaRecorder.onstop = handleRecorderStop

  mediaRecorder.start()
  updateState('recording')
  recordSeconds.value = 0
  willCancel.value = false

  // 计时
  timerHandle = setInterval(() => {
    recordSeconds.value++
    if (recordSeconds.value >= MAX_SECONDS) {
      stopRecording(false)  // 自动结束
    }
  }, 1000)
}

const stopRecording = (cancel: boolean) => {
  if (state.value !== 'recording') return
  willCancel.value = cancel

  if (timerHandle) {
    clearInterval(timerHandle)
    timerHandle = null
  }

  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop()
  }
}

const handleRecorderStop = async () => {
  cleanupStream()

  if (willCancel.value || chunks.length === 0) {
    // 取消或空录音
    updateState('idle')
    return
  }

  // 录音<1秒视为误触
  if (recordSeconds.value < 1) {
    emit('error', '说话太短了，再试一次')
    updateState('idle')
    return
  }

  // 上传转写
  const blob = new Blob(chunks, { type: mediaRecorder?.mimeType || 'audio/webm' })
  updateState('uploading')

  try {
    const { transcribe } = useVideoScript()
    const result = await transcribe(blob)
    if (result.text) {
      emit('transcribed', result.text)
    } else {
      emit('error', '没听清，再试一次')
    }
  } catch (err: any) {
    emit('error', err?.data?.detail || err?.message || '识别失败')
  }
  updateState('idle')
}

const cleanupStream = () => {
  if (mediaStream) {
    mediaStream.getTracks().forEach((t) => t.stop())
    mediaStream = null
  }
}

// 触屏事件
const onTouchStart = (e: TouchEvent) => {
  e.preventDefault()
  startRecording(e)
}

const onTouchMove = (e: TouchEvent) => {
  if (state.value !== 'recording') return
  const y = e.touches[0].clientY
  // 上滑超过50px视为要取消
  willCancel.value = touchStartY - y > 50
}

const onTouchEnd = (e: TouchEvent) => {
  e.preventDefault()
  stopRecording(willCancel.value)
}

// 鼠标事件（PC用）
const onMouseDown = (e: MouseEvent) => startRecording(e)
const onMouseUp = () => stopRecording(false)
const onMouseLeave = () => {
  if (state.value === 'recording') stopRecording(true)  // 离开按钮取消
}

onUnmounted(() => {
  cleanupStream()
  if (timerHandle) clearInterval(timerHandle)
})
</script>

<template>
  <div class="flex flex-col items-center w-full">
    <!-- 录音中提示 -->
    <div
      v-if="state === 'recording'"
      class="text-center mb-4 text-base"
      :class="willCancel ? 'text-red-500' : 'text-gray-700'"
    >
      <div class="text-2xl font-bold mb-1">
        {{ willCancel ? '松开取消' : '正在听...' }}
      </div>
      <div class="text-sm text-gray-500">
        {{ recordSeconds }}s / {{ MAX_SECONDS }}s
        <span v-if="!willCancel" class="ml-2">手指上滑取消</span>
      </div>
    </div>

    <div
      v-else-if="state === 'uploading'"
      class="text-center mb-4 text-base text-orange-600 font-bold"
    >
      正在识别...
    </div>

    <!-- 大按钮 -->
    <button
      class="select-none touch-none px-8 py-6 rounded-full text-white font-bold text-2xl shadow-lg transition-all w-full max-w-md"
      :class="[
        state === 'idle' && 'bg-orange-500 hover:bg-orange-600 active:scale-95',
        state === 'recording' && (willCancel ? 'bg-red-500' : 'bg-red-600 scale-105'),
        state === 'uploading' && 'bg-gray-400 cursor-wait',
      ]"
      :disabled="state === 'uploading'"
      @touchstart.prevent="onTouchStart"
      @touchmove.prevent="onTouchMove"
      @touchend.prevent="onTouchEnd"
      @mousedown="onMouseDown"
      @mouseup="onMouseUp"
      @mouseleave="onMouseLeave"
    >
      <span v-if="state === 'idle'">🎙 按住说话</span>
      <span v-else-if="state === 'recording'">● 录音中</span>
      <span v-else>识别中...</span>
    </button>

    <!-- 帮助提示 -->
    <p v-if="state === 'idle'" class="mt-3 text-sm text-gray-500 text-center">
      想说什么主题？比如"薏米红豆水祛湿"
    </p>

    <!-- 错误信息 -->
    <p v-if="errorMessage" class="mt-3 text-sm text-red-500 text-center">
      {{ errorMessage }}
    </p>
  </div>
</template>
