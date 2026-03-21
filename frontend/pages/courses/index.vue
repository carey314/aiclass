<template>
  <div class="pt-16 md:pt-20 pb-32 max-w-5xl mx-auto px-6">
    <!-- 标题区域 -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-14" data-reveal>
      <div>
        <div class="inline-block px-4 py-1.5 rounded-full bg-brand-50 text-brand-600 text-sm font-bold mb-5 border border-brand-100">
          📚 全部课程
        </div>
        <h1 class="text-3xl md:text-4xl font-black text-slate-900 mb-3">课程目录</h1>
        <p class="text-lg text-slate-500">点击分类展开详细课时，开启你的 AI 达人之路</p>
      </div>
      <div v-if="!loading && stages.length" class="flex gap-3">
        <div class="stat-pill">
          <span class="text-xl font-black text-slate-900">{{ totalLessons }}</span>
          <span class="text-xs text-slate-400 font-bold">总课时</span>
        </div>
        <div class="stat-pill">
          <span class="text-xl font-black text-slate-900">{{ stages.length }}</span>
          <span class="text-xs text-slate-400 font-bold">工具分类</span>
        </div>
      </div>
    </div>

    <!-- 骨架屏加载 -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 4" :key="i" class="skeleton-accordion">
        <div class="flex items-center gap-5 p-5 md:p-8">
          <div class="skeleton-el w-12 h-12 rounded-xl flex-shrink-0" />
          <div class="flex-1 space-y-2">
            <div class="skeleton-el w-1/3 h-5 rounded-lg" />
            <div class="skeleton-el w-1/2 h-4 rounded-lg" />
          </div>
          <div class="skeleton-el w-10 h-10 rounded-full flex-shrink-0" />
        </div>
      </div>
    </div>

    <!-- 手风琴课程列表 -->
    <div v-else class="space-y-4">
      <div
        v-for="(stage, idx) in stages"
        :key="stage.id"
        class="accordion-item overflow-hidden"
        :class="openStage === stage.id ? 'accordion-active' : ''"
        data-reveal
        :data-reveal-delay="idx * 80"
      >
        <!-- 标题按钮 -->
        <button
          class="w-full flex items-center justify-between p-5 md:p-8 text-left transition-all min-h-0 group"
          @click="openStage = openStage === stage.id ? null : stage.id"
        >
          <div class="flex items-center gap-5 md:gap-6">
            <div class="flex-shrink-0 transition-all duration-500" :class="openStage === stage.id ? 'scale-105' : ''">
              <UiStageIcon :emoji="stage.icon" size="md" />
            </div>
            <div>
              <h3 class="text-lg md:text-xl font-black text-slate-900 mb-0.5">{{ stage.title }}</h3>
              <p class="text-slate-400 font-medium text-sm">
                {{ stage.subtitle }} · {{ stage.lessons?.length || 0 }} 节课
              </p>
            </div>
          </div>
          <div
            class="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 transition-all duration-300"
            :class="openStage === stage.id ? 'rotate-180 bg-slate-100' : 'bg-slate-50 group-hover:bg-slate-100'"
          >
            <Icon name="heroicons:chevron-down" class="w-5 h-5 text-slate-400" />
          </div>
        </button>

        <!-- 展开的课程列表 -->
        <div v-if="openStage === stage.id" class="px-4 md:px-6 pb-4 md:pb-6 space-y-1">
          <NuxtLink
            v-for="(lesson, lIdx) in stage.lessons"
            :key="lesson.id"
            :to="`/courses/${stage.id}/${lesson.id}`"
            class="lesson-item group no-underline"
          >
            <div class="flex items-center gap-4 md:gap-5">
              <span
                class="w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold flex-shrink-0 transition-all"
                :class="stageColors[idx]?.lessonNum || 'bg-slate-100 text-slate-500 group-hover:bg-brand-500 group-hover:text-white'"
              >
                {{ lIdx + 1 }}
              </span>
              <span class="text-base md:text-lg text-slate-600 group-hover:text-slate-900 transition-colors">
                {{ lesson.title }}
              </span>
            </div>
            <div class="flex items-center gap-3 flex-shrink-0">
              <span v-if="lesson.duration_minutes" class="text-slate-400 text-xs font-bold bg-slate-50 px-2.5 py-1 rounded-lg hidden md:block">
                {{ lesson.duration_minutes }}分钟
              </span>
              <Icon name="heroicons:chevron-right" class="w-5 h-5 text-slate-300 group-hover:text-slate-500 group-hover:translate-x-1 transition-all" />
            </div>
          </NuxtLink>

          <div v-if="!stage.lessons?.length" class="py-12 text-center text-slate-300 text-base">
            内容正在准备中...
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const api = useApi()
const loading = ref(true)
const stages = ref<any[]>([])
const openStage = ref<number | null>(null)

