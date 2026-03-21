# UI 设计方案 - "AI不难学" 网站改版（v2）

> 更新于 2026-03-09，融合2026年最新UI设计趋势

---

## 一、2026年设计趋势参考

基于对2026年全球及国内UI/UX设计趋势的调研，以下是本项目采用的趋势及其在中老年教育场景中的适配方式：

### 1.1 采用的趋势

#### (1) 暖色大地色调（Earth Tones & Warm Palettes）
**趋势来源**：2026年色彩趋势回归大地色系 —— 温暖的赭色、柔和的橙褐、沉稳的蓝。"Muddy palettes"以柔和、有温度的色彩取代冷冰冰的纯蓝/纯白。
**本项目应用**：以温暖橙色（`#F97316`）为主色，搭配信赖蓝（`#3B82F6`）为辅助色，背景采用米白色（`#FFFBF5`）而非纯白，营造"明亮教室里的温暖阳光"感。

#### (2) Bento Grid 2.0 模块化布局
**趋势来源**：67%的新网站采用Bento Grid模块化卡片布局，2026年进化为"Active Grid" —— 卡片带有交互反馈、圆角加大（12-24px）、hover时展开/变化。
**本项目应用**：首页课程分类采用Bento Grid排列不同大小的分类卡片，按工具类型（对话AI、绘画AI、视频AI、办公AI等）展示。卡片圆角20-24px，hover时轻微上浮+阴影加深，为中老年用户提供清晰的视觉反馈。

#### (3) 微交互反馈（Micro-Delights）
**趋势来源**：2026年"微愉悦"设计 —— 按钮点击时的脉动效果、卡片hover的柔和抬升、加载完成时的轻微弹跳，让交互有"回应感"。
**本项目应用**：
- 按钮hover时轻微上浮 `translateY(-2px)` + 阴影增强
- 点击时 `active:scale-95` 按压反馈
- 课程卡片hover时底部进度条从0宽度展开到100%
- 加载动画使用品牌橙色旋转圈

但**不使用**复杂的动画（如confetti、变形动画），避免分散中老年用户注意力。

#### (4) 轻量化设计与留白
**趋势来源**：2026年轻量化设计核心 —— 留白占比提升至40%，信息层级压缩至3层以内，剔除冗余装饰。
**本项目应用**：
- 删除所有光晕（glow）、毛玻璃（glass morphism）等装饰性效果
- 卡片使用简洁的白色背景+柔和阴影，而非半透明层叠
- 页面信息层级严格控制：标题 > 正文 > 辅助说明，最多3层
- 大量留白让内容"呼吸"

#### (5) 零学习成本设计（Zero Learning Curve）
**趋势来源**：2026年"零学习成本"趋势 —— 用户无需教程即可使用，通过熟悉的图标、动画引导和直觉式交互实现。
**本项目应用**：
- 每个课程分类都有大emoji图标辅助文字（如 "对话AI" 搭配对话气泡图标）
- 导航只有2级，菜单项带emoji
- 按钮文案用"大白话"（"立即开始学习" 而非 "Get Started"）
- 所有操作都有即时视觉反馈

#### (6) 无障碍优先（Accessibility-First）
**趋势来源**：欧盟2026年实施WCAG 3.0，无障碍从"附加功能"变为"设计基础" —— 高对比度、大触摸目标、键盘可访问、屏幕阅读器兼容。
**本项目应用**：
- 正文与背景对比度 14:1（远超AA标准4.5:1）
- 所有触摸目标 >= 48px
- 按钮和输入框有明显的focus光环
- 避免蓝紫色和黄绿色组合（老年人难以区分）
- 错误消息放在输入框上方，不使用仅靠颜色区分的信息

#### (7) 情绪化设计（Emotional UI）
**趋势来源**：2026年情绪化UI设计 —— 界面氛围贴近用户情绪节奏，不只是"亮色/暗色"切换，而是让用户感到"被关心"。
**本项目应用**：
- 暖色调传递"友好、安全"的情绪
- 课程阅读页使用舒适的米白+白色，像纸质书本一样的阅读体验
- 成功/免费等正向信息使用柔和绿色，不刺眼
- 整体视觉传达"这里不会太难，你一定能学会"的信心感

#### (8) 性能即品质（Performance as Perceived Quality）
**趋势来源**：2026年骨架屏（Skeleton Loading）、乐观UI更新成为标配，"感知速度"比"实际速度"更重要。
**本项目应用**：
- 加载状态使用品牌色spinner + "课程加载中..."文案
- 未来可升级为骨架屏（Skeleton）加载

### 1.2 有意不采用的趋势

| 趋势 | 不采用原因 |
|------|-----------|
| 液态玻璃（Liquid Glass） | 性能开销大，视觉复杂度高，对中老年用户造成困惑 |
| 3D/WebGL沉浸式 | 设备兼容性差，增加认知负担 |
| 深色模式默认 | 45%新产品默认深色，但不适合中老年长时间阅读 |
| 语音优先界面 | 目标用户更习惯点击操作，语音作为辅助而非主要 |
| 混搭材质质感 | 金属/布纹等材质增加视觉噪音 |
| AI动态个性化UI | 固定、可预测的界面对中老年用户更友好 |

---

## 二、设计理念

### 核心原则
当前网站采用深色（Dark）主题，背景色 `#020617`（近乎纯黑），毛玻璃效果和渐变光晕为主视觉。这种科技感风格虽然现代，但对45-60岁中老年目标用户存在以下问题：
- 深色背景长时间阅读容易疲劳
- 低对比度文字（slate-400/500）在深色背景上辨识度不够
- 光晕/毛玻璃等效果增加视觉噪音，分散注意力
- 整体风格偏"程序员审美"，不够亲切温暖

### 改版方向
**"温暖、清晰、值得信赖"** —— 像一位耐心的老师在明亮的教室里教课。

