# AI不难学 - 管理后台视觉设计规范 v1.0

> 本规范基于用户端设计风格，结合 2025-2026 年管理后台设计趋势，为 9 个管理页面提供统一的视觉升级方案。

---

## 一、设计理念

### 核心原则
1. **品牌统一** — 管理端与用户端共享品牌色（橙色渐变）和信任色（蓝色），保持视觉一致性
2. **专业高效** — 管理端侧重信息密度和操作效率，圆角和间距适度收敛（相比用户端）
3. **温暖亲切** — 延续用户端的暖色调和柔和质感，避免冷硬的传统后台风格
4. **极简克制** — 减少视觉噪音，聚焦数据与操作，留白充分

### 设计亮点
- 深色品牌渐变侧边栏（从 slate-900 到 slate-800 的深色底，配合橙色品牌色高亮）
- 欢迎横幅区域（仪表盘顶部，带渐变背景和问候语）
- 统计卡片带微妙的顶部色条
- 表格行悬停效果 + 操作列优化
- 统一的空状态/加载状态插画风格
- 全局 300ms 过渡动画，与用户端一致

---

## 二、整体布局架构

### 布局结构
```
+------+----------------------------------------+
|      |  顶栏 (h-16, sticky, 毛玻璃效果)        |
|      +----------------------------------------+
| 侧   |                                        |
| 边   |  内容区                                  |
| 栏   |  (p-6 md:p-8, max-w-7xl, mx-auto)      |
| w-64 |                                        |
|      |                                        |
+------+----------------------------------------+
```

### 侧边栏 (Sidebar)
- **宽度**: `w-64` (256px)，移动端抽屉式展开
- **背景**: 深色渐变 `bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900`
- **Logo区域**: h-16, 左侧显示品牌图标（橙色渐变底）+ "AI不难学" 白色文字 + "管理后台" 小字
- **导航项**:
  - 默认: `text-slate-400`, hover: `text-white bg-white/10`
  - 激活: `text-white bg-white/10 border-l-3 border-brand-500` 或 `bg-brand-500/15 text-brand-300`
  - 图标 + 文字，py-3 px-4，圆角 rounded-lg
- **分隔线**: `border-slate-700/50`, 用于分隔主导航与辅助链接
- **底部**: 退出登录按钮 + 查看前台链接，使用 `text-slate-500` 色调
- **移动端**: 抽屉从左侧滑入，遮罩 `bg-black/60 backdrop-blur-sm`

### 顶栏 (Header)
- **高度**: `h-16`
- **背景**: `bg-white/80 backdrop-blur-md`（毛玻璃效果）
- **左侧**: 面包屑导航（可选，用 `/` 分隔），移动端显示汉堡菜单按钮
- **右侧**: 管理员头像圆圈（brand-100底 + brand首字母） + 管理员名称
- **底边框**: `border-b border-slate-200/80`
- **z-index**: `z-30`, sticky定位

### 内容区 (Main)
- **内边距**: `p-6 md:p-8`
- **最大宽度**: 不设固定max-width（表格页面需要宽屏），表单页面自行 `max-w-3xl` 或 `max-w-5xl`
- **背景色**: `bg-slate-50`（整页背景，非 warm-white，用于与用户端区分管理语境）

---

## 三、色彩系统

### 主色
| 用途 | 色值 | Tailwind Token | 说明 |
|------|------|----------------|------|
| 品牌主色 | `#F97316` | `brand-500` | 按钮、高亮、激活状态 |
| 品牌渐变 | `#F97316 → #FB923C` | `from-brand-500 to-brand-400` | 渐变按钮、Logo背景 |
| 品牌浅底 | `#FFF7ED` | `brand-50` | 激活项背景、badge背景 |
| 信任蓝 | `#3B82F6` | `trust-500` | 链接、信息提示 |

### 中性色（管理端专用灰度层级）
| 用途 | 色值 | Token |
|------|------|-------|
| 页面背景 | `#F8FAFC` | `slate-50` |
| 卡片/面板背景 | `#FFFFFF` | `white` |
| 细边框 | `#E2E8F0` | `slate-200` |
| 浅分割线 | `#F1F5F9` | `slate-100` |
| 次要文字 | `#64748B` | `slate-500` |
| 主文字 | `#1E293B` | `slate-800` |
| 标题文字 | `#0F172A` | `slate-900` |
| 侧边栏深底 | `#0F172A → #1E293B` | `slate-900 → slate-800` |

