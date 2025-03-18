import request from "@/utils/request";

const DICT_BASE_URL1 = "/api/tag";
const DICT_BASE_URL2 = "";

class TagsAPI {
    // 获取所有标签
    static getAllTagsAPI() {
        return request({
            url: `${DICT_BASE_URL2}/get_all_tags/`,
            method: "get",
        });
    }

    // 记录标签浏览
    static viewTagAPI(userId: number, tagId: number) {
        return request({
            url: `${DICT_BASE_URL1}/view`,
            method: "post",
            data: {
                user_id: userId,
                tag_id: tagId
            }
        });
    }

    // 切换标签点赞状态
    static toggleLikeAPI(userId: number, tagId: number) {
        return request({
            url: `${DICT_BASE_URL1}/like`,
            method: "post",
            data: {
                user_id: userId,
                tag_id: tagId
            }
        });
    }

    // 切换标签收藏状态
    static toggleFavoriteAPI(userId: number, tagId: number) {
        return request({
            url: `${DICT_BASE_URL1}/favorite`,
            method: "post",
            data: {
                user_id: userId,
                tag_id: tagId
            }
        });
    }

    // 获取标签状态
    static getTagStatusAPI(userId: number, tagId: number) {
        return request({
            url: `${DICT_BASE_URL1}/status`,
            method: "get",
            params: {
                user_id: userId,
                tag_id: tagId
            }
        });
    }

    // 获取用户的标签状态
    static getUserTagStatusAPI(userId: number) {
        return request({
            url: `${DICT_BASE_URL1}/get_user_tag_status`,
            method: "get",
            params: { user_id: userId }
        });
    }
}

export default TagsAPI;
