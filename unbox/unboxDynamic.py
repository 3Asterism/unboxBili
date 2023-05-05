import json
import requests
import jsonpath
from flask import Flask, request

server = Flask(__name__)


def checkAllResult(tagNeed, dynamic):
    dictTag = dict.fromkeys(tagNeed, 0)
    for comment in dynamic:
        for key in dictTag.keys():
            if key in comment:
                dictTag[key] += 1

    return json.dumps(dictTag).encode('utf-8')


def circulateForAllDynamic(uid):
    originalURL = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset=&host_mid={0}&timezone_offset=-480&features=itemOpusStyle".format(
        uid)
    response = requests.get(url=originalURL)
    page = json.loads(response.text)
    # 拿到第一页的数据
    resultList = jsonpath.jsonpath(page["data"]["items"], '$..orig_text')
    flag0 = jsonpath.jsonpath(page["data"], '$..has_more')[0]
    # 如果有更多内容 进行循环
    if flag0 is True:
        while (True):
            OldOffsetList = jsonpath.jsonpath(page["data"], '$..offset')
            fullDynamicURL = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset={0}&host_mid={1}&timezone_offset=-480&features=itemOpusStyle".format(
                OldOffsetList[0], uid)
            response = requests.get(url=fullDynamicURL)
            page = json.loads(response.text)
            resultData = page["data"]["items"]
            commentList = jsonpath.jsonpath(resultData, '$..orig_text')
            flag = jsonpath.jsonpath(page["data"], '$..has_more')[0]
            for dynamic in commentList:
                resultList.append(dynamic)
            # 循环结束的标志为 has_more字段为False
            if flag is True:
                continue
            else:
                break

    return resultList


def circulateForFollow(uid):
    originalURL = "https://api.bilibili.com/x/relation/followings?vmid={0}&pn=1&ps=50&order=desc".format(
        uid)
    response = requests.get(url=originalURL)
    page = json.loads(response.text)
    # 检查是否设置了隐私
    if jsonpath.jsonpath(page, '$..message')[0] != '0':
        return "该用户设置了隐私！"
    # 拿到第一页的up主名字数据
    resultList = jsonpath.jsonpath(page["data"]["list"], '$..uname')
    flag = int(jsonpath.jsonpath(page["data"], '$..total')[0] / 50)
    # 如果有更多内容 进行循环
    if flag - 1 >= 0:
        for i in range(flag - 1):
            if i + 2 > 5:
                break
            newFlag = i + 2
            newURL = "https://api.bilibili.com/x/relation/followings?vmid={0}&pn={1}&ps=50&order=desc".format(
                uid, newFlag)
            response = requests.get(url=newURL)
            page = json.loads(response.text)
            uList = jsonpath.jsonpath(page["data"]["list"], '$..uname')
            for uname in uList:
                resultList.append(uname)

    return resultList


@server.route('/sendRequest', methods=['POST'])
def sendRequest():
    # 返回b站动态数据
    uid = json.loads(request.get_data())['uid']
    tagNeed = json.loads(request.get_data())['tag']
    resultWhat = json.loads(request.get_data())['result']
    result = checkAllResult(tagNeed, circulateForAllDynamic(uid))
    # 返回动态列表或者返回统计值
    if resultWhat == "1":
        return circulateForAllDynamic(uid)
    else:
        return result


@server.route('/sendFollowRequest', methods=['POST'])
def sendFollowRequest():
    # 返回b站关注数据
    uid = json.loads(request.get_data())['uid']
    tagNeed = json.loads(request.get_data())['tag']
    resultWhat = json.loads(request.get_data())['result']
    result = checkAllResult(tagNeed, circulateForFollow(uid))
    # 返回关注列表或者返回统计值
    if resultWhat == "1":
        return circulateForFollow(uid)
    else:
        return result


if __name__ == '__main__':
    server.run(host='127.0.0.1', port=5000)
