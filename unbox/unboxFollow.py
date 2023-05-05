import json
import requests
import jsonpath
from flask import Flask, request

server = Flask(__name__)

if __name__ == '__main__':
    server.run(host='127.0.0.1', port=5001)
