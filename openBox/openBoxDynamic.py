import json

import requests
import jsonpath


def WhosFriend(tag, dynamic):
    return tag in dynamic


def checkAllResult(tagNeed, dynamic):
    dictTag = dict.fromkeys(tagNeed, 0)
    for comment in dynamic:
        for key in dictTag.keys():
            if key in comment:
                dictTag[key] += 1

    return dictTag


def sendRequest(uid):
    url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset=&host_mid={0}&timezone_offset=-480&features=itemOpusStyle".format(
        uid)
    response = requests.get(url=url)
    page = json.loads(response.text)
    resultData = page["data"]["items"]
    commentList = jsonpath.jsonpath(resultData, '$..orig_text')

    return commentList


if __name__ == '__main__':
    tagNeed1 = ["明日方舟", "原神", "星穹铁道", "虚拟主播", "抽奖"]
    print(checkAllResult(tagNeed1, sendRequest("208259")))
    print(sendRequest("208259"))