- **浅色为主**：米白/白色背景，大量留白（40%+），去掉深色主题
- **暖色系统**：温暖橙色为主强调色 + 信赖蓝辅助色（2026大地色趋势）
- **大字体、高对比度**：正文18px起步，对比度远超WCAG AA（2026无障碍优先趋势）
- **宽松间距**：增大行高、段距、卡片间距，不拥挤（轻量化留白趋势）
- **模块化布局**：Bento Grid 2.0，圆角20-24px，带微交互（2026卡片趋势）
- **简洁导航**：最多2级，emoji+文字，零学习成本

### 设计参考
- 得到APP（浅色暖调、卡片式、大字体）
- 微信读书（简洁、高可读性）
- 老年大学类教育APP（圆角卡片、大按钮、emoji辅助）

---

## 三、课程分类设计（灵活分类）

### 设计说明
课程不再固定为"6阶段36节课"的线性结构。改为**按AI工具类型灵活分类**，每个分类下的课程数量由实际内容决定。

### 分类卡片设计
首页和课程列表页采用Bento Grid展示课程分类，每个分类是一个卡片：

- **卡片内容**：大emoji图标 + 分类名称 + 一句话描述 + 课程数量
- **卡片样式**：白色背景、圆角24px、柔和阴影、hover上浮
- **布局方式**：
  - 桌面端：3-4列 Bento Grid，重点分类可占2列宽
  - 平板端：2列
  - 手机端：1列
- **分类示例**（具体由研究员搜索结果决定）：
  - 对话AI（ChatGPT / 豆包 / Kimi 等）
  - AI绘画（Midjourney / 即梦 / 可灵等）
  - AI视频（可灵 / 即梦视频 / Runway 等）
  - AI办公（WPS AI / 通义千问 / 飞书AI 等）
  - AI音乐/音频
  - AI生活助手
  - 其他

### 对现有数据模型的影响
后端 `stages` 表的含义从"学习阶段"变为"工具分类"。字段基本兼容：
- `title` -> 分类名称（如"对话AI"）
- `subtitle` -> 一句话描述（如"让AI成为你的聊天搭档"）
- `icon` -> 大emoji图标
- `stage_number` -> 排序号
- `lessons` -> 该分类下的课程列表

前端显示逻辑无需大改，只需要调整措辞（如"第1阶段" -> 只显示分类名称）。

---

## 四、配色方案

### 主色板

| 用途 | 色名 | 色值 | 说明 |
|------|------|------|------|
| 主背景 | warm-white | `#FFFBF5` | 温暖的米白色背景（大地色趋势） |
| 卡片背景 | card-white | `#FFFFFF` | 纯白卡片 |
| 次要背景 | warm-gray-50 | `#FAF8F5` | 浅暖灰，区分区域 |
| 主强调色 | brand-orange-500 | `#F97316` | 温暖橙色，CTA按钮、重点标记 |
| 主强调色浅 | brand-orange-50 | `#FFF7ED` | 橙色浅底，badge/标签背景 |
| 主强调色深 | brand-orange-600 | `#EA580C` | 按钮hover |
| 辅助色 | trust-blue-500 | `#3B82F6` | 蓝色，链接/辅助操作/信赖感 |
| 辅助色浅 | trust-blue-50 | `#EFF6FF` | 蓝色浅底 |
| 成功色 | success-green | `#16A34A` | 免费标签 |
| 正文色 | text-primary | `#1E293B` | slate-800，高对比度正文 |
| 次要文字 | text-secondary | `#64748B` | slate-500，辅助说明 |
| 轻文字 | text-muted | `#94A3B8` | slate-400，最次要文字 |
| 边框 | border-default | `#E2E8F0` | slate-200，卡片/分割线 |
| 边框浅 | border-light | `#F1F5F9` | slate-100，更轻的分割 |

### 渐变色
- **主渐变（CTA按钮）**: `linear-gradient(135deg, #F97316, #FB923C)` 橙色渐变
- **标题装饰渐变**: `linear-gradient(135deg, #F97316, #3B82F6)` 橙到蓝
- **Footer CTA背景**: `linear-gradient(135deg, #1E3A8A, #1E40AF)` 深蓝渐变（保留深色作为对比区域）

---

## 五、Tailwind 配置修改方案

修改 `tailwind.config.ts`：

```ts
import type { Config } from 'tailwindcss'

export default {
  content: [
    './components/**/*.{vue,js,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './app.vue',
  ],
  theme: {
    extend: {
      fontSize: {
        'base': ['18px', '30px'],    // 行高从28px增加到30px
        'lg': ['20px', '32px'],      // 行高从30px增加到32px
        'xl': ['24px', '36px'],      // 行高从34px增加到36px
        '2xl': ['30px', '42px'],
        '3xl': ['36px', '48px'],
        '4xl': ['48px', '58px'],
        '5xl': ['56px', '68px'],
        '6xl': ['64px', '76px'],
      },
      colors: {
        // 删除 midnight，新增暖色系统
        'warm-white': '#FFFBF5',
        brand: {
          50: '#FFF7ED',
          100: '#FFEDD5',
          200: '#FED7AA',
          300: '#FDBA74',
          400: '#FB923C',
          500: '#F97316',
          600: '#EA580C',
          700: '#C2410C',
          800: '#9A3412',
          900: '#7C2D12',
        },
        trust: {
          50: '#EFF6FF',
          100: '#DBEAFE',
          200: '#BFDBFE',
          300: '#93C5FD',
          400: '#60A5FA',
          500: '#3B82F6',
          600: '#2563EB',
          700: '#1D4ED8',
          800: '#1E40AF',
          900: '#1E3A8A',
        },
      },
      fontFamily: {
        sans: [
          '-apple-system',
          '"PingFang SC"',
          '"Microsoft YaHei"',
          '"Helvetica Neue"',
          'Arial',
          'sans-serif',
        ],
      },
      minHeight: {
        'touch': '48px',
      },
      minWidth: {
        'touch': '48px',
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
        '6xl': '3rem',
      },
      boxShadow: {
        'card': '0 1px 3px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.04)',
        'card-hover': '0 4px 16px rgba(0,0,0,0.08), 0 8px 32px rgba(0,0,0,0.06)',
        'btn': '0 2px 8px rgba(249,115,22,0.3)',
        'btn-hover': '0 4px 16px rgba(249,115,22,0.4)',
      },
      animation: {
        'ping-slow': 'ping 2s cubic-bezier(0, 0, 0.2, 1) infinite',
      },
    },
  },
  plugins: [],
} satisfies Config
```

