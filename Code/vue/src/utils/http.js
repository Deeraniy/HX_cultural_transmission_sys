import axios from 'axios';

const httpInstance = axios.create({
    baseURL: '/api/',
    timeout: 5000
});

httpInstance.interceptors.response.use(res => {
    let data = res.data;
    if (res.status == 200) {
        return res.data;
    } else if (res.status == 401) {
        ElMessage.error("未授权！！！");
    } else {
        ElMessage.error(res.data.msg);
    }
}, e => {
    return Promise.reject(e);
});

httpInstance.interceptors.request.use(
    config => {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers.Authorization = token;
        }else {
            delete config.headers['Authorization']; // 确保在未登录时不发送认证头
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

export default httpInstance;
