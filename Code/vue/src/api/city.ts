import request from "@/utils/request";

const DICT_BASE_URL = "";

class CityAPI {
    static getCityAPI() {
        return request({
            url: `${DICT_BASE_URL}/get_city/`,
            method: "get",
        });
    }

}

export default CityAPI;

