import request from "@/utils/request";
import { s } from "vite/dist/node/types.d-aGj9QkWt";

const DICT_BASE_URL = "";

class PreviewAPI {
    static PreviewAPI(data:any[],steps:number=5,degree:number=3) {
        return request({
            url: `${DICT_BASE_URL}/preview/`,
            method: "post",
            data: {
                data: data,
                steps:steps,
                degree:degree
            }
        });
    }

}

export default PreviewAPI;

