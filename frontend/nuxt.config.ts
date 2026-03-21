export default defineNuxtConfig({
  devtools: { enabled: true },

  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@nuxt/image',
    '@nuxt/icon',
  ],

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000/api/v1',
    },
  },

  app: {
    head: {
      title: 'AI不难学 - 中老年AI工具实战训练营',
      htmlAttrs: { lang: 'zh-CN' },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: '用最土的话，教最新的AI。让45-60岁的你从零开始学会80%以上的AI工具。24节课全部免费，手机就能学。' },
        { name: 'keywords', content: 'AI课程,人工智能教程,中老年学AI,AI工具,ChatGPT教程,豆包教程,Kimi教程,通义千问,免费AI课程,零基础学AI' },
        // Open Graph
        { property: 'og:type', content: 'website' },
        { property: 'og:title', content: 'AI不难学 - 中老年AI工具实战训练营' },
        { property: 'og:description', content: '用最土的话，教最新的AI。24节免费课程，手机就能学，专为45-60岁朋友打造。' },
        { property: 'og:site_name', content: 'AI不难学' },
        { property: 'og:locale', content: 'zh_CN' },
        // Twitter Card
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: 'AI不难学 - 中老年AI工具实战训练营' },
        { name: 'twitter:description', content: '用最土的话，教最新的AI。24节免费课程，手机就能学。' },
        // Additional SEO
        { name: 'author', content: 'AI不难学团队' },
        { name: 'robots', content: 'index, follow' },
        { name: 'theme-color', content: '#F97316' },
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      ],
      script: [
        {
          type: 'application/ld+json',
          innerHTML: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'Course',
            name: 'AI不难学 - 中老年AI工具实战训练营',
            description: '专为45-60岁中老年朋友打造的AI工具实战课程，24节课全部免费，从零基础到熟练使用AI工具。',
            provider: {
              '@type': 'Organization',
              name: 'AI不难学',
            },
            isAccessibleForFree: true,
            numberOfCredits: 24,
            educationalLevel: 'Beginner',
            inLanguage: 'zh-CN',
            audience: {
              '@type': 'EducationalAudience',
              educationalRole: 'student',
              audienceType: '中老年学习者',
            },
          }),
        },
      ],
    },
  },

  ssr: true,

  compatibilityDate: '2025-01-01',
})
