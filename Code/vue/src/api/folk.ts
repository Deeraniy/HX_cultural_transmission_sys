import request from "@/utils/request";

const DICT_BASE_URL = "";

class FolkAPI {
    static getFolkCustomAPI() {
        return request({
            url: `${DICT_BASE_URL}/get_folkcustom/`,
            method: "get",
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

