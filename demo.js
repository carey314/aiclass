import React, { useState, useEffect } from 'react';
import { 
  Home, 
  BookOpen, 
  Info, 
  Menu, 
  X, 
  ChevronRight, 
  ChevronDown, 
  LayoutDashboard, 
  Layers, 
  FileText, 
  Image as ImageIcon, 
  LogOut,
  ArrowLeft,
  ArrowRight,
  Search,
  Plus,
  Edit2,
  Trash2,
  CheckCircle2,
  Smartphone,
  Zap,
  Target,
  ShieldCheck,
  Cpu,
  Sparkles
} from 'lucide-react';

// --- 模拟数据 ---
const COURSE_STAGES = [
  { id: 1, title: '第一阶段：揭开 AI 神秘面纱', desc: '不讲代码，只谈生活。带你轻松跨过技术门槛，理解 AI 逻辑。', icon: <Zap /> },
  { id: 2, title: '第二阶段：手机里的 AI 小助手', desc: '深度拆解微信、浏览器中的 AI 功能，让你的手机变成超级管家。', icon: <Smartphone /> },
  { id: 3, title: '第三阶段：AI 聊天与写作实战', desc: '学会精准对话技巧，让 AI 替你写总结、写信、甚至代写朋友圈。', icon: <FileText /> },
  { id: 4, title: '第四阶段：AI 图片生成艺术', desc: '只需一句话，生成全家福、节日贺卡及极具艺术感的照片。', icon: <ImageIcon /> },
  { id: 5, title: '第五阶段：生活效率提升专家', desc: 'AI 辅助查病、做菜、制定旅游攻略，让退休生活井井有条。', icon: <Target /> },
  { id: 6, title: '第六阶段：终极实战：数字生活家', desc: '综合实战演练，掌握全套 AI 技能，成为社区中最懂科技的长辈。', icon: <CheckCircle2 /> },
];

const MOCK_LESSONS = [
  { id: 101, stageId: 1, title: '第一课：AI 是什么？(非技术大白话版)', duration: '15分钟' },
  { id: 102, stageId: 1, title: '第二课：为什么现在的 AI 变聪明了？', duration: '20分钟' },
  { id: 201, stageId: 2, title: '第三课：微信里的 AI 怎么找？', duration: '10分钟' },
];

// --- 样式常量：全新配色与 UI 规范 ---
const UI_STYLE = {
  background: "bg-[#020617]", // 更深邃的午夜蓝
  glass: "bg-white/[0.03] backdrop-blur-xl border border-white/[0.08] shadow-[0_8px_32px_0_rgba(0,0,0,0.36)]",
  glassHover: "hover:bg-white/[0.07] hover:border-white/[0.15] hover:shadow-indigo-500/10 hover:-translate-y-1",
  gradientText: "bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400",
  primaryBtn: "bg-gradient-to-br from-indigo-500 via-blue-600 to-blue-700 hover:shadow-[0_0_20px_rgba(79,70,229,0.4)] text-white",
  secondaryBtn: "bg-slate-800/50 hover:bg-slate-700/80 border border-slate-700/50 text-slate-200",
  heading: "font-black tracking-tight text-white",
  bodyText: "text-slate-400 leading-relaxed font-normal",
};

