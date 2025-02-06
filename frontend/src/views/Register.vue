<template>
  <div class="register-container">
    <van-nav-bar
      title="注册"
      left-arrow
      @click-left="router.back()"
    />
    
    <div class="form-wrapper">
      <van-form @submit="onSubmit">
        <van-cell-group inset>
          <van-field
            v-model="email"
            name="email"
            label="邮箱"
            placeholder="请输入邮箱"
            :rules="[
              { required: true, message: '请输入邮箱' },
              { pattern: emailPattern, message: '请输入正确的邮箱格式' }
            ]"
          />
          <van-field
            v-model="password"
            type="password"
            name="password"
            label="密码"
            placeholder="请输入密码"
            :rules="[
              { required: true, message: '请输入密码' },
              { min: 6, message: '密码至少6个字符' }
            ]"
          />
          <van-field
            v-model="confirmPassword"
            type="password"
            name="confirmPassword"
            label="确认密码"
            placeholder="请再次输入密码"
            :rules="[
              { required: true, message: '请确认密码' },
              { validator: validateConfirmPassword, message: '两次输入的密码不一致' }
            ]"
          />
        </van-cell-group>

        <div class="submit-btn-wrapper">
          <van-button round block type="primary" native-type="submit">
            注册
          </van-button>
        </div>

        <div class="login-link">
          已有账号？
          <router-link to="/login">立即登录</router-link>
        </div>
      </van-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import md5 from 'md5'

const router = useRouter()
const userStore = useUserStore()

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

const validateConfirmPassword = (value) => {
  return value === password.value
}

const onSubmit = async (values) => {
  const success = await userStore.register({
    user: values.email,
    pass: md5(values.password)
  })
  
  if (success) {
    router.push('/')
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  background-color: var(--background-color);
}

.form-wrapper {
  padding: 20px;
  margin-top: 20px;
}

.submit-btn-wrapper {
  margin: 24px 16px 16px;
}

.login-link {
  text-align: center;
  margin-top: 16px;
  color: var(--text-color);
}

.login-link a {
  color: var(--theme-color);
  text-decoration: none;
}
</style> 