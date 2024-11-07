import request from "@/utils/request";

const DICT_BASE_URL = "";

class SpotsAPI {
    static getSpotsAPI() {
        return request({
            url: `${DICT_BASE_URL}/get_spot/`,
            method: "get",
        });
    }
    static getSpotByNameAPI(spot_name:string) {
        return request({
            url: `${DICT_BASE_URL}/get_spot_by_name/`,
            method: "get",
            params: {
                spot_name: spot_name
            }
        });
    }

}

export default SpotsAPI;