### 功能色 / 状态色
| 状态 | 主色 | 浅底色 | 边框色 | 用途 |
|------|------|--------|--------|------|
| 成功 | `#16A34A` | `#F0FDF4` | `#BBF7D0` | 已发布、保存成功、是 |
| 警告 | `#D97706` | `#FFFBEB` | `#FDE68A` | 草稿状态 |
| 危险 | `#EF4444` | `#FEF2F2` | `#FECACA` | 删除、错误提示 |
| 信息 | `#3B82F6` | `#EFF6FF` | `#BFDBFE` | 链接、信息提示 |

---

## 四、排版规范

### 字号层级（管理端适当收紧）
| 层级 | 字号 | 行高 | 字重 | 用途 |
|------|------|------|------|------|
| 页面标题 | 24px (text-2xl) | 36px | font-black (900) | 页面顶部 H1 |
| 区块标题 | 18px (text-lg) | 28px | font-bold (700) | 卡片区块标题 |
| 正文 | 15px (text-[15px]) | 24px | font-medium (500) | 表格内容、导航文字 |
| 辅助文字 | 14px (text-sm) | 20px | font-medium (500) | 标签、描述、时间 |
| 微小文字 | 12px (text-xs) | 18px | font-bold (700) | badge、表头 |

### 字体
继承用户端字体栈：`-apple-system, "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif`

代码/编辑器区域使用：`ui-monospace, "SF Mono", "Menlo", monospace`

---

## 五、组件规范

### 5.1 卡片 (Card)
```css
/* 基础管理卡片 */
.admin-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 1rem;        /* 16px — 比用户端的 2.5rem 更紧凑 */
  padding: 1.5rem;
  transition: all 0.2s ease;
}

/* 带顶部色条的统计卡片 */
.admin-stat-card {
  /* 继承 admin-card */
  border-top: 3px solid;       /* 颜色动态设置 */
  padding-top: 1.25rem;
}
```

### 5.2 按钮 (Button)

#### 主要按钮 (Primary)
- 保存、创建等主操作
- 背景: `linear-gradient(135deg, #F97316, #FB923C)`
- 文字: 白色, font-bold
- 圆角: `rounded-xl` (12px)
- 内边距: `py-3 px-6`（管理端比用户端紧凑）
- Hover: `translateY(-1px)`, 阴影加深
- Active: `scale(0.98)`
- Disabled: `opacity-50, cursor-not-allowed`

#### 次要按钮 (Secondary/Outline)
- 取消、返回等次操作
- 背景: `#FFFFFF`
- 边框: `2px solid #E2E8F0`
- 文字: `#334155` (slate-700)
- Hover: 边框变 `#F97316`, 文字变 `#F97316`, 背景变 `#FFF7ED`

#### 操作按钮 (Action - 用在表格等紧凑场景)
- 编辑：`bg-brand-50 text-brand-600 border border-brand-200`, hover `bg-brand-100`
- 删除：`bg-red-50 text-red-600 border border-red-200`, hover `bg-red-100`
- 尺寸：`text-sm py-2 px-4 rounded-xl min-h-0`

#### 文字按钮 (Ghost)
- 返回列表等
- 无背景，`text-slate-500`, hover `text-slate-900`
- 搭配左箭头图标

### 5.3 表格 (Table)

```css
.admin-table {
  width: 100%;
  text-align: left;
}

/* 表头 */
.admin-table thead th {
  padding: 14px 20px;
  font-size: 12px;
  font-weight: 700;
  color: #64748B;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  background: #F8FAFC;
  border-bottom: 2px solid #E2E8F0;
}

/* 表体 */
.admin-table tbody td {
  padding: 16px 20px;
  color: #475569;
  border-bottom: 1px solid #F1F5F9;
  font-size: 15px;
}

/* 行悬停 */
.admin-table tbody tr:hover {
  background: #FFFBF5;  /* 使用用户端的 warm-white 作为 hover 底色，呼应品牌 */
}

/* 斑马纹（可选，默认不启用） */
.admin-table-striped tbody tr:nth-child(even) {
  background: #FAFAFA;
}
```

### 5.4 表单 (Form)

#### 输入框
- 背景: `#FFFFFF`
- 边框: `1px solid #E2E8F0`, 圆角 `rounded-xl` (12px)
- 内边距: `py-3.5 px-5`
- 字号: `text-base` (16px for admin context)
- Focus: 边框 `#F97316`, `box-shadow: 0 0 0 3px rgba(249,115,22,0.1)`
- Placeholder: `#94A3B8`

