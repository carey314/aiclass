<template>
  <div>
    <!-- 骨架屏 -->
    <div v-if="loading" class="space-y-6">
      <div class="skeleton h-28 w-full rounded-2xl"></div>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-5">
        <div v-for="i in 6" :key="i" class="skeleton h-36 rounded-2xl"></div>
      </div>
    </div>

    <template v-else>
      <!-- 欢迎横幅 -->
      <div class="mb-8 relative overflow-hidden" style="background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); border-radius: 1rem; padding: 28px 32px; box-shadow: 0 4px 20px rgba(79,70,229,0.35);">
        <!-- 装饰圆 -->
        <div class="absolute -right-10 -top-10 w-40 h-40 rounded-full" style="background: rgba(255,255,255,0.1);"></div>
        <div class="absolute right-20 -bottom-8 w-24 h-24 rounded-full" style="background: rgba(255,255,255,0.05);"></div>
        <div class="relative z-10 flex items-center justify-between">
          <div>
            <div style="font-size: 24px; font-weight: 900; color: #FFFFFF; margin-bottom: 6px;">{{ greeting }}，{{ authStore.user?.display_name || '管理员' }}</div>
            <div style="font-size: 14px; color: rgba(255,255,255,0.8);">
              今天是 {{ todayDate }}，目前有 <span style="color: #FFFFFF; font-weight: 700;">{{ stats.published_lessons }}</span> 节课程已发布
              <template v-if="stats.draft_lessons">，<span style="color: #FFFFFF; font-weight: 700;">{{ stats.draft_lessons }}</span> 篇草稿待处理</template>
            </div>
          </div>
          <NuxtLink to="/admin/lessons/create"
            class="hidden md:inline-flex items-center gap-2 no-underline px-5 py-2.5 rounded-xl transition-all"
            style="background: rgba(255,255,255,0.2); color: #FFFFFF; font-size: 14px; font-weight: 700; backdrop-filter: blur(4px);">
            <Icon name="heroicons:plus" class="w-4 h-4" />
            创建课程
          </NuxtLink>
        </div>
      </div>

      <!-- 统计卡片 - 彩色渐变风格 -->
      <div class="grid grid-cols-2 md:grid-cols-3 gap-5 mb-8">
        <div v-for="(card, i) in statCards" :key="i"
             class="stat-card group relative overflow-hidden"
             :class="card.cardClass">
          <!-- 装饰圆 -->
          <div class="absolute -right-6 -top-6 w-24 h-24 rounded-full opacity-[0.08] group-hover:opacity-[0.15] group-hover:scale-125 transition-all duration-700"
               :class="card.decoClass"></div>
          <div class="absolute -right-3 -bottom-3 w-16 h-16 rounded-full opacity-[0.05] group-hover:opacity-[0.10] transition-all duration-700"
               :class="card.decoClass"></div>
          <!-- 内容 -->
          <div class="relative z-10">
            <div class="flex items-start justify-between mb-4">
              <div class="w-12 h-12 rounded-xl flex items-center justify-center" :class="card.iconBg">
                <Icon :name="card.icon" class="w-6 h-6" :class="card.iconColor" />
              </div>
            </div>
            <div class="text-3xl font-black text-slate-900 mb-1">{{ card.value }}</div>
            <div class="text-sm text-slate-500 font-medium">{{ card.label }}</div>
          </div>
        </div>
      </div>

      <!-- 两栏布局 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 最近更新 -->
        <div class="lg:col-span-2">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-1 h-6 bg-brand-500 rounded-full"></div>
            <span class="text-base font-bold text-slate-900">最近更新</span>
          </div>
          <div class="admin-card p-0 overflow-hidden">
            <template v-if="stats.recent_lessons.length">
              <NuxtLink
                v-for="lesson in stats.recent_lessons"
                :key="lesson.id"
                :to="`/admin/lessons/${lesson.id}`"
                class="flex items-center gap-3 px-5 py-3.5 no-underline group transition-colors hover:bg-brand-50/30 border-b border-slate-100 last:border-b-0"
              >
                <div class="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center flex-shrink-0 group-hover:bg-brand-50 transition-colors">
                  <Icon name="heroicons:document-text" class="w-4 h-4 text-slate-400 group-hover:text-brand-500 transition-colors" />
                </div>
                <div class="flex-1 min-w-0">
                  <span class="text-sm font-semibold text-slate-800 group-hover:text-brand-600 transition-colors">{{ lesson.title }}</span>
                  <div class="flex items-center gap-2 mt-0.5">
                    <span class="text-xs text-slate-400">{{ lesson.stage_title }}</span>
                    <span class="text-xs text-slate-300">·</span>
                    <span class="text-xs text-slate-400">{{ relativeTime(lesson.updated_at) }}</span>
                  </div>
                </div>
                <span class="text-xs font-bold px-2.5 py-1 rounded-md flex-shrink-0"
                  :class="lesson.is_published ? 'text-emerald-700 bg-emerald-50' : 'text-amber-600 bg-amber-50'">
                  {{ lesson.is_published ? '已发布' : '草稿' }}
                </span>
                <Icon name="heroicons:chevron-right" class="w-4 h-4 text-slate-300 group-hover:text-brand-500 transition-colors flex-shrink-0" />
              </NuxtLink>
            </template>
            <div v-else class="py-16 text-center">
              <Icon name="heroicons:document" class="w-10 h-10 text-slate-200 mx-auto mb-3" />
              <p class="text-sm text-slate-400">暂无课程数据</p>
            </div>
          </div>
        </div>

        <!-- 快捷操作 -->
        <div>
          <div class="flex items-center gap-3 mb-4">
            <div class="w-1 h-6 bg-brand-500 rounded-full"></div>
            <span class="text-base font-bold text-slate-900">快捷操作</span>
          </div>
          <div class="space-y-3">
            <NuxtLink
              v-for="item in shortcuts"
              :key="item.to"
              :to="item.to"
              class="admin-card flex items-center gap-4 no-underline group p-4"
            >
              <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0" :class="item.iconBg">
                <Icon :name="item.icon" class="w-5 h-5" :class="item.iconColor" />
              </div>
              <div class="flex-1">
                <span class="text-sm font-bold text-slate-800 group-hover:text-brand-600 transition-colors">{{ item.label }}</span>
                <p class="text-xs text-slate-400 mt-0.5">{{ item.desc }}</p>
              </div>
              <Icon name="heroicons:chevron-right" class="w-4 h-4 text-slate-300 group-hover:text-brand-500 transition-all flex-shrink-0" />
            </NuxtLink>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

