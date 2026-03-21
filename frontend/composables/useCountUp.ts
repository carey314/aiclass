/**
 * 数字计数动画 composable
 * 当元素进入视口时触发从 0 到目标值的动画
 */
export function useCountUp() {
  const counters = ref<Map<HTMLElement, { target: number; current: number; suffix: string }>>(new Map())

  function startCount(el: HTMLElement, target: number, suffix: string = '', duration: number = 2000) {
    const startTime = performance.now()
    const animate = (now: number) => {
      const elapsed = now - startTime
      const progress = Math.min(elapsed / duration, 1)
      // easeOutExpo
      const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress)
      const current = Math.floor(eased * target)
      el.textContent = current.toLocaleString() + suffix
      if (progress < 1) requestAnimationFrame(animate)
    }
    requestAnimationFrame(animate)
  }

  onMounted(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target as HTMLElement
            const target = parseFloat(el.dataset.countTarget || '0')
            const suffix = el.dataset.countSuffix || ''
            startCount(el, target, suffix)
            observer.unobserve(el)
          }
        })
      },
      { threshold: 0.3 }
    )

    nextTick(() => {
      document.querySelectorAll('[data-count-target]').forEach((el) => {
        ;(el as HTMLElement).textContent = '0'
        observer.observe(el)
      })
    })

    onUnmounted(() => observer.disconnect())
  })
}