#### 标签 (Label)
- 字号: `text-sm` (14px)
- 字重: `font-semibold`
- 颜色: `#475569` (slate-600)
- 底部间距: `mb-2`

#### 选择框 (Select)
- 与输入框样式一致
- 添加自定义下拉箭头（品牌色）

#### 复选框 (Checkbox)
- 尺寸: `w-5 h-5`
- 选中色: `accent-brand-500`
- 搭配 `text-slate-700` 标签文字

#### 文本域 (Textarea)
- 与输入框样式一致
- 最小高度: `min-h-[120px]`
- Markdown编辑器: 使用 `font-mono text-sm leading-relaxed`

### 5.5 徽章 (Badge)

| 类型 | 文字色 | 背景色 | 边框色 | 用途 |
|------|--------|--------|--------|------|
| 成功/绿色 | `#16A34A` | `#F0FDF4` | `#BBF7D0` | 已发布、是、免费 |
| 灰色/默认 | `#64748B` | `#F8FAFC` | `#E2E8F0` | 草稿、否 |
| 警告/黄色 | `#D97706` | `#FFFBEB` | `#FDE68A` | 待审核 |
| 危险/红色 | `#EF4444` | `#FEF2F2` | `#FECACA` | 下架 |
| 品牌/橙色 | `#F97316` | `#FFF7ED` | `#FFEDD5` | 推荐、新 |

- 尺寸: `text-xs font-bold px-3 py-1 rounded-lg`
- 可选圆点前缀: `w-1.5 h-1.5 rounded-full` 在文字前

### 5.6 消息提示 (Alert / Toast)

```css
/* 成功 */
.admin-alert-success {
  background: #F0FDF4;
  border: 1px solid #BBF7D0;
  color: #16A34A;
  border-radius: 12px;
  padding: 14px 20px;
  font-size: 15px;
}

/* 错误 */
.admin-alert-error {
  background: #FEF2F2;
  border: 1px solid #FECACA;
  color: #EF4444;
  border-radius: 12px;
  padding: 14px 20px;
  font-size: 15px;
}
```

### 5.7 模态框 (Modal) — 用于确认删除等

- 遮罩: `bg-black/60 backdrop-blur-sm`
- 卡片: `bg-white rounded-2xl shadow-2xl max-w-md p-8`
- 标题: `text-xl font-bold text-slate-900`
- 描述: `text-slate-500 mt-2`
- 按钮: 底部右对齐，主操作 + 取消
- 进入动画: `scale(0.95) → scale(1)` + `opacity 0 → 1`, 300ms

---

## 六、侧边栏深色设计（重点改造项）

### 当前问题
当前侧边栏是白色背景 + 浅灰边框，与内容区缺乏层次感，且缺少品牌识别度。

### 改造方案
```
┌─────────────────┐
│  [橙色图标] AI不难学  │  ← Logo区: 白色文字 + 橙色渐变图标
│  管理后台            │
├─────────────────┤
│                     │
│  ■ 仪表盘         │  ← 激活项: 左侧橙色竖条 + 半透明白底
│    分类管理         │  ← 默认: slate-400 文字
│    课程管理         │
│    媒体库           │
│                     │
│  ─────────────── │  ← 分隔线: slate-700/50
│    查看前台   ↗    │  ← 辅助链接
│    退出登录         │  ← 红色系
└─────────────────┘
```

### 关键 CSS
```css
/* 侧边栏容器 */
aside {
  background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
}

/* Logo区 */
.sidebar-logo-text {
  color: #FFFFFF;
  font-weight: 900;
  font-size: 18px;
}
.sidebar-logo-sub {
  color: #94A3B8;
  font-size: 12px;
}

/* 导航链接 */
.sidebar-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  border-radius: 10px;
  color: #94A3B8;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.2s;
}
.sidebar-link:hover {
  color: #FFFFFF;
  background: rgba(255, 255, 255, 0.08);
}

/* 激活态 */
.sidebar-link-active {
  color: #FFFFFF;
  background: rgba(249, 115, 22, 0.15);
  border-left: 3px solid #F97316;
  font-weight: 600;
}
.sidebar-link-active .icon {
  color: #FB923C;
}
```

---

## 七、仪表盘欢迎横幅

