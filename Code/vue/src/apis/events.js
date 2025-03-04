/**
 * 注意！ 本文件代码用以获取后端数据
 * 为了文件结构而保留，其本身需根据您的需求进行编写
 * 在组件中已经将此部分注释
 * @author xxh 2023-6-3
 */

import httpInstance from "@/utils/http";

// 与搜索有关的API
export function getAllEvents(){
    return httpInstance({
        url:`/event`,
        method:'get'
    })

}
export function getAllEventsRate(){
    return httpInstance({
        url:`/event/rate`,
        method:'get'
    })

}

export function getEventInfo(communityId){
    return httpInstance({
        url:`/event/${communityId}`,
        method:'get'
    })

}

export function getEventGenderStats(){
    return httpInstance({
        url:`/event/gender-stats`,
        method:'get'
    })

}