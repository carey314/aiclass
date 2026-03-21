export function useScrollReveal() {
  let observer: IntersectionObserver | null = null
  let mutationObserver: MutationObserver | null = null
  const observed = new WeakSet<Element>()

  function observeElements() {
    document.querySelectorAll('[data-reveal]').forEach((el) => {
      if (!observed.has(el) && !el.classList.contains('revealed')) {
        observed.add(el)
        observer?.observe(el)
      }
    })
  }

  onMounted(() => {
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target as HTMLElement
            const delay = el.dataset.revealDelay
            if (delay) {
              setTimeout(() => el.classList.add('revealed'), Number(delay))
            } else {
              el.classList.add('revealed')
            }
            observer?.unobserve(el)
          }
        })
      },
      { threshold: 0.15, rootMargin: '0px 0px -60px 0px' }
    )

    observeElements()

    // Watch for dynamically added elements (v-for async data)
    mutationObserver = new MutationObserver(() => {
      observeElements()
    })
    mutationObserver.observe(document.body, { childList: true, subtree: true })
  })

  onUnmounted(() => {
    observer?.disconnect()
    observer = null
    mutationObserver?.disconnect()
    mutationObserver = null
  })
}
