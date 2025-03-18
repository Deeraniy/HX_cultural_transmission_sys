import request from "@/utils/request";

const DICT_BASE_URL = "";

class TagsAPI {
    // 获取所有标签
    static getAllTagsAPI() {
        return request({
            url: `${DICT_BASE_URL}/get_all_tags/`,
            method: "get",
        });
    }

    // 更新标签交互（点击/收藏）
    static updateTagInteractionAPI(userId: number, tagId: number, actionType: string) {
        return request({
            url: `${DICT_BASE_URL}/update_tag_interaction`,
            method: "post",
            data: {
                user_id: userId,
                tag_id: tagId,
                action_type: actionType
            }
        });
    }

    // 获取用户的标签状态
    static getUserTagStatusAPI(userId: number) {
        return request({
            url: `${DICT_BASE_URL}/get_user_tag_status`,
            method: "get",
            params: { user_id: userId }
        });
    }
}

export default TagsAPI;
