import request from "@/utils/request";

const DICT_BASE_URL = "";

class SpotsAPI {
    static getSpotsAPI() {
        return request({
            url: `${DICT_BASE_URL}/get_spot/`,
            method: "get",
        });
    }

}

export default SpotsAPI;

