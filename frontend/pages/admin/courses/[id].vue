<template>
  <div class="max-w-3xl">
    <div class="flex items-center gap-2 mb-8 text-sm">
      <NuxtLink to="/admin/courses" class="text-slate-500 hover:text-brand-500 no-underline transition-colors font-medium">
        分类管理
      </NuxtLink>
      <Icon name="heroicons:chevron-right" class="w-4 h-4 text-slate-300" />
      <span class="text-slate-900 font-bold">编辑分类</span>
    </div>

    <div v-if="loading" class="text-center py-12 text-slate-500">加载中...</div>

    <form v-else @submit.prevent="handleSave" class="admin-card space-y-6">
      <h2 class="text-lg font-bold text-slate-900 flex items-center gap-3">
        <div class="w-1 h-6 bg-brand-500 rounded-full" />
        基本信息
      </h2>
      <div class="grid grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-semibold text-slate-600 mb-2">排序序号</label>
          <input v-model.number="form.stage_number" type="number" class="admin-input" />
        </div>
        <div>
          <label class="block text-sm font-semibold text-slate-600 mb-2">图标 (emoji)</label>
          <input v-model="form.icon" type="text" class="admin-input" />
        </div>
      </div>

      <div>
        <label class="block text-sm font-semibold text-slate-600 mb-2">标题</label>
        <input v-model="form.title" type="text" class="admin-input" required />
      </div>

      <div>
        <label class="block text-sm font-semibold text-slate-600 mb-2">副标题</label>
        <input v-model="form.subtitle" type="text" class="admin-input" />
      </div>

      <div>
        <label class="block text-sm font-semibold text-slate-600 mb-2">描述</label>
        <textarea v-model="form.description" rows="4" class="admin-input" />
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

      <div v-if="message" :class="messageType === 'success' ? 'admin-alert-success' : 'admin-alert-error'">
        {{ message }}
      </div>

      <div class="flex gap-4">
        <button type="submit" :disabled="saving" class="btn-primary disabled:opacity-50">
          {{ saving ? '保存中...' : '保存' }}
        </button>
        <NuxtLink to="/admin/courses" class="btn-outline no-underline text-center">取消</NuxtLink>
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
const message = ref('')
const messageType = ref<'success' | 'error'>('success')

const form = ref({
  title: '',
  subtitle: '',
  description: '',
  stage_number: 1,
  icon: '',
  is_free: false,
  is_published: false,
})

onMounted(async () => {
  try {
    const stages = await adminApi.get<any[]>('/admin/stages')
    const stage = stages.find((s: any) => s.id === Number(route.params.id))
    if (stage) {
      form.value = {
        title: stage.title,
        subtitle: stage.subtitle,
        description: stage.description,
        stage_number: stage.stage_number,
        icon: stage.icon || '',
        is_free: stage.is_free,
        is_published: stage.is_published,
      }
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
    await adminApi.put(`/admin/stages/${route.params.id}`, form.value)
    message.value = '保存成功！'
    messageType.value = 'success'
  } catch (e: any) {
    message.value = '保存失败：' + (e.message || '未知错误')
    messageType.value = 'error'
  } finally {
    saving.value = false
  }
}

useHead({ title: '编辑分类 - AI不难学' })
</script>
