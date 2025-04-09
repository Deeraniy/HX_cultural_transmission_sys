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

interface UserDistributionData {
    status: string;
    data: {
        [region: string]: {
            total: number;
            themes: {
                '名胜古迹': number;
                '美食文化': number;
                '影视文学': number;
                '非遗民俗': number;
            };
        };
    };
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
        }).then(response => {
            console.log("response",response);
            if (response  === "添加成功") {
                console.log('浏览记录添加成功:', response);
            } else {
                console.error('浏览记录添加失败:', response);
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
            params: { uid:uid }
        });
    }
    static GetUserStar(uid: number) {
        return request({
            url: `${BASE_URL}/get_user_star/`,
            method: 'get',
            params: { uid:uid }
        });
    }
    static GetAllHistory(uid: number) {
        return request({
            url: `${BASE_URL}/history/`,
            method: 'get',
        });
    }

    // 获取用户地区分布数据
    static getUserDistribution(): Promise<any> {
        return request({
            url: `${DICT_BASE_URL}/user/distribution`,
            method: 'get'
        }).catch(error => {
            console.error('Get user distribution error:', error.response?.data || error);
            throw error;
        });
    }

    // 删除指定的用户历史记录
    static DeleteUserHistory(uid: number, historyIds: number[]): Promise<any> {
        console.log('准备删除历史记录', { uid, historyIds });
        // 确保参数类型正确
        const numericUid = Number(uid);
        const numericHistoryIds = historyIds.map(id => Number(id));
        
        return request({
            url: `${BASE_URL}/delete_user_history/`,
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                uid: numericUid,
                history_ids: numericHistoryIds
            }
        }).then(response => {
            console.log('删除历史记录成功', response);
            return response;
        }).catch(error => {
            console.error('Delete history error:', error.response?.data || error);
            throw error;
        });
    }

    // 通过复合键删除历史记录（用于没有ID字段的记录）
    static DeleteUserHistoryByCompositeKey(uid: number, criteria: {
        history_times?: string[], // 时间戳列表
        types?: string[],         // 类型列表
        names?: string[]          // 名称列表
    }): Promise<any> {
        console.log('准备通过复合键删除历史记录', { uid, criteria });
        
        return request({
            url: `${BASE_URL}/delete_user_history_by_composite/`,
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                uid: Number(uid),
                history_times: criteria.history_times || [],
                types: criteria.types || [],
                names: criteria.names || []
            }
        }).then(response => {
            console.log('通过复合键删除历史记录成功', response);
            return response;
        }).catch(error => {
            // 如果后端API不存在，使用本地删除
            console.error('通过复合键删除历史记录失败，可能后端API不存在:', error);
            return { success: false, message: "后端API可能不支持此操作，仅执行了前端删除" };
        });
    }

    // 清空用户所有历史记录
    static ClearUserHistory(uid: number): Promise<any> {
        console.log('准备清空历史记录', { uid });
        // 确保参数类型正确
        const numericUid = Number(uid);
        
        return request({
            url: `${BASE_URL}/clear_user_history/`,
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                uid: numericUid
            }
        }).then(response => {
            console.log('清空历史记录成功', response);
            return response;
        }).catch(error => {
            console.error('Clear history error:', error.response?.data || error);
            throw error;
        });
    }

    // 更新收藏状态
    static UpdateFavorite(data: {
        user_id: number | string,
        tag_id: number | string,
        is_favorite: number
    }): Promise<any> {
        console.log('准备更新收藏状态', data);
        
        return request({
            url: `${BASE_URL}/update_favorite/`,
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                user_id: Number(data.user_id),
                tag_id: Number(data.tag_id),
                is_favorite: Number(data.is_favorite)
            }
        }).then(response => {
            console.log('更新收藏状态成功', response);
            return response;
        }).catch(error => {
            console.error('Update favorite error:', error.response?.data || error);
            throw error;
        });
    }

    //用户浏览记录表

}

export default UserAPI ;

