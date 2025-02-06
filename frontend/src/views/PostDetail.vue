<template>
  <div class="post-detail-container">
    <van-nav-bar title="帖子详情" left-arrow @click-left="router.back()" />

    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="onLoad">
        <div class="post-list">
          <div v-for="post in posts" :key="post.id" class="post-item" :class="{ 'is-first': post.id === postId }">
            <div class="post-content">
              <div class="post-quote" v-if="post.quote">
                <van-icon name="quote" />
                {{ post.quote }}
              </div>
              <div class="post-text">{{ post.content }}</div>
            </div>

            <div class="post-meta">
              <div class="author-info">
                <span class="author">{{ post.author.name }}</span>
                <span class="time">{{ post.time.formatted }}</span>
              </div>
              <div class="time-info">
                <div style="gap: 10px; display: flex; align-items: center;cursor: pointer;" v-if="post.actions && post.actions.length > 0">
                  <a v-for="action in post.actions" :key="action.type" size="mini" type="primary" plain
                    :icon="getActionIcon(action.type)" @click.stop="handleAction(action, post)">
                    {{ getActionText(action.type) }}
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </van-list>
    </van-pull-refresh>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postApi } from '../api/posts'
import { showToast } from 'vant'

const route = useRoute()
const router = useRouter()
const postId = route.params.id

const posts = ref([])
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)
const nextTimestamp = ref('')

const getActionIcon = (type) => {
  const icons = {
    reply: 'chat-o',
    edit: 'edit'
  }
  return icons[type] || 'more-o'
}

const getActionText = (type) => {
  const texts = {
    reply: '回复',
    edit: '编辑'
  }
  return texts[type] || type
}

const handleAction = (action, post) => {
  // TODO: 实现回复和编辑功能
  showToast('功能开发中')
}

const loadPosts = async () => {
  try {
    const response = await postApi.getPostDetail(postId, nextTimestamp.value)
    const newPosts = response.data.posts

    if (refreshing.value) {
      posts.value = newPosts
      refreshing.value = false
      finished.value = false
      nextTimestamp.value = response.data.pagination.next_timestamp
    } else {
      posts.value.push(...newPosts)
      nextTimestamp.value = response.data.pagination.next_timestamp
    }

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
  if (!refreshing.value) {
    loadPosts()
  }
}

const onRefresh = () => {
  nextTimestamp.value = ''
  finished.value = false
  loading.value = true
  loadPosts()
}

// onMounted(() => {
//   loadPosts()
// })
</script>

<style scoped>
.post-detail-container {
  min-height: 100vh;
  background-color: var(--background-color);
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
}

.post-item.is-first {
  background: #f0f9ff;
  border: 1px solid var(--theme-color);
}

.post-content {
  margin-bottom: 16px;
}

.post-quote {
  background: #f5f5f5;
  border-left: 3px solid #ddd;
  padding: 8px 12px;
  margin-bottom: 12px;
  font-size: 14px;
  color: #666;
}

.post-quote .van-icon {
  margin-right: 4px;
  color: #999;
}

.post-text {
  font-size: 15px;
  line-height: 1.6;
  color: var(--text-color);
  white-space: pre-wrap;
  /* 将超宽的文字强制换行 */
  word-break: break-all;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: #666;
  margin-bottom: 12px;
}

.author-info,
.time-info {
  display: flex;
  align-items: center;
  gap: 4px;
}

.post-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

:deep(.van-nav-bar) {
  background-color: var(--theme-color);
}

:deep(.van-nav-bar .van-icon),
:deep(.van-nav-bar__text),
:deep(.van-nav-bar__title) {
  color: #fff;
}

.van-button {
  border-radius: 4px;
}
</style>