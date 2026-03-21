<template>
  <div class="pt-16 md:pt-20 pb-32 max-w-5xl mx-auto px-6">
    <!-- 面包屑 -->
    <nav class="flex items-center gap-3 text-slate-400 font-bold mb-10 text-sm">
      <NuxtLink to="/" class="hover:text-slate-900 no-underline transition-colors">首页</NuxtLink>
      <Icon name="heroicons:chevron-right" class="w-4 h-4" />
      <NuxtLink to="/courses" class="hover:text-slate-900 no-underline transition-colors">全部课程</NuxtLink>
      <Icon name="heroicons:chevron-right" class="w-4 h-4" />
      <span class="text-brand-500">{{ stage?.title }}</span>
    </nav>

    <!-- 加载中 -->
    <div v-if="loading" class="text-center py-16 text-slate-500 text-lg">
      <div class="inline-flex items-center gap-3">
        <svg class="animate-spin w-5 h-5 text-brand-500" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
        加载中...
      </div>
    </div>

    <div v-else-if="stage">
      <!-- 阶段信息 -->
      <div class="card-light rounded-6xl p-8 md:p-12 mb-12">
        <div class="flex items-start gap-6 mb-8">
          <div class="flex-shrink-0">
            <UiStageIcon :emoji="stage.icon" size="lg" />
          </div>
          <div>
            <div class="flex items-center gap-3 mb-3">
              <span
                v-if="stage.is_free"
                class="text-sm font-bold text-emerald-600 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-lg"
              >
                免费
              </span>
            </div>
            <h1 class="text-3xl md:text-4xl font-black text-slate-900 mb-3">{{ stage.title }}</h1>
            <p class="text-xl text-slate-600 mb-3">{{ stage.subtitle }}</p>
            <p class="text-lg text-slate-500">{{ stage.description }}</p>
          </div>
        </div>
      </div>

      <!-- 课程列表 -->
      <div>
        <h2 class="text-2xl font-black text-slate-900 mb-8 flex items-center gap-3">
          <div class="w-1.5 h-8 bg-brand-500 rounded-full" />
          课程目录（{{ stage.lessons?.length || 0 }} 节课）
        </h2>
        <div class="space-y-3">
          <NuxtLink
            v-for="lesson in stage.lessons"
            :key="lesson.id"
            :to="`/courses/${stage.id}/${lesson.id}`"
            class="group flex items-center justify-between p-5 md:p-6 card-light rounded-4xl hover:bg-slate-50 transition-all no-underline"
          >
            <div class="flex items-center gap-5">
              <div class="w-10 h-10 rounded-xl bg-brand-50 border border-brand-200 flex items-center justify-center text-brand-600 font-black text-sm flex-shrink-0">
                {{ lesson.lesson_number }}
              </div>
              <div>
                <h4 class="text-lg font-bold text-slate-700 group-hover:text-slate-900 transition-colors">
                  {{ lesson.title }}
                </h4>
                <p v-if="lesson.summary" class="text-slate-500 text-sm mt-1">{{ lesson.summary }}</p>
              </div>
            </div>
            <div class="flex items-center gap-3 flex-shrink-0">
              <span v-if="lesson.duration_minutes" class="text-slate-500 text-sm font-bold bg-slate-100 px-3 py-1 rounded-lg">
                {{ lesson.duration_minutes }}分钟
              </span>
              <span
                v-if="lesson.is_free"
                class="text-emerald-600 text-xs font-bold bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-lg"
              >
                免费
              </span>
              <Icon name="heroicons:chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-brand-500 transition-colors" />
            </div>
          </NuxtLink>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-16 text-slate-500 text-lg">
      该分类不存在
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const api = useApi()
const loading = ref(true)
const stage = ref<any>(null)

onMounted(async () => {
  try {
    stage.value = await api.get<any>(`/stages/${route.params.stageId}`)
  } catch (e) {
    console.error('获取阶段数据失败:', e)
  } finally {
    loading.value = false
  }
})

useHead({
  title: computed(() => stage.value ? `${stage.value.title} - AI不难学` : 'AI不难学'),
})
</script>
