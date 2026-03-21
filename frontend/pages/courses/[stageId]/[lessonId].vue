<template>
  <div class="max-w-5xl mx-auto px-4 md:px-6 pt-8 md:pt-12 pb-32">
    <!-- 阅读进度条 -->
    <div class="reading-progress-bar" :style="{ width: readingProgress + '%' }" />

    <!-- 加载中 -->
    <div v-if="loading" class="text-center py-24 text-slate-400">
      <svg class="animate-spin w-8 h-8 text-brand-500 mx-auto mb-4" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
      课程加载中...
    </div>

    <div v-else-if="lesson">
      <!-- 面包屑 + 返回 -->
      <nav class="flex items-center gap-2 text-sm text-slate-400 font-medium mb-8 flex-wrap">
        <NuxtLink to="/courses" class="hover:text-slate-700 no-underline transition-colors flex items-center gap-1.5">
          <Icon name="heroicons:chevron-left" class="w-4 h-4" />
          全部课程
        </NuxtLink>
        <span class="text-slate-300">/</span>
        <NuxtLink
          v-if="lesson.stage"
          :to="`/courses/${lesson.stage.id}`"
          class="hover:text-slate-700 no-underline transition-colors"
        >
          {{ lesson.stage.title }}
        </NuxtLink>
        <span class="text-slate-300">/</span>
        <span class="text-slate-600">{{ lesson.title }}</span>
      </nav>

      <!-- 同分类课程横向导航（带箭头） -->
      <div v-if="stageLessons.length > 1" class="mb-8 -mx-1 relative">
        <!-- 左箭头 -->
        <button
          v-show="canScrollLeft"
          class="scroll-arrow scroll-arrow-left"
          @click="scrollNav('left')"
        >
          <Icon name="heroicons:chevron-left" class="w-4 h-4" />
        </button>
        <div ref="navScrollRef" class="flex gap-2 overflow-x-auto pb-2 scrollbar-hide px-8" @scroll="updateScrollState">
          <NuxtLink
            v-for="l in stageLessons"
            :key="l.id"
            :ref="(el: any) => { if (l.id === lesson?.id) activeTabRef = el?.$el || el }"
            :to="`/courses/${route.params.stageId}/${l.id}`"
            class="flex-shrink-0 px-4 py-2.5 rounded-xl text-sm font-bold no-underline transition-all whitespace-nowrap"
            :class="l.id === lesson?.id
              ? 'bg-brand-500 text-white shadow-md shadow-brand-500/20'
              : 'bg-slate-100 text-slate-500 hover:bg-slate-200 hover:text-slate-700'"
          >
            {{ l.title }}
          </NuxtLink>
        </div>
        <!-- 右箭头 -->
        <button
          v-show="canScrollRight"
          class="scroll-arrow scroll-arrow-right"
          @click="scrollNav('right')"
        >
          <Icon name="heroicons:chevron-right" class="w-4 h-4" />
        </button>
      </div>

      <!-- 文章正文 -->
      <article class="lesson-article">
        <!-- 标题区 -->
        <header class="mb-10 pb-8 border-b border-slate-100">
          <div class="flex items-center gap-2.5 mb-5 flex-wrap">
            <span class="text-sm font-bold text-brand-600 bg-brand-50 px-3 py-1 rounded-full">
              第{{ lesson.lesson_number }}课
            </span>
            <span v-if="lesson.duration_minutes" class="text-sm text-slate-400 font-medium bg-slate-50 px-3 py-1 rounded-full">
              约{{ lesson.duration_minutes }}分钟
            </span>
            <span
              v-if="lesson.is_free"
              class="text-sm font-bold text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full"
            >
              免费
            </span>
          </div>
          <h1 class="text-2xl md:text-3xl font-black text-slate-900 leading-snug mb-3">{{ lesson.title }}</h1>
          <p v-if="lesson.subtitle" class="text-lg text-slate-400">{{ lesson.subtitle }}</p>
        </header>

        <!-- Markdown 内容 -->
        <div class="lesson-content" v-html="renderedContent" />

        <!-- 上下课导航 -->
        <div class="mt-16 pt-8 border-t border-slate-100">
          <div class="grid gap-4" :class="prevLesson && nextLesson ? 'grid-cols-1 sm:grid-cols-2' : 'grid-cols-1'">
            <NuxtLink
              v-if="prevLesson"
              :to="`/courses/${route.params.stageId}/${prevLesson.id}`"
              class="nav-prev group no-underline"
            >
              <Icon name="heroicons:chevron-left" class="w-5 h-5 text-slate-300 group-hover:text-slate-500 group-hover:-translate-x-1 transition-all flex-shrink-0" />
              <div>
                <div class="text-xs text-slate-400 mb-1 font-medium">上一课</div>
                <div class="text-base font-bold text-slate-600 group-hover:text-slate-900 transition-colors">{{ prevLesson.title }}</div>
              </div>
            </NuxtLink>
            <NuxtLink
              v-if="nextLesson"
              :to="`/courses/${route.params.stageId}/${nextLesson.id}`"
              class="nav-next group no-underline"
              :class="!prevLesson ? 'sm:col-start-2' : ''"
            >
              <div class="text-right">
                <div class="text-xs text-slate-400 mb-1 font-medium">下一课</div>
                <div class="text-base font-bold text-slate-600 group-hover:text-slate-900 transition-colors">{{ nextLesson.title }}</div>
              </div>
              <Icon name="heroicons:chevron-right" class="w-5 h-5 text-slate-300 group-hover:text-brand-500 group-hover:translate-x-1 transition-all flex-shrink-0" />
            </NuxtLink>
          </div>
        </div>
      </article>
    </div>

    <div v-else class="text-center py-24 text-slate-400 text-lg">
      课程不存在
    </div>

    <!-- 浮动目录按钮 -->
    <button
      v-if="lesson && allStages.length"
      class="catalog-fab"
      @click="catalogOpen = true"
    >
      <Icon name="heroicons:bars-4" class="w-5 h-5" />
      <span class="hidden sm:inline text-sm font-bold">目录</span>
    </button>

    <!-- 课程目录侧边面板 -->
    <Teleport to="body">
      <Transition name="catalog">
        <div v-if="catalogOpen" class="catalog-overlay" @click.self="catalogOpen = false">
          <div class="catalog-panel">
            <!-- 面板头 -->
            <div class="flex items-center justify-between px-6 py-5 border-b border-slate-100">
              <h3 class="text-lg font-black text-slate-900">全部课程目录</h3>
              <button class="w-9 h-9 rounded-xl bg-slate-100 hover:bg-slate-200 flex items-center justify-center transition-colors min-h-0" @click="catalogOpen = false">
                <Icon name="heroicons:x-mark" class="w-5 h-5 text-slate-500" />
              </button>
            </div>
            <!-- 面板内容 -->
            <div class="catalog-body">
              <div v-for="stage in allStages" :key="stage.id" class="mb-6">
                <div class="flex items-center gap-3 px-5 py-3">
                  <UiStageIcon :emoji="stage.icon" size="sm" />
                  <span class="text-sm font-black text-slate-900">{{ stage.title }}</span>
                  <span class="text-xs text-slate-400 font-medium">{{ stage.lessons?.length || 0 }}节</span>
                </div>
                <div class="space-y-0.5 px-3">
                  <NuxtLink
                    v-for="(l, lIdx) in stage.lessons"
                    :key="l.id"
                    :to="`/courses/${stage.id}/${l.id}`"
                    class="catalog-lesson no-underline"
                    :class="l.id === lesson?.id ? 'catalog-lesson-active' : ''"
                    @click="catalogOpen = false"
                  >
                    <span
                      class="w-6 h-6 rounded-md flex items-center justify-center text-xs font-bold flex-shrink-0"
                      :class="l.id === lesson?.id ? 'bg-brand-500 text-white' : 'bg-slate-100 text-slate-400'"
                    >
                      {{ lIdx + 1 }}
                    </span>
                    <span class="text-sm" :class="l.id === lesson?.id ? 'font-bold text-brand-600' : 'text-slate-600'">
                      {{ l.title }}
                    </span>
                    <!-- 当前课标记 -->
                    <span v-if="l.id === lesson?.id" class="ml-auto text-[10px] font-bold text-brand-500 bg-brand-50 px-2 py-0.5 rounded-full flex-shrink-0">
                      当前
                    </span>
                  </NuxtLink>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const api = useApi()

