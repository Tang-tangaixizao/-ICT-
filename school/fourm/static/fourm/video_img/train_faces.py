import cv2
# import urllib2
import time
import urllib.request
import numpy as np
import sys
import requests

num=0
while True:
    url = 'http://192.168.113.10:8080/?action=snapshot'
    res = requests.get(url)
    content = res.content
    if num==5:
        num=0
    with open('./fourm/static/fourm/video_img/AAA.jpg', 'wb') as f:
        f.write(content)
        print("保存完成！")
        f.close()
    ## 照片可用
    img1 = cv2.imread('./fourm/static/fourm/video_img/AAA.jpg')
    num += 1
    cv2.imshow('img', img1)
    cv2.waitKey(1)