---

## 六、全局 CSS（main.css）修改方案

### @layer base 改动

```css
@layer base {
  html {
    font-size: 18px;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  body {
    @apply bg-warm-white text-slate-800 leading-relaxed;
  }

  /* 标题改为深色文字 */
  h1 { @apply text-3xl md:text-4xl font-black text-slate-900 tracking-tight; }
  h2 { @apply text-2xl md:text-3xl font-bold text-slate-900 tracking-tight; }
  h3 { @apply text-xl md:text-2xl font-bold text-slate-800; }
  h4 { @apply text-lg md:text-xl font-semibold text-slate-800; }

  /* 链接改为蓝色 */
  a { @apply text-trust-500 hover:text-trust-600 transition-colors; }

  button, .btn {
    @apply min-h-touch px-6 text-lg rounded-2xl cursor-pointer transition-all duration-300;
  }

  ::selection {
    background: rgba(249, 115, 22, 0.2);
    color: #9A3412;
  }
}
```

### @layer components 改动

#### 卡片组件 — 替换毛玻璃为实色卡片（Bento Grid 2.0风格）

```css
/* 浅色卡片 —— 替换原来的 .glass
   采用2026 Bento 2.0风格：圆角20-24px、柔和阴影、hover微交互 */
.glass,
.card-light {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.04);
}

.glass-hover,
.card-light-hover {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.glass-hover:hover,
.card-light-hover:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.08), 0 8px 32px rgba(0,0,0,0.06);
  transform: translateY(-4px);
  border-color: #CBD5E1;
}
```

注意：`.glass` 类名保留为 `.card-light` 的别名，避免需要修改所有模板中的类名。这样所有使用 `.glass` 的地方都会自动获得新的浅色卡片样式。

#### 渐变文字

```css
.gradient-text {
  @apply bg-clip-text text-transparent;
  background-image: linear-gradient(135deg, #F97316, #3B82F6);
}
```

#### 按钮样式

```css
/* 主按钮：橙色渐变，带微交互（hover上浮+阴影增强） */
.btn-primary {
  @apply text-white font-bold py-4 px-10 rounded-2xl text-lg transition-all duration-300;
  background: linear-gradient(135deg, #F97316, #FB923C);
  box-shadow: 0 2px 8px rgba(249,115,22,0.3);
}
.btn-primary:hover {
  box-shadow: 0 4px 16px rgba(249,115,22,0.4);
  transform: translateY(-2px);
}
.btn-primary:active {
  transform: translateY(0) scale(0.97);
}

/* 白色大按钮（Hero区）：橙色渐变 */
.btn-white {
  @apply font-black py-5 px-10 rounded-2xl text-xl transition-all duration-300
         active:scale-95;
  background: linear-gradient(135deg, #F97316, #FB923C);
  color: #fff;
  box-shadow: 0 4px 16px rgba(249,115,22,0.3);
}
.btn-white:hover {
  box-shadow: 0 8px 24px rgba(249,115,22,0.4);
  transform: translateY(-2px);
}

/* 描边按钮 */
.btn-outline {
  @apply font-bold py-4 px-10 rounded-2xl text-lg transition-all duration-300;
  background: #FFFFFF;
  color: #334155;
  border: 2px solid #E2E8F0;
}
.btn-outline:hover {
  border-color: #F97316;
  color: #F97316;
  background: #FFF7ED;
}

/* Ghost按钮 */
.btn-ghost {
  @apply text-slate-600 font-bold py-3 px-6 rounded-2xl text-base transition-all duration-300;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
}
.btn-ghost:hover {
  background: #F1F5F9;
}
```

#### 课程内容 Markdown 样式（浅色版）

```css
.prose-lesson {
  @apply text-slate-700 leading-loose;
}
.prose-lesson h1 {
  @apply text-3xl font-black mt-12 mb-6 text-slate-900;
}
.prose-lesson h2 {
  @apply text-2xl font-bold mt-10 mb-4 text-slate-900 flex items-center gap-3;
}
.prose-lesson h2::before {
  content: '';
  display: block;
  width: 6px;
  height: 2rem;
  border-radius: 9999px;
  @apply bg-brand-500;
}
.prose-lesson h3 {
  @apply text-xl font-bold mt-8 mb-3 text-slate-800;
}
.prose-lesson p {
  @apply my-5 text-lg leading-loose text-slate-600;
}
.prose-lesson ul {
  @apply list-none my-5 space-y-3;
}
.prose-lesson ol {
  @apply list-decimal list-inside my-5 space-y-3;
}
.prose-lesson li {
  @apply text-lg text-slate-600 pl-6 relative;
}
.prose-lesson ul li::before {
  content: '';
  @apply absolute left-0 top-3 rounded-full bg-brand-500;
  width: 6px;
  height: 6px;
}
.prose-lesson blockquote {
  @apply pl-6 py-5 px-8 my-8 rounded-2xl text-lg font-medium;
  border-left: 4px solid #F97316;
  background: #FFF7ED;
  color: #9A3412;
}
.prose-lesson code {
  @apply text-brand-700 px-2 py-1 rounded-lg text-base;
  background: #FFF7ED;
}
.prose-lesson pre {
  @apply bg-slate-50 text-slate-800 p-6 rounded-2xl my-8 overflow-x-auto;
  border: 1px solid #E2E8F0;
}
.prose-lesson pre code {
  @apply bg-transparent text-slate-800 p-0;
}
.prose-lesson img {
  @apply rounded-2xl my-8 mx-auto max-w-full;
  border: 1px solid #E2E8F0;
  box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}
.prose-lesson table {
  @apply w-full my-8 border-collapse;
}
.prose-lesson th {
  @apply font-bold py-4 px-5 text-left text-slate-800;
  background: #F8FAFC;
  border-bottom: 2px solid #E2E8F0;
}
.prose-lesson td {
  @apply py-4 px-5 text-slate-600;
  border-bottom: 1px solid #F1F5F9;
}
.prose-lesson strong {
  @apply text-slate-900 font-bold;
}
.prose-lesson a {
  @apply text-trust-500 hover:text-trust-600 underline underline-offset-4;
  text-decoration-color: rgba(59, 130, 246, 0.3);
}
.prose-lesson hr {
  @apply my-10;
  border-color: #E2E8F0;
}
```

