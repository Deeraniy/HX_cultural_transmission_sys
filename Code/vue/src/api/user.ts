import request from "@/utils/request";

const DICT_BASE_URL = "";
const BASE_URL = "";

interface UserUpdateData {
    uid: number;
    nickname?: string;
    gender?: string;
    age?: number;
    description?: string;
    avatar?: string;
    email?: string;
    mobile?: string;
    location?: string;
}
interface UserHistoryData {
    uid: number;    // 对应后端的username参数
    type: string;        // 记录类型
    name: string;        // 项目名称
    img_url: string;   // 图片URL
    describe: string;    // 描述
}

class UserAPI {
    // 用户注册
    static registerAPI(data: {
        username: string,
        password: string,
        age: number,
        sex: 'male' | 'female' | 'other',
        location: string,
        avatar?: string,
        email?: string,
        mobile?: string,
        description?: string
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

    // 获取用户完整信息
    static getUserFullInfo(userId: string | number) {
        let urlPath = 'user';
        return request({
            url: `${DICT_BASE_URL}/${urlPath}`,
            method: 'get',
            params: { userId }
        });
    }

    // 更新用户信息
    static updateUserInfo(data: UserUpdateData) {
        return request({
            url: `/user/update`,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                uid: data.uid,
                nickname: data.nickname,
                gender: data.gender,
                age: data.age,
                description: data.description,
                location: data.location,
                email: data.email,
                mobile: data.mobile
            }
        });
    }



    // 删除用户
    static deleteUser(userId: string) {
        return request({
            url: `/user/${userId}`,
            method: 'delete'
        });
    }

    // 用户浏览记录添加（对应后端的add_history）
    static AddUserHistory(data: UserHistoryData) {
        return request({
            url: `${BASE_URL}/add_user_history/`,
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                uid: data.uid,
                type: data.type,
                name: data.name,
                img_url: data.img_url,
                describe: data.describe,
            }
        }).catch(error => {
            console.error('Add history error:', error.response?.data || error);
            throw error;
        });
    }

    // 用户浏览记录获取
    static GetUserHistory(uid: number) {
        return request({
            url: `${BASE_URL}/get_all_history/`,
            method: 'get',
            params: { uid }
        });
    }


    //用户浏览记录表

}

export default UserAPI ;

