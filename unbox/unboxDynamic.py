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


@server.route('/sendRequest', methods=['POST'])
def sendRequest():
    uid = json.loads(request.get_data())['uid']
    tagNeed = json.loads(request.get_data())['tag']
    url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset=&host_mid={0}&timezone_offset=-480&features=itemOpusStyle".format(
        uid)
    response = requests.get(url=url)
    page = json.loads(response.text)
    pageForOffset = page["data"]
    # 拿到offset字段 以获得全部动态 不然动态不全
    offsetList = jsonpath.jsonpath(pageForOffset, '$..offset')
    fullDynamicURL = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset={0}&host_mid={1}&timezone_offset=-480&features=itemOpusStyle".format(
        offsetList[0], uid)
    # 重新拉取动态
    response = requests.get(url=fullDynamicURL)
    page = json.loads(response.text)
    resultData = page["data"]["items"]
    commentList = jsonpath.jsonpath(resultData, '$..orig_text')
    # 检查动态是否已经完全拉取 返回False即完全拉取
    print(jsonpath.jsonpath(page["data"], '$..has_more')[0])
    result = checkAllResult(tagNeed, commentList)

    return result


if __name__ == '__main__':
    server.run(host='127.0.0.1', port=5000)
