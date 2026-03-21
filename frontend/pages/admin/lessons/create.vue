<template>
  <div class="max-w-3xl">
    <div class="flex items-center gap-2 mb-8 text-sm">
      <NuxtLink to="/admin/lessons" class="text-slate-500 hover:text-brand-500 no-underline transition-colors font-medium">
        课程管理
      </NuxtLink>
      <Icon name="heroicons:chevron-right" class="w-4 h-4 text-slate-300" />
      <span class="text-slate-900 font-bold">新增课程</span>
    </div>

    <form @submit.prevent="handleCreate" class="space-y-6">
      <!-- 基本信息 -->
      <div class="admin-card space-y-6">
        <h2 class="text-lg font-bold text-slate-900 flex items-center gap-3">
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
          <input v-model="form.summary" type="text" class="admin-input" />
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

      <!-- 课程内容 -->
      <div class="admin-card space-y-6">
        <h2 class="text-lg font-bold text-slate-900 flex items-center gap-3">
          <div class="w-1 h-6 bg-brand-500 rounded-full" />
          课程内容
        </h2>

        <div>
          <label class="block text-sm font-semibold text-slate-600 mb-2">内容 (Markdown)</label>
          <textarea v-model="form.content" rows="15" class="admin-input font-mono text-sm" placeholder="在这里编写课程内容..." />
          <p class="text-xs text-slate-400 mt-1">支持 Markdown 格式，可使用标题、列表、代码块等</p>
        </div>
      </div>

      <div v-if="message" :class="messageType === 'success' ? 'admin-alert-success' : 'admin-alert-error'">
        {{ message }}
      </div>

      <div class="flex gap-4">
        <button type="submit" :disabled="saving" class="btn-primary disabled:opacity-50">
          {{ saving ? '创建中...' : '创建' }}
        </button>
        <NuxtLink to="/admin/lessons" class="btn-outline no-underline text-center">取消</NuxtLink>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: ['admin-auth'],
})

const adminApi = useAdminApi()
const stages = ref<any[]>([])
const saving = ref(false)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')

const form = ref({
  title: '',
  stage_id: 1,
  lesson_number: 1,
  content: '',
  summary: '',
  duration_minutes: 30,
  is_free: false,
  is_published: false,
})

onMounted(async () => {
  stages.value = await adminApi.get<any[]>('/admin/stages')
})

const handleCreate = async () => {
  saving.value = true
  message.value = ''
  try {
    await adminApi.post('/admin/lessons', form.value)
    message.value = '创建成功！'
    messageType.value = 'success'
    setTimeout(() => navigateTo('/admin/lessons'), 1000)
  } catch (e: any) {
    message.value = '创建失败：' + (e.message || '未知错误')
    messageType.value = 'error'
  } finally {
    saving.value = false
  }
}

useHead({ title: '新增课程 - AI不难学' })
</script>