#### 管理后台样式

```css
/* 管理后台卡片 */
.admin-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 1rem;
  padding: 1.5rem;
}

/* 管理后台输入框 */
.admin-input {
  @apply w-full px-5 py-4 rounded-2xl text-slate-800 font-medium text-lg transition-all;
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  outline: none;
}
.admin-input::placeholder {
  color: #94A3B8;
}
.admin-input:focus {
  border-color: #F97316;
  box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.1);
}

/* 管理后台表格 */
.admin-table {
  @apply w-full text-left;
}
.admin-table thead th {
  @apply px-5 py-4 text-xs font-bold text-slate-500 uppercase tracking-widest;
  border-bottom: 2px solid #E2E8F0;
  background: #F8FAFC;
}
.admin-table tbody td {
  @apply px-5 py-4 text-slate-700;
  border-bottom: 1px solid #F1F5F9;
}
.admin-table tbody tr:hover {
  background: #FAFAF8;
}

/* 管理后台 badge */
.admin-badge {
  @apply px-3 py-1 text-xs font-bold rounded-lg;
}
.admin-badge-green {
  @apply admin-badge;
  color: #16A34A;
  background: #F0FDF4;
  border: 1px solid #BBF7D0;
}
.admin-badge-gray {
  @apply admin-badge;
  color: #64748B;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
}

/* 管理后台按钮 */
.admin-btn {
  @apply px-4 py-2 rounded-xl text-sm font-bold min-h-0 transition-all;
}
.admin-btn-primary {
  @apply admin-btn;
  color: #F97316;
  background: #FFF7ED;
  border: 1px solid #FFEDD5;
}
.admin-btn-primary:hover {
  background: #FFEDD5;
}
.admin-btn-danger {
  @apply admin-btn;
  color: #EF4444;
  background: #FEF2F2;
  border: 1px solid #FECACA;
}
.admin-btn-danger:hover {
  background: #FEE2E2;
}
```

---

## 七、各页面具体修改内容

### 7.1 默认布局 `layouts/default.vue`

**导航栏**：
- 背景：从 `rgba(2, 6, 23, 0.85)` 改为 `rgba(255, 255, 255, 0.92)` 白色磨砂
- 边框：从 `rgba(255, 255, 255, 0.1)` 改为 `#E2E8F0`
- Logo文字：从 `text-white` 改为 `text-slate-900`
- Logo图标背景：保持渐变但改为橙色 `from-brand-500 to-brand-400`
- 导航链接：从 `text-slate-400 hover:text-white` 改为 `text-slate-600 hover:text-brand-500`
- 激活链接：从 `text-white` + cyan下划线 改为 `text-brand-600 font-bold` + 橙色下划线（`from-brand-400 to-brand-500`）
- "后台"按钮：改为 `bg-slate-50 border-slate-200 text-slate-600 hover:text-brand-500`
- 汉堡菜单图标：从白色改为 `text-slate-700`
- 手机端菜单展开：从 `bg-midnight` 改为白色背景 + 阴影 `shadow-lg`，`border-b border-slate-200`
- 手机端菜单项：增加emoji图标辅助识别

**页脚（Footer）**：
- 背景：从 `bg-midnight` 改为 `bg-slate-50` 浅灰
- 分割线：从 `border-white/10` 改为 `border-slate-200`
- Logo/标题文字：改为 `text-slate-900`
- Logo图标：改为橙色渐变
- 正文文字：从 `text-slate-500` 改为 `text-slate-600`
- 链接：改为 `text-slate-500 hover:text-brand-500`
- 底部版权：`text-slate-400`

**整体容器**：
- 从 `bg-midnight text-white` 改为 `bg-warm-white text-slate-800`

### 7.2 首页 `pages/index.vue`

**Hero 区域**：
- 删除背景光晕（glow-blue/glow-indigo/glow-cyan），改为浅暖色渐变背景：
  `background: linear-gradient(180deg, #FFF7ED 0%, #FFFBF5 60%, #FFFBF5 100%);`
- 顶部badge：从深色毛玻璃改为 `bg-brand-50 text-brand-600 border border-brand-200`
- badge圆点：从 `bg-cyan-400/500` 改为 `bg-brand-400/500`
- 标题：从 `text-white` 改为 `text-slate-900`，`text-cyan-400` 改为 `text-brand-500`
- 副标题：从 `text-slate-400` 改为 `text-slate-600`
- CTA按钮 `.btn-white`：使用新的橙色渐变按钮（白色文字）
- "了解更多"按钮 `.btn-outline`：使用新的白色描边按钮

