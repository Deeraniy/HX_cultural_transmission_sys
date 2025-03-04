
<script setup>import { ref } from 'vue';
import { ElMessage } from 'element-plus';
 // 假设系统存储在stores/system中

 // 头像上传地址
const multiple = ref(false); // 是否支持多选文件
const limitFile = ref(1); // 文件上传限制
const fileList = ref([]); // 上传的文件列表


// 当文件超过上传限制时触发的钩子函数
const handleExceed = () => {
  ElMessage.warning('头像只允许上传一个');
};

// 文件上传成功时的钩子函数
const handleSuccess = (response, uploadFile) => {
  console.log(response);
  ruleForm.value.avatar = response.data;
};

const ruleForm = ref({
  avatar: '',
});
</script>
<template>
  <el-form-item label="头像" prop="avatar">
    <el-upload
        v-model:file-list="fileList"
        class="upload-demo"

        :on-exceed="handleExceed"
        :on-success="handleSuccess"
        list-type="picture"
        :multiple="multiple"
        :limit="limitFile"

        name="avatar"
    >
      <el-button type="primary">上传头像</el-button>
    </el-upload>
  </el-form-item>
</template>

<style scoped>

</style>
