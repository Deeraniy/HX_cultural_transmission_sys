import request from "@/utils/request";

const DICT_BASE_URL = "";

class CommentAPI {
    static getCommentList(name: string, type: number) {
        let urlPath = 'get_comment_list';
        if (type === 1) {
            urlPath = 'spot_comment_list';
        } else if (type === 2) {
            urlPath = 'lite_comment_list';
        }
        
        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "get",
            params: {
                name: name
            }
        });
    }

    static getCommentListRecent(name: string, type: number) {
        let urlPath = 'get_comment_list_recent';
        if (type === 1) {
            urlPath = 'spot_comment_list_recent';
        } else if (type === 2) {
            urlPath = 'lite_comment_list_recent';
        }
        
        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "get",
            params: {
                name: name
            }
        });
    }

    static getCommentTimeSpan(name: string, type: number) {
        let urlPath = 'get_comment_time_span';
        if (type === 1) {
            urlPath = 'spot_comment_time_span';
        } else if (type === 2) {
            urlPath = 'lite_comment_time_span';
        }
        
        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "get",
            params: {
                name: name
            }
        });
    }

    static getCommentCountLastYear(name: string, type: number) {
        let urlPath = 'get_comment_count_last_12_months';
        if (type === 1) {
            urlPath = 'spot_comment_count_last_12_months';
        } else if (type === 2) {
            urlPath = 'lite_comment_count_last_12_months';
        }
        
        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "get",
            params: {
                name: name
            }
        });
    }

    static getCommentIPCount(name: string, type: number) {
        let urlPath = 'get_comment_ip_count';
        if (type === 1) {
            urlPath = 'spot_comment_ip_count';
        } else if (type === 2) {
            urlPath = 'lite_comment_ip_count';
        }
        
        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "get",
            params: {
                name: name
            }
        });
    }

    static getAverageScore(name: string, type: number) {
        let urlPath = 'get_average_score_by_bi_month';
        if (type === 1) {
            urlPath = 'spot_average_score_by_bi_month';
        } else if (type === 2) {
            urlPath = 'lite_average_score_by_bi_month';
        }
        
        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "get",
            params: {
                name: name
            }
        });
    }
}

export default CommentAPI;

