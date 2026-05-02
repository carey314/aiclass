<script setup lang="ts">
/**
 * ScriptResultCard V2 — 脚本结果展示卡片
 *
 * 升级：
 * - 支持4段时间线口播（钩子/痛点/方案/CTA）每段独立展示+复制
 * - 支持shooting_plan：鞠姐自拍指南 vs 即梦B-roll
 * - 支持jimeng_prompt.summary（一段直接复制版）
 * - 高亮hook_type让用户看到用了哪种钩子套路
 *
 * 兼容：可解析V1旧格式（voiceover为string）
 */
import { ref, computed } from 'vue'
import type { ScriptTemplate } from '~/composables/useVideoScript'

const props = defineProps<{
  template: ScriptTemplate
  meta?: { generation_ms?: number; created_at?: string }
}>()

const copiedKey = ref<string>('')

const copyText = async (text: string, key: string) => {
  try {
    await navigator.clipboard.writeText(text)
    copiedKey.value = key
    setTimeout(() => {
      if (copiedKey.value === key) copiedKey.value = ''
    }, 2000)
  } catch (e) {
    const ta = document.createElement('textarea')
    ta.value = text
    document.body.appendChild(ta)
    ta.select()
    try {
      document.execCommand('copy')
      copiedKey.value = key
      setTimeout(() => {
        if (copiedKey.value === key) copiedKey.value = ''
      }, 2000)
    } finally {
      document.body.removeChild(ta)
    }
  }
}

// 兼容V1: voiceover可能是string，V2是object
const voiceoverFullText = computed(() => {
  const v = props.template.voiceover
  if (typeof v === 'string') return v
  return v?.full_text || ''
})

const voiceoverSegments = computed(() => {
  const v = props.template.voiceover
  if (typeof v === 'string') return []
  return v?.segments || []
})

const totalDuration = computed(
  () => props.template.estimated_total_duration || props.template.estimated_duration || ''
)

const formatJimengPrompt = () => {
  const j = props.template.jimeng_prompt
  // 优先使用summary（V2新增），否则拼接6段
  if (j.summary && j.summary.trim().length > 10) return j.summary
  return [
    `[主体] ${j.subject}`,
    `[场景] ${j.scene}`,
    `[运动] ${j.motion}`,
    `[镜头] ${j.camera}`,
    `[氛围] ${j.mood}`,
    `[风格] ${j.style}`,
  ].join('\n')
}

const copyAll = () => {
  const t = props.template
  const lines = [
    `📌 主题：${t.topic}`,
    '',
    `【3个候选标题】`,
    ...t.titles.map((s, i) => `${i + 1}. ${s}`),
    '',
    `【开场钩子】(${t.hook_type || ''})`,
    t.hook,
    '',
    `【口播文案】(${totalDuration.value})`,
    voiceoverFullText.value,
    '',
  ]

  if (voiceoverSegments.value.length > 0) {
    lines.push('【分段时间线】')
    voiceoverSegments.value.forEach((seg) => {
      lines.push(`${seg.time} | ${seg.label}`)
      lines.push(seg.text)
      lines.push('')
    })
  }

  if (t.shooting_plan?.self_shot && t.shooting_plan.self_shot.length > 0) {
    lines.push('【鞠姐自拍镜头】')
    t.shooting_plan.self_shot.forEach((s) => lines.push(`- ${s}`))
    lines.push('')
  }

  lines.push(`【即梦提示词】`)
  lines.push(formatJimengPrompt())
  lines.push('')

  if (t.shooting_plan?.broll_jimeng && t.shooting_plan.broll_jimeng.length > 0) {
    lines.push('【B-roll时间线】')
    t.shooting_plan.broll_jimeng.forEach((b) => lines.push(`${b.time}: ${b.scene}`))
    lines.push('')
  }

  lines.push(`【参考图建议】`)
  lines.push(t.reference_image_guide)
  lines.push('')

  lines.push(`【话题标签】`)
  lines.push(t.hashtags.join(' '))
  lines.push('')

  if (t.shooting_tips) {
    lines.push(`【拍摄小技巧】`)
    if (Array.isArray(t.shooting_tips)) {
      t.shooting_tips.forEach((tip) => lines.push(`- ${tip}`))
    } else {
      lines.push(t.shooting_tips)
    }
  }

  copyText(lines.join('\n'), 'all')
}