// --- 子组件：导航栏 ---
const Navbar = ({ activePage, setActivePage, isMobileMenuOpen, setIsMobileMenuOpen }) => {
  const navItems = [
    { id: 'home', label: '首页' },
    { id: 'courses', label: '全部课程' },
    { id: 'about', label: '关于我们' },
  ];

  return (
    <nav className="fixed top-0 w-full z-[100] transition-all duration-500">
      <div className="absolute inset-0 bg-[#020617]/70 backdrop-blur-md border-b border-white/[0.05]" />
      <div className="max-w-7xl mx-auto px-6 h-20 relative flex items-center justify-between">
        <div className="flex items-center gap-3 cursor-pointer group" onClick={() => setActivePage('home')}>
          <div className="relative">
            <div className="w-10 h-10 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg transform group-hover:rotate-12 transition-transform">
              <Sparkles className="text-white" size={20} />
            </div>
          </div>
          <span className="text-2xl font-black tracking-tighter text-white">AI 不难学</span>
        </div>

        <div className="hidden md:flex items-center gap-10">
          {navItems.map(item => (
            <button
              key={item.id}
              onClick={() => setActivePage(item.id)}
              className={`text-[17px] font-medium transition-all relative py-2 ${activePage === item.id ? 'text-white' : 'text-slate-400 hover:text-white'}`}
            >
              {item.label}
              {activePage === item.id && (
                <span className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full" />
              )}
            </button>
          ))}
          <button 
            onClick={() => setActivePage('admin-login')}
            className="px-5 py-2 rounded-xl text-sm font-bold bg-white/5 border border-white/10 hover:bg-white/10 transition-all"
          >
            后台
          </button>
        </div>

        <button className="md:hidden text-white p-2" onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
          {isMobileMenuOpen ? <X size={28} /> : <Menu size={28} />}
        </button>
      </div>

      {isMobileMenuOpen && (
        <div className="md:hidden absolute top-20 left-0 w-full bg-[#020617] border-b border-white/[0.05] p-6 space-y-4 animate-in fade-in slide-in-from-top-4">
          {navItems.map(item => (
            <button
              key={item.id}
              onClick={() => { setActivePage(item.id); setIsMobileMenuOpen(false); }}
              className={`block w-full text-left p-4 rounded-2xl text-xl font-bold ${activePage === item.id ? 'bg-blue-600/10 text-blue-400' : 'text-slate-300'}`}
            >
              {item.label}
            </button>
          ))}
        </div>
      )}
    </nav>
  );
};

