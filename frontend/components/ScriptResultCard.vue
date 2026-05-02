<script setup lang="ts">
/**
 * ScriptResultCard — 脚本结果展示卡片
 *
 * 接收已经解析好的 ScriptTemplate，展示成可读+可复制的UI。
 * 每个模块（标题/钩子/口播/即梦提示词等）都有独立"复制"按钮。
 *
 * 移动端优先：大字体、大按钮、明显的复制反馈。
 */
import { ref } from 'vue'
import type { ScriptTemplate } from '~/composables/useVideoScript'

const props = defineProps<{
  template: ScriptTemplate
  meta?: { generation_ms?: number; created_at?: string }
}>()

// 每个区域的复制状态（用 key 作 map 的key）
const copiedKey = ref<string>('')

const copyText = async (text: string, key: string) => {
  try {
    await navigator.clipboard.writeText(text)
    copiedKey.value = key
    setTimeout(() => {
      if (copiedKey.value === key) copiedKey.value = ''
    }, 2000)
  } catch (e) {
    // 降级到 fallback
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

const formatJimengPrompt = () => {
  const j = props.template.jimeng_prompt
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
  const text = [
    `📌 主题：${t.topic}`,
    '',
    `【标题（3选1）】`,
    ...t.titles.map((s, i) => `${i + 1}. ${s}`),
    '',
    `【开场钩子】`,
    t.hook,
    '',
    `【口播文案】（${t.estimated_duration}）`,
    t.voiceover,
    '',
    `【即梦提示词】`,
    formatJimengPrompt(),
    '',
    `【参考图建议】`,
    t.reference_image_guide,
    '',
    `【话题标签】`,
    t.hashtags.join(' '),
    '',
    `【拍摄小技巧】`,
    t.shooting_tips,
  ].join('\n')
  copyText(text, 'all')
}
</script>

<template>
  <div class="bg-white rounded-xl shadow-md p-5 space-y-5">
    <!-- 头部：主题 + 一键全复制 -->
    <div class="flex items-start justify-between gap-3 pb-3 border-b">
      <div class="flex-1">
        <div class="text-xs text-gray-400">主题</div>
        <div class="text-lg font-bold text-gray-900">{{ template.topic }}</div>
        <div v-if="meta?.generation_ms" class="text-xs text-gray-400 mt-1">
          生成耗时 {{ Math.round(meta.generation_ms / 1000) }} 秒
        </div>
      </div>
      <button
        class="px-4 py-2 rounded-lg font-bold text-white transition-all whitespace-nowrap"
        :class="copiedKey === 'all' ? 'bg-green-500' : 'bg-orange-500 active:scale-95'"
        @click="copyAll"
      >
        {{ copiedKey === 'all' ? '已复制 ✓' : '复制全部' }}
      </button>
    </div>

    <!-- 候选标题（3选1） -->
    <section>
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-base font-bold text-gray-900">📝 标题（3选1）</h3>
      </div>
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
        <h3 class="text-base font-bold text-gray-900">🎯 开场钩子（前5秒）</h3>
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
      <p class="bg-yellow-50 rounded-lg px-3 py-2 text-base leading-relaxed">
        {{ template.hook }}
      </p>
    </section>

    <!-- 口播文案 -->
    <section>
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-base font-bold text-gray-900">
          🎤 口播文案（{{ template.estimated_duration }}）
        </h3>
        <button
          class="text-sm px-3 py-1 rounded font-medium transition-colors"
          :class="
            copiedKey === 'voiceover'
              ? 'bg-green-500 text-white'
              : 'bg-orange-500 text-white active:bg-orange-600'
          "
          @click="copyText(template.voiceover, 'voiceover')"
        >
          {{ copiedKey === 'voiceover' ? '已复制' : '复制' }}
        </button>
      </div>
      <p class="bg-blue-50 rounded-lg px-3 py-3 text-base leading-relaxed">
        {{ template.voiceover }}
      </p>
    </section>

    <!-- 即梦提示词（最关键！） -->
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
      <div class="bg-purple-50 rounded-lg px-3 py-3 space-y-2">
        <div class="flex">
          <span class="font-bold text-purple-700 w-12 shrink-0">主体</span>
          <span class="text-gray-800">{{ template.jimeng_prompt.subject }}</span>
        </div>
        <div class="flex">
          <span class="font-bold text-purple-700 w-12 shrink-0">场景</span>
          <span class="text-gray-800">{{ template.jimeng_prompt.scene }}</span>
        </div>
        <div class="flex">
          <span class="font-bold text-purple-700 w-12 shrink-0">运动</span>
          <span class="text-gray-800">{{ template.jimeng_prompt.motion }}</span>
        </div>
        <div class="flex">
          <span class="font-bold text-purple-700 w-12 shrink-0">镜头</span>
          <span class="text-gray-800">{{ template.jimeng_prompt.camera }}</span>
        </div>
        <div class="flex">
          <span class="font-bold text-purple-700 w-12 shrink-0">氛围</span>
          <span class="text-gray-800">{{ template.jimeng_prompt.mood }}</span>
        </div>
        <div class="flex">
          <span class="font-bold text-purple-700 w-12 shrink-0">风格</span>
          <span class="text-gray-800">{{ template.jimeng_prompt.style }}</span>
        </div>
      </div>
    </section>

    <!-- 参考图建议 -->
    <section>
      <h3 class="text-base font-bold text-gray-900 mb-2">📷 参考图建议</h3>
      <p class="bg-green-50 rounded-lg px-3 py-2 text-base">
        {{ template.reference_image_guide }}
      </p>
    </section>

    <!-- 话题标签 -->
    <section>
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
    <section v-if="template.shooting_tips">
      <h3 class="text-base font-bold text-gray-900 mb-2">💡 拍摄小技巧</h3>
      <p class="bg-amber-50 rounded-lg px-3 py-2 text-base text-gray-700">
        {{ template.shooting_tips }}
      </p>
    </section>
  </div>
</template>
