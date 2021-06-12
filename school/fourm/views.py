from django.shortcuts import render
from django.core.paginator import Paginator
#from login.models import person
from django.shortcuts import render
from django.shortcuts import redirect
# from django.shortcuts import reverse
from django.conf import settings
#from . import models
from django.http import HttpResponse ,HttpResponseRedirect
from django.shortcuts import redirect
import re
import json
import requests
import random
import datetime
import cv2
# import urllib2
import time
import urllib.request
import numpy as np
import sys
import requests

from django.template import Template, Context, RequestContext

# Create your views here.

import re
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig
from huaweicloudsdkiotda.v5 import *


def single(request):
    return render(request,'single.html')



#参数pIndex表示：当前要显示的页码
def page_test(request):

    message = find_device_message()
    message_out = dis_str(message)
    humidity = message_out[2]
    temperature = message_out[8]
    battery = message_out[6]
    get_value = get_all_data(datetime.datetime.now().hour)
    ai_str = second_ai(datetime.datetime.now().hour)

    return render(request, 'fourm.html',{ 'humidity': humidity ,'temperature': temperature,'battery':  battery, 'time': get_value[0], 'wendu':get_value[1],'shidu':get_value[2], 'renshu':get_value[3], 'ai_str0':ai_str[0],'ai_str1':ai_str[1],'ai_str2':ai_str[2],'ai_str3':ai_str[3],'ai_str4':ai_str[4],'ai_str5':ai_str[5]})

def post_meaage(request):


    dire = request.GET.get('dire',None)
    #print("the value" + dire) #得到按键值

    if (int(dire) == 1): #前进
        command = "shebei"
        arg =  int(1)
        print("发送ing")
        post_huawei_message(command, arg)
    if (int(dire) == 2):  # 后退
        command = "shebei"
        arg = int(0)
        post_huawei_message(command, arg)
    if (int(dire) == 3):  # 左
        command = "shebei2"
        arg = int(1)
        post_huawei_message(command, arg)
    if (int(dire) == 4):  # 右
        command = "shebei2"
        arg = int(0)
        post_huawei_message(command, arg)
    if (int(dire) == 5):  # 开灯
        command = "shebei3"
        arg = int(1)
        post_huawei_message(command, arg)
    if (int(dire) == 6):  # 关灯
        command = "shebei3"
        arg = int(0)
        post_huawei_message(command, arg)
    if (int(dire) == 7):  # 开灯
            command = "shebei4"
            arg = int(1)
            post_huawei_message(command, arg)
    if (int(dire) == 8):  # 关灯
        command = "shebei4"
        arg = int(0)
        post_huawei_message(command, arg)

    #command = request.GET.get('command', None)
    #arg = request.GET.get('arg', None)

    #post_huawei_message(command, arg)
    message = find_device_message()
    message_out = dis_str(message)
    humidity = message_out[2]
    temperature = message_out[8]
    battery = message_out[6]

    return render(request, 'direction.html', {'humidity': humidity, 'temperature': temperature, 'battery': battery,  })



###  huawei


### 查询所有信息
def find_device_message():
    ak = "4MSDTDVTPSTEDCYFDXOS"
    sk = "kLluTIa57HabASGp4bxrfytKUwCSWbbYlCLHoYm1"
    endpoint = "https://iotda.cn-north-4.myhuaweicloud.com"
    project_id = "08d0cfa57b80f5d32f54c019654ee2eb"

    config = HttpConfig.get_default_config()
    config.timeout = 3

    credentials = BasicCredentials(ak, sk, project_id)

    client = IoTDAClient.new_builder(IoTDAClient) \
        .with_http_config(config) \
        .with_credentials(credentials) \
        .with_endpoint(endpoint) \
        .build()
    print("start build ")

    try:
        request = ShowDeviceShadowRequest()
        request.device_id = "5f26687704feea02bac7dd35_11111111"
        response = client.show_device_shadow(request)
        print("ok\n")
        print(response)

        return(str(response))

    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print("************")
        print(e.request_id)
        print("************")
        print(e.error_code)
        print("************")
        print(e.error_msg)

### 如果都有引号,就都能返回
def dis_str(content):
    str = re.findall(r"(\n[\s\S]*\n)", content, re.DOTALL)
    # str1=re.findall(r"\n([\s\S]*)\n",str[0])
    str1 = str[0].replace('\n', '')
    str2 = str1.replace(' ', '')
    str3 = re.findall(r"'properties':{(.+?)}},", str2)

    str4 = re.findall(r"'(.+?)'", str3[0])
    str5 = re.findall(r"'(.+?)'", str3[1])
    str6 = re.findall(r"[0-9][0-9]", str3[1])
    str4.append(str5[0])
    str4.append(str6[0])
    print(str4[3])
    return str4



