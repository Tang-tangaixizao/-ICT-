### 图标数据处理
import os
import re
import random
import datetime


def find_data(now_time):
    dataSet = []
    with open("F:/py_code/django/tangjiacang\school/fourm/zhenshuju.txt", "r") as f:  # 打开文件
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

text=get_all_data(2)
print(text)