const loading = ref(true)
const lesson = ref<any>(null)
const stageLessons = ref<any[]>([])
const allStages = ref<any[]>([])
const catalogOpen = ref(false)
const readingProgress = ref(0)

// 阅读进度条
function updateReadingProgress() {
  const scrollTop = window.scrollY
  const docHeight = document.documentElement.scrollHeight - window.innerHeight
  readingProgress.value = docHeight > 0 ? Math.min((scrollTop / docHeight) * 100, 100) : 0
}

// 横向导航滚动控制
const navScrollRef = ref<HTMLElement | null>(null)
const activeTabRef = ref<HTMLElement | null>(null)
const canScrollLeft = ref(false)
const canScrollRight = ref(false)

function updateScrollState() {
  const el = navScrollRef.value
  if (!el) return
  canScrollLeft.value = el.scrollLeft > 8
  canScrollRight.value = el.scrollLeft < el.scrollWidth - el.clientWidth - 8
}

function scrollNav(dir: 'left' | 'right') {
  const el = navScrollRef.value
  if (!el) return
  el.scrollBy({ left: dir === 'left' ? -200 : 200, behavior: 'smooth' })
}

function scrollToActiveTab() {
  nextTick(() => {
    const tab = activeTabRef.value
    const container = navScrollRef.value
    if (!tab || !container) return
    const tabRect = tab.getBoundingClientRect()
    const containerRect = container.getBoundingClientRect()
    if (tabRect.left < containerRect.left || tabRect.right > containerRect.right) {
      tab.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' })
    }
    updateScrollState()
  })
}

