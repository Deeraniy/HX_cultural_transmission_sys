import requests
import json
import pandas as pd
from tqdm import tqdm
 
userNames = []
commentDetails = []
commentTimes = []
 
total_pages = 1
 
for pagen in tqdm(range(0, total_pages), desc='爬取进度', unit='页'):
    #payload参数实质上就是网络下的负载
    payload = {
        "arg": {
            "channelType": 7,
            "collapseTpte": 1,
            "commentTagId": 0,
            "pageIndex": pagen,
            "pageSize": 10,
            "resourceId":22176,
            "resourceType":11,
            "sourseType": 1,
            "sortType": 3,
            "starType": 0
        },
        "head": {
            "cid": "09031081213865125571",
            "ctok": "",
            "cver": "1.0",
            "lang": "01",
            "sid": "8888",
            "syscode": "09",
            "auth": "",
            "xsid": "",
            "extension": []
        }
    }
 
    #网络的标头中的url路径，采用POST请求方法，其？后面的内容就是payload
    postUrl = "https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList"
 
    html = requests.post(postUrl, data=json.dumps(payload)).text
    html_1 = json.loads(html)#html_1实质就是网络下面的响应界面
 
    # 检查响应中是否存在'items'
    if 'items' in html_1["result"]:
        commentItems = html_1["result"]["items"]
        for i in range(0, len(commentItems)):
            # 在访问元素之前检查当前项是否不为None
            if commentItems[i] is not None and 'userInfo' in commentItems[i] and 'userNick' in commentItems[i][
                'userInfo']:
                userName = commentItems[i]['userInfo']['userNick']
                commentDetail = commentItems[i]['content']
                commentTime = commentItems[i]['publishTypeTag']
 
                userNames.append(userName)
                commentDetails.append(commentDetail)
                commentTimes.append(commentTime)
 
# 创建 DataFrame
df = pd.DataFrame({
    '用户评论内容': commentDetails,
    '用户名': userNames,
    '用户评论时间': commentTimes
})
 
# 保存到 Excel 文件
df.to_excel('只爬黄龙溪评论1223url.xlsx', index=False)