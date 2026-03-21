<template>
  <div class="max-w-5xl">
    <div class="flex items-center gap-2 mb-8 text-sm">
      <NuxtLink to="/admin/lessons" class="text-slate-500 hover:text-brand-500 no-underline transition-colors font-medium">
        课程管理
      </NuxtLink>
      <Icon name="heroicons:chevron-right" class="w-4 h-4 text-slate-300" />
      <span class="text-slate-900 font-bold">编辑课程</span>
    </div>

    <div v-if="loading" class="text-center py-12 text-slate-500">加载中...</div>

    <form v-else @submit.prevent="handleSave" class="space-y-6">
      <!-- 基本信息 -->
      <div class="admin-card space-y-6">
        <h2 class="text-lg font-black text-slate-900 flex items-center gap-3">
          <div class="w-1 h-6 bg-brand-500 rounded-full" />
          基本信息
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label class="block text-sm font-semibold text-slate-600 mb-2">所属分类</label>
            <select v-model.number="form.stage_id" class="admin-input" required>
              <option v-for="stage in stages" :key="stage.id" :value="stage.id">
                {{ stage.title }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-semibold text-slate-600 mb-2">课程序号</label>
            <input v-model.number="form.lesson_number" type="number" class="admin-input" required />
          </div>
          <div>
            <label class="block text-sm font-semibold text-slate-600 mb-2">时长 (分钟)</label>
            <input v-model.number="form.duration_minutes" type="number" class="admin-input" />
          </div>
        </div>

        <div>
          <label class="block text-sm font-semibold text-slate-600 mb-2">标题</label>
          <input v-model="form.title" type="text" class="admin-input" required />
        </div>

        <div>
          <label class="block text-sm font-semibold text-slate-600 mb-2">摘要</label>
          <input v-model="form.summary" type="text" class="admin-input" placeholder="一句话描述这节课的内容" />
        </div>

        <div class="flex items-center gap-8">
          <label class="flex items-center gap-2 cursor-pointer">
            <input v-model="form.is_free" type="checkbox" class="w-5 h-5 rounded border-slate-300 accent-brand-500">
            <span class="text-slate-700">免费</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input v-model="form.is_published" type="checkbox" class="w-5 h-5 rounded border-slate-300 accent-brand-500">
            <span class="text-slate-700">已发布</span>
          </label>
        </div>
      </div>

      <!-- 课程内容编辑器 -->
      <div class="admin-card">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-black text-slate-900 flex items-center gap-3">
            <div class="w-1 h-6 bg-brand-500 rounded-full" />
            课程内容 (Markdown)
          </h2>
          <button
            type="button"
            class="text-sm font-bold min-h-0 px-4 py-2 rounded-xl transition-all inline-flex items-center gap-1.5"
            :class="showPreview ? 'bg-brand-50 text-brand-600 border border-brand-200' : 'text-slate-500 hover:text-slate-900'"
            @click="showPreview = !showPreview"
          >
            <Icon :name="showPreview ? 'heroicons:eye-slash' : 'heroicons:eye'" class="w-4 h-4" />
            {{ showPreview ? '关闭预览' : '预览效果' }}
          </button>
        </div>

        <div :class="showPreview ? 'grid grid-cols-1 lg:grid-cols-2 gap-6' : ''">
          <div>
            <textarea
              v-model="form.content"
              rows="25"
              class="admin-input font-mono text-sm leading-relaxed"
              placeholder="在这里编写课程内容，支持 Markdown 格式..."
            />
          </div>
          <div v-if="showPreview" class="prose-lesson bg-slate-50 border border-slate-200 rounded-xl p-5 overflow-auto max-h-[600px]">
            <div v-html="renderedContent" />
          </div>
        </div>
      </div>

      <!-- 保存 -->
      <div class="flex items-center gap-4">
        <button type="submit" :disabled="saving" class="btn-primary disabled:opacity-50">
          {{ saving ? '保存中...' : '保存' }}
        </button>
        <NuxtLink to="/admin/lessons" class="btn-outline no-underline text-center">取消</NuxtLink>
        <span v-if="message" :class="messageType === 'success' ? 'admin-alert-success' : 'admin-alert-error'">
          {{ message }}
        </span>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: ['admin-auth'],
})

const route = useRoute()
const adminApi = useAdminApi()

const loading = ref(true)
const saving = ref(false)
const showPreview = ref(false)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')
const stages = ref<any[]>([])

const form = ref({
  title: '',
  subtitle: '',
  stage_id: 1,
  lesson_number: 1,
  content: '',
  summary: '',
  duration_minutes: 30,
  is_free: false,
  is_published: false,
})

// 简单 Markdown 渲染
function renderMarkdown(md: string): string {
  if (!md) return '<p class="text-slate-400">暂无内容</p>'
  let html = md
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^> (.+)$/gm, '<blockquote><p>$1</p></blockquote>')
    .replace(/^---$/gm, '<hr>')
    .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1">')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/\n\n/g, '</p><p>')
  return '<p>' + html + '</p>'
}

const renderedContent = computed(() => renderMarkdown(form.value.content))

onMounted(async () => {
  try {
    stages.value = await adminApi.get<any[]>('/admin/stages')
    const lesson = await adminApi.get<any>(`/admin/lessons/${route.params.id}`)
    form.value = {
      title: lesson.title,
      subtitle: lesson.subtitle || '',
      stage_id: lesson.stage_id,
      lesson_number: lesson.lesson_number,
      content: lesson.content,
      summary: lesson.summary || '',
      duration_minutes: lesson.duration_minutes || 30,
      is_free: lesson.is_free,
      is_published: lesson.is_published,
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

const handleSave = async () => {
  saving.value = true
  message.value = ''
  try {
    await adminApi.put(`/admin/lessons/${route.params.id}`, form.value)
    message.value = '保存成功！'
    messageType.value = 'success'
  } catch (e: any) {
    message.value = '保存失败：' + (e.message || '未知错误')
    messageType.value = 'error'
  } finally {
    saving.value = false
  }
}

useHead({ title: '编辑课程 - AI不难学' })
</script>
