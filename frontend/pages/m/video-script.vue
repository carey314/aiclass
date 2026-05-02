<script setup lang="ts">
/**
 * 移动端：即梦AI视频脚本生成器
 *
 * 状态机：
 *   idle → input → generating → result
 *                       ↓
 *                     error → input
 *
 * 用户流程：
 *   按住说话/手输 → 主题输入框 → 点"生成脚本"
 *   → 流式接收 → 实时预览 → 完成 → 展示完整结果 + 复制
 */
import { ref, onMounted, computed } from 'vue'
import type { ScriptTemplate } from '~/composables/useVideoScript'

definePageMeta({
  layout: false,  // 不用默认layout，全屏
})

const auth = useAuthStore()
const { generateStream, fetchHistory, deleteScript } = useVideoScript()

// 状态
type Phase = 'input' | 'generating' | 'result' | 'error'
const phase = ref<Phase>('input')
const topicInput = ref('')
const errorMessage = ref('')
const isInputFocused = ref(false)

// 流式生成中
const streamingText = ref('')
const generationStartTime = ref(0)
const generationDoneId = ref<number | null>(null)
const generationDoneMs = ref(0)
let abortFn: (() => void) | null = null

// 解析后的最终结果
const finalTemplate = ref<ScriptTemplate | null>(null)

// 历史
const showHistory = ref(false)
const historyItems = ref<{ id: number; topic: string; created_at: string }[]>([])
const historyLoading = ref(false)

// 检查登录
onMounted(async () => {
  await auth.init()
  if (!auth.isAuthenticated) {
    navigateTo('/admin/login?redirect=/m/video-script')
    return
  }
})

// 录音转文字回调
const handleTranscribed = (text: string) => {
  topicInput.value = text
  errorMessage.value = ''
}

const handleVoiceError = (msg: string) => {
  errorMessage.value = msg
}

// 启动生成
const startGenerate = () => {
  const topic = topicInput.value.trim()
  if (!topic) {
    errorMessage.value = '请说一个主题再生成'
    return
  }
  if (topic.length > 300) {
    errorMessage.value = '主题太长了，再短一点（300字以内）'
    return
  }

  errorMessage.value = ''
  streamingText.value = ''
  finalTemplate.value = null
  generationStartTime.value = Date.now()
  generationDoneId.value = null
  phase.value = 'generating'

  const { abort } = generateStream(topic, {
    onChunk: (_chunk, accumulated) => {
      streamingText.value = accumulated
    },
    onDone: (id, ms) => {
      generationDoneId.value = id
      generationDoneMs.value = ms
      // 解析最终JSON
      try {
        const cleaned = stripCodeBlock(streamingText.value)
        finalTemplate.value = JSON.parse(cleaned)
        phase.value = 'result'
      } catch (e) {
        errorMessage.value = 'AI输出格式异常，请重试'
        phase.value = 'error'
      }
    },
    onError: (detail, kind) => {
      const friendly = mapErrorMessage(detail, kind)
      errorMessage.value = friendly
      phase.value = 'error'
    },
  })
  abortFn = abort
}

const stripCodeBlock = (text: string) => {
  let t = text.trim()
  if (t.startsWith('```')) {
    const lines = t.split('\n')
    return lines.slice(1, lines[lines.length - 1].startsWith('```') ? -1 : undefined).join('\n').trim()
  }
  return t
}

const mapErrorMessage = (detail: string, kind: string): string => {
  if (kind === 'auth') return '服务器配置异常，请联系管理员'
  if (kind === 'rate_limit') return 'AI繁忙，等几秒再试'
  if (kind === 'timeout') return 'AI响应超时，请重试'
  if (kind === 'bad_json') return 'AI输出格式不对，再试一次'
  if (kind === 'aborted') return '已取消'
  return detail || '出错了，请重试'
}

const cancelGenerate = () => {
  if (abortFn) abortFn()
  phase.value = 'input'
}

const startOver = () => {
  topicInput.value = ''
  streamingText.value = ''
  finalTemplate.value = null
  errorMessage.value = ''
  phase.value = 'input'
}

const reuseTopic = () => {
  // 保留当前topic，但回到输入态
  streamingText.value = ''
  finalTemplate.value = null
  errorMessage.value = ''
  phase.value = 'input'
}

// 历史
const loadHistory = async () => {
  historyLoading.value = true
  try {
    const res = await fetchHistory(1, 50)
    historyItems.value = res.items
  } catch (e: any) {
    errorMessage.value = '加载历史失败'
  }
  historyLoading.value = false
}

const openHistory = async () => {
  showHistory.value = true
  await loadHistory()
}

const closeHistory = () => {
  showHistory.value = false
}

const removeHistory = async (id: number) => {
  if (!confirm('确定删除？')) return
  try {
    await deleteScript(id)
    historyItems.value = historyItems.value.filter((x) => x.id !== id)
  } catch (e) {
    alert('删除失败')
  }
}

const reuseHistoryTopic = (topic: string) => {
  topicInput.value = topic
  closeHistory()
}

