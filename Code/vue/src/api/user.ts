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
}
export default RecommendAPI;