definePageMeta({
  layout: 'admin',
  middleware: ['admin-auth'],
})

useHead({ title: '管理后台 - AI不难学' })

const authStore = useAuthStore()
const adminApi = useAdminApi()
const loading = ref(true)
const stats = ref({
  total_stages: 0,
  total_lessons: 0,
  published_lessons: 0,
  draft_lessons: 0,
  total_media: 0,
  total_duration_minutes: 0,
  recent_lessons: [] as any[],
})

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 6) return '夜深了'
  if (h < 12) return '早上好'
  if (h < 14) return '中午好'
  if (h < 18) return '下午好'
  return '晚上好'
})

const todayDate = computed(() => {
  const d = new Date()
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
})

const formattedDuration = computed(() => {
  const mins = stats.value.total_duration_minutes
  if (!mins) return '0分'
  const h = Math.floor(mins / 60)
  const m = mins % 60
  return h ? `${h}小时${m ? m + '分' : ''}` : `${m}分`
})

const statCards = computed(() => [
  { icon: 'heroicons:folder-open', iconBg: 'bg-blue-100 shadow-sm shadow-blue-200/50', iconColor: 'text-blue-600', cardClass: 'stat-blue', decoClass: 'bg-blue-500', label: '工具分类', value: stats.value.total_stages },
  { icon: 'heroicons:document-text', iconBg: 'bg-violet-100 shadow-sm shadow-violet-200/50', iconColor: 'text-violet-600', cardClass: 'stat-violet', decoClass: 'bg-violet-500', label: '课程总数', value: stats.value.total_lessons },
  { icon: 'heroicons:check-circle', iconBg: 'bg-teal-100 shadow-sm shadow-teal-200/50', iconColor: 'text-teal-600', cardClass: 'stat-teal', decoClass: 'bg-teal-500', label: '已发布', value: stats.value.published_lessons },
  { icon: 'heroicons:pencil-square', iconBg: 'bg-amber-100 shadow-sm shadow-amber-200/50', iconColor: 'text-amber-600', cardClass: 'stat-amber', decoClass: 'bg-amber-500', label: '草稿', value: stats.value.draft_lessons },
  { icon: 'heroicons:photo', iconBg: 'bg-rose-100 shadow-sm shadow-rose-200/50', iconColor: 'text-rose-600', cardClass: 'stat-rose', decoClass: 'bg-rose-500', label: '媒体文件', value: stats.value.total_media },
  { icon: 'heroicons:clock', iconBg: 'bg-indigo-100 shadow-sm shadow-indigo-200/50', iconColor: 'text-indigo-600', cardClass: 'stat-indigo', decoClass: 'bg-indigo-500', label: '总时长', value: formattedDuration.value },
])

