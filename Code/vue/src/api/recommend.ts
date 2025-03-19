import request from "@/utils/request";
import TagsAPI from "./tags";

const DICT_BASE_URL = "";
const BASE_URL = "";  // 根据实际情况设置基础URL

class RecommendAPI {
    // 获取用户偏好数据
   

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
    static getTagDetailAPI(tagIds: number[]) {
        let urlPath = 'get_tag_details';
        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "get",
            params: { tag_ids: tagIds.join(',') }
        });
    }
}

export default RecommendAPI ;

