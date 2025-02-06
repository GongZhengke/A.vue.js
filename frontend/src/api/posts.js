import axios from 'axios'

export const postApi = {
  // 获取帖子列表
  getPosts(timestamp = '') {
    return axios.get(`/api/posts${timestamp ? `?timestamp=${timestamp}` : ''}`)
  },

  // 获取帖子详情
  getPostDetail(postId, timestamp = '') {
    return axios.get(`/api/posts/${postId}${timestamp ? `?timestamp=${timestamp}` : ''}`)
  }
} 