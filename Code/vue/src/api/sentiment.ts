import request from "@/utils/request";

const DICT_BASE_URL = "";

class SentimentAPI {
    static getSentimentAnalyzeAPI(name: string, type: number) {
        let urlPath = 'sentiments_analyze';
        if (type === 1) {
            urlPath = 'spot_sentiments_analyze';
        } else if (type === 2) {
            urlPath = 'lite_sentiments_analyze';
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
        if (type === 1) {
            urlPath = 'spot_sentiments_result';
        } else if (type === 2) {
            urlPath = 'lite_sentiments_result';
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
        if (type === 1) {
            urlPath = 'spot_generate_report';
        } else if (type === 2) {
            urlPath = 'lite_generate_report';
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
        if (type === 1) {
            urlPath = 'spot_sentiments_count';
        } else if (type === 2) {
            urlPath = 'lite_sentiments_count';
        }

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
        if (type === 1) {
            urlPath = 'spot_word_frequency';
        } else if (type === 2) {
            urlPath = 'lite_word_frequency';
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

export default SentimentAPI;

