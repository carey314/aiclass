<template>
  <div class="relative">
    <!-- 背景装饰 -->
    <div class="pointer-events-none absolute inset-0 overflow-hidden -z-10" aria-hidden="true">
      <div class="absolute -top-20 -left-10 w-72 h-72 rounded-full bg-violet-300/25 blur-3xl"></div>
      <div class="absolute top-60 right-0 w-64 h-64 rounded-full bg-blue-300/20 blur-3xl"></div>
      <div class="absolute -bottom-10 left-1/2 w-80 h-80 rounded-full bg-brand-300/15 blur-3xl"></div>
    </div>

    <!-- 顶部 -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-black text-slate-900 flex items-center gap-3">
          <Icon name="heroicons:document-text" class="w-7 h-7 text-brand-500" />
          课程管理
        </h1>
        <p class="text-sm text-slate-500 mt-1">管理所有课程内容，编辑发布课程</p>
      </div>
      <NuxtLink to="/admin/lessons/create"
        class="no-underline text-sm px-5 py-2.5 rounded-xl font-bold text-white inline-flex items-center gap-2 transition-all hover:-translate-y-0.5"
        style="background: linear-gradient(135deg, #F97316, #FB923C); box-shadow: 0 2px 8px rgba(249,115,22,0.3);">
        <Icon name="heroicons:plus" class="w-4 h-4" />
        新增课程
      </NuxtLink>
    </div>

    <!-- 筛选栏 -->
    <div class="glass-bar flex items-center gap-3 mb-6 p-3 rounded-2xl">
      <Icon name="heroicons:funnel" class="w-5 h-5 text-slate-400 ml-1" />
      <div class="flex flex-wrap gap-2">
        <button
          @click="filterStageId = null"
          class="filter-chip min-h-0"
          :class="filterStageId === null ? 'filter-chip-active' : ''"
        >
          全部
          <span class="filter-count">{{ lessons.length }}</span>
        </button>
        <button
          v-for="stage in stages"
          :key="stage.id"
          @click="filterStageId = stage.id"
          class="filter-chip min-h-0"
          :class="filterStageId === stage.id ? 'filter-chip-active' : ''"
        >
          {{ stage.icon }} {{ stage.title }}
          <span class="filter-count">{{ getLessonCount(stage.id) }}</span>
        </button>
      </div>
    </div>

    <!-- 统计条 -->
    <div class="flex items-center gap-4 mb-5 text-sm text-slate-500">
      <span>共 <b class="text-slate-800">{{ filteredLessons.length }}</b> 节课程</span>
      <span class="text-slate-300">|</span>
      <span class="flex items-center gap-1">
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        已发布 {{ publishedCount }}
      </span>
      <span class="flex items-center gap-1">
        <span class="w-2 h-2 rounded-full bg-amber-400"></span>
        草稿 {{ draftCount }}
      </span>
    </div>

    <!-- 加载骨架屏 -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 6" :key="i" class="skeleton h-20 rounded-2xl"></div>
    </div>

    <template v-else>
      <div v-if="filteredLessons.length" class="space-y-3">
        <div
          v-for="lesson in filteredLessons"
          :key="lesson.id"
          class="glass-card group rounded-2xl px-5 py-4 flex items-center gap-4 transition-all duration-300 hover:-translate-y-0.5"
        >
          <!-- 课号 -->
          <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 text-sm font-black"
               :class="lesson.is_published ? 'bg-emerald-50 text-emerald-600 border border-emerald-200' : 'bg-slate-50 text-slate-400 border border-slate-200'">
            {{ lesson.lesson_number }}
          </div>

          <!-- 标题 + 分类 -->
          <div class="flex-1 min-w-0">
            <div class="font-bold text-slate-900 text-base truncate">{{ lesson.title }}</div>
            <div class="flex items-center gap-2 mt-1">
              <span class="text-xs font-medium text-slate-400">{{ getStageTitle(lesson.stage_id) }}</span>
            </div>
          </div>

          <!-- 发布状态 -->
          <span class="flex-shrink-0 text-xs font-bold px-3 py-1 rounded-lg"
                :class="lesson.is_published
                  ? 'text-emerald-700 bg-emerald-50 border border-emerald-200'
                  : 'text-amber-600 bg-amber-50 border border-amber-200'">
            {{ lesson.is_published ? '已发布' : '草稿' }}
          </span>

          <!-- 操作按钮 -->
          <div class="flex items-center gap-2 flex-shrink-0">
            <NuxtLink
              :to="`/admin/lessons/${lesson.id}`"
              class="no-underline w-9 h-9 rounded-xl flex items-center justify-center transition-all text-brand-500 bg-brand-50/80 hover:bg-brand-100 border border-brand-200/50"
              title="编辑"
            >
              <Icon name="heroicons:pencil-square" class="w-4 h-4" />
            </NuxtLink>
            <button
              @click="handleDelete(lesson)"
              class="w-9 h-9 rounded-xl flex items-center justify-center transition-all text-red-400 bg-red-50/80 hover:bg-red-100 border border-red-200/50 min-h-0 px-0"
              title="删除"
            >
              <Icon name="heroicons:trash" class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-20">
        <Icon name="heroicons:document-text" class="w-16 h-16 text-slate-200 mx-auto mb-4" />
        <p class="text-base font-bold text-slate-400">暂无课程数据</p>
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
const lessons = ref<any[]>([])
const filterStageId = ref<number | null>(null)