// 简单的 Markdown 渲染
function renderMarkdown(md: string): string {
  if (!md) return ''
  let html = md
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^> (.+)$/gm, '<blockquote><p>$1</p></blockquote>')
    .replace(/^---$/gm, '<hr>')
    .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1">')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
    .replace(/^\|(.+)\|$/gm, (match) => {
      const cells = match.split('|').filter(c => c.trim())
      return '<tr>' + cells.map(c => {
        const trimmed = c.trim()
        if (trimmed.match(/^[-:]+$/)) return ''
        return `<td>${trimmed}</td>`
      }).join('') + '</tr>'
    })
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/\n\n/g, '</p><p>')

  html = html.replace(/<\/blockquote>\s*<blockquote>/g, '')
  html = html.replace(/<tr><\/tr>/g, '')
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
  html = html.replace(/(<tr>.*<\/tr>)/s, '<table>$1</table>')
  html = '<p>' + html + '</p>'
  html = html.replace(/<p>\s*<(h[1-6]|blockquote|pre|ul|ol|table|hr)/g, '<$1')
  html = html.replace(/<\/(h[1-6]|blockquote|pre|ul|ol|table)>\s*<\/p>/g, '</$1>')

  return html
}

const renderedContent = computed(() => renderMarkdown(lesson.value?.content || ''))

const prevLesson = computed(() => {
  if (!lesson.value || !stageLessons.value.length) return null
  const idx = stageLessons.value.findIndex((l: any) => l.id === lesson.value.id)
  return idx > 0 ? stageLessons.value[idx - 1] : null
})

const nextLesson = computed(() => {
  if (!lesson.value || !stageLessons.value.length) return null
  const idx = stageLessons.value.findIndex((l: any) => l.id === lesson.value.id)
  return idx < stageLessons.value.length - 1 ? stageLessons.value[idx + 1] : null
})

