
"""
BML 图像分类 调用模型公有云API Python3实现
"""

import json
import base64

import requests
"""
使用 requests 库发送请求
使用 pip（或者 pip3）检查我的 python3 环境是否安装了该库，执行命令
  pip freeze | grep requests
若返回值为空，则安装该库
  pip install requests
"""


# 目标图片的 本地文件路径，支持jpg/png/bmp格式
# IMAGE_FILEPATH = r"C:\Users\ASUS\Desktop\Vue\data\1.JPG"
IMAGE_FILEPATH = r"../upload/lian.jpg"

# 可选的请求参数
# top_num: 返回的分类数量，只需要一个结果所以就是1
PARAMS = {"baike_num": 5}

# 服务详情 中的 接口地址
MODEL_API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom_bml/v1/classification/yezimoxing"

# 这个不用管，别改就行
# 调用 API 需要 ACCESS_TOKEN。若已有 ACCESS_TOKEN 则于下方填入该字符串
# 否则，留空 ACCESS_TOKEN，于下方填入 该模型部署的 API_KEY 以及 SECRET_KEY，会自动申请并显示新 ACCESS_TOKEN
ACCESS_TOKEN = "24.737bbe3df34af25ece4a96bc7b1dccd6.2592000.1685615817.282335-33078001"
API_KEY = "Y4v0F2afBtNVW1X7BqSsqCPK"
SECRET_KEY = "BAujPIBVsWvs1rAfKt5vLpKfRqz33wvM"


print("1. 读取目标图片 '{}'".format(IMAGE_FILEPATH))
with open(IMAGE_FILEPATH, 'rb') as f:
    base64_data = base64.b64encode(f.read())
    base64_str = base64_data.decode('UTF-8')
print("将 BASE64 编码后图片的字符串填入 PARAMS 的 'image' 字段")
PARAMS["image"] = base64_str


if not ACCESS_TOKEN:
    print("2. ACCESS_TOKEN 为空，调用鉴权接口获取TOKEN")
    auth_url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials"\
               "&client_id={}&client_secret={}".format(API_KEY, SECRET_KEY)
    auth_resp = requests.get(auth_url)
    auth_resp_json = auth_resp.json()
    ACCESS_TOKEN = auth_resp_json["access_token"]
    print("新 ACCESS_TOKEN: {}".format(ACCESS_TOKEN))
else:
    print("2. 使用已有 ACCESS_TOKEN")


print("3. 向模型接口 'MODEL_API_URL' 发送请求")
request_url = "{}?access_token={}".format(MODEL_API_URL, ACCESS_TOKEN)
response = requests.post(url=request_url, data=json.dumps(PARAMS), headers={'content-type': 'application/x-www-form-urlencoded'})
response_json = response.json()
# print(response_json.get('name'))
response_str = json.dumps(response_json, indent=4, ensure_ascii=False)
# pprint.pprint(response_str)
print(response_json)
print("结果:{}".format(response_str.split(",")[1]))
raw_str = response_str.split(',')[1]
print(raw_str)
# ('{\n'
#  '    "log_id": 4480013629347031227,\n'
#  '    "results": [\n'
#  '        {\n'
#  '            "name": "番茄叶斑病",\n'
#  '            "score": 0.8320052623748779\n'
#  '        }\n'
#  '    ]\n'
#  '}')
