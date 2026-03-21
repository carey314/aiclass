<template>
  <div class="login-page">
    <!-- 装饰性渐变圆形 -->
    <div class="login-orb login-orb-left"></div>
    <div class="login-orb login-orb-right"></div>

    <!-- 登录卡片 -->
    <div class="login-card">
      <!-- Logo -->
      <div class="login-header">
        <div class="login-logo">
          <Icon name="heroicons:sparkles" class="w-8 h-8 text-white" />
        </div>
        <h1 class="login-title">管理入口</h1>
        <p class="login-subtitle">AI不难学 · 课程管理系统</p>
      </div>

      <!-- 表单 -->
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="login-field">
          <label class="login-label">管理员账号</label>
          <input
            v-model="username"
            type="text"
            required
            class="login-input"
            placeholder="输入用户名"
            autocomplete="username"
          >
        </div>

        <div class="login-field">
          <label class="login-label">安全密钥</label>
          <input
            v-model="password"
            type="password"
            required
            class="login-input"
            placeholder="输入密码"
            autocomplete="current-password"
          >
        </div>

        <!-- 错误提示 -->
        <div v-if="error" class="login-error">
          {{ error }}
        </div>

        <!-- 提交按钮 -->
        <button
          type="submit"
          :disabled="loading"
          class="login-btn"
        >
          {{ loading ? '验证中...' : '验证并进入' }}
        </button>

        <!-- 返回首页 -->
        <NuxtLink to="/" class="login-back">
          返回门户首页
        </NuxtLink>
      </form>
    </div>

    <!-- 版权文字 -->
    <p class="text-xs text-slate-400 mt-8 text-center" style="position:relative;z-index:10;">© 2026 AI不难学 · 课程管理系统</p>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

definePageMeta({ layout: false })

const authStore = useAuthStore()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  try {
    await authStore.login(username.value, password.value)
    navigateTo('/admin')
  } catch (e: any) {
    error.value = '用户名或密码错误'
  } finally {
    loading.value = false
  }
}

useHead({ title: '管理员登录 - AI不难学' })
</script>

<style scoped>
/* 整页容器 */
.login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #FFFBF5, #FFF7ED, #EFF6FF);
  padding: 24px;
  position: relative;
  overflow: hidden;
}

/* 装饰性渐变圆形 */
.login-orb {
  position: absolute;
  border-radius: 9999px;
  pointer-events: none;
}
.login-orb-left {
  width: 24rem;
  height: 24rem;
  background: linear-gradient(to bottom right, rgba(253, 186, 116, 0.2), transparent);
  filter: blur(48px);
  left: -5rem;
  bottom: -5rem;
}
.login-orb-right {
  width: 20rem;
  height: 20rem;
  background: linear-gradient(to bottom right, rgba(147, 197, 253, 0.15), transparent);
  filter: blur(48px);
  right: -4rem;
  top: -4rem;
}

/* 登录卡片 */
.login-card {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 440px;
  padding: 48px 40px;
  border-radius: 2.5rem;
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  box-shadow:
    0 32px 100px rgba(0, 0, 0, 0.1),
    0 8px 32px rgba(0, 0, 0, 0.05);
}

/* 头部 */
.login-header {
  text-align: center;
  margin-bottom: 40px;
}
.login-logo {
  width: 64px;
  height: 64px;
  border-radius: 18px;
  background: linear-gradient(135deg, #F97316, #FB923C);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  box-shadow: 0 8px 24px rgba(249, 115, 22, 0.25);
  animation: logo-breathe 2s ease-in-out infinite;
}
@keyframes logo-breathe {
  0%, 100% { transform: scale(1); box-shadow: 0 8px 24px rgba(249, 115, 22, 0.25); }
  50% { transform: scale(1.05); box-shadow: 0 12px 32px rgba(249, 115, 22, 0.35); }
}
.login-title {
  font-size: 28px;
  font-weight: 900;
  color: #1E293B;
  margin: 0 0 8px;
  letter-spacing: -0.02em;
}
.login-subtitle {
  font-size: 15px;
  color: #64748B;
  margin: 0;
}

/* 表单 */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.login-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.login-label {
  font-size: 14px;
  font-weight: 700;
  color: #64748B;
  padding-left: 4px;
}
.login-input {
  width: 100%;
  padding: 16px 20px;
  border-radius: 16px;
  font-size: 17px;
  font-weight: 500;
  color: #1E293B;
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  outline: none;
  transition: all 0.3s;
  min-height: 0;
}
.login-input::placeholder {
  color: #94A3B8;
}
.login-input:focus {
  border-color: #F97316;
  box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.1);
}

/* 错误提示 */
.login-error {
  text-align: center;
  font-size: 15px;
  color: #EF4444;
  background: #FEF2F2;
  border: 1px solid #FECACA;
  border-radius: 14px;
  padding: 14px 16px;
}

/* 提交按钮 */
.login-btn {
  width: 100%;
  padding: 18px 0;
  border-radius: 16px;
  font-size: 18px;
  font-weight: 900;
  color: #fff;
  background: linear-gradient(135deg, #F97316, #FB923C);
  border: none;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(249, 115, 22, 0.3);
  min-height: 0;
  margin-top: 4px;
}
.login-btn:hover {
  box-shadow: 0 4px 20px rgba(249, 115, 22, 0.4);
  transform: translateY(-1px);
}
.login-btn:active {
  transform: translateY(0);
}
.login-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* 返回首页 */
.login-back {
  display: block;
  text-align: center;
  font-size: 15px;
  font-weight: 700;
  color: #64748B;
  text-decoration: none;
  transition: color 0.3s;
}
.login-back:hover {
  color: #F97316;
}

/* 移动端适配 */
@media (max-width: 480px) {
  .login-card {
    padding: 36px 24px;
    border-radius: 2rem;
  }
  .login-title {
    font-size: 24px;
  }
}
</style>
