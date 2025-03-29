import request from "@/utils/request";

const DICT_BASE_URL = "";

class FoodAPI {
    // 获取所有美食
    static getFoodAPI() {
        return request({
            url: `${DICT_BASE_URL}/get_food/`,
            method: "get",
        });
    }

    // 根据名称搜索美食
    static searchFoodByNameAPI(name: string) {
        return request({
            url: `${DICT_BASE_URL}/search_food/`,
            method: "get",
            params: { name }
        });
    }

    static getFoodInfluence(){
        return request({
            url: `${DICT_BASE_URL}/get_food_influence/`,
            method: "get",
        });
    }
}

export default FoodAPI;

