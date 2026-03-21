<template>
  <div class="pt-16 md:pt-24 pb-32 max-w-4xl mx-auto px-6">
    <!-- 顶部引言 -->
    <div class="text-center mb-20" data-reveal>
      <div class="inline-block px-4 py-1.5 rounded-full bg-brand-50 text-brand-600 text-sm font-bold mb-8 border border-brand-100">
        ✨ 关于我们
      </div>
      <h1 class="text-2xl md:text-4xl lg:text-5xl font-black text-slate-900 mb-8 leading-tight whitespace-nowrap">
        "在这个时代，<span class="hero-highlight">好奇心</span>是唯一的门槛。"
      </h1>
      <p class="text-lg md:text-xl text-slate-500 leading-relaxed max-w-2xl mx-auto">
        我们不仅仅是在教 AI，我们是在重新连接每一个渴望与时代同步的灵魂。
        无论你是 45 岁还是 85 岁，只要你愿意点开这个网页，你就是我们的同学。
      </p>
    </div>

    <!-- 数据卡片 -->
    <div class="grid grid-cols-3 gap-4 md:gap-6 mb-20">
      <div v-for="(stat, i) in stats" :key="i" class="stat-card text-center" data-reveal :data-reveal-delay="i * 100">
        <div class="text-3xl md:text-4xl font-black mb-1" :class="stat.color">
          <span :data-count-target="stat.num" :data-count-suffix="stat.suffix">0</span>
        </div>
        <div class="text-slate-400 font-bold text-xs md:text-sm uppercase tracking-wider">{{ stat.label }}</div>
      </div>
    </div>

    <!-- 理念卡片 -->
    <div class="content-card p-8 md:p-14" data-reveal>
      <h2 class="text-2xl md:text-3xl font-black text-slate-900 mb-8 flex items-center gap-3">
        <div class="w-1.5 h-10 bg-brand-500 rounded-full" />
        为什么做这门课？
      </h2>
      <div class="space-y-5 text-lg text-slate-500 leading-loose">
        <p>
          AI 时代已经到来，但市面上的 AI 课程要么太专业（面向程序员），要么太贵（动辄几千块），
          要么太水（教你按个按钮就收费）。
        </p>
        <p>
          我们想做一件简单的事：<strong class="text-slate-900">用最土的话，教最新的 AI</strong>。
        </p>
      </div>

      <div class="my-10 quote-box">
        不讲原理，只讲用法。不说术语，只说人话。不求全面，只求实用。
      </div>

      <h3 class="text-xl md:text-2xl font-black text-slate-900 mb-8 flex items-center gap-3">
        <div class="w-1.5 h-8 bg-trust-500 rounded-full" />
        课程特色
      </h3>
      <div class="space-y-4">
        <div v-for="(feature, i) in features" :key="i" class="feature-item">
          <div class="w-8 h-8 rounded-lg bg-emerald-100 flex items-center justify-center flex-shrink-0">
            <Icon name="heroicons:check" class="w-4 h-4 text-emerald-600" />
          </div>
          <p class="text-lg text-slate-500">
            <strong class="text-slate-900">{{ feature.title }}</strong> — {{ feature.desc }}
          </p>
        </div>
      </div>

      <div class="mt-14 pt-10 border-t border-slate-100">
        <h3 class="text-xl md:text-2xl font-black text-slate-900 mb-6 flex items-center gap-3">
          <div class="w-1.5 h-8 bg-amber-500 rounded-full" />
          联系我们
        </h3>
        <p class="text-lg text-slate-500 mb-5">如果你有任何问题、建议或合作意向，欢迎联系我们。</p>
        <div class="flex flex-wrap gap-4">
          <div class="contact-badge">
            📱 微信：<span class="text-slate-900 font-bold">A115939</span>
          </div>
          <div class="contact-badge">
            📞 电话：<span class="text-slate-900 font-bold">13884635775</span>
          </div>
        </div>
      </div>
    </div>

    <!-- FAQ 常见问题 -->
    <div class="mt-16" data-reveal>
      <div class="text-center mb-10">
        <div class="inline-block px-4 py-1.5 rounded-full bg-trust-50 text-trust-600 text-sm font-bold mb-5 border border-trust-100">
          ❓ 常见问题
        </div>
        <h2 class="text-2xl md:text-3xl font-black text-slate-900">你可能想知道的</h2>
      </div>
      <div class="space-y-3">
        <div
          v-for="(faq, idx) in faqs"
          :key="idx"
          class="faq-item"
        >
          <button
            class="w-full flex items-center justify-between p-5 md:p-6 text-left min-h-0 group"
            @click="openFaq = openFaq === idx ? -1 : idx"
          >
            <span class="text-lg font-bold text-slate-800 pr-4">{{ faq.q }}</span>
            <div
              class="w-8 h-8 rounded-full bg-slate-100 group-hover:bg-slate-200 flex items-center justify-center flex-shrink-0 transition-all duration-300"
              :class="openFaq === idx ? 'rotate-180' : ''"
            >
              <Icon name="heroicons:chevron-down" class="w-4 h-4 text-slate-400" />
            </div>
          </button>
          <div v-if="openFaq === idx" class="px-5 md:px-6 pb-5 md:pb-6">
            <p class="text-slate-500 text-base leading-relaxed">{{ faq.a }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const stats = [
  { num: 12000, suffix: '+', label: '活跃学员', color: 'text-brand-500' },
  { num: 24, suffix: '节', label: '精品课程', color: 'text-trust-500' },
  { num: 99, suffix: '%', label: '好评率', color: 'text-emerald-500' },
]

const features = [
  { title: '大字体、大按钮', desc: '专门为中老年朋友优化的阅读体验' },
  { title: '每课一技能', desc: '每节课只学一个技能，学完就能用' },
  { title: '真实场景', desc: '所有案例都来自真实的生活和工作场景' },
  { title: '有作品', desc: '每节课都有作品产出，学习有成就感' },
]

const openFaq = ref(-1)
const faqs = [
  { q: '课程真的完全免费吗？', a: '是的！24节课全部免费，没有任何隐藏收费。我们的使命是帮助每一位渴望学习的朋友跨越数字鸿沟，让AI不再有门槛。' },
  { q: '我完全不懂电脑，能学会吗？', a: '当然能！我们的课程专门为零基础的朋友设计，全程用大白话讲解，手把手教你操作。只要你有一部智能手机，就能开始学习。' },
  { q: '需要什么设备？要不要买电脑？', a: '一部智能手机就够了！课程中教的AI工具大部分都有手机版。如果你有电脑也可以用，但不是必须的。' },
  { q: '每天需要花多少时间学习？', a: '每节课大约15-30分钟。建议每天学一课，但你完全可以按照自己的节奏来。重要的是坚持，不用着急。' },
  { q: '学了之后到底能干什么？', a: '你可以用AI写文章、做PPT、画图、剪视频、分析数据、辅助工作决策等等。很多学员学完后工作效率提升了一倍以上！' },
  { q: '和网上其他AI课程有什么区别？', a: '我们只说人话不说术语，只教实用不讲原理，字体大排版好，专为中老年朋友优化。而且完全免费，绝不割韭菜。' },
]

useScrollReveal()
useCountUp()

useHead({
  title: '关于我们 - AI不难学',
})
</script>

<style scoped>
.hero-highlight {
  background: linear-gradient(135deg, #F97316, #3B82F6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-card {
  background: white;
  border: 1px solid #F1F5F9;
  border-radius: 1.25rem;
  padding: 1.5rem 1rem;
  transition: all 0.3s ease;
}
.stat-card:hover {
  border-color: #E2E8F0;
  box-shadow: 0 4px 16px -4px rgba(0,0,0,0.06);
  transform: translateY(-2px);
}

.content-card {
  background: white;
  border: 1px solid #F1F5F9;
  border-radius: 2rem;
}

.quote-box {
  background: linear-gradient(135deg, #FFF7ED, #FEF3C7);
  border: 1px solid #FDE68A;
  border-radius: 1.25rem;
  padding: 1.5rem 2rem;
  color: #92400E;
  font-weight: 600;
  font-size: 1.125rem;
  line-height: 1.8;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 0.75rem 0;
}

.contact-badge {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 1rem;
  padding: 0.875rem 1.25rem;
  color: #64748B;
  font-size: 1rem;
}

.faq-item {
  background: white;
  border: 1px solid #F1F5F9;
  border-radius: 1.25rem;
  transition: all 0.3s ease;
  overflow: hidden;
}
.faq-item:hover {
  border-color: #E2E8F0;
}
</style>
