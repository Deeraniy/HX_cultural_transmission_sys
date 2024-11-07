import request from "@/utils/request";

const DICT_BASE_URL = "";

class CloudAPI {
    static getCloudAPI(spot_name:string) {
        return request({
            url: `${DICT_BASE_URL}/get_cloud/`,
            method: "get",
            params: {
                spot_name: spot_name
            }
        });
    }

}

export default CloudAPI;