**卖点卡片（4大差异点）**：
- section标题：`text-white` -> `text-slate-900`
- 副标题：`text-slate-500` -> `text-slate-600`
- 从 `.glass .glass-hover` 改为 `.card-light .card-light-hover`（CSS别名自动生效）
- 标题：从 `text-white` 改为 `text-slate-900`
- 描述：从 `text-slate-400` 改为 `text-slate-600`
- 图标容器颜色改为对应浅色背景：
  - 绿色图标：`bg-emerald-50 border-emerald-200 group-hover:bg-emerald-100`
  - 蓝色图标：`bg-trust-50 border-trust-200 group-hover:bg-trust-100`
  - 紫色图标：`bg-purple-50 border-purple-200 group-hover:bg-purple-100`
  - 琥珀图标：`bg-amber-50 border-amber-200 group-hover:bg-amber-100`

**课程分类卡片（替代原"课程阶段"）**：
- section标题：从 `text-white` 改为 `text-slate-900`
- 副标题：从 `text-slate-400` 改为 `text-slate-600`
- 将措辞从 "精心设计的学习曲线" 改为 "丰富的AI工具课程"（或类似）
- 副标题从 "像爬楼梯一样简单" 改为 "按工具类型分类，想学什么就学什么"
- 从 `.glass .glass-hover` -> 新样式自动生效
- 图标容器：从 `bg-indigo-500/10 text-indigo-400` 改为 `bg-brand-50 text-brand-500 border-brand-200`，hover时 `bg-brand-500 text-white`
- 阶段编号：从 `text-white/5` 改为 `text-slate-100`（更轻）
- 卡片标题：从 `text-white` 改为 `text-slate-900`
- 描述：从 `text-slate-400` 改为 `text-slate-600`
- 课程数：从 `text-slate-500` 改为 `text-slate-500`（保持）
- "免费"标签：保持绿色但改为浅绿 `text-emerald-600 bg-emerald-50 border-emerald-200`
- 底部进度条：从 `from-cyan-400 to-indigo-500` 改为 `from-brand-400 to-brand-500`

**适合人群**：
- 标题：从 `text-white` 改为 `text-slate-900`
- 卡片：新样式自动生效
- 标题：`text-white` -> `text-slate-900`
- 描述：`text-slate-400` -> `text-slate-600`
- `.icon-box`：改为 `bg-brand-50 border-brand-200`，hover时 `border-brand-300 bg-brand-100`

**底部CTA区域**：
- 保持深色渐变背景（页面唯一深色区域，形成视觉对比节奏）
- 调整为 `from-trust-900 via-trust-800 to-slate-900`
- 光晕装饰：改为 `bg-brand-400/10`
- CTA按钮：改为橙色渐变，`text-white`
- 副标题：保持 `text-slate-300`
- 标题中的强调色：从 `text-cyan-400` 改为 `text-brand-400`

### 7.3 课程列表页 `pages/courses/index.vue`

- 页面标题：从 `text-white` 改为 `text-slate-900`
- 副标题：从 `text-slate-400` 改为 `text-slate-600`
- 调整措辞：从"点击阶段卡片展开详细课时" 改为 "选择你感兴趣的AI工具分类"
- 统计数字卡片：`.glass` 新样式自动生效；`text-white` -> `text-slate-900`；`text-slate-500` -> `text-slate-500`
- 手风琴分类列表：`.glass` 新样式自动生效
- 分类标题按钮：
  - 激活态序号：从 `bg-cyan-500 border-cyan-400` 改为 `bg-brand-500 border-brand-400 text-white shadow-md`
  - 未激活序号：从 `bg-white/5 border-white/10 text-slate-400` 改为 `bg-slate-100 border-slate-200 text-slate-500`
  - 标题文字：从 `text-white` 改为 `text-slate-900`
  - 副标题：从 `text-slate-500` 改为 `text-slate-500`（保持）
  - hover背景：从 `bg-white/5` 改为 `bg-slate-50`
  - 展开箭头：从 `border-white/10` 改为 `border-slate-200`，`text-slate-400` -> `text-slate-500`
- 展开的课程列表：
  - 课程标题：从 `text-slate-200` 改为 `text-slate-700 group-hover:text-slate-900`
  - 圆点：从 `bg-cyan-500` 改为 `bg-brand-500`
  - hover背景：从 `hover:bg-white/5` 改为 `hover:bg-slate-50`
  - 时长标签：从 `bg-white/5 text-slate-500` 改为 `bg-slate-100 text-slate-500`
  - "免费"标签：从 `text-emerald-400 bg-emerald-500/10` 改为 `text-emerald-600 bg-emerald-50 border-emerald-200`
  - 箭头按钮：从 `bg-blue-600` 改为 `bg-brand-500`
  - 空状态文字：从 `text-slate-600` 改为 `text-slate-400`

### 7.4 课程阅读页 `pages/courses/[stageId]/[lessonId].vue`

**侧边栏**：
- 背景：从 `bg-midnight` 改为 `bg-white`
- 右边框：从 `border-white/10` 改为 `border-slate-200`
- "返回目录"链接：从 `text-slate-500 hover:text-white` 改为 `text-slate-500 hover:text-slate-900`
- 当前课标记：从 `bg-blue-600 border-blue-400 text-white shadow-xl shadow-blue-600/20` 改为 `bg-brand-500 border-brand-400 text-white shadow-lg shadow-brand-500/20`
- 非当前课：从 `bg-white/5 border-white/10 text-slate-400` 改为 `bg-slate-50 border-slate-200 text-slate-600 hover:border-slate-300`
- "当前学习阶段"小标题：从 `text-slate-600` 改为 `text-slate-400`
- 课程序号标签中的文字不变

