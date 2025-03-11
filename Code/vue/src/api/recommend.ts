import request from "@/utils/request";

const DICT_BASE_URL = "";

class RecommendAPI {

    // 获取标签详细信息
    static getTagDetailAPI(tagIds: number[]) {
        return request({
            url: `${DICT_BASE_URL}/get_tag_details`,
            method: "get",
            params: { tag_ids: tagIds.join(',') }
        });
    }

 
}

export default RecommendAPI; 