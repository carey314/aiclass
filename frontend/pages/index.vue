<template>
  <div>
    <!-- Hero Section -->
    <section class="relative min-h-[85vh] flex items-center justify-center overflow-hidden py-20">
      <!-- 背景 -->
      <div class="absolute inset-0 hero-bg" />
      <!-- 渐变光球 -->
      <div class="absolute inset-0 overflow-hidden pointer-events-none">
        <div class="hero-orb hero-orb-blue absolute top-[10%] left-[5%] w-40 h-40 md:w-72 md:h-72" />
        <div class="hero-orb hero-orb-orange absolute bottom-[10%] right-[5%] w-40 h-40 md:w-72 md:h-72" />
        <div class="hero-orb hero-orb-purple absolute top-[40%] right-[20%] w-32 h-32 md:w-56 md:h-56" />
      </div>
      <!-- 点阵图案 -->
      <div class="absolute inset-0 hero-dots pointer-events-none" />
      <!-- 底部波浪 -->
      <div class="hero-wave" />

      <div class="max-w-5xl mx-auto px-6 relative z-10 text-center">
        <!-- 标签 -->
        <div class="hero-enter hero-enter-1 inline-flex items-center gap-2.5 px-6 py-3 rounded-full bg-white/80 backdrop-blur-sm text-brand-600 border border-brand-200/60 text-sm font-bold mb-10 shadow-sm">
          <span class="relative flex h-2.5 w-2.5">
            <span class="animate-ping-slow absolute inline-flex h-full w-full rounded-full bg-emerald-500 opacity-75" />
            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500" />
          </span>
          2026 全新升级 · 已有 1.2万+ 学员
        </div>

        <h1 class="hero-enter hero-enter-2 text-4xl md:text-5xl lg:text-6xl font-black leading-[1.15] mb-8 text-slate-900 tracking-tight">
          让每一位长辈<br>
          轻松玩转 <span class="hero-highlight">AI 智能工具</span>
        </h1>

        <p class="hero-enter hero-enter-3 text-lg md:text-xl text-slate-500 mb-12 max-w-2xl mx-auto leading-relaxed">
          不教代码、不讲术语，只用大白话。<br class="hidden md:block">
          一部手机，从"看不懂"到"玩得溜"，24节课全部免费。
        </p>

        <div class="hero-enter hero-enter-4 flex flex-col sm:flex-row items-center justify-center gap-4">
          <NuxtLink to="/courses" class="btn-hero no-underline group">
            免费开始学习
            <Icon name="heroicons:chevron-right" class="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </NuxtLink>
          <NuxtLink to="/about" class="btn-hero-outline no-underline">
            了解更多
          </NuxtLink>
        </div>

        <!-- 信任指标 -->
        <div class="hero-enter hero-enter-5 mt-14 flex items-center justify-center gap-8 md:gap-12 text-sm text-slate-400">
          <div class="flex items-center gap-2">
            <Icon name="heroicons:check-20-solid" class="w-4 h-4 text-emerald-500" />
            <span>完全免费</span>
          </div>
          <div class="flex items-center gap-2">
            <Icon name="heroicons:check-20-solid" class="w-4 h-4 text-emerald-500" />
            <span>无需基础</span>
          </div>
          <div class="flex items-center gap-2">
            <Icon name="heroicons:check-20-solid" class="w-4 h-4 text-emerald-500" />
            <span>手机就能学</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 课程分类 — Bento Grid -->
    <section class="py-20 md:py-28 px-6">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-14 md:mb-20" data-reveal>
          <div class="inline-block px-4 py-1.5 rounded-full bg-brand-50 text-brand-600 text-sm font-bold mb-5 border border-brand-100">
            📚 课程体系
          </div>
          <h2 class="text-3xl md:text-4xl font-black text-slate-900 mb-4">
            6大分类，24节实战课
          </h2>
          <p class="text-lg text-slate-500 max-w-xl mx-auto">覆盖当下最热门的国产AI工具，从入门到进阶，想学什么点什么</p>
        </div>

        <!-- 骨架屏加载 -->
        <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 md:gap-6">
          <div
            v-for="i in 6"
            :key="i"
            class="skeleton-card"
            :class="i === 1 ? 'lg:col-span-2' : ''"
          >
            <div class="flex items-start gap-5 p-7 md:p-9">
              <div class="skeleton-circle w-14 h-14 flex-shrink-0" />
              <div class="flex-1 space-y-3">
                <div class="skeleton-line w-2/3 h-6" />
                <div class="skeleton-line w-full h-4" />
                <div class="skeleton-line w-1/3 h-5 mt-4" />
              </div>
            </div>
          </div>
        </div>

        <!-- Bento Grid 课程卡片 -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 md:gap-6">
          <NuxtLink
            v-for="(stage, idx) in stages"
            :key="stage.id"
            :to="`/courses/${stage.id}`"
            class="course-card group no-underline block relative overflow-hidden"
            :class="[
              cardThemes[idx]?.cardClass || 'card-default',
              idx === 0 ? 'lg:col-span-2 lg:row-span-1' : ''
            ]"
            data-reveal
            :data-reveal-delay="idx * 100"
          >
            <!-- 背景装饰圆 -->
            <div
              class="absolute -right-8 -top-8 w-32 h-32 rounded-full opacity-[0.08] group-hover:opacity-[0.15] group-hover:scale-125 transition-all duration-700"
              :class="cardThemes[idx]?.decoClass || 'bg-slate-400'"
            />
            <div
              class="absolute -right-4 -bottom-4 w-20 h-20 rounded-full opacity-[0.05] group-hover:opacity-[0.10] transition-all duration-700"
              :class="cardThemes[idx]?.decoClass || 'bg-slate-400'"
            />

            <div class="relative z-10 p-7 md:p-9" :class="idx === 0 ? 'lg:flex lg:items-center lg:gap-10' : ''">
              <!-- 大图标 -->
              <div class="mb-5 transition-all duration-500 group-hover:scale-110 group-hover:rotate-3" :class="idx === 0 ? 'lg:mb-0' : ''">
                <UiStageIcon :emoji="stage.icon" size="lg" />
              </div>

              <!-- 文本区域 -->
              <div class="flex-1">
                <h3 class="text-xl md:text-2xl font-black text-slate-900 mb-2 leading-tight">
                  {{ stage.title }}
                </h3>
                <p class="text-slate-500 text-base leading-relaxed mb-4">{{ stage.subtitle }}</p>

                <!-- 底部信息 -->
                <div class="flex items-center gap-3 flex-wrap">
                  <span
                    class="inline-flex items-center gap-1.5 text-sm font-bold px-3 py-1 rounded-full"
                    :class="cardThemes[idx]?.badgeClass || 'bg-slate-100 text-slate-600'"
                  >
                    <Icon name="heroicons:book-open" class="w-3.5 h-3.5" />
                    {{ stage.lessons?.length || 0 }} 节课
                  </span>
                  <span class="text-xs font-bold text-emerald-600 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded-full">
                    免费
                  </span>
                </div>
              </div>

              <!-- 箭头指示器 -->
              <div
                class="absolute right-7 md:right-9 bottom-7 md:bottom-9 w-10 h-10 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 group-hover:translate-x-1"
                :class="cardThemes[idx]?.arrowClass || 'bg-slate-200 text-slate-600'"
              >
                <Icon name="heroicons:chevron-right" class="w-5 h-5" />
              </div>
            </div>
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- 4大优势 -->
    <section class="py-20 md:py-28 px-6 bg-slate-50/80">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-14 md:mb-20" data-reveal>
          <div class="inline-block px-4 py-1.5 rounded-full bg-trust-50 text-trust-600 text-sm font-bold mb-5 border border-trust-100">
            💎 核心优势
          </div>
          <h2 class="text-3xl md:text-4xl font-black text-slate-900 mb-4">
            为什么选择AI不难学
          </h2>
          <p class="text-lg text-slate-500">专为中老年朋友打造，让学习不再是负担</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5 md:gap-6">
          <div
            v-for="(point, idx) in sellingPoints"
            :key="idx"
            class="advantage-card group"
            data-reveal
            :data-reveal-delay="idx * 100"
          >
            <div class="flex items-start gap-6">
              <div
                class="w-14 h-14 rounded-2xl flex items-center justify-center flex-shrink-0 transition-all duration-500 group-hover:scale-110"
                :class="point.iconBg"
              >
                <Icon :name="point.icon" class="w-7 h-7" :class="point.iconColor" />
              </div>
              <div>
                <h3 class="text-xl font-black text-slate-900 mb-2">{{ point.title }}</h3>
                <p class="text-slate-500 text-base leading-relaxed">{{ point.desc }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 数据统计 -->
    <section class="py-16 md:py-20 px-6 bg-white">
      <div class="max-w-5xl mx-auto">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-5 md:gap-8" data-reveal>
          <div v-for="(stat, idx) in heroStats" :key="idx" class="text-center">
            <div class="text-3xl md:text-4xl font-black mb-1" :class="stat.color">
              <span :data-count-target="stat.num" :data-count-suffix="stat.suffix">0</span>
            </div>
            <div class="text-slate-400 text-sm font-bold">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 适合人群 -->
    <section class="py-20 md:py-28 px-6">
      <div class="max-w-5xl mx-auto">
        <div class="text-center mb-14 md:mb-20" data-reveal>
          <div class="inline-block px-4 py-1.5 rounded-full bg-purple-50 text-purple-600 text-sm font-bold mb-5 border border-purple-100">
            🎯 适合人群
          </div>
          <h2 class="text-3xl md:text-4xl font-black text-slate-900 mb-4">
            这门课适合谁？
          </h2>
          <p class="text-lg text-slate-500">只要你愿意学，就是我们的同学</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 md:gap-6">
          <div
            v-for="(audience, idx) in audiences"
            :key="idx"
            class="audience-card group text-center"
            data-reveal
            :data-reveal-delay="idx * 120"
          >
            <div
              class="w-20 h-20 rounded-3xl flex items-center justify-center mx-auto mb-5 transition-all duration-500 group-hover:scale-110 group-hover:-rotate-3"
              :class="audience.iconBg"
            >
              <Icon :name="audience.icon" class="w-10 h-10" :class="audience.iconColor" />
            </div>
            <h3 class="text-xl font-black text-slate-900 mb-2">{{ audience.title }}</h3>
            <p class="text-slate-500 text-base leading-relaxed">{{ audience.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 学员好评 -->
    <section class="py-20 md:py-28 px-6 bg-slate-50/80">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-14 md:mb-20" data-reveal>
          <div class="inline-block px-4 py-1.5 rounded-full bg-emerald-50 text-emerald-600 text-sm font-bold mb-5 border border-emerald-100">
            💬 学员好评
          </div>
          <h2 class="text-3xl md:text-4xl font-black text-slate-900 mb-4">
            听听他们怎么说
          </h2>
          <p class="text-lg text-slate-500">来自真实学员的反馈</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 md:gap-6">
          <div
            v-for="(review, idx) in reviews"
            :key="idx"
            class="review-card"
            data-reveal
            :data-reveal-delay="idx * 100"
          >
            <!-- 星星评分 -->
            <div class="flex gap-1 mb-4">
              <Icon v-for="s in 5" :key="s" name="heroicons:star-solid" class="w-5 h-5 text-amber-400" />
            </div>
            <!-- 评价内容 -->
            <p class="text-slate-600 text-base leading-relaxed mb-6">{{ review.content }}</p>
            <!-- 用户信息 -->
            <div class="flex items-center gap-3 mt-auto">
              <div
                class="w-11 h-11 rounded-full flex items-center justify-center text-lg font-bold text-white flex-shrink-0"
                :class="review.avatarBg"
              >
                {{ review.name.charAt(0) }}
              </div>
              <div>
                <div class="text-sm font-bold text-slate-900">{{ review.name }}</div>
                <div class="text-xs text-slate-400">{{ review.role }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 学习路径 -->
    <section class="py-20 md:py-28 px-6">
      <div class="max-w-4xl mx-auto">
        <div class="text-center mb-14 md:mb-20" data-reveal>
          <div class="inline-block px-4 py-1.5 rounded-full bg-indigo-50 text-indigo-600 text-sm font-bold mb-5 border border-indigo-100">
            🗺️ 学习路径
          </div>
          <h2 class="text-3xl md:text-4xl font-black text-slate-900 mb-4">
            从零到 AI 达人，只需 4 步
          </h2>
        </div>
        <div class="relative">
          <!-- 连接线 -->
          <div class="hidden md:block absolute left-1/2 top-0 bottom-0 w-0.5 bg-gradient-to-b from-blue-200 via-brand-300 to-emerald-200 -translate-x-1/2" />
          <div class="space-y-8 md:space-y-0">
            <div
              v-for="(step, idx) in learningSteps"
              :key="idx"
              class="relative md:flex items-center"
              :class="idx % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'"
              data-reveal
              :data-reveal-delay="idx * 120"
            >
              <div class="md:w-[calc(50%-2rem)] md:px-4">
                <div class="step-card">
                  <div class="flex items-center gap-3 mb-3">
                    <span
                      class="w-9 h-9 rounded-xl flex items-center justify-center text-sm font-black text-white flex-shrink-0"
                      :class="step.numBg"
                    >
                      {{ idx + 1 }}
                    </span>
                    <h3 class="text-lg font-black text-slate-900">{{ step.title }}</h3>
                  </div>
                  <p class="text-slate-500 text-base leading-relaxed">{{ step.desc }}</p>
                </div>
              </div>
              <!-- 中间节点 -->
              <div class="hidden md:flex w-16 items-center justify-center flex-shrink-0 relative z-10">
                <div
                  class="w-10 h-10 rounded-full flex items-center justify-center shadow-lg"
                  :class="step.dotBg"
                >
                  <Icon :name="step.icon" class="w-5 h-5 text-white" />
                </div>
              </div>
              <div class="md:w-[calc(50%-2rem)]" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer CTA -->
    <section class="py-20 md:py-28 px-6">
      <div class="max-w-4xl mx-auto cta-card relative overflow-hidden" data-reveal="scale">
        <!-- 装饰 -->
        <div class="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-1/3 translate-x-1/3 blur-2xl" />
        <div class="absolute bottom-0 left-0 w-48 h-48 bg-brand-400/10 rounded-full translate-y-1/3 -translate-x-1/3 blur-2xl" />

        <div class="relative z-10 text-center px-8 py-16 md:px-16 md:py-20">
          <div class="text-5xl mb-6">🎓</div>
          <h2 class="text-3xl md:text-4xl font-black text-white mb-6 leading-tight">
            活到老，学到老<br>拥抱智能时代
          </h2>
          <p class="text-lg text-blue-200 mb-10 max-w-lg mx-auto leading-relaxed">
            24节课全部免费，零风险体验。<br>你愿意成为下一个 AI 达人吗？
          </p>
          <NuxtLink
            to="/courses"
            class="inline-flex items-center gap-2 px-10 py-5 rounded-2xl text-lg font-black text-trust-900 bg-white hover:bg-brand-50 shadow-xl hover:shadow-2xl hover:scale-105 active:scale-[0.97] transition-all no-underline"
          >
            免费开始学习
            <Icon name="heroicons:chevron-right" class="w-5 h-5" />
          </NuxtLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const api = useApi()
const loading = ref(true)
const stages = ref<any[]>([])

useScrollReveal()
useCountUp()

// 每个课程分类的独特视觉主题
const cardThemes = [
  {
    cardClass: 'card-blue',
    iconClass: 'bg-blue-100 shadow-sm shadow-blue-200/50',
    decoClass: 'bg-blue-500',
    badgeClass: 'bg-blue-100/80 text-blue-700',
    arrowClass: 'bg-blue-500 text-white',
  },
  {
    cardClass: 'card-teal',
    iconClass: 'bg-teal-100 shadow-sm shadow-teal-200/50',
    decoClass: 'bg-teal-500',
    badgeClass: 'bg-teal-100/80 text-teal-700',
    arrowClass: 'bg-teal-500 text-white',
  },
  {
    cardClass: 'card-violet',
    iconClass: 'bg-violet-100 shadow-sm shadow-violet-200/50',
    decoClass: 'bg-violet-500',
    badgeClass: 'bg-violet-100/80 text-violet-700',
    arrowClass: 'bg-violet-500 text-white',
  },
  {
    cardClass: 'card-amber',
    iconClass: 'bg-amber-100 shadow-sm shadow-amber-200/50',
    decoClass: 'bg-amber-500',
    badgeClass: 'bg-amber-100/80 text-amber-700',
    arrowClass: 'bg-amber-500 text-white',
  },
  {
    cardClass: 'card-rose',
    iconClass: 'bg-rose-100 shadow-sm shadow-rose-200/50',
    decoClass: 'bg-rose-500',
    badgeClass: 'bg-rose-100/80 text-rose-700',
    arrowClass: 'bg-rose-500 text-white',
  },
  {
    cardClass: 'card-indigo',
    iconClass: 'bg-indigo-100 shadow-sm shadow-indigo-200/50',
    decoClass: 'bg-indigo-500',
    badgeClass: 'bg-indigo-100/80 text-indigo-700',
    arrowClass: 'bg-indigo-500 text-white',
  },
]

const sellingPoints = [
  { icon: 'solar:eye-bold-duotone', title: '超大字体，看得清', desc: '全站18px以上字体、高对比度配色，专为中老年朋友优化阅读体验，再也不用眯着眼。', iconBg: 'bg-emerald-100 border border-emerald-200', iconColor: 'text-emerald-600' },
  { icon: 'solar:target-bold-duotone', title: '每课一技能，学得会', desc: '每节课只学一个技能，配合真实生活场景，学完马上就能用，绝不绕弯子。', iconBg: 'bg-blue-100 border border-blue-200', iconColor: 'text-blue-600' },
  { icon: 'solar:smartphone-bold-duotone', title: '手机就能学，门槛低', desc: '不需要电脑、不需要基础，一部智能手机就够了。下载APP就能开始。', iconBg: 'bg-purple-100 border border-purple-200', iconColor: 'text-purple-600' },
  { icon: 'solar:cup-star-bold-duotone', title: '有作品有成就，学得开心', desc: '每节课都有作品产出——AI画的画、写的信、做的视频，发朋友圈让朋友羡慕。', iconBg: 'bg-amber-100 border border-amber-200', iconColor: 'text-amber-600' },
]

const audiences = [
  { icon: 'solar:home-smile-bold-duotone', title: '退休人士', desc: '想跟上时代步伐，和子女孙辈有共同话题，让生活更有趣', iconBg: 'bg-rose-100 border border-rose-200', iconColor: 'text-rose-600' },
  { icon: 'solar:user-id-bold-duotone', title: '企业管理者', desc: '想了解AI能为企业做什么，不想被时代淘汰，提升竞争力', iconBg: 'bg-blue-100 border border-blue-200', iconColor: 'text-blue-600' },
  { icon: 'solar:shop-bold-duotone', title: '个体经营者', desc: '想用AI提高工作效率、降低成本，让生意更轻松', iconBg: 'bg-amber-100 border border-amber-200', iconColor: 'text-amber-600' },
]

const heroStats = [
  { num: 12000, suffix: '+', label: '累计学员', color: 'text-brand-500' },
  { num: 24, suffix: '节', label: '精品课程', color: 'text-trust-500' },
  { num: 99, suffix: '%', label: '好评率', color: 'text-emerald-500' },
  { num: 6, suffix: '大', label: '工具分类', color: 'text-violet-500' },
]

const reviews = [
  {
    content: '我今年56岁，以前觉得AI是年轻人的东西。学了这个课才发现，AI真的能帮我写通知、做报告，同事都问我怎么变高效了！',
    name: '张大姐',
    role: '事业单位行政人员 · 56岁',
    avatarBg: 'bg-rose-500',
  },
  {
    content: '退休后想学点新东西，试了好几个课程都太难了。这个课真的是大白话，每节课学一个技能，我现在能用AI写诗、画画了！',
    name: '李叔',
    role: '退休教师 · 62岁',
    avatarBg: 'bg-blue-500',
  },
  {
    content: '开了个小餐馆，以前写菜单、发朋友圈文案都很头疼。现在用AI几分钟就搞定，还比自己写的好看，生意都好了不少！',
    name: '王老板',
    role: '餐饮经营者 · 48岁',
    avatarBg: 'bg-amber-500',
  },
]

const learningSteps = [
  { title: '认识AI，消除恐惧', desc: '了解AI是什么、能做什么，在手机上安装你的第一个AI助手', icon: 'heroicons:light-bulb', numBg: 'bg-blue-500', dotBg: 'bg-blue-500' },
  { title: '学会对话，掌握技巧', desc: '掌握和AI对话的"问法"，让AI精准回答你的问题', icon: 'heroicons:chat-bubble-left-right', numBg: 'bg-teal-500', dotBg: 'bg-teal-500' },
  { title: '实战应用，提升效率', desc: '用AI写文章、做PPT、画图、分析数据，解决实际工作需求', icon: 'heroicons:rocket-launch', numBg: 'bg-brand-500', dotBg: 'bg-brand-500' },
  { title: '融入生活，成为达人', desc: '把AI融入日常生活，成为朋友圈里最潮的AI达人', icon: 'heroicons:star', numBg: 'bg-emerald-500', dotBg: 'bg-emerald-500' },
]

onMounted(async () => {
  try {
    stages.value = await api.get<any[]>('/stages')
  } catch (e) {
    console.error('获取课程数据失败:', e)
  } finally {
    loading.value = false
  }
})

useHead({
  title: 'AI不难学 - 中老年AI工具实战训练营',
})
</script>

<style scoped>
/* === Hero === */
.hero-bg {
  background: linear-gradient(180deg, #EFF6FF 0%, #FFF7ED 40%, #FFFBF5 100%);
}

.hero-highlight {
  background: linear-gradient(135deg, #F97316, #3B82F6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.btn-hero {
  @apply inline-flex items-center gap-2 px-10 py-5 rounded-2xl text-lg font-black text-white transition-all duration-300 active:scale-95;
  background: linear-gradient(135deg, #F97316, #FB923C);
  box-shadow: 0 4px 20px rgba(249,115,22,0.35);
}
.btn-hero:hover {
  box-shadow: 0 8px 30px rgba(249,115,22,0.45);
  transform: translateY(-2px);
}

.btn-hero-outline {
  @apply inline-flex items-center gap-2 px-10 py-5 rounded-2xl text-lg font-bold text-slate-600 transition-all duration-300 active:scale-95;
  background: white;
  border: 2px solid #E2E8F0;
}
.btn-hero-outline:hover {
  border-color: #F97316;
  color: #F97316;
  background: #FFF7ED;
}

/* === Hero 光球 === */
.hero-orb {
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.3;
}
@media (max-width: 767px) {
  .hero-orb { filter: blur(40px); opacity: 0.2; }
}
.hero-orb-blue {
  background: radial-gradient(circle, #93C5FD, #3B82F6);
  animation: orb-float 20s ease-in-out infinite;
}
.hero-orb-orange {
  background: radial-gradient(circle, #FDBA74, #F97316);
  animation: orb-float 25s ease-in-out infinite reverse;
}
.hero-orb-purple {
  background: radial-gradient(circle, #C4B5FD, #8B5CF6);
  animation: orb-float 18s ease-in-out infinite 5s;
}
@keyframes orb-float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -20px) scale(1.05); }
  50% { transform: translate(-20px, 15px) scale(0.95); }
  75% { transform: translate(15px, 25px) scale(1.02); }
}

/* === 点阵图案 === */
.hero-dots {
  background-image: radial-gradient(circle, #CBD5E1 1px, transparent 1px);
  background-size: 32px 32px;
  opacity: 0.3;
}

/* === 底部波浪 === */
.hero-wave {
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 60px;
  background: #FFFBF5;
  clip-path: ellipse(55% 100% at 50% 100%);
  z-index: 5;
}

/* === Hero 入场动画 === */
@keyframes hero-fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.hero-enter {
  opacity: 0;
  animation: hero-fade-up 0.8s ease forwards;
}
.hero-enter-1 { animation-delay: 0.1s; }
.hero-enter-2 { animation-delay: 0.2s; }
.hero-enter-3 { animation-delay: 0.35s; }
.hero-enter-4 { animation-delay: 0.5s; }
.hero-enter-5 { animation-delay: 0.65s; }

@media (prefers-reduced-motion: reduce) {
  .hero-enter { animation: none; opacity: 1; }
  .hero-orb { animation: none; }
}

/* === 课程卡片 === */
.course-card {
  border-radius: 1.5rem;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid transparent;
}
.course-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 40px -12px rgba(0,0,0,0.12);
}

.card-blue {
  background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
  border-color: #BFDBFE;
}
.card-blue:hover { border-color: #93C5FD; }

.card-teal {
  background: linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 100%);
  border-color: #99F6E4;
}
.card-teal:hover { border-color: #5EEAD4; }

.card-violet {
  background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
  border-color: #DDD6FE;
}
.card-violet:hover { border-color: #C4B5FD; }

.card-amber {
  background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
  border-color: #FDE68A;
}
.card-amber:hover { border-color: #FCD34D; }

.card-rose {
  background: linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 100%);
  border-color: #FECDD3;
}
.card-rose:hover { border-color: #FDA4AF; }

.card-indigo {
  background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
  border-color: #C7D2FE;
}
.card-indigo:hover { border-color: #A5B4FC; }

/* === 优势卡片 === */
.advantage-card {
  background: white;
  border: 1px solid #F1F5F9;
  border-radius: 1.5rem;
  padding: 2rem;
  transition: all 0.3s ease;
}
.advantage-card:hover {
  border-color: #E2E8F0;
  box-shadow: 0 8px 24px -8px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}

/* === 人群卡片 === */
.audience-card {
  background: white;
  border: 1px solid #F1F5F9;
  border-radius: 1.5rem;
  padding: 2.5rem 2rem;
  transition: all 0.3s ease;
}
.audience-card:hover {
  border-color: #E2E8F0;
  box-shadow: 0 8px 24px -8px rgba(0,0,0,0.08);
  transform: translateY(-3px);
}

/* === CTA 卡片 === */
.cta-card {
  background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 40%, #1D4ED8 100%);
  border-radius: 2.5rem;
  box-shadow: 0 25px 60px -12px rgba(30, 58, 138, 0.4);
}

/* === 骨架屏 === */
@keyframes skeleton-pulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 0.8; }
}
.skeleton-card {
  background: white;
  border: 1px solid #F1F5F9;
  border-radius: 1.5rem;
}
.skeleton-circle {
  border-radius: 1rem;
  background: linear-gradient(90deg, #F1F5F9 25%, #E2E8F0 50%, #F1F5F9 75%);
  background-size: 200% 100%;
  animation: skeleton-pulse 1.5s ease-in-out infinite;
}
.skeleton-line {
  border-radius: 0.5rem;
  background: linear-gradient(90deg, #F1F5F9 25%, #E2E8F0 50%, #F1F5F9 75%);
  background-size: 200% 100%;
  animation: skeleton-pulse 1.5s ease-in-out infinite;
}

/* === 学员评价卡片 === */
.review-card {
  background: white;
  border: 1px solid #F1F5F9;
  border-radius: 1.5rem;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}
.review-card:hover {
  border-color: #E2E8F0;
  box-shadow: 0 8px 24px -8px rgba(0,0,0,0.08);
  transform: translateY(-3px);
}

/* === 学习路径卡片 === */
.step-card {
  background: white;
  border: 1px solid #F1F5F9;
  border-radius: 1.25rem;
  padding: 1.5rem;
  transition: all 0.3s ease;
}
.step-card:hover {
  border-color: #E2E8F0;
  box-shadow: 0 4px 16px -4px rgba(0,0,0,0.06);
}
</style>
