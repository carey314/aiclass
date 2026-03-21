<template>
  <div
    class="stage-icon-wrapper flex items-center justify-center rounded-3xl"
    :class="[sizeClass, themeClass]"
  >
    <Icon :name="iconName" :class="iconSizeClass" />
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(defineProps<{
  emoji?: string
  size?: 'sm' | 'md' | 'lg'
}>(), {
  emoji: '📖',
  size: 'lg',
})

const iconMap: Record<string, { icon: string; theme: string }> = {
  '🤖': { icon: 'solar:cpu-bolt-bold-duotone', theme: 'stage-blue' },
  '💬': { icon: 'solar:chat-round-dots-bold-duotone', theme: 'stage-teal' },
  '🎨': { icon: 'solar:palette-bold-duotone', theme: 'stage-violet' },
  '💼': { icon: 'solar:suitcase-bold-duotone', theme: 'stage-amber' },
  '🌟': { icon: 'solar:stars-bold-duotone', theme: 'stage-rose' },
  '🚀': { icon: 'solar:rocket-2-bold-duotone', theme: 'stage-indigo' },
  '📖': { icon: 'solar:book-bold-duotone', theme: 'stage-blue' },
}

const matched = computed(() => iconMap[props.emoji] || iconMap['📖'])
const iconName = computed(() => matched.value.icon)
const themeClass = computed(() => matched.value.theme)

const sizeClass = computed(() => ({
  sm: 'w-10 h-10',
  md: 'w-14 h-14',
  lg: 'w-16 h-16 md:w-20 md:h-20',
}[props.size]))

const iconSizeClass = computed(() => ({
  sm: 'w-5 h-5',
  md: 'w-7 h-7',
  lg: 'w-8 h-8 md:w-10 md:h-10',
}[props.size]))
</script>

<style scoped>
.stage-blue {
  background: linear-gradient(135deg, #DBEAFE, #BFDBFE);
  color: #2563EB;
}
.stage-teal {
  background: linear-gradient(135deg, #CCFBF1, #99F6E4);
  color: #0D9488;
}
.stage-violet {
  background: linear-gradient(135deg, #EDE9FE, #DDD6FE);
  color: #7C3AED;
}
.stage-amber {
  background: linear-gradient(135deg, #FEF3C7, #FDE68A);
  color: #D97706;
}
.stage-rose {
  background: linear-gradient(135deg, #FFE4E6, #FECDD3);
  color: #E11D48;
}
.stage-indigo {
  background: linear-gradient(135deg, #E0E7FF, #C7D2FE);
  color: #4F46E5;
}
</style>