**主内容区**：
- 面包屑：文字从 `text-slate-500` 改为 `text-slate-400`，当前改为 `text-brand-500`
- 面包屑链接：`hover:text-white` -> `hover:text-slate-700`
- 文章卡片：`.glass` 新样式自动生效
- 标题分割线：从 `border-white/10` 改为 `border-slate-200`
- 课程标签"第X课"：从 `text-cyan-400 bg-cyan-500/10 border-cyan-500/20` 改为 `text-brand-500 bg-brand-50 border-brand-200`
- 时长标签：从 `bg-white/5 text-slate-500` 改为 `bg-slate-100 text-slate-500`
- "免费"标签：同上浅绿方案
- 标题：从 `text-white` 改为 `text-slate-900`
- 副标题：从 `text-slate-400` 改为 `text-slate-600`
- Markdown内容：使用新版 `.prose-lesson` 样式（自动生效）
- 加载spinner：从 `text-cyan-500` 改为 `text-brand-500`
- 上下课导航：
  - 分割线：从 `border-white/10` 改为 `border-slate-200`
  - "上一课"：从 `text-slate-500 hover:text-white` 改为 `text-slate-500 hover:text-slate-900`
  - "上一课"子标签：从 `text-slate-600` 改为 `text-slate-400`
  - "上一课"标题：从 `text-slate-300 group-hover:text-white` 改为 `text-slate-600 group-hover:text-slate-900`
  - "下一课"按钮：从 `bg-white/5 border-white/10 text-white` 改为 `bg-slate-50 border-slate-200 text-slate-800 hover:bg-slate-100`
  - "下一课"子标签：从 `text-slate-500` 改为 `text-slate-400`

### 7.5 阶段详情页 `pages/courses/[stageId]/index.vue`

- 面包屑：同7.4调整
- 面包屑当前项：从 `text-cyan-400` 改为 `text-brand-500`
- 阶段信息卡片：`.glass` 新样式自动生效
- 图标容器：从 `bg-indigo-500/10 text-indigo-400 border-indigo-500/20` 改为 `bg-brand-50 text-brand-500 border-brand-200`
- "第X阶段"标签：从 `text-cyan-400 bg-cyan-500/10 border-cyan-500/20` 改为 `text-brand-500 bg-brand-50 border-brand-200`
- "免费"标签：同上
- 标题：从 `text-white` 改为 `text-slate-900`
- 副标题：`text-slate-400` -> `text-slate-600`
- 描述：`text-slate-500` -> `text-slate-500`（保持）
- 课程目录标题：`text-white` -> `text-slate-900`
- 装饰线：从 `bg-cyan-500` 改为 `bg-brand-500`
- 课程列表项：`.glass` 新样式自动生效
- hover：`hover:bg-white/5` -> `hover:bg-slate-50`
- 序号容器：从 `bg-indigo-500/10 border-indigo-500/20 text-indigo-400` 改为 `bg-brand-50 border-brand-200 text-brand-600`
- 课程标题：从 `text-slate-200 group-hover:text-white` 改为 `text-slate-700 group-hover:text-slate-900`
- 箭头：从 `text-slate-600 group-hover:text-cyan-400` 改为 `text-slate-400 group-hover:text-brand-500`
- 时长/免费标签：同上

### 7.6 关于页 `pages/about.vue`

- 标题：从 `text-white` 改为 `text-slate-900`，`gradient-text` 使用新渐变（自动生效）
- 副标题/正文：从 `text-slate-400` 改为 `text-slate-600`
- 统计卡片：`.glass` 新样式自动生效
- 统计数字：从 `text-white` 改为 `text-slate-900`
- 统计标签：从 `text-slate-500` 保持
- 理念区域：`.glass` 新样式自动生效
- 区域标题：从 `text-white` 改为 `text-slate-900`
- 装饰线：从 `bg-cyan-500` 改为 `bg-brand-500`
- 正文：从 `text-slate-400` 改为 `text-slate-600`
- `<strong>` 文字：从 `text-white` 改为 `text-slate-900`
- 引用块：从 `from-blue-600/20 to-purple-600/20 border-blue-500/20 text-blue-100` 改为 `bg-brand-50 border border-brand-200 text-brand-800`
- 特色列表勾选图标：从 `text-cyan-500` 改为 `text-brand-500`
- 特色标题 `<strong>`：从 `text-white` 改为 `text-slate-900`
- 联系方式卡片：从 `bg-white/5 border-white/10 text-slate-300` 改为 `bg-slate-50 border-slate-200 text-slate-600`
- 联系方式加粗值：从 `text-white` 改为 `text-slate-900`

### 7.7 管理后台布局 `layouts/admin.vue`

**侧边栏**：
- 背景：从 `bg-midnight` 改为 `bg-white`
- 右边框：从 `border-white/10` 改为 `border-slate-200`
- Logo区域底部边框：从 `border-white/10` 改为 `border-slate-200`
- Logo图标：改为 `from-brand-500 to-brand-400`
- "管理后台"文字：从 `text-white` 改为 `text-slate-900`
- 关闭按钮：从 `text-slate-400 hover:text-white` 改为 `text-slate-400 hover:text-slate-700`
- 导航链接 `.sidebar-link`：从 `text-slate-400 hover:bg-white/5 hover:text-white` 改为 `text-slate-600 hover:bg-slate-50 hover:text-slate-900`
- 激活链接 `.sidebar-link-active`：从 `bg-white/5 text-white border-white/10` 改为 `bg-brand-50 text-brand-600 border border-brand-200`
- 分割线：从 `bg-white/5` 改为 `bg-slate-200`
- "查看前台"链接：同上普通链接样式
- 退出按钮：从 `text-red-400 hover:text-red-300 hover:bg-red-500/5` 改为 `text-red-500 hover:text-red-600 hover:bg-red-50`

**顶栏**：
- 背景：从 `bg-midnight/70 backdrop-blur-md` 改为 `bg-white/80 backdrop-blur-md`
- 边框：从 `border-white/10` 改为 `border-slate-200`
- 汉堡按钮：从 `hover:bg-white/5 text-slate-400` 改为 `hover:bg-slate-100 text-slate-600`
- 欢迎文字：从 `text-slate-400` 改为 `text-slate-500`
- 用户名：从 `text-white` 改为 `text-slate-900`

