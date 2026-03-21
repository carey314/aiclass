/**
 * 字体大小切换 composable
 * 专为中老年用户设计，支持三档字体大小
 */
type FontSize = 'normal' | 'large' | 'xlarge'

const fontSize = ref<FontSize>('normal')

const fontSizeConfig: Record<FontSize, { label: string; scale: string }> = {
  normal: { label: '标准', scale: '1' },
  large: { label: '大字', scale: '1.15' },
  xlarge: { label: '特大', scale: '1.3' },
}

export function useFontSize() {
  function applyFontSize(size: FontSize) {
    document.documentElement.style.setProperty('--font-scale', fontSizeConfig[size].scale)
    document.documentElement.dataset.fontSize = size
  }

  function setFontSize(size: FontSize) {
    fontSize.value = size
    applyFontSize(size)
    try {
      localStorage.setItem('aiclass-font-size', size)
    } catch {}
  }

  function cycleFontSize() {
    const sizes: FontSize[] = ['normal', 'large', 'xlarge']
    const idx = sizes.indexOf(fontSize.value)
    setFontSize(sizes[(idx + 1) % sizes.length])
  }

  function initFontSize() {
    try {
      const saved = localStorage.getItem('aiclass-font-size') as FontSize | null
      if (saved && fontSizeConfig[saved]) {
        fontSize.value = saved
        applyFontSize(saved)
      }
    } catch {}
  }

  return {
    fontSize,
    fontSizeConfig,
    setFontSize,
    cycleFontSize,
    initFontSize,
  }
}
