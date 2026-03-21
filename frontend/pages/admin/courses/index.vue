<template>
  <div class="relative">
    <!-- 背景装饰色块，让毛玻璃有东西可以模糊 -->
    <div class="pointer-events-none absolute inset-0 overflow-hidden -z-10" aria-hidden="true">
      <div class="absolute -top-20 -left-20 w-72 h-72 rounded-full bg-blue-300/30 blur-3xl"></div>
      <div class="absolute top-40 right-0 w-64 h-64 rounded-full bg-violet-300/25 blur-3xl"></div>
      <div class="absolute -bottom-10 left-1/3 w-80 h-80 rounded-full bg-brand-300/20 blur-3xl"></div>
      <div class="absolute top-10 left-1/2 w-56 h-56 rounded-full bg-teal-300/20 blur-3xl"></div>
    </div>

    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-black text-slate-900 flex items-center gap-3">
          <Icon name="heroicons:folder-open" class="w-7 h-7 text-brand-500" />
          分类管理
        </h1>
        <p class="text-sm text-slate-500 mt-1">管理工具分类，调整课程归属和排序</p>
      </div>
    </div>

    <!-- 加载骨架屏 -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <div v-for="i in 6" :key="i" class="skeleton h-44 rounded-2xl"></div>
    </div>

    <template v-else>
      <div v-if="stages.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        <div
          v-for="(stage, idx) in stages"
          :key="stage.id"
          class="glass-card group rounded-2xl p-6 transition-all duration-300 hover:-translate-y-1"
        >
          <!-- 顶部：图标 + 序号 -->
          <div class="flex items-center justify-between mb-4">
            <UiStageIcon :emoji="stage.icon" size="sm" />
            <span class="text-xs font-bold text-slate-400">#{{ stage.stage_number }}</span>
          </div>

          <!-- 标题 -->
          <div class="font-black text-slate-900 text-lg mb-1">{{ stage.title }}</div>
          <div class="text-sm text-slate-500 mb-4">{{ stage.subtitle }}</div>

          <!-- 底部：信息 + 编辑 -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="text-sm font-bold text-slate-700">{{ stage.lessons?.length || 0 }} 节课</span>
              <span v-if="stage.is_free" class="text-xs font-bold text-emerald-600 bg-emerald-50/80 border border-emerald-200 px-2 py-0.5 rounded-md">免费</span>
            </div>
            <NuxtLink
              :to="`/admin/courses/${stage.id}`"
              class="no-underline text-sm font-bold px-3 py-1.5 rounded-lg transition-all flex items-center gap-1 text-brand-600 bg-brand-50/80 hover:bg-brand-100"
            >
              <Icon name="heroicons:pencil-square" class="w-3.5 h-3.5" />
              编辑
            </NuxtLink>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-20">
        <Icon name="heroicons:folder-open" class="w-16 h-16 text-slate-200 mx-auto mb-4" />
        <p class="text-base font-bold text-slate-400">暂无分类数据</p>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: ['admin-auth'],
})

const adminApi = useAdminApi()
const stages = ref<any[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    stages.value = await adminApi.get<any[]>('/admin/stages')
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

useHead({ title: '分类管理 - AI不难学' })
</script>

<style scoped>
.glass-card {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow:
    0 4px 16px rgba(0, 0, 0, 0.04),
    0 1px 3px rgba(0, 0, 0, 0.03),
    inset 0 1px 0 rgba(255, 255, 255, 0.7);
}
.glass-card:hover {
  background: rgba(255, 255, 255, 0.75);
  border-color: rgba(255, 255, 255, 1);
  box-shadow:
    0 12px 40px rgba(0, 0, 0, 0.08),
    0 2px 6px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
}
</style>