### 设计方案
在仪表盘页面顶部增加一个欢迎横幅，取代简单的 H1 标题。

```
┌────────────────────────────────────────────┐
│  ☀ 下午好，管理员                            │
│  今天是 2026年3月10日                        │
│  目前有 12 节课程已发布，3 篇草稿待处理        │
│                                    [去创建→] │
└────────────────────────────────────────────┘
```

### 样式
```css
.welcome-banner {
  background: linear-gradient(135deg, #FFF7ED 0%, #EFF6FF 100%);
  border: 1px solid #FFEDD5;
  border-radius: 1rem;
  padding: 24px 32px;
  margin-bottom: 32px;
}
```

- 左侧大图标（太阳/月亮根据时间段变化）
- 问候语: `text-xl font-bold text-slate-900`
- 日期/摘要: `text-sm text-slate-500`
- 右侧可放快捷操作按钮

---

## 八、数据可视化卡片（仪表盘统计区）

### 当前问题
统计卡片只有图标 + 数字 + 标签，缺乏视觉层次和品牌感。

### 改造方案
每张卡片增加顶部 3px 色条（对应图标颜色），并优化布局：

```
┌──────────────────┐
│████████████████│  ← 3px 色条 (蓝/紫/绿/橙...)
│                  │
│  [图标]           │
│  12              │  ← 数值: text-3xl font-black
│  课程总数         │  ← 标签: text-sm text-slate-500
│  ↑ 较上周+2      │  ← 趋势指示（可选，未来可接入）
└──────────────────┘
```

### 样式关键点
- 卡片: `admin-card` + `border-t-3 border-{color}-400`
- 图标: `w-11 h-11 rounded-xl` 带对应浅色背景
- 数值: `text-3xl font-black text-slate-900 mt-3`
- 标签: `text-sm text-slate-500 font-medium mt-1`
- Grid: `grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-5`

---

## 九、空状态设计

### 统一风格
```
        ┌──────────┐
        │  [Icon]  │   ← 大图标 w-16 h-16, text-slate-200
        │          │
        │ 暂无数据  │   ← text-lg font-bold text-slate-400
        │ 描述文字  │   ← text-sm text-slate-400 mt-2
        │          │
        │ [操作按钮] │   ← 可选的引导按钮
        └──────────┘
```

### 使用场景
- 课程列表为空 → "暂无课程，点击右上角创建第一节课"
- 媒体库为空 → "暂无媒体文件，上传第一个文件吧"
- 最近更新为空 → "暂无课程数据"

### 样式
```css
.admin-empty {
  text-align: center;
  padding: 48px 24px;
}
.admin-empty-icon {
  width: 64px;
  height: 64px;
  color: #CBD5E1;
  margin: 0 auto 16px;
}
.admin-empty-title {
  font-size: 16px;
  font-weight: 700;
  color: #94A3B8;
}
.admin-empty-desc {
  font-size: 14px;
  color: #94A3B8;
  margin-top: 8px;
}
```

---

## 十、加载状态设计

### 骨架屏 (Skeleton)
对表格和卡片使用骨架屏代替简单的 spinner：

