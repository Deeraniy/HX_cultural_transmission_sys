import request from "@/utils/request";

const DICT_BASE_URL = "";

class CommentAPI {
    static getCommentList(spot_name:string) {
        return request({
            url: `${DICT_BASE_URL}/get_comment_list/`,
            method: "get",
            params: {
                spot_name: spot_name
            }
        });
    }
    static getCommentListRecent(spot_name:string) {
        return request({
            url: `${DICT_BASE_URL}/get_comment_list_recent/`,
            method: "get",
            params: {
                spot_name: spot_name
            }
        });
    }
    static getCommentTimeSpan(spot_name:string) {
        return request({
            url: `${DICT_BASE_URL}/get_comment_time_span/`,
            method: "get",
            params: {
                spot_name: spot_name
            }
        });
    }
    static getCommentCountLastYear(spot_name:string) {
        return request({
            url: `${DICT_BASE_URL}/get_comment_count_last_12_months/`,
            method: "get",
            params: {
                spot_name: spot_name
            }
        });
    }
    static getCommentIPCount(spot_name:string) {
        return request({
            url: `${DICT_BASE_URL}/get_comment_ip_count/`,
            method: "get",
            params: {
                spot_name: spot_name
            }
        });
    }
    static getAverageScore(spot_name:string) {
        return request({
            url: `${DICT_BASE_URL}/get_average_score_by_bi_month/`,
            method: "get",
            params: {
                spot_name: spot_name
            }
        });
    }


}

export default CommentAPI;

