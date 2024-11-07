import request from "@/utils/request";

const DICT_BASE_URL = "";

class LdaAPI {
    static LdaAPI(spot_name:string) {
        return request({
            url: `${DICT_BASE_URL}/lda_analyze/`,
            method: "get",
            params: {
                spot_name: spot_name
            }
        });
    }

}

export default LdaAPI;

