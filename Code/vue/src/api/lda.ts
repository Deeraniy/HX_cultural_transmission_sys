import request from "@/utils/request";

const DICT_BASE_URL = "";

class LdaAPI {
    static LdaAPI(name: string, type: number) {
        let urlPath = 'lda_analyze';
        if (type === 1) {
            urlPath = 'spot_lda_analyze';
        } else if (type === 2) {
            urlPath = 'lite_lda_analyze';
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