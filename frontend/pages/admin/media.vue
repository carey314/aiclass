<template>
  <div>
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-black text-slate-900 flex items-center gap-3">
          <Icon name="heroicons:photo" class="w-7 h-7 text-brand-500" />
          媒体库
        </h1>
        <p class="text-sm text-slate-500 mt-1">管理课程图片、视频和文档资源</p>
      </div>
    </div>

    <!-- 上传区域 -->
    <div
      class="admin-card border-2 border-dashed p-12 mb-8 text-center transition-all cursor-pointer group"
      :class="dragActive ? 'border-brand-400 bg-brand-50/50' : 'border-slate-300 hover:border-brand-400 hover:bg-brand-50/30'"
      @click="triggerUpload"
      @dragover.prevent="dragActive = true"
      @dragleave="dragActive = false"
      @drop.prevent="handleDrop"
    >
      <input ref="fileInput" type="file" class="hidden" accept="image/*,video/*,.pdf" @change="handleFileSelect" />
      <div class="w-16 h-16 rounded-2xl bg-brand-50 flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
        <Icon name="heroicons:cloud-arrow-up" class="w-8 h-8 text-brand-400" />
      </div>
      <p class="text-lg text-slate-700 font-bold">点击上传或拖拽文件到这里</p>
      <p class="text-sm text-slate-400 mt-2">支持图片、视频、PDF，最大10MB</p>
    </div>

    <!-- 上传进度条 -->
    <div v-if="uploading" class="mb-6">
      <div class="flex items-center gap-3 mb-2">
        <Icon name="heroicons:arrow-path" class="w-5 h-5 text-brand-500 animate-spin" />
        <span class="text-sm font-bold text-brand-600">上传中...</span>
      </div>
      <div class="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
        <div class="h-full rounded-full transition-all duration-300" style="background: linear-gradient(90deg, #F97316, #FB923C); width: 60%"></div>
      </div>
    </div>

    <!-- 媒体列表 -->
    <div v-if="mediaList.length" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
      <div
        v-for="media in mediaList"
        :key="media.id"
        class="admin-card p-0 overflow-hidden group hover:shadow-lg hover:border-slate-300 transition-all"
      >
        <div class="aspect-square bg-slate-50 flex items-center justify-center overflow-hidden relative">
          <img
            v-if="media.media_type === 'image'"
            :src="getMediaUrl(media.url)"
            :alt="media.alt_text || media.filename"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
          <div v-else class="flex flex-col items-center gap-2">
            <Icon
              :name="media.media_type === 'video' ? 'heroicons:film' : 'heroicons:document'"
              class="w-10 h-10 text-slate-300"
            />
            <span class="text-xs text-slate-400 font-medium">{{ media.media_type === 'video' ? '视频' : '文档' }}</span>
          </div>
        </div>
        <div class="p-3">
          <p class="text-xs text-slate-600 font-medium truncate" :title="media.filename">{{ media.filename }}</p>
          <p v-if="media.file_size" class="text-xs text-slate-400 mt-0.5">{{ formatSize(media.file_size) }}</p>
          <div class="flex items-center justify-between mt-2">
            <button
              class="text-xs text-brand-500 hover:text-brand-600 bg-transparent border-none cursor-pointer min-h-0 px-0 inline-flex items-center gap-1 transition-colors"
              @click="copyUrl(media)"
            >
              <Icon name="heroicons:clipboard-document" class="w-3.5 h-3.5" />
              复制
            </button>
            <button
              class="text-xs text-red-400 hover:text-red-600 bg-transparent border-none cursor-pointer min-h-0 px-0 inline-flex items-center gap-1 transition-colors"
              @click="handleDelete(media)"
            >
              <Icon name="heroicons:trash" class="w-3.5 h-3.5" />
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else-if="!uploading" class="admin-empty">
      <div class="w-16 h-16 rounded-2xl bg-slate-50 flex items-center justify-center mx-auto mb-4">
        <Icon name="heroicons:photo" class="w-8 h-8 text-slate-200" />
      </div>
      <p class="text-base font-bold text-slate-400">暂无媒体文件</p>
      <p class="text-sm text-slate-400 mt-1">上传第一个文件吧</p>
    </div>

    <!-- 复制成功 Toast -->
    <Transition>
      <div v-if="copySuccess" class="fixed bottom-6 right-6 z-50 admin-alert-success flex items-center gap-2 shadow-lg">
        <Icon name="heroicons:check-circle" class="w-5 h-5" />
        链接已复制！
      </div>
    </Transition>

    <!-- 删除成功 Toast -->
    <Transition>
      <div v-if="deleteSuccess" class="fixed bottom-6 right-6 z-50 admin-alert-success flex items-center gap-2 shadow-lg">
        <Icon name="heroicons:check-circle" class="w-5 h-5" />
        文件已删除！
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: ['admin-auth'],
})

const config = useRuntimeConfig()
const adminApi = useAdminApi()
const fileInput = ref<HTMLInputElement | null>(null)
const mediaList = ref<any[]>([])
const uploading = ref(false)
const dragActive = ref(false)
const copySuccess = ref(false)
const deleteSuccess = ref(false)

const getMediaUrl = (url: string) => {
  if (url.startsWith('http')) return url
  return `http://localhost:8000${url}`
}

const formatSize = (bytes: number) => {
  if (!bytes) return ''
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

const loadMedia = async () => {
  try {
    mediaList.value = await adminApi.get<any[]>('/admin/media')
  } catch (e) {
    console.error(e)
  }
}

const triggerUpload = () => fileInput.value?.click()

const uploadFile = async (file: File) => {
  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    await adminApi.upload('/admin/media/upload', formData)
    await loadMedia()
  } catch (e) {
    alert('上传失败')
  } finally {
    uploading.value = false
  }
}

const handleFileSelect = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) uploadFile(file)
}

const handleDrop = (e: DragEvent) => {
  dragActive.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) uploadFile(file)
}

const copyUrl = (media: any) => {
  const url = getMediaUrl(media.url)
  navigator.clipboard.writeText(url)
  copySuccess.value = true
  setTimeout(() => copySuccess.value = false, 2000)
}

const handleDelete = async (media: any) => {
  if (!confirm(`确定删除 ${media.filename}？`)) return
  try {
    await adminApi.del(`/admin/media/${media.id}`)
    await loadMedia()
    deleteSuccess.value = true
    setTimeout(() => deleteSuccess.value = false, 2000)
  } catch (e) {
    alert('删除失败')
  }
}

onMounted(loadMedia)

useHead({ title: '媒体库 - AI不难学' })
</script>