useScrollReveal()

const stageColors = [
  { icon: 'bg-blue-100', activeIcon: 'bg-blue-500 text-white shadow-lg shadow-blue-200', lessonNum: 'bg-blue-50 text-blue-600 group-hover:bg-blue-500 group-hover:text-white' },
  { icon: 'bg-teal-100', activeIcon: 'bg-teal-500 text-white shadow-lg shadow-teal-200', lessonNum: 'bg-teal-50 text-teal-600 group-hover:bg-teal-500 group-hover:text-white' },
  { icon: 'bg-violet-100', activeIcon: 'bg-violet-500 text-white shadow-lg shadow-violet-200', lessonNum: 'bg-violet-50 text-violet-600 group-hover:bg-violet-500 group-hover:text-white' },
  { icon: 'bg-amber-100', activeIcon: 'bg-amber-500 text-white shadow-lg shadow-amber-200', lessonNum: 'bg-amber-50 text-amber-600 group-hover:bg-amber-500 group-hover:text-white' },
  { icon: 'bg-rose-100', activeIcon: 'bg-rose-500 text-white shadow-lg shadow-rose-200', lessonNum: 'bg-rose-50 text-rose-600 group-hover:bg-rose-500 group-hover:text-white' },
  { icon: 'bg-indigo-100', activeIcon: 'bg-indigo-500 text-white shadow-lg shadow-indigo-200', lessonNum: 'bg-indigo-50 text-indigo-600 group-hover:bg-indigo-500 group-hover:text-white' },
]

const totalLessons = computed(() =>
  stages.value.reduce((sum, s) => sum + (s.lessons?.length || 0), 0)
)

onMounted(async () => {
  try {
    stages.value = await api.get<any[]>('/stages')
    if (stages.value.length) {
      openStage.value = stages.value[0].id
    }
  } catch (e) {
    console.error('获取课程数据失败:', e)
  } finally {
    loading.value = false
  }
})

useHead({
  title: '全部课程 - AI不难学',
})
</script>

<style scoped>
.stat-pill {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: white;
  border: 1px solid #F1F5F9;
  border-radius: 1rem;
  padding: 0.625rem 1.25rem;
}

.accordion-item {
  background: white;
  border: 1px solid #F1F5F9;
  border-radius: 1.25rem;
  transition: all 0.3s ease;
}
.accordion-item:hover {
  border-color: #E2E8F0;
}
.accordion-active {
  border-color: #E2E8F0;
  box-shadow: 0 4px 20px -4px rgba(0,0,0,0.06);
}

.lesson-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.875rem 1rem;
  border-radius: 0.875rem;
  transition: all 0.2s ease;
}
.lesson-item:hover {
  background: #F8FAFC;
}

/* === 骨架屏 === */
@keyframes skeleton-pulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 0.8; }
}
.skeleton-accordion {
  background: white;
  border: 1px solid #F1F5F9;
  border-radius: 1.25rem;
}
.skeleton-el {
  background: linear-gradient(90deg, #F1F5F9 25%, #E2E8F0 50%, #F1F5F9 75%);
  background-size: 200% 100%;
  animation: skeleton-pulse 1.5s ease-in-out infinite;
}
</style>
