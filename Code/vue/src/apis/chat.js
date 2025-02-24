/**
 * 注意！ 本文件代码用以获取后端数据
 * 为了文件结构而保留，其本身需根据您的需求进行编写
 * 在组件中已经将此部分注释
 * @author xxh 2023-6-3
 */

import httpInstance from "@/utils/http";

// 热评
export function getChatMessages(fromuser,touser){
    return httpInstance({
        url:'/chat/messages',
        method:'get',
        params:{fromuser,touser}
    })
}
export function getGroupChatMessages(group){
    return httpInstance({
        url:'/chat/groupmessages',
        method:'get',
        params:{group}
    })
}
export function getGroups(username){
    return httpInstance({
        url:'/chat/group',
        method:'get',
        params:{username}
    })
}
export function saveGroup(group,username){
    return httpInstance({
        url:'/chat/save',
        method:'post',
        params:{username,group}
    })
}
export function updateLikeStatus(aid){
    return httpInstance({
        url:`/article/likeit/${aid}`,
        method:'get',

    })
}

