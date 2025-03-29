import request from "@/utils/request";

const DICT_BASE_URL = "";
/*因为最后少了一个"/"导致了虚假的跨域问题*/
class FilmLiteratureAPI {
    static getBook(type_name:string) {
        return request({
            url: `${DICT_BASE_URL}/get_literature_by_type/`,
            method: "get",
            params: {
                type_name: type_name
            }
        });
    }

}
export default FilmLiteratureAPI;