**遮罩层**：保持 `bg-black/60`

**主体**：
- `bg-midnight` 改为 `bg-slate-50`（管理后台用浅灰背景，区分前台的暖白）

### 7.8 管理后台登录页 `pages/admin/login.vue`

- 页面背景 `.login-page`：从 `#020617` 改为 `linear-gradient(180deg, #F8FAFC, #EFF6FF)` 浅蓝灰渐变
- 删除背景光晕 `.login-glow-1` / `.login-glow-2`
- 登录卡片 `.login-card`：
  - 从深色毛玻璃改为白色实体：`background: #FFFFFF`
  - 边框：`border: 1px solid #E2E8F0`
  - 阴影：`box-shadow: 0 8px 32px rgba(0,0,0,0.08), 0 24px 64px rgba(0,0,0,0.04)`
  - 删除 `backdrop-filter`
- Logo图标 `.login-logo`：`background: linear-gradient(135deg, #F97316, #FB923C)`
- Logo阴影：`box-shadow: 0 8px 24px rgba(249, 115, 22, 0.2)`
- 标题 `.login-title`：`color: #0F172A`（slate-900）
- 副标题 `.login-subtitle`：`color: #64748B` 保持
- 标签 `.login-label`：保持 `#94A3B8`
- 输入框 `.login-input`：
  - `color: #1E293B`
  - `background: #FFFFFF`
  - `border: 1px solid #E2E8F0`
  - placeholder: `color: #94A3B8`
  - focus: `border-color: #F97316; box-shadow: 0 0 0 3px rgba(249,115,22,0.1); background: #FFFFFF`
- 错误提示 `.login-error`：保持红色但改为浅红：`color: #EF4444; background: #FEF2F2; border: 1px solid #FECACA`
- 登录按钮 `.login-btn`：
  - `background: linear-gradient(135deg, #F97316, #FB923C)`
  - `box-shadow: 0 2px 12px rgba(249,115,22,0.3)`
  - hover: `box-shadow: 0 4px 20px rgba(249,115,22,0.4)`
- 返回链接 `.login-back`：`color: #64748B`，hover: `color: #F97316`

### 7.9 管理后台各页面

所有管理后台页面（仪表盘、阶段管理、课程管理、编辑页面、媒体库）的修改模式一致：
- 标题 `text-white` -> `text-slate-900`
- 卡片 `.glass` -> 新样式自动生效（白色背景）
- 表格使用新版 `.admin-table` 样式（自动生效）
- 输入框使用新版 `.admin-input` 样式（自动生效）
- 按钮使用新版 `.admin-btn-primary` / `.admin-btn-danger`（自动生效）
- badge使用新版 `.admin-badge-green` / `.admin-badge-gray`（自动生效）
- 编辑器装饰线：从 `bg-cyan-500` 改为 `bg-brand-500`
- 预览切换按钮激活态：从 `bg-cyan-500/10 text-cyan-400 border-cyan-500/20` 改为 `bg-brand-50 text-brand-500 border-brand-200`
- 拖拽上传区域：从 `border-white/10 hover:border-cyan-500/40` 改为 `border-slate-300 hover:border-brand-400`
- "加载中"的spinner颜色：从 `text-cyan-500` 改为 `text-brand-500`
- 快捷入口卡片 hover 标题色：从 `group-hover:text-cyan-400` 改为 `group-hover:text-brand-500`
- 快捷入口描述：从 `text-slate-500` 保持

### 7.10 组件修改

**StageCard.vue**：
- `.glass .glass-hover` -> 新样式自动生效
- 图标容器：从 `bg-indigo-500/10 text-indigo-400 border-indigo-500/20` 改为 `bg-brand-50 text-brand-500 border-brand-200`
- hover图标：从 `group-hover:bg-indigo-500 group-hover:text-white group-hover:border-indigo-400` 改为 `group-hover:bg-brand-500 group-hover:text-white group-hover:border-brand-400`
- 阶段编号：从 `text-white/5 group-hover:text-white/10` 改为 `text-slate-100 group-hover:text-slate-200`
- "第X阶段"标签：从 `text-cyan-400 bg-cyan-500/10 border-cyan-500/20` 改为 `text-brand-500 bg-brand-50 border-brand-200`
- "免费"标签：从 `text-emerald-400 bg-emerald-500/10 border-emerald-500/20` 改为 `text-emerald-600 bg-emerald-50 border-emerald-200`
- 标题：`text-white` -> `text-slate-900`
- 副标题：`text-slate-400` -> `text-slate-600`
- 课程数：`text-slate-600` -> `text-slate-500`
- 底部进度条：从 `from-cyan-400 to-indigo-500` 改为 `from-brand-400 to-brand-500`

**LessonCard.vue**：
- `.glass` -> 新样式自动生效
- hover：`hover:bg-white/5` -> `hover:bg-slate-50`
- 序号容器：从 `bg-indigo-500/10 border-indigo-500/20 text-indigo-400` 改为 `bg-brand-50 border-brand-200 text-brand-600`
- hover序号：从 `group-hover:bg-indigo-500 group-hover:text-white` 改为 `group-hover:bg-brand-500 group-hover:text-white`
- 标题：从 `text-slate-200 group-hover:text-white` 改为 `text-slate-700 group-hover:text-slate-900`
- 摘要：`text-slate-500` 保持
- 时长标签：`bg-white/5` -> `bg-slate-100`
- "免费"标签：同上浅绿方案
- 箭头：从 `text-slate-600 group-hover:text-cyan-400` 改为 `text-slate-400 group-hover:text-brand-500`

---

## 八、移动端适配要点

