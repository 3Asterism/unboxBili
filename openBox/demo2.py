import json
import requests
import jsonpath
from flask import Flask, request

json1 = "data = {'uid' : 1899520, 'tag' : '原神'}"
json2 = [{'uid': 1899520, 'tag': '原神'}]

server = Flask(__name__)


@server.route('/demo', methods=['POST'])
def demo1():
    raw = request.get_data()
    data = json.loads(raw)
    print(data['tag'])
    return "ok!"


if __name__ == '__main__':
    server.run(host='127.0.0.1', port=5001)
