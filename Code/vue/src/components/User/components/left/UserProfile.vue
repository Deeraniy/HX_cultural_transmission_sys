<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElButton, ElMessage } from 'element-plus'
import UserPassword from '@/components/User/components/left/UserPassword.vue'
import UserAPI from '@/api/user'
import httpInstance from '@/utils/http.js'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const visible = ref(false)
const formSize = ref('default')
const ruleFormRef = ref<FormInstance>()

interface UserForm {
    uid: number;
    nickname: string;
    gender: string;
    age: number;
    email: string;
    mobile: string;
    location: string;
    description: string;
    avatar: string;
}

// 表单数据
const ruleForm = ref<UserForm>({
    uid: 0,
    nickname: '',
    gender: '',
    age: 0,
    email: '',
    mobile: '',
    location: '',
    description: '',
    avatar: ''
})

onMounted(() => {
    getUserInfo();
});

const fileList = ref([])

const password = ref('')

// 获取用户信息
const getUserInfo = () => {
    UserAPI.getUserFullInfo(userStore.userId).then((res: any) => {
        if (res && res.data) {
            // 转换后端性别值为前端显示值
            console.log("用户信息为:", res.data);
            let displayGender = res.data.gender;
            if (displayGender === 'male') {
                displayGender = '男';
            } else if (displayGender === 'female') {
                displayGender = '女';
            } else {
                displayGender = '其他';
            }

            ruleForm.value = {
                ...res.data,
                uid: typeof res.data.uid === 'string' ? parseInt(res.data.uid) : (res.data.uid || 0),
                age: Number(res.data.age || 0),
                gender: displayGender,  // 使用转换后的值
                email: res.data.email || '',
                mobile: res.data.mobile || '',
                location: res.data.location || '',
                description: res.data.description || '',
                avatar: res.data.avatar || ''
            };
        }
    });
};

// 提交表单
const submitForm = async () => {
    try {
        console.log("提交的表单数据:", ruleForm.value);
        const res: any = await UserAPI.updateUserInfo(ruleForm.value);
        if (res?.status === 'success') {
            ElMessage({
                type: 'success',
                message: '保存成功'
            });
            // 触发用户信息更新事件
            window.dispatchEvent(new Event('user-info-updated'));
        } else {
            throw new Error(res?.message || '保存失败');
        }
    } catch (error) {
        ElMessage({
            type: 'error',
            message: error instanceof Error ? error.message : '保存失败'
        });
    }
};

// 初始化表单数据
const initForm = () => {
    ruleForm.value = {
        uid: typeof userStore.userId === 'string' ? parseInt(userStore.userId) : (userStore.userId || 0),
        nickname: '',
        gender: '',
        age: 0,
        email: '',
        mobile: '',
        location: '',
        description: '',
        avatar: ''
    };
};

// 文件上传前的检查
const beforeAvatarUpload = (file) => {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/gif'
  const isLt3M = file.size / 1024 / 1024 < 3

  if (!isJPG) {
    ElMessage.error('只允许jpg、png、gif格式的图片')
  }
  if (!isLt3M) {
    ElMessage.error('上传的图片大小不能超过3MB')
  }
  return isJPG && isLt3M
}

// 文件上传成功后的处理
const handleAvatarSuccess = (data) => {
  console.log('上传响应数据:', data);
  if (data && data.status === 'success' && data.data && data.data.url) {
    // 确保URL是完整的
    const imageUrl = data.data.url;
    ruleForm.value.avatar = imageUrl;
    ElMessage({
      message: '上传成功',
      type: 'success'
    });
  } else {
    handleAvatarError(new Error('上传失败：返回的数据格式不正确'));
  }
}

const uploadFile = (params) => {
  const file = params.file;
  const formData = new FormData();
  formData.append('file', file);
  formData.append('userId', userStore.userId);

  httpInstance.post('/user/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(response => {
    console.log('上传响应:', response);
    // 直接传递整个响应数据
    handleAvatarSuccess(response);
  }).catch((error) => {
    console.error('上传错误:', error);
    handleAvatarError(error);
  });
}

// 文件上传失败后的处理
const handleAvatarError = (error) => {
  console.error('处理上传错误:', error);
  ElMessage({
    message: '上传失败: ' + (error.message || '未知错误'),
    type: 'error'
  });
}

const handleImageError = () => {
  ruleForm.value.avatar = '';  // 清空错误的图片URL
}
</script>

<template>
    <div>
        <!-- 标题 -->
        <div>
            <el-text class="mainTitle">修改资料与密码</el-text>
        </div>
        <div style="display: flex;">
            <el-card shadow="hover" class="box-card">
                <!-- 用户资料表单 -->
                <div class="profile">
                    <el-form ref="ruleFormRef" :model="ruleForm" label-width="90px" label-position="left"
                        class="demo-ruleForm" :size="formSize" status-icon>
                        <el-form-item label="修改头像">
                          <el-upload
                              class="avatar-uploader"
                              action="#"
                              :http-request="uploadFile"
                              :before-upload="beforeAvatarUpload"
                              list-type="picture-card"
                              :file-list="fileList"
                              :show-file-list="false"
                              :auto-upload="true"
                          >
                            <img v-if="ruleForm.avatar" :src="ruleForm.avatar" class="img" @error="handleImageError">
                            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                          </el-upload>
                        </el-form-item>
                        <el-form-item label="用户昵称" prop="nickname">
                            <el-input v-model="ruleForm.nickname" />
                        </el-form-item>
                        <el-form-item label="邮箱" prop="email">
                            <el-input v-model="ruleForm.email" />
                        </el-form-item>
                        <el-form-item label="手机号" prop="mobile">
                            <el-input v-model="ruleForm.mobile" />
                        </el-form-item>
                        <el-form-item label="年龄" prop="age">
                            <el-input v-model="ruleForm.age" />
                        </el-form-item>

                        <el-form-item label="性别" prop="gender">
                            <el-radio-group v-model="ruleForm.gender">
                                <el-radio label="男">男</el-radio>
                                <el-radio label="女">女</el-radio>
                                <el-radio label="其他">其他</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="地区" prop="location">
                            <el-input v-model="ruleForm.location" />
                        </el-form-item>
                        <el-form-item label="个人简介" prop="description">
                            <el-input
                                v-model="ruleForm.description"
                                type="textarea"
                                :rows="4"
                                placeholder="写点什么介绍一下自己吧..."
                            />
                        </el-form-item>
                        <!-- 提交表单 -->
                        <el-form-item>
                            <el-button type="primary" @click="submitForm()">
                                保存
                            </el-button>
                            <el-button type="danger" @click="initForm()">清除</el-button>
                        </el-form-item>
                    </el-form>
                </div>
            </el-card>

        </div><UserPassword />
    </div>
</template>

<style scoped>
.img{
    height: 40px;
    width: 40px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 10px;
}
.box-card {
    margin-top: 21px;
    margin-left: 20px;
    border-radius: 7px;
    width: 750px;
    padding-right: 30px;
}

.card {
    margin-top: 21px;
    margin-left: 20px;
    border-radius: 5px;
    width: 300px;
    height: 300px;
}

.input {
    width: 500px;
    height: 40px;
}

.input-mini {
    width: 250px;
    height: 40px;
}

.mainTitle {
    margin-left: 30px;
    font-size: 24px;
    color: #000;
    font-weight: bolder;
}

.profile {
    margin-left: 30px;
    margin-top: 20px;
}
</style>
