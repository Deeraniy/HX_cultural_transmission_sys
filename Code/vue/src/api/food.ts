import request from "@/utils/request";

const DICT_BASE_URL = "";

class FoodAPI {
    static getFoodAPI() {
        return request({
            url: `${DICT_BASE_URL}/get_food/`,
            method: "get",
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

