import request from "@/utils/request";
import TagsAPI from "./tags";

const DICT_BASE_URL = "";

class RecommendAPI {
    static getPerferenceAPI(userId) {
        let urlPath = 'get_user_preference';

        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "get",
            params: {
                user_id: userId
            }
        });
    }
        // 获取标签详细信息
    static getTagDetailAPI(tagIds) {
        if (!Array.isArray(tagIds)) {
            console.error("getTagDetailAPI: tagIds 不是数组", tagIds);
            return Promise.resolve({ data: { tag_details: [] } });
        }
        let urlPath = 'get_tag_details';
        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "get",
            params: { tag_ids: tagIds.join(',') }
        });
    }

}
export default RecommendAPI;