// --- 页面：首页 ---
const HomePage = ({ onStart }) => (
  <div className="pt-20">
    {/* Hero Section */}
    <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden py-24">
      {/* 背景光晕 */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-blue-600/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-indigo-600/10 rounded-full blur-[120px]" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-r from-cyan-500/5 to-purple-500/5 rounded-full blur-[100px]" />
      </div>

      <div className="max-w-7xl mx-auto px-6 relative z-10 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/[0.03] border border-white/[0.08] text-cyan-400 text-sm font-bold mb-10 shadow-2xl">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
          </span>
          2024 中老年数字素养提升计划
        </div>
        <h1 className="text-5xl md:text-[5.5rem] font-black leading-[1.1] mb-10 text-white tracking-tighter">
          用最<span className="text-cyan-400">大白话</span>的语言<br />
          开启<span className={UI_STYLE.gradientText}>人工智能</span>生活
        </h1>
        <p className="text-xl md:text-2xl text-slate-400 mb-14 max-w-3xl mx-auto leading-relaxed font-light">
          我们不教代码，不讲玄学。只需一部智能手机，带你从“看不懂”到“玩得溜”，
          享受高科技带来的便捷与尊严。
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
          <button 
            onClick={onStart}
            className="px-10 py-5 rounded-3xl bg-white text-slate-950 text-xl font-black shadow-[0_0_30px_rgba(255,255,255,0.2)] hover:scale-105 active:scale-95 transition-all flex items-center gap-2"
          >
            立即开启学习之旅 <ChevronRight size={24} />
          </button>
          <button className="px-10 py-5 rounded-3xl bg-white/5 border border-white/10 text-xl font-bold hover:bg-white/10 transition-all">
            免费领取纸质教材
          </button>
        </div>
      </div>
    </section>

    {/* 4大差异点卡片 */}
    <section className="py-24 px-6 relative">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {[
          { title: '极简大字', desc: '全站超大字体，高对比度设计，不费眼，一看就懂。', icon: <ShieldCheck className="text-emerald-400" /> },
          { title: '实战导向', desc: '避开枯燥理论，每节课都在教你如何用 AI 处理生活琐事。', icon: <Cpu className="text-blue-400" /> },
          { title: '全程陪伴', desc: '遇到困难别担心，专属助教随时在线解答，手把手指导。', icon: <Smartphone className="text-purple-400" /> },
          { title: '成果可见', desc: '学完就能在朋友圈展示 AI 生成的作品，让邻居都羡慕。', icon: <Zap className="text-yellow-400" /> },
        ].map((item, idx) => (
          <div key={idx} className={`${UI_STYLE.glass} ${UI_STYLE.glassHover} p-10 rounded-[2.5rem] transition-all duration-500`}>
            <div className="w-14 h-14 bg-white/[0.03] rounded-2xl flex items-center justify-center mb-8 border border-white/5">
              {React.cloneElement(item.icon, { size: 30 })}
            </div>
            <h3 className="text-2xl font-black text-white mb-4">{item.title}</h3>
            <p className="text-slate-400 text-lg leading-relaxed">{item.desc}</p>
          </div>
        ))}
      </div>
    </section>

    {/* 课程阶段：时间轴/卡片流布局 */}
    <section className="py-24 px-6 bg-white/[0.01]">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-20">
          <h2 className="text-4xl md:text-5xl font-black text-white mb-6">精心设计的 <span className={UI_STYLE.gradientText}>学习曲线</span></h2>
          <p className="text-xl text-slate-400">像爬楼梯一样简单，每一步都稳健扎实</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
          {COURSE_STAGES.map((stage) => (
            <div key={stage.id} className={`${UI_STYLE.glass} ${UI_STYLE.glassHover} p-1 rounded-[3rem] overflow-hidden group`}>
              <div className="p-8 md:p-10">
                <div className="flex justify-between items-start mb-10">
                  <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center border border-indigo-500/20 group-hover:bg-indigo-500 group-hover:text-white transition-all duration-500">
                    {React.cloneElement(stage.icon, { size: 32 })}
                  </div>
                  <span className="text-5xl font-black text-white/5 group-hover:text-white/10 transition-colors">0{stage.id}</span>
                </div>
                <h3 className="text-2xl font-black text-white mb-4 leading-tight">{stage.title}</h3>
                <p className="text-slate-400 text-lg leading-relaxed mb-8">{stage.desc}</p>
                <div className="h-1 w-0 group-hover:w-full bg-gradient-to-r from-cyan-400 to-indigo-500 transition-all duration-700 rounded-full" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>

    {/* Footer CTA */}
    <section className="py-32 px-6">
      <div className="max-w-5xl mx-auto rounded-[4rem] bg-gradient-to-br from-indigo-900 via-blue-900 to-slate-900 p-12 md:p-24 text-center relative overflow-hidden shadow-[0_40px_100px_-20px_rgba(0,0,0,0.5)]">
        <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-400/10 rounded-full -translate-y-1/2 translate-x-1/2 blur-[80px]" />
        <h2 className="text-4xl md:text-6xl font-black text-white mb-10 tracking-tighter">活到老，学到老<br />拥抱<span className="text-cyan-400">智能时代</span></h2>
        <p className="text-xl md:text-2xl text-slate-300 mb-14 max-w-xl mx-auto font-light leading-relaxed">
          已有 12,000+ 位学员在这里找到了科技的乐趣，你愿意成为下一个吗？
        </p>
        <button 
          onClick={onStart}
          className="bg-white text-slate-950 px-12 py-6 rounded-full text-2xl font-black shadow-2xl hover:scale-105 active:scale-95 transition-all"
        >
          免费试听前两课
        </button>
      </div>
    </section>
  </div>
);

// --- 页面：全部课程 (手风琴布局) ---
const CoursesPage = ({ onSelectLesson }) => {
  const [openStage, setOpenStage] = useState(1);

  return (
    <div className="pt-40 pb-32 max-w-5xl mx-auto px-6">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-16">
        <div>
          <h1 className="text-5xl font-black text-white mb-4">全部课程目录</h1>
          <p className="text-xl text-slate-400">点击阶段卡片展开详细课时，开启你的 AI 达人之路。</p>
        </div>
        <div className="flex gap-4">
          <div className="bg-white/5 border border-white/10 rounded-2xl px-6 py-3 text-center">
            <div className="text-2xl font-black text-white">42</div>
            <div className="text-xs text-slate-500 font-bold uppercase tracking-wider">总课时数</div>
          </div>
          <div className="bg-white/5 border border-white/10 rounded-2xl px-6 py-3 text-center">
            <div className="text-2xl font-black text-white">6</div>
            <div className="text-xs text-slate-500 font-bold uppercase tracking-wider">课程阶段</div>
          </div>
        </div>
      </div>

      <div className="space-y-6">
        {COURSE_STAGES.map(stage => (
          <div key={stage.id} className={`${UI_STYLE.glass} rounded-[2.5rem] overflow-hidden transition-all duration-500`}>
            <button 
              className={`w-full flex items-center justify-between p-8 md:p-10 text-left transition-all ${openStage === stage.id ? 'bg-white/[0.04]' : 'hover:bg-white/[0.02]'}`}
              onClick={() => setOpenStage(openStage === stage.id ? null : stage.id)}
            >
              <div className="flex items-center gap-8">
                <span className={`w-14 h-14 rounded-2xl flex items-center justify-center text-2xl font-black border transition-all ${openStage === stage.id ? 'bg-cyan-500 border-cyan-400 text-white shadow-[0_0_20px_rgba(34,211,238,0.4)]' : 'bg-white/5 border-white/10 text-slate-400'}`}>
                  {stage.id}
                </span>
                <div>
                  <h3 className="text-2xl font-black text-white mb-1">{stage.title}</h3>
                  <p className="text-slate-500 font-medium">包含 7 个课时 · 预计耗时 2 小时</p>
                </div>
              </div>
              <div className={`w-12 h-12 rounded-full border border-white/10 flex items-center justify-center transition-transform duration-500 ${openStage === stage.id ? 'rotate-180 bg-white/5' : ''}`}>
                <ChevronDown size={24} className="text-slate-400" />
              </div>
            </button>

            {openStage === stage.id && (
              <div className="p-4 md:p-6 grid grid-cols-1 gap-3 animate-in fade-in slide-in-from-top-2 duration-500">
                {MOCK_LESSONS.filter(l => l.stageId === stage.id).map((lesson) => (
                  <button
                    key={lesson.id}
                    onClick={() => onSelectLesson(lesson)}
                    className="w-full group flex items-center justify-between p-6 hover:bg-white/[0.05] rounded-[1.5rem] transition-all"
                  >
                    <div className="flex items-center gap-6">
                      <div className="w-1.5 h-1.5 rounded-full bg-cyan-500 group-hover:scale-[3] transition-transform" />
                      <span className="text-xl text-slate-200 group-hover:text-white transition-colors">{lesson.title}</span>
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="text-slate-500 text-sm font-bold bg-white/5 px-3 py-1 rounded-lg">{lesson.duration}</span>
                      <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                        <ChevronRight size={18} />
                      </div>
                    </div>
                  </button>
                ))}
                {MOCK_LESSONS.filter(l => l.stageId === stage.id).length === 0 && (
                  <div className="py-16 text-center text-slate-600 text-lg">内容拼命上传中...</div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

// --- 页面：课程详情 ---
const LessonDetailPage = ({ lesson, onBack }) => (
  <div className="pt-24 flex flex-col lg:flex-row min-h-screen">
    {/* 侧边导航 */}
    <aside className="hidden lg:block w-96 fixed left-0 h-full bg-[#020617] border-r border-white/[0.05] p-10 overflow-y-auto">
      <button 
        onClick={onBack}
        className="flex items-center gap-3 text-slate-500 hover:text-white mb-12 transition-colors font-bold text-lg group"
      >
        <ArrowLeft size={22} className="group-hover:-translate-x-1 transition-transform" /> 返回目录
      </button>
      
      <div className="space-y-10">
        <div>
          <h4 className="text-xs font-black text-slate-600 uppercase tracking-widest mb-6">当前学习阶段</h4>
          <div className="space-y-3">
            {MOCK_LESSONS.map(l => (
              <div 
                key={l.id} 
                className={`p-5 rounded-2xl cursor-pointer transition-all border ${l.id === lesson.id ? 'bg-blue-600 border-blue-400 text-white shadow-xl shadow-blue-600/20' : 'bg-white/[0.02] border-white/[0.05] hover:border-white/20 text-slate-400'}`}
              >
                <div className="text-xs opacity-60 mb-2 font-bold uppercase tracking-tighter">Lesson {l.id % 100}</div>
                <div className="font-bold text-lg leading-tight">{l.title}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </aside>

    {/* 主内容 */}
    <main className="flex-1 lg:ml-96 pb-32">
      <div className="max-w-4xl mx-auto px-6 py-12">
        {/* 面包屑 */}
        <nav className="flex items-center gap-3 text-slate-500 font-bold mb-10">
          <span className="hover:text-white cursor-pointer" onClick={onBack}>全部课程</span>
          <ChevronRight size={18} />
          <span className="text-slate-400">第一阶段</span>
          <ChevronRight size={18} />
          <span className="text-cyan-400">正在观看</span>
        </nav>

        <div className="space-y-12">
          {/* 视频容器 */}
          <div className={`${UI_STYLE.glass} p-2 rounded-[3rem] overflow-hidden shadow-2xl`}>
            <div className="aspect-video bg-slate-950 rounded-[2.5rem] relative group cursor-pointer overflow-hidden">
              <div className="absolute inset-0 flex items-center justify-center z-10">
                <div className="w-24 h-24 bg-white text-slate-950 rounded-full flex items-center justify-center shadow-2xl transform group-hover:scale-110 transition-transform">
                  <div className="w-0 h-0 border-t-[14px] border-t-transparent border-l-[22px] border-l-current border-b-[14px] border-b-transparent ml-2" />
                </div>
              </div>
              <div className="absolute inset-0 bg-gradient-to-t from-[#020617] via-transparent to-transparent opacity-60" />
            </div>
          </div>

          {/* 文章正文 */}
          <article className={`${UI_STYLE.glass} p-10 md:p-16 rounded-[3rem]`}>
            <h1 className="text-4xl md:text-5xl font-black text-white mb-10 pb-10 border-b border-white/[0.05]">{lesson.title}</h1>
            
            <div className="space-y-10 text-xl text-slate-400 leading-[1.8] font-light">
              <p>
                欢迎来到人工智能的第一站。很多朋友可能会担心：<span className="text-white font-bold italic">“我连电脑都不太会，能学会 AI 吗？”</span>
              </p>
              <div className="bg-gradient-to-br from-blue-600/20 to-purple-600/20 border border-blue-500/20 p-8 rounded-[2rem] text-blue-100 font-medium">
                我们的核心理念：AI 不是你的“考试题”，而是你的“老花镜”。它不是用来难为你的，而是用来帮你把生活看得更清楚、处理得更轻松。
              </div>
              <h3 className="text-3xl font-black text-white mt-16 mb-6 flex items-center gap-3">
                <div className="w-2 h-10 bg-cyan-500 rounded-full" /> 本课知识点
              </h3>
              <ul className="space-y-6">
                {[
                  '理解 AI 的全称：人工智能 (Artificial Intelligence)',
                  'AI 与机器人的区别：它是看不见的智能助手',
                  '为什么它比以前的手机软件更聪明、更听话'
                ].map((item, i) => (
                  <li key={i} className="flex items-start gap-4">
                    <CheckCircle2 className="text-cyan-500 mt-1 shrink-0" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
              <div className="aspect-[16/9] bg-white/[0.02] border border-white/[0.05] rounded-[2.5rem] flex items-center justify-center mt-12 group hover:border-white/20 transition-all">
                 <ImageIcon size={64} className="text-slate-800" />
              </div>
            </div>

            {/* 下一课导航 */}
            <div className="mt-20 pt-12 border-t border-white/[0.05] flex justify-between items-center">
              <button className="text-slate-500 font-bold hover:text-white transition-colors flex items-center gap-2">
                <ArrowLeft size={20} /> 上一节
              </button>
              <button className="px-8 py-4 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all font-black text-white flex items-center gap-3 group">
                下一节：为什么 AI 变聪明了 <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
              </button>
            </div>
          </article>
        </div>
      </div>
    </main>
  </div>
);

// --- 页脚 ---
const Footer = () => (
  <footer className="bg-[#020617] border-t border-white/[0.05] py-24 px-6">
    <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-16">
      <div className="col-span-1 md:col-span-2">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 bg-cyan-500 rounded-xl flex items-center justify-center">
            <Sparkles className="text-white" size={20} />
          </div>
          <span className="text-3xl font-black text-white">AI 不难学</span>
        </div>
        <p className="text-xl text-slate-500 max-w-md leading-relaxed">
          我们致力于通过最通俗易懂的方式，赋能每一位渴望学习的中老年朋友，跨越数字鸿沟。
        </p>
      </div>
      <div>
        <h4 className="text-white font-black text-lg mb-8 uppercase tracking-widest">学习中心</h4>
        <ul className="space-y-5 text-slate-500 text-lg font-medium">
          <li className="hover:text-cyan-400 cursor-pointer transition-colors">新手第一课</li>
          <li className="hover:text-cyan-400 cursor-pointer transition-colors">常用工具下载</li>
          <li className="hover:text-cyan-400 cursor-pointer transition-colors">学员作品展</li>
        </ul>
      </div>
      <div>
        <h4 className="text-white font-black text-lg mb-8 uppercase tracking-widest">联系客服</h4>
        <div className="space-y-4 text-slate-500 text-lg">
          <p className="flex items-center gap-2">微信：<span className="text-slate-300">LearnAI_2024</span></p>
          <p className="flex items-center gap-2">电话：<span className="text-slate-300">400-666-888</span></p>
          <p className="bg-white/5 p-4 rounded-2xl border border-white/5 text-sm">工作时间：9:00 - 21:00 (含节假日)</p>
        </div>
      </div>
    </div>
    <div className="max-w-7xl mx-auto mt-24 pt-10 border-t border-white/[0.05] flex flex-col md:flex-row justify-between items-center gap-4 text-slate-600 font-medium">
      <p>© 2024 AI 不难学培训平台 - 智慧生活，触手可及</p>
      <div className="flex gap-8">
        <span className="hover:text-slate-400 cursor-pointer">隐私条款</span>
        <span className="hover:text-slate-400 cursor-pointer">用户协议</span>
      </div>
    </div>
  </footer>
);

// --- 根组件 ---
export default function App() {
  const [activePage, setActivePage] = useState('home');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [selectedLesson, setSelectedLesson] = useState(null);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [activePage]);

  const renderContent = () => {
    switch(activePage) {
      case 'home': return <HomePage onStart={() => setActivePage('courses')} />;
      case 'courses': return <CoursesPage onSelectLesson={(l) => { setSelectedLesson(l); setActivePage('lesson-detail'); }} />;
      case 'lesson-detail': return <LessonDetailPage lesson={selectedLesson} onBack={() => setActivePage('courses')} />;
      case 'about': return (
        <div className="pt-48 pb-32 max-w-4xl mx-auto px-6 text-center">
          <h1 className="text-5xl font-black text-white mb-10 italic">"在这个时代，好奇心是唯一的门槛。"</h1>
          <p className="text-2xl text-slate-400 leading-relaxed font-light">
            我们不仅仅是在教 AI，我们是在重新连接每一个渴望与时代同步的灵魂。
            无论你是 45 岁还是 85 岁，只要你愿意点开这个网页，你就是我们的同学。
          </p>
          <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-10">
            {[
              { val: '1.2万+', label: '活跃学员' },
              { val: '42门', label: '精品课时' },
              { val: '99%', label: '好评率' },
            ].map((stat, i) => (
              <div key={i} className={`${UI_STYLE.glass} p-10 rounded-3xl`}>
                <div className="text-4xl font-black text-white mb-2">{stat.val}</div>
                <div className="text-slate-500 font-bold uppercase tracking-wider text-sm">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      );
      case 'admin-login': return (
        <div className="min-h-screen flex items-center justify-center bg-[#020617] p-6">
          <div className={`${UI_STYLE.glass} max-w-md w-full p-12 rounded-[3.5rem] shadow-2xl`}>
            <h2 className="text-3xl font-black mb-10 text-center text-white">管理入口</h2>
            <div className="space-y-8">
              <div className="space-y-3">
                <label className="text-slate-400 font-bold ml-1">管理员令牌</label>
                <input type="text" className="w-full bg-white/[0.03] border border-white/10 p-5 rounded-2xl focus:border-cyan-500 focus:outline-none text-white font-medium" placeholder="输入 ID" />
              </div>
              <div className="space-y-3">
                <label className="text-slate-400 font-bold ml-1">安全密钥</label>
                <input type="password" className="w-full bg-white/[0.03] border border-white/10 p-5 rounded-2xl focus:border-cyan-500 focus:outline-none text-white" placeholder="••••••••" />
              </div>
              <button 
                onClick={() => setActivePage('home')}
                className={`w-full py-5 rounded-2xl text-xl font-black transition-all ${UI_STYLE.primaryBtn}`}
              >
                验证并进入
              </button>
              <button onClick={() => setActivePage('home')} className="w-full text-slate-500 font-bold hover:text-white transition-colors">返回门户首页</button>
            </div>
          </div>
        </div>
      );
      default: return <HomePage />;
    }
  };

  return (
    <div className="min-h-screen bg-[#020617] text-white selection:bg-cyan-500/30 selection:text-cyan-200">
      {activePage !== 'admin-login' && (
        <Navbar 
          activePage={activePage} 
          setActivePage={setActivePage} 
          isMobileMenuOpen={isMobileMenuOpen}
          setIsMobileMenuOpen={setIsMobileMenuOpen}
        />
      )}
      
      {renderContent()}
      
      {activePage !== 'admin-login' && <Footer />}
    </div>
  );
}