const shortcuts = [
  { icon: 'heroicons:plus-circle', iconBg: 'bg-brand-50 border border-brand-200', iconColor: 'text-brand-500', label: '新增课程', desc: '创建一节新课程', to: '/admin/lessons/create' },
  { icon: 'heroicons:folder-open', iconBg: 'bg-blue-50 border border-blue-200', iconColor: 'text-blue-500', label: '分类管理', desc: '管理工具分类和排序', to: '/admin/courses' },
  { icon: 'heroicons:document-text', iconBg: 'bg-violet-50 border border-violet-200', iconColor: 'text-violet-500', label: '课程管理', desc: '编辑和发布课程内容', to: '/admin/lessons' },
  { icon: 'heroicons:photo', iconBg: 'bg-rose-50 border border-rose-200', iconColor: 'text-rose-500', label: '媒体库', desc: '管理图片和文件资源', to: '/admin/media' },
]

const relativeTime = (dateStr: string) => {
  const now = Date.now()
  const diff = now - new Date(dateStr).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return '刚刚'
  if (mins < 60) return `${mins}分钟前`
  const hours = Math.floor(mins / 60)
  if (hours < 24) return `${hours}小时前`
  const days = Math.floor(hours / 24)
  return `${days}天前`
}

onMounted(async () => {
  try {
    stats.value = await adminApi.get<any>('/admin/dashboard/stats')
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
/* === 统计卡片 — 彩色渐变，参考用户端课程卡片 === */
.stat-card {
  border-radius: 1.25rem;
  padding: 1.5rem;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid transparent;
}
.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.1);
}

.stat-blue {
  background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
  border-color: #BFDBFE;
}
.stat-blue:hover { border-color: #93C5FD; }

.stat-violet {
  background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
  border-color: #DDD6FE;
}
.stat-violet:hover { border-color: #C4B5FD; }

.stat-teal {
  background: linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 100%);
  border-color: #99F6E4;
}
.stat-teal:hover { border-color: #5EEAD4; }

.stat-amber {
  background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
  border-color: #FDE68A;
}
.stat-amber:hover { border-color: #FCD34D; }

.stat-rose {
  background: linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 100%);
  border-color: #FECDD3;
}
.stat-rose:hover { border-color: #FDA4AF; }

.stat-indigo {
  background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
  border-color: #C7D2FE;
}
.stat-indigo:hover { border-color: #A5B4FC; }
</style>
