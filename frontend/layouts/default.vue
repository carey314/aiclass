<template>
  <div class="min-h-screen flex flex-col bg-warm-white text-slate-800" :class="fontSizeClass">
    <!-- 顶部导航 -->
    <nav class="fixed top-0 w-full z-[100] transition-all duration-500">
      <div class="navbar-bg absolute inset-0" />
      <div class="max-w-7xl mx-auto px-6 h-20 relative flex items-center justify-between">
        <!-- Logo -->
        <NuxtLink to="/" class="flex items-center gap-3 no-underline group">
          <div class="w-10 h-10 bg-gradient-to-br from-brand-500 to-brand-400 rounded-xl flex items-center justify-center shadow-lg transform group-hover:rotate-12 transition-transform">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
            </svg>
          </div>
          <span class="text-2xl font-black tracking-tighter text-slate-900">AI 不难学</span>
        </NuxtLink>

        <!-- 桌面导航 -->
        <div class="hidden md:flex items-center gap-10">
          <NuxtLink
            v-for="item in navItems"
            :key="item.to"
            :to="item.to"
            class="nav-link"
            :class="{ 'nav-link-active': isActive(item.to) }"
          >
            {{ item.label }}
            <span v-if="isActive(item.to)" class="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-brand-500 to-brand-400 rounded-full" />
          </NuxtLink>
          <!-- 字体大小切换 -->
          <button
            class="font-size-btn"
            :title="`当前：${fontSizeConfig[currentFontSize].label}，点击切换`"
            @click="cycleFontSize()"
          >
            <Icon name="heroicons:magnifying-glass-plus" class="w-4 h-4" />
            <span class="text-xs font-bold">{{ fontSizeConfig[currentFontSize].label }}</span>
          </button>
          <NuxtLink
            to="/admin/login"
            class="px-5 py-2 rounded-xl text-sm font-bold bg-slate-100 border border-slate-200 hover:bg-slate-200 transition-all no-underline text-slate-600 hover:text-slate-900 min-h-0"
          >
            后台
          </NuxtLink>
        </div>

        <!-- 手机端汉堡菜单 -->
        <button class="md:hidden text-slate-700 p-2 min-h-0" @click="mobileMenuOpen = !mobileMenuOpen">
          <Icon v-if="!mobileMenuOpen" name="heroicons:bars-3" class="w-7 h-7" />
          <Icon v-else name="heroicons:x-mark" class="w-7 h-7" />
        </button>
      </div>

      <!-- 手机端菜单展开 -->
      <div
        v-if="mobileMenuOpen"
        class="md:hidden absolute top-20 left-0 w-full bg-white border-b border-slate-200 p-5 space-y-3 shadow-lg"
      >
        <NuxtLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="block w-full text-left p-4 rounded-2xl text-xl font-bold no-underline transition-colors"
          :class="isActive(item.to) ? 'bg-brand-50 text-brand-600' : 'text-slate-600 hover:text-slate-900'"
          @click="mobileMenuOpen = false"
        >
          {{ item.label }}
        </NuxtLink>
        <!-- 手机端字体切换 -->
        <button
          class="w-full text-left p-4 rounded-2xl text-xl font-bold text-slate-600 hover:text-slate-900 transition-colors flex items-center gap-3"
          @click="cycleFontSize()"
        >
          <Icon name="heroicons:magnifying-glass-plus" class="w-6 h-6" />
          字体：{{ fontSizeConfig[currentFontSize].label }}
        </button>
      </div>
    </nav>

    <!-- 主内容 -->
    <main class="flex-1 pt-20">
      <slot />
    </main>

    <!-- 底部 -->
    <footer class="bg-slate-50 border-t border-slate-200 py-20 md:py-24 px-6">
      <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-12 md:gap-16">
        <div class="col-span-1 md:col-span-2">
          <div class="flex items-center gap-3 mb-8">
            <div class="w-10 h-10 bg-brand-500 rounded-xl flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <span class="text-2xl font-black text-slate-900">AI 不难学</span>
          </div>
          <p class="text-lg text-slate-600 max-w-md leading-relaxed">
            我们致力于通过最通俗易懂的方式，赋能每一位渴望学习的中老年朋友，跨越数字鸿沟。
          </p>
        </div>
        <div>
          <h4 class="text-slate-900 font-black text-base mb-8 uppercase tracking-widest">学习中心</h4>
          <ul class="space-y-5 text-slate-500 text-lg font-medium list-none p-0">
            <li>
              <NuxtLink to="/courses" class="text-slate-500 hover:text-brand-500 no-underline transition-colors">全部课程</NuxtLink>
            </li>
            <li>
              <NuxtLink to="/about" class="text-slate-500 hover:text-brand-500 no-underline transition-colors">关于我们</NuxtLink>
            </li>
          </ul>
        </div>
        <div>
          <h4 class="text-slate-900 font-black text-base mb-8 uppercase tracking-widest">联系客服</h4>
          <div class="space-y-4 text-slate-600 text-lg">
            <p>微信：<span class="text-slate-900 font-bold">A115939</span></p>
            <p>电话：<span class="text-slate-900 font-bold">13884635775</span></p>
            <p class="bg-slate-100 p-4 rounded-2xl border border-slate-200 text-sm">
              工作时间：9:00 - 21:00 (含节假日)
            </p>
          </div>
        </div>
      </div>
      <div class="max-w-7xl mx-auto mt-20 pt-10 border-t border-slate-200 flex flex-col md:flex-row justify-between items-center gap-4 text-slate-400 font-medium">
        <p>&copy; {{ new Date().getFullYear() }} AI 不难学培训平台 - 智慧生活，触手可及</p>
        <div class="flex gap-8">
          <span class="hover:text-slate-600 cursor-pointer">隐私条款</span>
          <span class="hover:text-slate-600 cursor-pointer">用户协议</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const mobileMenuOpen = ref(false)
const { fontSize: currentFontSize, fontSizeConfig, cycleFontSize, initFontSize } = useFontSize()

const navItems = [
  { to: '/', label: '首页' },
  { to: '/courses', label: '全部课程' },
  { to: '/about', label: '关于我们' },
]

const isActive = (path: string) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

const fontSizeClass = computed(() => {
  return `font-size-${currentFontSize.value}`
})

watch(() => route.path, () => {
  mobileMenuOpen.value = false
})

onMounted(() => {
  initFontSize()
})
</script>

<style scoped>
.navbar-bg {
  background: rgba(255, 255, 255, 0.92);
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid #E2E8F0;
}
.nav-link {
  @apply text-[17px] font-medium transition-all relative py-2
         text-slate-600 hover:text-brand-500 no-underline;
}
.nav-link-active {
  @apply text-brand-600 font-bold;
}
.font-size-btn {
  @apply flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-600 transition-all cursor-pointer min-h-0;
}
</style>

<style>
/* 字体大小全局样式（不能 scoped） */
.font-size-large {
  font-size: 115%;
}
.font-size-xlarge {
  font-size: 130%;
}
</style>
