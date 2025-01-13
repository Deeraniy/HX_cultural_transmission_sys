import request from "@/utils/request";

const DICT_BASE_URL = "";

class CommentAPI {
    static getCommentList(name: string, type: number) {
        console.log("Before any logic, type:", type);  // 打印 type 的值
        let urlPath = 'get_comment_list';

        // 确保 type 是数字类型
        if (typeof type === 'string') {
            type = parseInt(type, 10);  // 如果是字符串类型，将其转化为数字
        }

        if (type === 1) {
            urlPath = 'spot_get_comment_list';
        } else if (type === 2) {
            urlPath = 'liter_get_comment_list';
        } else if (type === 3) {
            urlPath = 'food_get_comment_list';
        } else if (type === 4) {
            urlPath = 'folk_get_comment_list';
        }
        console.log("urlPath after logic:", urlPath);  // 确保 urlPath 被正确赋值
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
        // 确保 type 是数字类型
        if (typeof type === 'string') {
            type = parseInt(type, 10);  // 如果是字符串类型，将其转化为数字
        }
        if (type === 1) {
            urlPath = 'spot_get_comment_list_recent';
        } else if (type === 2) {
            urlPath = 'liter_get_comment_list_recent';
        } else if (type === 3) {
            urlPath = 'food_get_comment_list_recent';
        } else if (type === 4) {
            urlPath = 'folk_get_comment_list_recent';
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
        // 确保 type 是数字类型
        if (typeof type === 'string') {
            type = parseInt(type, 10);  // 如果是字符串类型，将其转化为数字
        }
        if (type === 1) {
            urlPath = 'spot_get_comment_time_span';
        } else if (type === 2) {
            urlPath = 'liter_get_comment_time_span';
        } else if (type === 3) {
            urlPath = 'food_get_comment_time_span';
        } else if (type === 4) {
            urlPath = 'folk_get_comment_time_span';
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
        // 确保 type 是数字类型
        if (typeof type === 'string') {
            type = parseInt(type, 10);  // 如果是字符串类型，将其转化为数字
        }
        if (type === 1) {
            urlPath = 'spot_get_comment_count_last_12_months';
        } else if (type === 2) {
            urlPath = 'liter_get_comment_count_last_12_months';
        } else if (type === 3) {
            urlPath = 'food_get_comment_count_last_12_months';
        } else if (type === 4) {
            urlPath = 'folk_get_comment_count_last_12_months';
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
        // 确保 type 是数字类型
        if (typeof type === 'string') {
            type = parseInt(type, 10);  // 如果是字符串类型，将其转化为数字
        }
        if (type === 1) {
            urlPath = 'spot_get_comment_ip_count';
        } else if (type === 2) {
            urlPath = 'liter_get_comment_ip_count';
        }else if (type === 3) {
            urlPath = 'food_get_comment_ip_count';
        } else if (type === 4) {
            urlPath = 'folk_get_comment_ip_count';
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
        // 确保 type 是数字类型
        if (typeof type === 'string') {
            type = parseInt(type, 10);  // 如果是字符串类型，将其转化为数字
        }
        if (type === 1) {
            urlPath = 'spot_get_average_score_by_bi_month';
        } else if (type === 2) {
            urlPath = 'liter_get_average_score_by_bi_month';
        } else if (type === 3) {
            urlPath = 'food_get_average_score_by_bi_month';
        } else if (type === 4) {
            urlPath = 'folk_get_average_score_by_bi_month';
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

