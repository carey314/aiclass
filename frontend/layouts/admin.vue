<template>
  <div class="min-h-screen flex bg-slate-50">
    <!-- 侧边栏 -->
    <aside
      class="fixed inset-y-0 left-0 z-40 w-64 bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 transform transition-transform duration-300"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'"
    >
      <!-- Logo -->
      <div class="flex items-center justify-between h-20 px-6">
        <NuxtLink to="/admin" class="flex items-center gap-3 no-underline">
          <div class="w-9 h-9 bg-gradient-to-br from-brand-500 to-brand-400 rounded-xl flex items-center justify-center">
            <Icon name="heroicons:sparkles" class="w-5 h-5 text-white" />
          </div>
          <div class="flex flex-col">
            <span class="text-lg font-black text-white leading-tight">AI不难学</span>
            <span class="text-xs text-slate-400">管理后台</span>
          </div>
        </NuxtLink>
        <button class="lg:hidden text-slate-500 hover:text-white p-2 min-h-0" @click="sidebarOpen = false">
          <Icon name="heroicons:x-mark" class="w-5 h-5" />
        </button>
      </div>
      <div class="h-px bg-white/5 mx-4" />

      <!-- 导航 -->
      <nav class="mt-6 px-4 space-y-1">
        <NuxtLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="sidebar-link"
          :class="{ 'sidebar-link-active': isExactActive(item.to) }"
        >
          <Icon :name="item.icon" class="w-5 h-5" />
          <span>{{ item.label }}</span>
        </NuxtLink>

        <div class="h-px bg-slate-700/50 my-4" />

        <NuxtLink to="/" class="sidebar-link !text-slate-500 hover:!text-slate-300" target="_blank">
          <Icon name="heroicons:globe-alt" class="w-5 h-5" />
          <span>查看前台</span>
        </NuxtLink>
        <button class="sidebar-link w-full text-left !text-red-400 hover:!text-red-300 hover:!bg-red-500/10" @click="handleLogout">
          <Icon name="heroicons:arrow-right-start-on-rectangle" class="w-5 h-5" />
          <span>退出登录</span>
        </button>
      </nav>
    </aside>

    <!-- 主内容区 -->
    <div class="flex-1 lg:ml-64">
      <!-- 顶栏 -->
      <header class="sticky top-0 z-30 h-16 flex items-center justify-between px-6 bg-white/80 backdrop-blur-md border-b border-slate-200">
        <button class="lg:hidden p-2 rounded-xl hover:bg-slate-50 text-slate-400 min-h-0" @click="sidebarOpen = true">
          <Icon name="heroicons:bars-3" class="w-6 h-6" />
        </button>
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-brand-100 border border-brand-200 flex items-center justify-center text-brand-600 text-sm font-black">
            {{ (authStore.user?.display_name || '管')[0] }}
          </div>
          <span class="text-slate-500 text-sm font-medium">
            <span class="text-slate-900 font-bold">{{ authStore.user?.display_name || '管理员' }}</span>
          </span>
        </div>
      </header>

      <!-- 内容 -->
      <main class="p-6 md:p-8">
        <slot />
      </main>
    </div>

    <!-- 遮罩层 -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 bg-black/60 backdrop-blur-sm z-30 lg:hidden"
      @click="sidebarOpen = false"
    />
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

const route = useRoute()
const authStore = useAuthStore()
const sidebarOpen = ref(false)

const navItems = [
  { to: '/admin', icon: 'heroicons:squares-2x2', label: '仪表盘' },
  { to: '/admin/courses', icon: 'heroicons:folder-open', label: '分类管理' },
  { to: '/admin/lessons', icon: 'heroicons:document-text', label: '课程管理' },
  { to: '/admin/media', icon: 'heroicons:photo', label: '媒体库' },
]

const isExactActive = (path: string) => {
  if (path === '/admin') return route.path === '/admin'
  return route.path.startsWith(path)
}

const handleLogout = () => {
  authStore.logout()
}

watch(() => route.path, () => {
  sidebarOpen.value = false
})
</script>

<style scoped>
.sidebar-link {
  @apply flex items-center gap-3 px-4 py-3 rounded-xl
         text-slate-400 hover:text-white hover:bg-white/[0.08]
         no-underline transition-all text-[15px] font-medium min-h-0;
}
.sidebar-link-active {
  @apply text-white bg-brand-500/15 border-l-[3px] border-brand-500 rounded-l-none;
}
</style>
