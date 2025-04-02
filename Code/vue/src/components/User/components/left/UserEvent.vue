<template>
  <div class="activity-container">
    <!-- 标题区域 -->
    <div class="header-section">
      <div class="title-wrapper">
        <el-icon><Calendar /></el-icon>
        <span class="main-title">我的活动</span>
      </div>
      <div class="subtitle">管理和参与您的文化活动</div>
    </div>

    <!-- 内容区域 -->
    <div class="content-layout">
      <!-- 主要内容卡片 -->
      <el-card class="main-card" shadow="hover">
        <!-- 可以在这里添加活动列表或其他内容 -->
        <div class="card-header">
          <div class="header-left">
            <h3>活动列表</h3>
            <span class="activity-count">共 0 个活动</span>
          </div>
          <div class="header-right">
            <el-button type="primary" plain>
              <el-icon><Plus /></el-icon>
              创建活动
            </el-button>
          </div>
        </div>

        <!-- 筛选区域 -->
        <div class="filter-section">
          <el-input
              class="search-input"
              placeholder="搜索活动"
              prefix-icon="Search"
          />
          <el-select class="filter-select" placeholder="活动状态">
            <el-option label="全部" value="all" />
            <el-option label="进行中" value="active" />
            <el-option label="已结束" value="ended" />
          </el-select>
          <el-select class="filter-select" placeholder="活动类型">
            <el-option label="全部类型" value="all" />
            <el-option label="线上活动" value="online" />
            <el-option label="线下活动" value="offline" />
          </el-select>
        </div>

        <!-- 活动列表占位 -->
        <div class="empty-state">
          <el-empty description="暂无活动" />
        </div>
      </el-card>

      <!-- 侧边栏卡片 -->
      <el-card class="side-card" shadow="hover">
        <div class="side-card-header">
          <h3>活动统计</h3>
        </div>
        <div class="stats-content">
          <div class="stat-item">
            <div class="stat-value">0</div>
            <div class="stat-label">进行中</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">0</div>
            <div class="stat-label">已结束</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">0</div>
            <div class="stat-label">参与人数</div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Calendar, Plus, Search } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElButton } from 'element-plus'
</script>

<style scoped>
.activity-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.header-section {
  margin-bottom: 30px;
}

.title-wrapper {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.main-title {
  margin-left: 10px;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.subtitle {
  color: #909399;
  font-size: 14px;
  margin-left: 34px;
}

.content-layout {
  display: flex;
  gap: 20px;
}

.main-card {
  flex: 1;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.side-card {
  width: 300px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.card-header {
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ebeef5;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-left h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.activity-count {
  color: #909399;
  font-size: 14px;
}

.filter-section {
  padding: 20px;
  display: flex;
  gap: 15px;
  border-bottom: 1px solid #ebeef5;
}

.search-input {
  width: 250px;
}

.filter-select {
  width: 150px;
}

.empty-state {
  padding: 40px;
  display: flex;
  justify-content: center;
}

.side-card-header {
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
}

.side-card-header h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.stats-content {
  padding: 20px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.stat-item {
  text-align: center;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #b71c1c;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 13px;
  color: #606266;
}

/* 响应式布局 */
@media screen and (max-width: 1200px) {
  .content-layout {
    flex-direction: column;
  }

  .side-card {
    width: 100%;
  }

  .stats-content {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media screen and (max-width: 768px) {
  .filter-section {
    flex-direction: column;
  }

  .search-input,
  .filter-select {
    width: 100%;
  }
}
</style>