const hookTypeBadge = computed(() => {
  const map: Record<string, { color: string; emoji: string }> = {
    反常识: { color: 'bg-purple-100 text-purple-700', emoji: '🤯' },
    纠错: { color: 'bg-red-100 text-red-700', emoji: '❌' },
    痛点暴击: { color: 'bg-orange-100 text-orange-700', emoji: '😖' },
    数字冲击: { color: 'bg-blue-100 text-blue-700', emoji: '📊' },
  }
  return map[props.template.hook_type || ''] || { color: 'bg-gray-100 text-gray-700', emoji: '🎯' }
})
</script>

<template>
  <div class="bg-white rounded-xl shadow-md p-5 space-y-5">
    <!-- 头部 -->
    <div class="flex items-start justify-between gap-3 pb-3 border-b">
      <div class="flex-1">
        <div class="text-xs text-gray-400">主题</div>
        <div class="text-lg font-bold text-gray-900">{{ template.topic }}</div>
        <div v-if="meta?.generation_ms" class="text-xs text-gray-400 mt-1">
          生成耗时 {{ Math.round(meta.generation_ms / 1000) }} 秒
          <span v-if="totalDuration"> · 视频时长 {{ totalDuration }}</span>
        </div>
      </div>
      <button
        class="px-4 py-2 rounded-lg font-bold text-white transition-all whitespace-nowrap"
        :class="copiedKey === 'all' ? 'bg-green-500' : 'bg-orange-500 active:scale-95'"
        @click="copyAll"
      >
        {{ copiedKey === 'all' ? '已复制 ✓' : '一键复制' }}
      </button>
    </div>

    <!-- 候选标题 -->
    <section>
      <h3 class="text-base font-bold text-gray-900 mb-2">📝 标题（3选1）</h3>
      <ul class="space-y-2">
        <li
          v-for="(title, i) in template.titles"
          :key="i"
          class="flex items-center justify-between bg-orange-50 rounded-lg px-3 py-2"
        >
          <span class="text-base text-gray-800 flex-1 mr-2">{{ i + 1 }}. {{ title }}</span>
          <button
            class="text-sm px-3 py-1 rounded font-medium transition-colors whitespace-nowrap"
            :class="
              copiedKey === `title-${i}`
                ? 'bg-green-500 text-white'
                : 'bg-orange-500 text-white active:bg-orange-600'
            "
            @click="copyText(title, `title-${i}`)"
          >
            {{ copiedKey === `title-${i}` ? '已复制' : '复制' }}
          </button>
        </li>
      </ul>
    </section>

    <!-- 开场钩子 -->
    <section>
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-base font-bold text-gray-900 flex items-center gap-2">
          🎯 开场钩子（前3秒）
          <span
            v-if="template.hook_type"
            class="text-xs px-2 py-0.5 rounded-full font-normal"
            :class="hookTypeBadge.color"
          >
            {{ hookTypeBadge.emoji }} {{ template.hook_type }}
          </span>
        </h3>
        <button
          class="text-sm px-3 py-1 rounded font-medium transition-colors"
          :class="
            copiedKey === 'hook'
              ? 'bg-green-500 text-white'
              : 'bg-orange-500 text-white active:bg-orange-600'
          "
          @click="copyText(template.hook, 'hook')"
        >
          {{ copiedKey === 'hook' ? '已复制' : '复制' }}
        </button>
      </div>
      <p class="bg-yellow-50 rounded-lg px-3 py-3 text-base leading-relaxed font-medium">
        {{ template.hook }}
      </p>
    </section>

    <!-- 口播文案（V2: 4段时间线） -->
    <section>
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-base font-bold text-gray-900">
          🎤 口播文案（{{ totalDuration || '约35秒' }}）
        </h3>
        <button
          class="text-sm px-3 py-1 rounded font-medium transition-colors"
          :class="
            copiedKey === 'voiceover'
              ? 'bg-green-500 text-white'
              : 'bg-orange-500 text-white active:bg-orange-600'
          "
          @click="copyText(voiceoverFullText, 'voiceover')"
        >
          {{ copiedKey === 'voiceover' ? '已复制' : '复制全部' }}
        </button>
      </div>

      <!-- 分段时间线 -->
      <div v-if="voiceoverSegments.length > 0" class="space-y-2">
        <div
          v-for="(seg, i) in voiceoverSegments"
          :key="i"
          class="bg-blue-50 rounded-lg p-3"
        >
          <div class="flex items-center justify-between mb-1">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-blue-700 bg-white px-2 py-0.5 rounded">{{ seg.time }}</span>
              <span class="text-sm font-medium text-blue-800">{{ seg.label }}</span>
            </div>
            <button
              class="text-xs px-2 py-1 rounded font-medium transition-colors"
              :class="
                copiedKey === `seg-${i}`
                  ? 'bg-green-500 text-white'
                  : 'bg-blue-500 text-white active:bg-blue-600'
              "
              @click="copyText(seg.text, `seg-${i}`)"
            >
              {{ copiedKey === `seg-${i}` ? '✓' : '复制' }}
            </button>
          </div>
          <p class="text-base text-gray-800 leading-relaxed">{{ seg.text }}</p>
        </div>
      </div>

      <!-- 兼容V1: 单段口播 -->
      <p v-else class="bg-blue-50 rounded-lg px-3 py-3 text-base leading-relaxed">
        {{ voiceoverFullText }}
      </p>
    </section>

    <!-- 鞠姐自拍指南（V2新增） -->
    <section v-if="template.shooting_plan?.self_shot && template.shooting_plan.self_shot.length > 0">
      <h3 class="text-base font-bold text-gray-900 mb-2">📱 鞠姐自拍镜头指南</h3>
      <ul class="bg-pink-50 rounded-lg px-3 py-3 space-y-1 text-sm text-gray-800">
        <li v-for="(s, i) in template.shooting_plan.self_shot" :key="i" class="flex gap-2">
          <span class="text-pink-500">→</span>
          <span>{{ s }}</span>
        </li>
      </ul>
    </section>

    <!-- 即梦提示词 -->
    <section>
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-base font-bold text-gray-900">🎬 即梦提示词（粘贴到即梦）</h3>
        <button
          class="text-sm px-3 py-1 rounded font-medium transition-colors"
          :class="
            copiedKey === 'jimeng'
              ? 'bg-green-500 text-white'
              : 'bg-orange-500 text-white active:bg-orange-600'
          "
          @click="copyText(formatJimengPrompt(), 'jimeng')"
        >
          {{ copiedKey === 'jimeng' ? '已复制' : '复制' }}
        </button>
      </div>

      <!-- summary版本（如果有，优先显示） -->
      <div v-if="template.jimeng_prompt.summary && template.jimeng_prompt.summary.length > 10"
           class="bg-purple-50 rounded-lg px-3 py-3">
        <pre class="text-sm text-gray-800 whitespace-pre-wrap font-sans leading-relaxed">{{ template.jimeng_prompt.summary }}</pre>
      </div>

      <!-- 6段详细 -->
      <details class="bg-purple-50 rounded-lg px-3 py-3 mt-2">
        <summary class="cursor-pointer text-sm text-purple-700 font-medium">
          {{ template.jimeng_prompt.summary ? '查看6段详细版' : '展开6段提示词' }}
        </summary>
        <div class="mt-3 space-y-2">
          <div class="flex">
            <span class="font-bold text-purple-700 w-12 shrink-0 text-sm">主体</span>
            <span class="text-sm text-gray-800">{{ template.jimeng_prompt.subject }}</span>
          </div>
          <div class="flex">
            <span class="font-bold text-purple-700 w-12 shrink-0 text-sm">场景</span>
            <span class="text-sm text-gray-800">{{ template.jimeng_prompt.scene }}</span>
          </div>
          <div class="flex">
            <span class="font-bold text-purple-700 w-12 shrink-0 text-sm">运动</span>
            <span class="text-sm text-gray-800">{{ template.jimeng_prompt.motion }}</span>
          </div>
          <div class="flex">
            <span class="font-bold text-purple-700 w-12 shrink-0 text-sm">镜头</span>
            <span class="text-sm text-gray-800">{{ template.jimeng_prompt.camera }}</span>
          </div>
          <div class="flex">
            <span class="font-bold text-purple-700 w-12 shrink-0 text-sm">氛围</span>
            <span class="text-sm text-gray-800">{{ template.jimeng_prompt.mood }}</span>
          </div>
          <div class="flex">
            <span class="font-bold text-purple-700 w-12 shrink-0 text-sm">风格</span>
            <span class="text-sm text-gray-800">{{ template.jimeng_prompt.style }}</span>
          </div>
        </div>
      </details>
    </section>

    <!-- B-roll时间线（V2新增） -->
    <section v-if="template.shooting_plan?.broll_jimeng && template.shooting_plan.broll_jimeng.length > 0">
      <h3 class="text-base font-bold text-gray-900 mb-2">⏱ B-roll时间线（即梦分段）</h3>
      <ul class="bg-green-50 rounded-lg px-3 py-3 space-y-2 text-sm">
        <li v-for="(b, i) in template.shooting_plan.broll_jimeng" :key="i" class="flex gap-2">
          <span class="font-bold text-green-700 shrink-0 w-16">{{ b.time }}</span>
          <span class="text-gray-800">{{ b.scene }}</span>
        </li>
      </ul>
    </section>

    <!-- 参考图建议 -->
    <section v-if="template.reference_image_guide">
      <h3 class="text-base font-bold text-gray-900 mb-2">📷 拍摄前准备</h3>
      <p class="bg-amber-50 rounded-lg px-3 py-2 text-sm">
        {{ template.reference_image_guide }}
      </p>
    </section>

    <!-- 话题标签 -->
    <section v-if="template.hashtags && template.hashtags.length > 0">
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-base font-bold text-gray-900"># 话题标签</h3>
        <button
          class="text-sm px-3 py-1 rounded font-medium transition-colors"
          :class="
            copiedKey === 'tags'
              ? 'bg-green-500 text-white'
              : 'bg-orange-500 text-white active:bg-orange-600'
          "
          @click="copyText(template.hashtags.join(' '), 'tags')"
        >
          {{ copiedKey === 'tags' ? '已复制' : '复制' }}
        </button>
      </div>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="(tag, i) in template.hashtags"
          :key="i"
          class="text-sm bg-gray-100 text-gray-700 rounded-full px-3 py-1"
        >
          {{ tag }}
        </span>
      </div>
    </section>

    <!-- 拍摄小技巧 -->
    <section v-if="template.shooting_tips && (Array.isArray(template.shooting_tips) ? template.shooting_tips.length > 0 : template.shooting_tips)">
      <h3 class="text-base font-bold text-gray-900 mb-2">💡 拍摄小技巧</h3>
      <ul v-if="Array.isArray(template.shooting_tips)" class="bg-amber-50 rounded-lg px-3 py-3 space-y-1 text-sm text-gray-700">
        <li v-for="(tip, i) in template.shooting_tips" :key="i" class="flex gap-2">
          <span>•</span>
          <span>{{ tip }}</span>
        </li>
      </ul>
      <p v-else class="bg-amber-50 rounded-lg px-3 py-2 text-sm text-gray-700">
        {{ template.shooting_tips }}
      </p>
    </section>
  </div>
</template>
