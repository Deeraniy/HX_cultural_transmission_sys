import request from "@/utils/request";

const DICT_BASE_URL = "/api";

class SpotsAPI {
    static getSpotsAPI() {
        return request({
            url: `${DICT_BASE_URL}/get_spot`,
            method: "get",
        });
    }
    /**
     * 获取字典分页列表
     *
     * @param queryParams 查询参数
     * @returns 字典分页结果
     */
    // static getPage(queryParams: DictPageQuery) {
    //     return request<any, PageResult<DictPageVO[]>>({
    //         url: `${DICT_BASE_URL}/page`,
    //         method: "get",
    //         // params: queryParams,
    //     });
    // }

    /**
     * 获取字典表单数据
     *
     * @param id 字典ID
     * @returns 字典表单数据
     */
    // static getFormData(id: number) {
    //     return request<any, ResponseData<DictForm>>({
    //         url: `${DICT_BASE_URL}/${id}/form`,
    //         method: "get",
    //     });
    // }

    /**
     * 新增字典
     *
     * @param data 字典表单数据
     * @returns 请求结果
     */
    // static add(data: DictForm) {
    //     return request({
    //         url: `${DICT_BASE_URL}`,
    //         method: "post",
    //         data: data,
    //     });
    // }

    /**
     * 修改字典
     *
     * @param id 字典ID
     * @param data 字典表单数据
     * @returns 请求结果
     */
    // static update(id: number, data: DictForm) {
    //     return request({
    //         url: `${DICT_BASE_URL}/${id}`,
    //         method: "put",
    //         data: data,
    //     });
    // }

    /**
     * 删除字典
     *
     * @param ids 字典ID，多个以英文逗号(,)分隔
     * @returns 请求结果
     */
    static deleteByIds(ids: string) {
        return request({
            url: `${DICT_BASE_URL}/${ids}`,
            method: "delete",
        });
    }

    /**
     * 获取字典的数据项
     *
     * @param typeCode 字典编码
     * @returns 字典数据项
     */
    // static getOptions(code: string) {
    //     return request<any, OptionType[]>({
    //         url: `${DICT_BASE_URL}/${code}/options`,
    //         method: "get",
    //     });
    // }
}

export default SpotsAPI;

