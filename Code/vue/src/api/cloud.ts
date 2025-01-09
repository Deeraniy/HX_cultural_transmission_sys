import request from "@/utils/request";

const DICT_BASE_URL = "";

class CloudAPI {
    static getCloudAPI(name: string, type: number) {
        let urlPath = 'get_cloud';
        // 确保 type 是数字类型
        if (typeof type === 'string') {
            type = parseInt(type, 10);  // 如果是字符串类型，将其转化为数字
        }
        if (type === 1) {
            urlPath = 'spot_get_cloud';
        } else if (type === 2) {
            urlPath = 'liter_get_cloud';
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

