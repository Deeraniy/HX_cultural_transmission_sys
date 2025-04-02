import request from "@/utils/request";

const DICT_BASE_URL = "";

class FolkAPI {
    // 获取所有非遗民俗
    static getFolkCustomAPI() {
        return request({
            url: `${DICT_BASE_URL}/get_folkcustom/`,
            method: "get",
        });
    }

    // 根据名称搜索非遗民俗
    static searchFolkByNameAPI(name: string) {
        return request({
            url: `${DICT_BASE_URL}/search_folk/`,
            method: "get",
            params: { name }
        });
    }

    static getFolkInfluence(){
        return request({
            url: `${DICT_BASE_URL}/get_folk_influence/`,
            method: "get",
        });
    }
}

export default FolkAPI;

