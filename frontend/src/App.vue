<template>
  <div class="app-container">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from './store/user';

const router = useRouter();
const userStore = useUserStore();

onMounted(async () => {
  await userStore.checkLoginStatus();
});
</script>

<style>
:root {
  --theme-color: #3498db;
  --background-color: #f8f9fa;
  --text-color: #2c3e50;
  --border-color: #e0e0e0;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 自定义Vant主题 */
:root:root {
  --van-primary-color: var(--theme-color);
  --van-background: var(--background-color);
  --van-text-color: var(--text-color);
  --van-border-color: var(--border-color);
}
</style> 