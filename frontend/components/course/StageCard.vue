<template>
  <NuxtLink
    :to="`/courses/${stage.id}`"
    class="card-light card-light-hover p-1 rounded-6xl overflow-hidden group no-underline block"
  >
    <div class="p-8 md:p-10">
      <div class="flex justify-between items-start mb-8">
        <div class="transition-all duration-500 group-hover:scale-110">
          <UiStageIcon :emoji="stage.icon" size="md" />
        </div>
        <span
          v-if="stage.is_free"
          class="text-xs font-bold text-emerald-600 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded-lg"
        >
          免费
        </span>
      </div>
      <h3 class="text-xl font-black text-slate-900 mb-3 leading-tight">{{ stage.title }}</h3>
      <p class="text-slate-600 text-base leading-relaxed mb-4">{{ stage.subtitle }}</p>
      <p class="text-slate-500 text-sm">{{ stage.lessons?.length || 0 }} 节课</p>
      <div class="h-1 w-0 group-hover:w-full bg-gradient-to-r from-brand-400 to-brand-500 transition-all duration-700 rounded-full mt-6" />
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
defineProps<{
  stage: {
    id: number
    title: string
    subtitle: string
    stage_number: number
    icon: string | null
    is_free: boolean
    lessons?: any[]
  }
}>()
</script>