// 显示流式生成的字数（让用户看到进度）
const streamingCount = computed(() => streamingText.value.length)
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-orange-50 to-white">
    <!-- 顶部栏 -->
    <header class="sticky top-0 z-10 bg-white shadow-sm">
      <div class="flex items-center justify-between px-4 py-3">
        <h1 class="text-lg font-bold text-gray-900">📝 视频脚本生成器</h1>
        <button
          class="text-sm text-gray-600 px-3 py-1 hover:bg-gray-100 rounded"
          @click="openHistory"
        >
          📂 历史
        </button>
      </div>
    </header>

    <main class="max-w-2xl mx-auto px-4 py-6 pb-24">
      <!-- 阶段1：输入 -->
      <section v-if="phase === 'input' || phase === 'error'" class="space-y-6">
        <div class="text-center">
          <h2 class="text-2xl font-bold text-gray-900 mb-2">
            说一句你想做的视频
          </h2>
          <p class="text-base text-gray-600">
            比如"薏米红豆水祛湿"
          </p>
        </div>

        <!-- 录音按钮 -->
        <div class="bg-white rounded-2xl p-6 shadow-sm">
          <VoiceRecorder
            @transcribed="handleTranscribed"
            @error="handleVoiceError"
          />
        </div>

        <!-- 文字输入（备选/编辑） -->
        <div class="bg-white rounded-2xl p-4 shadow-sm">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            或者直接输入主题（可编辑识别结果）：
          </label>
          <textarea
            v-model="topicInput"
            rows="3"
            placeholder="比如：薏米红豆水祛湿"
            class="w-full px-3 py-3 text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none"
            @focus="isInputFocused = true"
            @blur="isInputFocused = false"
          />
          <div class="text-right text-xs text-gray-400 mt-1">
            {{ topicInput.length }} / 300
          </div>
        </div>

        <!-- 错误提示 -->
        <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg px-4 py-3">
          <p class="text-red-700 text-sm">⚠️ {{ errorMessage }}</p>
        </div>

        <!-- 生成按钮（粘性底部） -->
        <button
          class="w-full py-4 rounded-xl text-white font-bold text-lg shadow-lg transition-all"
          :class="
            topicInput.trim()
              ? 'bg-orange-500 hover:bg-orange-600 active:scale-95'
              : 'bg-gray-300 cursor-not-allowed'
          "
          :disabled="!topicInput.trim()"
          @click="startGenerate"
        >
          ✨ 生成脚本
        </button>
      </section>

      <!-- 阶段2：生成中（流式） -->
      <section v-if="phase === 'generating'" class="space-y-6">
        <div class="text-center pt-8">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-orange-100 rounded-full mb-4">
            <span class="text-3xl animate-pulse">✍️</span>
          </div>
          <h2 class="text-xl font-bold text-gray-900 mb-1">AI正在为你写脚本...</h2>
          <p class="text-sm text-gray-500">
            主题：{{ topicInput }}
          </p>
          <p class="text-xs text-gray-400 mt-2">
            已生成 {{ streamingCount }} 字 ·
            通常需要20-30秒
          </p>
        </div>

        <!-- 流式预览（让用户知道在工作） -->
        <div class="bg-white rounded-xl p-4 shadow-sm border-2 border-orange-200">
          <div class="text-xs text-gray-400 mb-2">实时生成内容（最终会整理成卡片）：</div>
          <pre class="text-sm text-gray-700 whitespace-pre-wrap font-sans leading-relaxed max-h-96 overflow-y-auto">{{ streamingText || '正在连接...' }}</pre>
        </div>

        <button
          class="w-full py-3 rounded-lg text-gray-700 bg-gray-100 hover:bg-gray-200 font-medium text-sm"
          @click="cancelGenerate"
        >
          取消生成
        </button>
      </section>

      <!-- 阶段3：结果 -->
      <section v-if="phase === 'result' && finalTemplate" class="space-y-4">
        <ScriptResultCard
          :template="finalTemplate"
          :meta="{ generation_ms: generationDoneMs }"
        />

        <div class="flex gap-3 mt-6">
          <button
            class="flex-1 py-3 rounded-xl bg-orange-500 text-white font-bold active:scale-95"
            @click="startOver"
          >
            做下一个
          </button>
          <button
            class="flex-1 py-3 rounded-xl bg-gray-100 text-gray-700 font-medium"
            @click="reuseTopic"
          >
            修改主题重生成
          </button>
        </div>
      </section>
    </main>

    <!-- 历史抽屉 -->
    <Transition name="slide">
      <div v-if="showHistory" class="fixed inset-0 z-50 bg-black/50" @click.self="closeHistory">
        <div class="absolute right-0 top-0 bottom-0 w-full max-w-md bg-white shadow-xl overflow-y-auto">
          <div class="sticky top-0 bg-white border-b px-4 py-3 flex items-center justify-between">
            <h2 class="text-lg font-bold">📂 历史脚本</h2>
            <button class="text-gray-500 text-xl" @click="closeHistory">×</button>
          </div>
          <div class="p-4">
            <div v-if="historyLoading" class="text-center py-8 text-gray-500">加载中...</div>
            <div v-else-if="historyItems.length === 0" class="text-center py-8 text-gray-500">
              还没生成过脚本<br>
              <span class="text-sm">关闭抽屉，按住按钮说一句开始第一条</span>
            </div>
            <ul v-else class="space-y-2">
              <li
                v-for="item in historyItems"
                :key="item.id"
                class="bg-gray-50 rounded-lg p-3"
              >
                <div class="flex items-start justify-between gap-2">
                  <div class="flex-1 min-w-0">
                    <div class="font-medium text-gray-900 truncate">{{ item.topic }}</div>
                    <div class="text-xs text-gray-400 mt-1">
                      {{ new Date(item.created_at).toLocaleString('zh-CN') }}
                    </div>
                  </div>
                  <div class="flex flex-col gap-1 shrink-0">
                    <button
                      class="text-xs px-2 py-1 bg-orange-500 text-white rounded"
                      @click="reuseHistoryTopic(item.topic)"
                    >
                      用此主题
                    </button>
                    <button
                      class="text-xs px-2 py-1 bg-gray-200 text-gray-600 rounded"
                      @click="removeHistory(item.id)"
                    >
                      删除
                    </button>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: opacity 0.2s;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
}
</style>
