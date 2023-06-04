# -*- coding: utf-8 -*-
# FileName: plant_identity.py
# Time : 2023/5/3 18:39
# Author: zzy
import json
import base64
import pprint
import re
import requests

PARAMS = {"top_num": 1}
MODEL_API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom_bml/v1/classification/yezimoxing"
ACCESS_TOKEN = "24.737bbe3df34af25ece4a96bc7b1dccd6.2592000.1685615817.282335-33078001"
API_KEY = "Y4v0F2afBtNVW1X7BqSsqCPK"
SECRET_KEY = "BAujPIBVsWvs1rAfKt5vLpKfRqz33wvM"


def img_ident(
        img_url: str, params=None,
        model_api_url="https://aip.baidubce.com/rpc/2.0/ai_custom_bml/v1/classification/yezimoxing",
        access_token="24.737bbe3df34af25ece4a96bc7b1dccd6.2592000.1685615817.282335-33078001",
):
    if params is None:
        params = {"top_num": 1}
    with open(img_url, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        base64_str = base64_data.decode('UTF-8')

    params["image"] = base64_str
    request_url = "{}?access_token={}".format(model_api_url, access_token)
    response = requests.post(url=request_url, json=params)
    response_json = response.json()
    response_str = json.dumps(response_json, indent=4, ensure_ascii=False)
    return response_str


def extract_info(response_str, *key_word):
    """
    :param response_str: 响应json字符串
    :param key_word: 要提取的keyname
    :return: list[response_str.get("key_name", )
    """
    return [re.findall('"{}": "(.*?)"'.format(kw), response_str) for kw in key_word]


