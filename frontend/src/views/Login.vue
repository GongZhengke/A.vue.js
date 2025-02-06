<template>
  <div class="login-container">
    <van-nav-bar
      title="登录"
      left-arrow
      @click-left="router.back()"
    />
    
    <div class="form-wrapper">
      <div class="logo">
        <svg t="1738832157743" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="15734" width="64" height="64"><path d="M899.6 117c9.9 7.1 13.8 16.7 12 28.5L797.3 831.2c-1.5 8.6-6.3 15.3-14.3 20.1-4.1 2.3-8.8 3.6-13.8 3.6-3.3 0-6.9-0.8-10.7-2.3L556.3 770 448.2 901.8c-5.4 6.9-12.7 10.2-21.9 10.2-3.8 0-7.1-0.6-9.9-1.8-5.6-2.1-10.2-5.5-13.6-10.5-3.4-4.9-5.2-10.3-5.2-16.3V727.7l385.7-472.8-477.2 413-176.3-72.3c-11-4.1-17-12.3-17.8-24.6-0.6-11.9 4.1-20.7 14.3-26.4L869.1 116c4.5-2.7 9.2-4 14.3-4 6 0 11.4 1.7 16.2 5z" fill="#1296db" p-id="15735" data-spm-anchor-id="a313x.search_index.0.i0.6f6b3a81SH3dVp" class="selected"></path></svg>
        <h2>屌丝论坛</h2>
      </div>

      <van-form @submit="onSubmit" class="login-form">
        <van-cell-group inset>
          <van-field
            v-model="formData.email"
            name="email"
            label="邮箱"
            placeholder="请输入邮箱"
            :rules="[
              { required: true, message: '请输入邮箱' },
              { pattern: emailPattern, message: '请输入正确的邮箱格式' }
            ]"
          >
            <template #left-icon>
              <van-icon name="envelop-o" />
            </template>
          </van-field>
          <van-field
            v-model="formData.password"
            type="password"
            name="password"
            label="密码"
            placeholder="请输入密码"
            :rules="[
              { required: true, message: '请输入密码' },
              { min: 6, message: '密码至少6个字符' }
            ]"
          >
            <template #left-icon>
              <van-icon name="lock" />
            </template>
          </van-field>
        </van-cell-group>

        <div class="submit-btn-wrapper">
          <van-button 
            round 
            block 
            type="primary" 
            native-type="submit"
            :loading="loading"
            loading-text="登录中..."
          >
            登录
          </van-button>
        </div>

        <!-- <div class="register-link">
          还没有账号？
          <router-link to="/register">立即注册</router-link>
        </div> -->
      </van-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import md5 from 'md5'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

const formData = reactive({
  email: '',
  password: ''
})

const onSubmit = async () => {
  loading.value = true
  try {
    // 创建FormData对象
    const form = new FormData()
    form.append('user', formData.email)
    form.append('pass', md5(formData.password))
    
    const success = await userStore.login(form)
    if (success) {
      router.push('/')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background-color: var(--background-color);
}

.form-wrapper {
  padding: 20px;
  margin-top: 20px;
}

.logo {
  text-align: center;
  margin-bottom: 32px;
}

.logo img {
  width: 80px;
  height: 80px;
  margin-bottom: 12px;
}

.logo h2 {
  font-size: 24px;
  color: var(--text-color);
  font-weight: 600;
}

.login-form {
  max-width: 400px;
  margin: 0 auto;
}

:deep(.van-cell-group--inset) {
  margin: 0;
}

:deep(.van-field__left-icon) {
  margin-right: 8px;
  color: #999;
}

.submit-btn-wrapper {
  margin: 24px 16px 16px;
}

.register-link {
  text-align: center;
  margin-top: 16px;
  color: var(--text-color);
  font-size: 14px;
}

.register-link a {
  color: var(--theme-color);
  text-decoration: none;
  font-weight: 500;
}

:deep(.van-nav-bar) {
  background-color: var(--theme-color);
}

:deep(.van-nav-bar .van-icon),
:deep(.van-nav-bar__text),
:deep(.van-nav-bar__title) {
  color: #fff;
}

:deep(.van-button--primary) {
  height: 44px;
  font-size: 16px;
}

:deep(.van-field__label) {
  width: 50px;
}
</style> 