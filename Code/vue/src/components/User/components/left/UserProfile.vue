<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElButton } from 'element-plus'
import UserPassword from '@/components/User/components/left/UserPassword.vue'
import { getUserInfo, updateUserInfo } from '@/apis/user.js';
import httpInstance from '@/utils/http.js'
// 侧栏是否打开
const visible = ref(false)
const formSize = ref('default')
const ruleFormRef = ref<FormInstance>()

// 表单数据
const ruleForm = ref({
    uid:0,
    avatar: '',
    nickname: '',
    gender: '',
    email: '',
    mobile: '',
    age:0,
    description: '',
})

onMounted(() => {
    getUserInfo().then(res => {
        console.log('用户信息',res.data);
        ruleForm.value = res.data;
    })
});
const fileList = ref([])

const password = ref('')
// 配置表单规则
// 判定验证是否通过
const submitForm = () => {
    console.log("avatar值为"+ruleForm.value.avatar)
    console.log(ruleForm.value);
    console.log('发送表单');
    updateUserInfo(ruleForm.value).then(res => {
        console.log(res);
        if(res.code==0){
            alert('保存成功')
        }
    })
}

const resetForm = () => {
    ruleForm.value = {
        uid:0,
        nickname: '',
        gender: '',
        email: '',
        mobile: '',
        age:0,
        description: '',
        avatar: '',
    }
}
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
  ruleForm.value.avatar = data;
  console.log(data)// 更新头像 URL
  ElMessage({
    message: '上传成功',
    type: 'success'
  })
}
const uploadFile = (params) => {
  const file = params.file;
  const formData = new FormData();
  formData.append('file', file);
  httpInstance.post('/file/upload', formData, {
  }).then((response) => {
    handleAvatarSuccess(response.data); // 成功回调
  }).catch((error) => {
    handleAvatarError(error); // 失败回调
  });

}
// 文件上传失败后的处理
const handleAvatarError = (error) => {
  ElMessage({
    message: '上传失败',
    type: 'error'
  })
  console.error('上传文件时发生错误:', error)
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
                              :on-success="handleAvatarSuccess"
                              :on-error="handleAvatarError"
                              list-type="picture-card"
                              :file-list="fileList"
                              :show-file-list="false"
                              :auto-upload="true"
                          >
                            <img v-if="ruleForm.avatar" :src="ruleForm.avatar" class="img">
                            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                          </el-upload>
                        </el-form-item>
                        <el-form-item label="用户昵称" prop="name">
                            <el-input class="input" v-model="ruleForm.nickname" />
                        </el-form-item>
                        <el-form-item label="邮箱" prop="email">
                            <el-input class="input-mini" v-model="ruleForm.email" />
                        </el-form-item>
                        <el-form-item label="电话" prop="mobile">
                            <el-input class="input-mini" v-model="ruleForm.mobile" />
                        </el-form-item>
                        <el-form-item label="年龄" prop="age">
                            <el-input class="input-mini" v-model="ruleForm.age" />
                        </el-form-item>

                        <el-form-item label="性别" prop="gender">
                            <el-radio-group v-model="ruleForm.gender">
                                <el-radio label="男" />
                                <el-radio label="女" />
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="用户描述" prop="desc">
                            <el-input v-model="ruleForm.description" type="textarea" />
                        </el-form-item>
                        <!-- 提交表单 -->
                        <el-form-item>
                            <el-button type="primary" @click="submitForm()">
                                保存
                            </el-button>
                            <el-button type="danger" @click="resetForm()">清除</el-button>
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
    font-size: 18px;
    color: #000;
    font-weight: bolder;
}

.profile {
    margin-left: 30px;
    margin-top: 20px;
}
</style>
