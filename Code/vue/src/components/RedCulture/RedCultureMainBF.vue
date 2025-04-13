<template>
  <el-main>
    <div class="chat-container">
      <!-- 聊天历史记录 -->
      <div class="chat-history" ref="chatHistoryRef">
        <div v-for="(msg, index) in messages" :key="index" class="message-wrapper">
          <div class="message user-message">
            <div class="avatar">你</div>
            <div class="message-content">{{ msg[0] }}</div>
          </div>
          <div class="message bot-message">
            <div class="avatar">AI</div>
            <div class="message-content">{{ msg[1] }}</div>
          </div>
        </div>
      </div>

      <!-- 输入框区域 -->
      <div class="input-area">
        <el-input
          v-model="userInput"
          type="textarea"
          :rows="3"
          placeholder="请输入您的问题..."
          @keyup.enter.native="sendMessage"
        />
        <el-button type="primary" @click="sendMessage" :loading="isLoading">
          发送
        </el-button>
      </div>
    </div>
  </el-main>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import axios from 'axios'

const messages = ref([])
const userInput = ref('')
const isLoading = ref(false)
const chatHistoryRef = ref<HTMLElement | null>(null)

// 发送消息
const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return

  isLoading.value = true
  const message = userInput.value
  userInput.value = ''

  try {
    const response = await axios.post('http://localhost:8080/api/ai/chat/', {
      message: message,
      history: messages.value
    })

    messages.value = response.data.history
  } catch (error) {
    console.error('发送消息失败:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.chat-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  padding: 20px;
}

.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  margin-bottom: 20px;
}

.message-wrapper {
  margin-bottom: 20px;
}

.message {
  display: flex;
  margin-bottom: 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f0f2f5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  flex-shrink: 0;
}

.message-content {
  padding: 10px 15px;
  border-radius: 8px;
  max-width: 70%;
  word-break: break-word;
}

.user-message .message-content {
  background: #e6f7ff;
}

.bot-message .message-content {
  background: #f6ffed;
}

.input-area {
  display: flex;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #eee;
}

.input-area .el-input {
  flex: 1;
}

:deep(.el-textarea__inner) {
  resize: none;
}
</style>