```css
.skeleton {
  background: linear-gradient(90deg, #F1F5F9 25%, #E2E8F0 50%, #F1F5F9 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: 8px;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### 使用方式
- 统计卡片加载: 6个骨架卡片 (h-24 的矩形)
- 表格加载: 5-6 行骨架行 (不同宽度的条状)
- 页面级 spinner: 保留当前的旋转图标，但居中显示在内容区

### 按钮加载态
- 文字切换为 "保存中..." / "创建中..."
- 添加 `animate-spin` 小图标在文字前
- `opacity-70` + `pointer-events-none`

---

## 十一、动画与过渡规范

### 全局过渡
| 属性 | 时长 | 缓动 | 使用场景 |
|------|------|------|----------|
| 颜色/背景/边框 | 200ms | ease | hover效果、状态切换 |
| 位移/缩放 | 300ms | ease-out | 按钮hover上浮、卡片悬浮 |
| 透明度 | 300ms | ease | 元素进出、模态框 |
| 侧边栏滑动 | 300ms | ease-in-out | 移动端侧边栏展开/收起 |

### 页面入场
- 内容区域使用 `opacity: 0 → 1` + `translateY(8px) → 0`, 200ms
- 避免过度动画，管理端追求效率

### 交互反馈
- 按钮点击: `transform: scale(0.98)`, 100ms
- 表格行hover: 背景色 200ms 过渡
- 徽章/Badge: 无动画，静态展示
- 下拉框展开: `max-height` 过渡 或 `scaleY(0) → scaleY(1)`, 200ms

### 响应 prefers-reduced-motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 十二、响应式适配方案

### 断点
| 断点 | 宽度 | 说明 |
|------|------|------|
| sm | 640px | 手机横屏 |
| md | 768px | 平板竖屏 |
| lg | 1024px | 平板横屏/小笔记本 |
| xl | 1280px | 桌面 |

### 布局适配

#### 移动端 (< 1024px)
- 侧边栏隐藏，抽屉式弹出
- 顶栏显示汉堡菜单按钮
- 统计卡片 `grid-cols-2`
- 表格横向滚动 `overflow-x-auto`
- 表单全宽 `grid-cols-1`
- 内容区 `p-4`

#### 平板 (768px - 1024px)
- 同移动端侧边栏策略
- 统计卡片 `grid-cols-3`
- 表单 `grid-cols-2`
- 内容区 `p-6`

#### 桌面 (>= 1024px)
- 侧边栏常驻显示
- 内容区 `ml-64 p-8`
- 统计卡片 `grid-cols-3` 或 `grid-cols-6`
- 编辑器双栏预览 `grid-cols-2`

### 触控适配
- 所有可点击元素最小尺寸 44x44px（管理端可适当放宽到 40px）
- 移动端表格操作按钮增大触控区域
- 下拉选择框高度不低于 44px

---

## 十三、各页面设计方向

### 13.1 login.vue — 登录页

**当前状态**: 已有不错的渐变背景 + 卡片式登录，基本符合品牌风格。

**优化点**:
- 背景: 将 `#F8FAFC → #EFF6FF` 改为更有温度的 `#FFFBF5 → #FFF7ED → #EFF6FF`（暖白到暖橙到信任蓝的三色渐变）
- 增加微妙的装饰: 左下角和右上角放置低透明度的渐变圆形 (orb)，呼应用户端装饰风格
- Logo图标增加微弱的 `animate-pulse` 或呼吸动画（2s cycle）
- 卡片阴影适当增强: `box-shadow: 0 32px 100px rgba(0,0,0,0.1)`
- 按钮hover增加光晕: `box-shadow: 0 0 40px rgba(249,115,22,0.2)`
- 添加底部版权文字: `text-xs text-slate-400`

**关键改动少量，保持现有好的设计。**

### 13.2 layouts/admin.vue — 侧边栏+顶栏布局

**重点改造项 — 侧边栏深色化**

关键改动:
1. 侧边栏背景从 `bg-white border-r` 改为 `bg-gradient-to-b from-slate-900 to-slate-800`
2. Logo区: 白色文字，去掉底边框，改用微妙的 `bg-white/5` 底色
3. 导航链接色: 从 `text-slate-600` 改为 `text-slate-400`，hover `text-white`
4. 激活态: `bg-brand-500/15 text-white` + 左侧橙色竖条
5. 分隔线: `bg-slate-700/50`
6. 退出按钮: `text-red-400 hover:text-red-300 hover:bg-red-500/10`
7. "查看前台" 链接: `text-slate-500 hover:text-slate-300`
8. 顶栏保持现有毛玻璃效果，微调左侧增加当前页面标题

### 13.3 admin/index.vue — 仪表盘

**重点改造项 — 增加欢迎横幅 + 统计卡片升级**

关键改动:
1. 顶部H1标题替换为欢迎横幅 (welcome-banner)
2. 统计卡片增加顶部色条 + 优化尺寸为 6 列（桌面）
3. "最近更新" 和 "快捷操作" 区块标题改为 section header 样式
4. 快捷操作卡片增加图标背景色圆圈
5. 加载状态从 spinner 改为骨架屏

### 13.4 admin/courses/index.vue — 分类列表

关键改动:
1. 页面标题区增加简短描述 `text-sm text-slate-500`
2. 表格行hover使用 `bg-warm-white` (品牌暖白)
3. "序号" 列加粗 + 品牌色圆点标识
4. 编辑按钮样式统一为 `admin-btn-primary`
5. 空状态: 如果没有分类，显示空状态组件

### 13.5 admin/courses/[id].vue — 编辑分类

