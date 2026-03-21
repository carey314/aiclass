<template>
  <NuxtLink
    :to="`/courses/${lesson.stage_id || stageId}/${lesson.id}`"
    class="group flex items-center justify-between p-5 card-light rounded-4xl hover:bg-slate-50 transition-all no-underline"
  >
    <div class="flex items-center gap-5 min-w-0">
      <div class="w-10 h-10 rounded-xl bg-brand-50 border border-brand-200 flex items-center justify-center text-brand-600 font-black text-sm flex-shrink-0 group-hover:bg-brand-500 group-hover:text-white transition-all">
        {{ lesson.lesson_number }}
      </div>
      <div class="min-w-0">
        <h4 class="text-lg font-bold text-slate-700 group-hover:text-slate-900 transition-colors truncate">
          {{ lesson.title }}
        </h4>
        <p v-if="lesson.summary" class="text-slate-500 text-sm mt-1 truncate">
          {{ lesson.summary }}
        </p>
      </div>
    </div>
    <div class="flex items-center gap-3 flex-shrink-0 ml-4">
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
</template>

<script setup lang="ts">
defineProps<{
  lesson: {
    id: number
    title: string
    subtitle?: string | null
    lesson_number: number
    summary?: string | null
    duration_minutes?: number | null
    is_free: boolean
    stage_id?: number
  }
  stageId?: number
}>()
</script>
