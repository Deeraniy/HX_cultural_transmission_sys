import request from "@/utils/request";

const DICT_BASE_URL = "";

class SentimentAPI {
    static getSentimentAnalyzeAPI(name: string, type: number) {
        let urlPath = 'sentiments_analyze';
        // 确保 type 是数字类型
        if (typeof type === 'string') {
            type = parseInt(type, 10);  // 如果是字符串类型，将其转化为数字
        }
        if (type === 1) {
            urlPath = 'spot_sentiments_analyze';
        } else if (type === 2) {
            urlPath = 'liter_sentiments_analyze';
        } else if (type === 3) {
            urlPath = 'food_sentiments_analyze';
        } else if (type === 4) {
            urlPath = 'folk_sentiments_analyze';
        }

        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "get",
            params: {
                name: name
            }
        });
    }

    static getSentimentResultAPI(name: string, type: number) {
        let urlPath = 'sentiments_result';
        // 确保 type 是数字类型
        if (typeof type === 'string') {
            type = parseInt(type, 10);  // 如果是字符串类型，将其转化为数字
        }
        if (type === 1) {
            urlPath = 'spot_sentiments_result';
        } else if (type === 2) {
            urlPath = 'liter_sentiments_result';
        } else if (type === 3) {
            urlPath = 'food_sentiments_result';
        } else if (type === 4) {
            urlPath = 'folk_sentiments_result';
        }

        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "get",
            params: {
                name: name
            }
        });
    }

    static getSentimentReportAPI(name: string, type: number) {
        let urlPath = 'generate_report';
        // 确保 type 是数字类型
        if (typeof type === 'string') {
            type = parseInt(type, 10);  // 如果是字符串类型，将其转化为数字
        }
        if (type === 1) {
            urlPath = 'spot_generate_report';
        } else if (type === 2) {
            urlPath = 'liter_generate_report';
        } else if (type === 3) {
            urlPath = 'food_generate_report';
        } else if (type === 4) {
            urlPath = 'folk_generate_report';
        }

        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "get",
            params: {
                name: name
            }
        });
    }

    static getSentimentPieAPI(name: string, type: number) {
        let urlPath = 'sentiments_count';
        // 确保 type 是数字类型
        if (typeof type === 'string') {
            type = parseInt(type, 10);  // 如果是字符串类型，将其转化为数字
        }
        if (type === 1) {
            urlPath = 'spot_sentiments_count';
        } else if (type === 2) {
            urlPath = 'liter_sentiments_count';
        } else if (type === 3) {
            urlPath = 'food_sentiments_count';
        } else if (type === 4) {
            urlPath = 'folk_sentiments_count';
        }
        console.log("俺不中嘞")
        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "get",
            params: {
                name: name
            }
        });
    }

    static getSentimentWordAPI(name: string, type: number) {
        let urlPath = 'get_word_frequency';
        // 确保 type 是数字类型
        if (typeof type === 'string') {
            type = parseInt(type, 10);  // 如果是字符串类型，将其转化为数字
        }
        if (type === 1) {
            urlPath = 'spot_get_word_frequency';
        } else if (type === 2) {
            urlPath = 'liter_get_word_frequency';
        } else if (type === 3) {
            urlPath = 'food_get_word_frequency';
        } else if (type === 4) {
            urlPath = 'folk_get_word_frequency';
        }

        return request({
            url: `${DICT_BASE_URL}/${urlPath}/`,
            method: "get",
            params: {
                name: name
            }
        });
    }

    static getCasualImpactAPI(name: string) {
        return request({
            url: `${DICT_BASE_URL}/get_casual_impact/`,
            method: "get",
            params: {
                name: name
            }
        });
    }
}

export default SentimentAPI;