const loadLesson = async () => {
  loading.value = true
  try {
    const [lessonData, stageData, stagesData] = await Promise.all([
      api.get<any>(`/lessons/${route.params.lessonId}`),
      api.get<any>(`/stages/${route.params.stageId}`),
      allStages.value.length ? Promise.resolve(allStages.value) : api.get<any[]>('/stages'),
    ])
    lesson.value = lessonData
    stageLessons.value = stageData.lessons || []
    allStages.value = stagesData
    scrollToActiveTab()
  } catch (e) {
    console.error('获取课程失败:', e)
  } finally {
    loading.value = false
  }
}

// ESC 关闭目录面板
function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') catalogOpen.value = false
}

onMounted(() => {
  loadLesson()
  document.addEventListener('keydown', onKeydown)
  window.addEventListener('scroll', updateReadingProgress, { passive: true })
})
onUnmounted(() => {
  document.removeEventListener('keydown', onKeydown)
  window.removeEventListener('scroll', updateReadingProgress)
})
watch(() => route.params.lessonId, loadLesson)

useHead({
  title: computed(() => lesson.value ? `${lesson.value.title} - AI不难学` : 'AI不难学'),
})
</script>

<style scoped>
/* === 阅读进度条 === */
.reading-progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: linear-gradient(90deg, #F97316, #3B82F6);
  z-index: 200;
  transition: width 0.1s linear;
  border-radius: 0 2px 2px 0;
}

.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

/* === 横向导航箭头 === */
.scroll-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-60%);
  z-index: 10;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: white;
  border: 1px solid #E2E8F0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748B;
  cursor: pointer;
  transition: all 0.2s;
  min-height: 0;
  padding: 0;
}
.scroll-arrow:hover {
  background: #F8FAFC;
  border-color: #CBD5E1;
  color: #334155;
}
.scroll-arrow-left { left: -4px; }
.scroll-arrow-right { right: -4px; }

/* === 浮动目录按钮 === */
.catalog-fab {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 50;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.25rem;
  background: linear-gradient(135deg, #F97316, #EA580C);
  color: white;
  border: none;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(249,115,22,0.35);
  cursor: pointer;
  transition: all 0.3s;
  min-height: 0;
}
.catalog-fab:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 28px rgba(249,115,22,0.45);
}

/* === 目录面板 === */
.catalog-overlay {
  position: fixed;
  inset: 0;
  z-index: 200;
  background: rgba(0,0,0,0.3);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: flex-end;
}
.catalog-panel {
  width: 380px;
  max-width: 90vw;
  height: 100%;
  background: white;
  box-shadow: -8px 0 40px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
}
.catalog-body {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 0;
}
.catalog-lesson {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.625rem 0.875rem;
  border-radius: 0.75rem;
  transition: all 0.15s;
}
.catalog-lesson:hover {
  background: #F8FAFC;
}
.catalog-lesson-active {
  background: #FFF7ED !important;
}

/* 面板动画 */
.catalog-enter-active,
.catalog-leave-active {
  transition: all 0.3s ease;
}
.catalog-enter-active .catalog-panel,
.catalog-leave-active .catalog-panel {
  transition: transform 0.3s ease;
}
.catalog-enter-from {
  opacity: 0;
}
.catalog-enter-from .catalog-panel {
  transform: translateX(100%);
}
.catalog-leave-to {
  opacity: 0;
}
.catalog-leave-to .catalog-panel {
  transform: translateX(100%);
}

.lesson-article {
  background: white;
  border: 1px solid #F1F5F9;
  border-radius: 1.5rem;
  padding: 2rem;
}
@media (min-width: 768px) {
  .lesson-article {
    padding: 3rem;
  }
}
@media (min-width: 1024px) {
  .lesson-article {
    padding: 3.5rem;
  }
}

/* === 课程内容排版 — 核心阅读体验 === */
.lesson-content {
  color: #334155;           /* slate-700，比纯黑柔和但对比度足够 */
  font-size: 1.125rem;      /* 20.25px (18px base * 1.125) */
  line-height: 2;           /* 双倍行距，中老年人阅读舒适 */
  letter-spacing: 0.02em;   /* 微微加宽字间距 */
}