### 下发参数 可同时传递两个变量
def post_huawei_message(message,name):
    ak = "4MSDTDVTPSTEDCYFDXOS"
    sk = "kLluTIa57HabASGp4bxrfytKUwCSWbbYlCLHoYm1"
    # ak = "G3XGSJU5GJXL7CANHN5W"
    # sk = "sq99MyKLLnqlQ27mDqG7bjNQKrlsS6HhZBBtOPu6"

    endpoint = "https://iotda.cn-north-4.myhuaweicloud.com"
    project_id = "08d0cfa57b80f5d32f54c019654ee2eb"

    config = HttpConfig.get_default_config()
    config.timeout = 3

    credentials = BasicCredentials(ak, sk, project_id)

    client = IoTDAClient.new_builder(IoTDAClient) \
        .with_http_config(config) \
        .with_credentials(credentials) \
        .with_endpoint(endpoint) \
        .build()

    try:
        request = CreateMessageRequest()
        request.device_id = "5f26687704feea02bac7dd35_11111111"
        request.body = DeviceMessageRequest(
            message=message,
            name=name
        )
        response = client.create_message(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)




### 图标数据处理
def find_data(now_time):
    dataSet = []
    with open("E:\\TangJiachang\\tangjiacang\\school\\fourm\\zhenshuju.txt", "r") as f:  # 打开文件
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            num = re.findall('\d+', line)
            #print(num)#时间,温度,湿度,人数
            # 开始编写csv
            time = int(num[0])
            wendu = int(num[1])
            shidu = int(num[2])
            people = int(num[3])
            random_data = [1]
            if(now_time == time):
                dataSet.append(num)
        return dataSet

def get_data(nowtime):
    num = find_data(nowtime)
    num = find_data(nowtime)[random.randint(0,len(num)-1)]
    time = int(num[0])
    wendu = int(num[1])
    shidu = int(num[2])
    people = int(num[3])
    print(time,wendu, shidu, people)
    print(datetime.datetime.now().hour)
    return(time,wendu,shidu,people)
    # if ((time == now_time)&(random.choice(random_data))):
    #     print(wendu,shidu,people)
    #     break;

def get_all_data(now_time):
    time_set = []
    wendu_set = []
    shidu_set = []
    people_set = []

    for i in range(0,7):
        if(now_time-i <1 ):
            now_time = now_time + 24
        time,wendu,shidu,people  = get_data(now_time-i)
        time_set.append(time)
        wendu_set.append(wendu)
        shidu_set.append(shidu)
        people_set.append(people)
        print( time,wendu,shidu,people)
    return(time_set,wendu_set,shidu_set,people_set)

### 人工智能预测
def one_ai():
    url = "https://a076d23d27ec4cf9bab17b3742eae51d.apigw.cn-north-4.huaweicloud.com/v1/infers/afdcac94-2bb5-4d03-b270-27ade46471ae "
    HEADERS = { "Content-Type": "application/json;charset=UTF-8","User-Agent": "API Explorer","X-Auth-Token": "***", }
    FormData = {
        "data": {
            "count": 1,
            "req_data": [
                {
                    "attr_1": "0",
                    "attr_2": "12",
                    "attr_3": "",
                    "attr_4": "39",
                    "attr_5": "13",

                }
            ]
        }
    }
    print(json.dumps(FormData))
    res = requests.post(url=url,data=json.dumps(FormData),headers=HEADERS)
    print(res.text)

def second_ai(now_time):
    if(now_time>23):
        now_time = now_time-2
    time,wendu,shidu,people = get_data(now_time)
    ai_str = []
    ai_str.append(people)
    ai_str.append(wendu)
    ai_str.append(shidu)
    if(people<10):
        ai_str.append("室内人数过两小时后减少,是不是可以关闭使用场所了")
    else:
        ai_str.append("人数会增加,要注意及时规划人员数量,避免病毒交叉传播哦")
    if(wendu<25):
        ai_str.append("未来温度下降,也许可以用监控车关闭空调了")
    else:
        ai_str.append("未来温度升高,可以用监控车打开空调了")
    if(shidu<40):
        ai_str.append("未来室内湿度良好,但是不要警惕呐")
    else:
        ai_str.append("未来室内湿度过高,是不是人员密集了,要及时换气")
    return ai_str