<template>
  <div class="home-container">
    <van-nav-bar
      title="屌丝论坛"
      :right-text="userStore.isLoggedIn ? '退出' : '登录'"
      @click-right="handleAuthAction"
    >
      <template #left>
        <van-icon name="user-o" size="18" />
        <span class="user-email" v-if="userStore.isLoggedIn">{{ userStore.email }}</span>
      </template>
    </van-nav-bar>

    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list
        v-model:loading="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="onLoad"
      >
        <div class="post-list">
          <div
            v-for="post in posts"
            :key="post.post_id"
            class="post-item"
            @click="router.push(`/post/${post.post_id}`)"
          >
            <div class="post-title">{{ post.title }}</div>
            <div class="post-meta">
              <span class="author">
                {{ post.author }}  {{ post.create_time.formatted }}
              </span><span v-if="post.replies_count">←</span>
              <span class="replies" v-if="post.replies_count">
                 <span class="author">{{ post.last_reply.author }} </span> <span class="time">{{ post.last_reply.formatted }}</span>
              </span>
            </div>
          </div>
        </div>
      </van-list>
    </van-pull-refresh>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import { postApi } from '../api/posts'
import { showToast, showDialog } from 'vant'

const router = useRouter()
const userStore = useUserStore()

const posts = ref([])
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)
const nextTimestamp = ref('')

const handleAuthAction = () => {
  if (userStore.isLoggedIn) {
    showDialog({
      title: '退出登录',
      message: '确定要退出登录吗？',
      showCancelButton: true,
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      confirmButtonColor: '#ee0a24'
    }).then(async () => {
      const success = await userStore.logout()
      if (success) {
        router.push('/login')
      }
    }).catch(() => {
      // 点击取消，不做任何操作
    })
  } else {
    router.push('/login')
  }
}

const loadPosts = async () => {
  try {
    const response = await postApi.getPosts(nextTimestamp.value)
    const newPosts = response.data.posts
    
    if (refreshing.value) {
      posts.value = newPosts
      refreshing.value = false
    } else {
      posts.value.push(...newPosts)
    }
    
    nextTimestamp.value = response.data.pagination.next_timestamp
    loading.value = false
    
    if (!response.data.pagination.next_timestamp) {
      finished.value = true
    }
  } catch (error) {
    showToast('加载失败')
    loading.value = false
    if (refreshing.value) {
      refreshing.value = false
    }
  }
}

const onLoad = () => {
  loadPosts()
}

const onRefresh = () => {
  finished.value = false
  nextTimestamp.value = ''
  loadPosts()
}

// onMounted(() => {
//   loadPosts()
// })
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background-color: var(--background-color);
}

.user-email {
  margin-left: 8px;
  font-size: 14px;
  /* 超宽的数据则用省略号表示 */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #fff;
  width: 40%;
}

.post-list {
  padding: 12px;
}

.post-item {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;
}

.post-item:active {
  transform: scale(0.98);
}

.post-title {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-color);
  margin-bottom: 12px;
  line-height: 1.4;
  /* 省略 */
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-meta {
  display: flex;
  align-items: center;
  font-size: 13px;
  color: #666;
  gap: 16px;
}

.post-meta .van-icon {
  font-size: 14px;
  margin-right: 4px;
}

.last-reply {
  margin-top: 12px;
}

.reply-meta {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #666;
}

.van-divider {
  margin: 12px 0;
  color: #999;
  font-size: 12px;
}

:deep(.van-nav-bar) {
  background-color: var(--theme-color);
}

:deep(.van-nav-bar .van-icon),
:deep(.van-nav-bar__text),
:deep(.van-nav-bar__title) {
  color: #fff;
}
</style> 