const filteredLessons = computed(() => {
  if (!filterStageId.value) return lessons.value
  return lessons.value.filter(l => l.stage_id === filterStageId.value)
})

const publishedCount = computed(() => filteredLessons.value.filter(l => l.is_published).length)
const draftCount = computed(() => filteredLessons.value.filter(l => !l.is_published).length)

const getStageTitle = (stageId: number) => {
  const stage = stages.value.find(s => s.id === stageId)
  return stage ? stage.title : ''
}

const getLessonCount = (stageId: number) => {
  return lessons.value.filter(l => l.stage_id === stageId).length
}

const loading = ref(true)

const loadData = async () => {
  loading.value = true
  try {
    stages.value = await adminApi.get<any[]>('/admin/stages')
    lessons.value = await adminApi.get<any[]>('/admin/lessons')
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const handleDelete = async (lesson: any) => {
  if (!confirm(`确定要删除"${lesson.title}"吗？`)) return
  try {
    await adminApi.del(`/admin/lessons/${lesson.id}`)
    await loadData()
  } catch (e) {
    alert('删除失败')
  }
}

onMounted(loadData)

useHead({ title: '课程管理 - AI不难学' })
</script>

<style scoped>
.glass-bar {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.glass-card {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow:
    0 2px 8px rgba(0, 0, 0, 0.03),
    0 1px 2px rgba(0, 0, 0, 0.02),
    inset 0 1px 0 rgba(255, 255, 255, 0.7);
}
.glass-card:hover {
  background: rgba(255, 255, 255, 0.8);
  border-color: rgba(255, 255, 255, 1);
  box-shadow:
    0 8px 24px rgba(0, 0, 0, 0.06),
    0 2px 4px rgba(0, 0, 0, 0.03),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.filter-chip {
  padding: 6px 14px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.filter-chip:hover {
  background: rgba(255, 255, 255, 0.8);
  border-color: #cbd5e1;
}
.filter-chip-active {
  background: linear-gradient(135deg, #F97316, #FB923C);
  color: #fff;
  border-color: transparent;
  box-shadow: 0 2px 8px rgba(249, 115, 22, 0.25);
}
.filter-chip-active:hover {
  background: linear-gradient(135deg, #F97316, #FB923C);
  border-color: transparent;
}
.filter-chip-active .filter-count {
  background: rgba(255, 255, 255, 0.25);
  color: #fff;
}

.filter-count {
  font-size: 11px;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 6px;
  background: #f1f5f9;
  color: #94a3b8;
}
</style>