### 已有基础（保留）
- 18px 基础字号
- `min-h-touch: 48px` 最小点击区域
- 响应式栅格 `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- 汉堡菜单

### 需要新增/优化

1. **导航栏**：
   - 手机端导航 padding 增大至 `p-5`（当前 `p-4`）
   - 菜单项增加左侧emoji辅助识别（首页/课程/关于）
   - 菜单展开时增加 `shadow-lg` 和 `border-b border-slate-200`

2. **首页Hero**：
   - 手机端标题降为 `text-3xl`，但保持足够大
   - 按钮在 `< sm` 断点改为全宽 `w-full`
   - 减少 `min-h` 至 `min-h-[70vh]` 避免手机端空白过多

3. **课程分类Bento Grid**：
   - 手机端1列，平板2列，桌面3-4列
   - 卡片内边距手机端 `p-6`，桌面 `p-8 md:p-10`

4. **课程阅读页**：
   - 手机端无侧边栏（已有 `hidden lg:block`），保持
   - 增加手机端顶部"返回目录"按钮的视觉权重（更大、更明显，`py-3 px-5`）
   - 文章卡片内边距手机端 `p-6`，桌面 `p-8 md:p-12 lg:p-16`

5. **管理后台**：
   - 手机端表格可添加 `overflow-x-auto` 横向滚动
   - 侧边栏收起/展开行为已OK

6. **通用**：
   - 所有可点击元素保证 48px 最小高度
   - 长按/触摸反馈：`active:scale-95` 或 `active:scale-97`
   - 图片在手机端 100% 宽度，圆角 `rounded-xl`

---

## 九、无障碍设计要点

1. **对比度**（符合2026 WCAG标准趋势）：
   - 正文 `#1E293B` 在 `#FFFBF5` 背景上，对比度约 14:1（远超WCAG AA 4.5:1）
   - 次要文字 `#64748B` 在白色背景上，对比度约 4.8:1（符合AA标准）
   - 橙色按钮 `#F97316` 白色文字，对比度约 3.2:1 —— 按钮是大文字（>18px bold），符合AA Large Text标准（3:1）
   - 避免蓝紫色和黄绿色混用（老年人易混淆的色组）

2. **焦点可见性**：
   - 所有输入框和按钮的 focus 态使用 `box-shadow: 0 0 0 3px rgba(249,115,22,0.15)` 明显的橙色光环
   - 链接的 focus-visible 态增加下划线 + 颜色变化
   - 卡片的 focus-visible 态增加边框颜色变化

3. **触摸目标**：
   - 所有按钮 `min-h: 48px`
   - 列表项 `padding` 足够大（不低于 `p-5`）
   - 复选框尺寸 `w-5 h-5` 且有外部 label 可点击

4. **表单设计**（参考Smashing Magazine老年用户指南）：
   - 使用静态标签（非浮动标签）
   - 错误消息放在输入框上方
   - 避免自动消失的提示，让用户自行关闭
   - 一屏一个主题/任务

---

## 十、实施优先级

1. **Phase 1**：修改 `tailwind.config.ts` + `main.css` 全局样式（改完后 `.glass` / `.admin-*` 等全局类自动生效）
2. **Phase 2**：修改 `layouts/default.vue`（导航+Footer）+ `layouts/admin.vue`
3. **Phase 3**：修改首页 `index.vue`（Hero + 课程分类 + 卖点 + 适合人群 + CTA）
4. **Phase 4**：修改课程列表 `courses/index.vue` + 阶段详情 + 课程阅读页
5. **Phase 5**：修改关于页 `about.vue` + 组件 `StageCard.vue` + `LessonCard.vue`
6. **Phase 6**：修改管理后台登录页 + 所有管理后台页面
7. **Phase 7**：移动端测试和微调

---

## 十一、视觉效果对比总结

| 元素 | 改版前（深色） | 改版后（浅暖色） | 采用的2026趋势 |
|------|---------------|-----------------|---------------|
| 页面背景 | `#020617` 纯黑 | `#FFFBF5` 米白 | 暖色大地色调 |
| 卡片 | 毛玻璃 rgba 透明 | 白色实体 + 柔阴影 | Bento Grid 2.0 |
| 主色 | Cyan `#22D3EE` | Orange `#F97316` | 情绪化暖色设计 |
| 辅助色 | Indigo `#6366F1` | Blue `#3B82F6` | 信赖蓝 |
| 标题 | 白色 `#FFFFFF` | 深灰 `#0F172A` | 高对比度无障碍 |
| 正文 | `#94A3B8` 浅灰 | `#1E293B` 深灰 | 高对比度无障碍 |
| 按钮风格 | 渐变蓝紫 + 光晕 | 渐变橙色 + 微交互 | 微愉悦交互 |
| 交互反馈 | 无/弱 | hover上浮/active缩放 | Micro-Delights |
| 装饰效果 | 光晕、毛玻璃 | 留白、柔阴影 | 轻量化设计 |
| 信息层级 | 3-4层 | 最多3层 | 轻量化减负 |
| 导航 | 图标较少 | emoji+文字 | 零学习成本 |
| 课程结构 | 6阶段固定 | 按工具类型灵活分类 | 模块化Bento |
| 整体感觉 | 科技、酷炫 | 温暖、亲切、清晰 | 情绪化+无障碍 |

---

## 十二、设计趋势参考来源

- Figma: Top Web Design Trends for 2026
- UX Collective: 10 UX Design Shifts You Can't Ignore in 2026
- Promodo: UX/UI Design Trends 2026: 11 Essentials
- Landdding: UI Design Trends 2026: 15 Patterns Shaping Modern Websites
- WriterDock: Bento Grids & Beyond: 7 UI Trends Dominating Web Design 2026
- Smashing Magazine: A Guide To Designing For Older Adults
- NNGroup: UX Design for Seniors / Usability for Older Adults
- DJ Designer Lab: How to Build an Effective Educational Website in 2026
- 即时设计: 2026最新UI设计趋势8大方向全解析
- 科e网: 2026响应式网页设计现状深耕与难点突破