关键改动:
1. 返回按钮 + 面包屑结合: `分类管理 / 编辑分类`
2. 表单卡片增加区块标题带色条装饰 (类似课程编辑页)
3. 成功/错误提示统一为 `.admin-alert-success/error` 样式
4. 保存按钮在卡片内部底端，紧凑排列

### 13.6 admin/lessons/index.vue — 课程列表

关键改动:
1. "新增课程" 按钮改用品牌渐变主按钮样式（白色文字）
2. 筛选区域: select 框增加背景色分区 `bg-white p-4 rounded-xl border`
3. 表格增加表头排序指示（可选，仅视觉优化）
4. 删除按钮hover增加红色边框加深效果
5. 空表格状态显示空状态组件
6. 表格底部增加总计/统计行（可选）

### 13.7 admin/lessons/create.vue — 新增课程

关键改动:
1. 页面标题和返回按钮布局与编辑页一致
2. 表单分为 "基本信息" 和 "课程内容" 两个区块卡片（与编辑页统一）
3. Markdown 文本域增加工具栏提示 `text-xs text-slate-400 mt-1 "支持 Markdown 格式"`
4. 操作按钮区域 sticky 在底部 (长表单时方便操作)

### 13.8 admin/lessons/[id].vue — 编辑课程

**这是最复杂的页面，当前设计已经不错**

关键改动:
1. 基本信息和内容编辑两个卡片增加区块标题色条
2. Markdown 预览面板增加浅色背景区分: `bg-slate-50 border rounded-xl p-5`
3. 预览切换按钮在激活时使用品牌色填充
4. 保存按钮区 sticky 底部 + 白色背景条 + 上边框
5. 自动保存提示（可选，未来功能）

### 13.9 admin/media.vue — 媒体库

关键改动:
1. 上传区域: 虚线边框从 `border-slate-300` 改为 hover 时 `border-brand-400` + 背景变 `bg-brand-50/50`
2. 上传区图标使用品牌色 `text-brand-300` 代替 `text-slate-300`
3. 网格卡片增加hover效果: 图片轻微放大 `scale-105`（overflow hidden 裁切）
4. 复制和删除按钮改为图标按钮，hover时显示文字 tooltip
5. 文件名截断显示，hover 时 tooltip 显示完整名
6. 增加上传进度条（品牌色渐变）
7. 支持多选删除的批量操作条（可选，未来功能）

---

## 十四、新增全局 CSS 类汇总

以下是需要新增或修改的全局 CSS 类，写入 `assets/css/main.css` 的 `@layer components` 中：

```css
/* ===== 侧边栏深色版 ===== */
.sidebar-dark { ... }
.sidebar-dark .sidebar-link { ... }
.sidebar-dark .sidebar-link-active { ... }

/* ===== 欢迎横幅 ===== */
.welcome-banner { ... }

/* ===== 统计卡片色条变体 ===== */
.admin-stat-card { ... }

/* ===== 提示框统一 ===== */
.admin-alert-success { ... }
.admin-alert-error { ... }

/* ===== 空状态 ===== */
.admin-empty { ... }

/* ===== 骨架屏 ===== */
.skeleton { ... }

/* ===== 徽章新增变体 ===== */
.admin-badge-yellow { ... }
.admin-badge-orange { ... }
.admin-badge-red { ... }
```

---

## 十五、实施优先级

| 优先级 | 改动项 | 影响范围 |
|--------|--------|----------|
| P0 | 侧边栏深色化 (layouts/admin.vue) | 全局 |
| P0 | 全局CSS新增/修改 (main.css) | 全局 |
| P1 | 仪表盘欢迎横幅 + 统计卡片升级 | admin/index.vue |
| P1 | 登录页微调 | admin/login.vue |
| P2 | 表格增强 (hover效果) | courses + lessons 列表 |
| P2 | 表单样式统一 | courses/[id] + lessons/create + lessons/[id] |
| P3 | 媒体库交互优化 | admin/media.vue |
| P3 | 空状态组件 | 全局复用 |
| P3 | 骨架屏加载 | 全局复用 |

---

## 附录：设计参考来源

本规范参考了以下 2025-2026 年管理后台设计趋势：
- 极简主义与留白优先
- 深色侧边栏 + 浅色内容区的经典双色调方案
- 渐变色条作为视觉锚点
- 骨架屏替代传统 loading spinner
- 毛玻璃 (Glassmorphism) 顶栏效果
- 微交互动画（hover上浮、按钮scale反馈）
- Mobile-first 响应式策略
