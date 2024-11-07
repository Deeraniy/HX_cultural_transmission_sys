import request from "@/utils/request";

const DICT_BASE_URL = "";

class SentimentAPI {
    static getSentimentAnalyzeAPI(spot_name:string) {
        return request({
            url: `${DICT_BASE_URL}/sentiments_analyze/`,
            method: "get",
            params: {
                spot_name: spot_name
            }
        });
    }
    static getSentimentResultAPI(spot_name:string) {
        return request({
            url: `${DICT_BASE_URL}/sentiments_result/`,
            method: "get",
            params: {
                spot_name: spot_name
            }
        });
    }

    static getSentimentReportAPI(spot_name:string) {
        return request({
            url: `${DICT_BASE_URL}/generate_report/`,
            method: "get",
            params: {
                spot_name: spot_name
            }
        });
    }

}

export default SentimentAPI;

