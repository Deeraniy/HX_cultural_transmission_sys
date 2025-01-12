import request from "@/utils/request";

const DICT_BASE_URL = "";

class LdaAPI {
    static LdaAPI(name: string, type: number) {
        let urlPath = 'lda_analyze';
        // 确保 type 是数字类型
        if (typeof type === 'string') {
            type = parseInt(type, 10);  // 如果是字符串类型，将其转化为数字
        }
        if (type === 1) {
            urlPath = 'spot_lda_analyze';
        } else if (type === 2) {
            urlPath = 'liter_lda_analyze';
        } else if (type === 3) {
            urlPath = 'food_lda_analyze';
        } else if (type === 4) {
            urlPath = 'folk_lda_analyze';
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

export default LdaAPI;
