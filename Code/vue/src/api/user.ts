import request from "@/utils/request";

const DICT_BASE_URL = "";


class UserAPI {
    // 用户注册
    static registerAPI(data: {
        username: string,
        password: string,
        age: number,
        sex: 'male' | 'female' | 'other',
        location: string,
        avatar?: string
    }) {
        let urlPath = 'register';
        
        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "post",
            data
        }).catch(error => {
            // 打印详细错误信息
            console.error('Registration error:', error.response?.data || error);
            throw error;
        });
    }

    // 用户登录
    static loginAPI(data: {
        username: string,
        password: string
    }) {
        let urlPath = 'login';
        
        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "post",
            data
        });
    }
}

export default UserAPI ;

