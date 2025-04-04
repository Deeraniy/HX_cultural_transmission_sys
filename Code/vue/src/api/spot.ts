import request from "@/utils/request";

const DICT_BASE_URL = "";

class SpotsAPI {
    // 获取所有景点
    static getSpotsAPI() {
        return request({
            url: `${DICT_BASE_URL}/get_spot/`,
            method: "get",
        });
    }

    // 根据名称搜索景点
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

