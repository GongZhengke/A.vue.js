import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { showToast } from 'vant'

export const useUserStore = defineStore('user', () => {
  const email = ref('')
  const isLoggedIn = ref(false)

  async function login(userData) {
    try {
      const response = await axios.post('/api/auth/login', userData)
      if (response.data.email) {
        email.value = response.data.email
        isLoggedIn.value = true
        showToast('登录成功')
        return true
      }
      return false
    } catch (error) {
      showToast(error.response?.data?.error || '登录失败')
      return false
    }
  }

  async function register(userData) {
    try {
      const response = await axios.post('/api/auth/register', userData)
      if (response.data.email) {
        email.value = response.data.email
        isLoggedIn.value = true
        showToast('注册成功')
        return true
      }
      return false
    } catch (error) {
      showToast(error.response?.data?.error || '注册失败')
      return false
    }
  }

  async function logout() {
    try {
      await axios.post('/api/auth/logout')
      email.value = ''
      isLoggedIn.value = false
      showToast('已退出登录')
      return true
    } catch (error) {
      showToast('退出登录失败')
      return false
    }
  }

  async function checkLoginStatus() {
    try {
      const response = await axios.get('/api/auth/status')
      if (response.data.logged_in) {
        email.value = response.data.email
        isLoggedIn.value = true
      } else {
        email.value = ''
        isLoggedIn.value = false
      }
    } catch (error) {
      console.error('检查登录状态失败:', error)
    }
  }

  return {
    email,
    isLoggedIn,
    login,
    register,
    logout,
    checkLoginStatus
  }
}) 