.lesson-content :deep(h1) {
  font-size: 1.75rem;
  font-weight: 900;
  color: #0F172A;
  margin-top: 3rem;
  margin-bottom: 1.25rem;
  line-height: 1.3;
}
.lesson-content :deep(h2) {
  font-size: 1.5rem;
  font-weight: 800;
  color: #0F172A;
  margin-top: 2.5rem;
  margin-bottom: 1rem;
  line-height: 1.35;
  padding-left: 1rem;
  border-left: 4px solid #F97316;
}
.lesson-content :deep(h3) {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1E293B;
  margin-top: 2rem;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.lesson-content :deep(p) {
  margin-top: 1.25rem;
  margin-bottom: 1.25rem;
  color: #475569;           /* slate-600 */
}

.lesson-content :deep(strong) {
  color: #0F172A;
  font-weight: 700;
}

.lesson-content :deep(ul) {
  list-style: none;
  margin: 1.5rem 0;
  padding: 0;
}
.lesson-content :deep(ul li) {
  position: relative;
  padding-left: 1.75rem;
  margin-bottom: 0.875rem;
  color: #475569;
}
.lesson-content :deep(ul li)::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.8em;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #F97316;
}

.lesson-content :deep(ol) {
  list-style: decimal;
  list-style-position: inside;
  margin: 1.5rem 0;
  padding: 0;
}
.lesson-content :deep(ol li) {
  margin-bottom: 0.875rem;
  color: #475569;
  padding-left: 0.5rem;
}

.lesson-content :deep(blockquote) {
  background: linear-gradient(135deg, #FFF7ED, #FFFBEB);
  border-left: 4px solid #F97316;
  border-radius: 0 1rem 1rem 0;
  padding: 1.25rem 1.5rem;
  margin: 2rem 0;
  color: #92400E;
  font-weight: 500;
}
.lesson-content :deep(blockquote p) {
  margin: 0;
  color: inherit;
}

.lesson-content :deep(code) {
  background: #FFF7ED;
  color: #C2410C;
  padding: 0.15em 0.4em;
  border-radius: 0.375rem;
  font-size: 0.9em;
}

.lesson-content :deep(pre) {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 1rem;
  padding: 1.5rem;
  margin: 2rem 0;
  overflow-x: auto;
}
.lesson-content :deep(pre code) {
  background: none;
  color: #334155;
  padding: 0;
}

.lesson-content :deep(img) {
  border-radius: 1rem;
  margin: 2rem auto;
  max-width: 100%;
  border: 1px solid #E2E8F0;
}

.lesson-content :deep(hr) {
  border: none;
  border-top: 1px solid #E2E8F0;
  margin: 2.5rem 0;
}

.lesson-content :deep(a) {
  color: #3B82F6;
  text-decoration: underline;
  text-underline-offset: 3px;
  text-decoration-color: rgba(59,130,246,0.3);
}
.lesson-content :deep(a:hover) {
  color: #2563EB;
  text-decoration-color: rgba(59,130,246,0.6);
}

.lesson-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0;
  font-size: 1rem;
}
.lesson-content :deep(th),
.lesson-content :deep(td) {
  padding: 0.875rem 1rem;
  text-align: left;
  border-bottom: 1px solid #F1F5F9;
  color: #475569;
}
.lesson-content :deep(th) {
  font-weight: 700;
  color: #1E293B;
  background: #F8FAFC;
  border-bottom-width: 2px;
  border-color: #E2E8F0;
}

/* === 上下课导航 === */
.nav-prev, .nav-next {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1.125rem 1.25rem;
  border-radius: 1rem;
  border: 1px solid #F1F5F9;
  transition: all 0.2s ease;
}
.nav-prev:hover, .nav-next:hover {
  border-color: #E2E8F0;
  background: #FAFAFA;
}
.nav-next {
  justify-content: flex-end;
}
</style>
