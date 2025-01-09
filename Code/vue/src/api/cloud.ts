import request from "@/utils/request";

const DICT_BASE_URL = "";

class CloudAPI {
    static getCloudAPI(name: string, type: number) {
        let urlPath = 'get_cloud';
        if (type === 1) {
            urlPath = 'spot_cloud';
        } else if (type === 2) {
            urlPath = 'lite_cloud';
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

export default CloudAPI;

