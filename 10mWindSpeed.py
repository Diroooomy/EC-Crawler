import json
import os
import datetime
import requests

url = 'https://apps.ecmwf.int/webapps/opencharts-api/v1/packages/opencharts/products/medium-10m-probability/axis/valid_time/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.58"
}
data = {
    "base_time": "",
    'threshold': '10',
    "projection": "opencharts_eastern_asia",
    "values": []
}
module_name = 'medium-10m-probability'    #数据名
base_sum = 11   # base_time的数量
valid_sum = 31  # 每个base_time中valid_time的数量
date = datetime.datetime(2020, 11, 5, 00, 00)  # 起始时间

for i in range(base_sum):
    # 选择base_time并转换格式放入字典
    base_time = date - datetime.timedelta(hours=12 * i)
    data['base_time'] = base_time.strftime('%Y%m%d%H%M')
    # 建立文件夹// 可修改
    folder = './' + module_name + '/' + data['base_time']
    if not os.path.exists(folder):  # 判断文件夹是否已经存在
        os.makedirs(folder)
    values = []
    data['values'] = []
    for j in range(valid_sum):
        # 选择valid_time并转换格式放入字典
        valid_time = base_time + datetime.timedelta(hours=12 * j)
        valid_time = valid_time.strftime('%Y%m%d%H%M')
        filename = r"./" + module_name + "/" + data['base_time'] + "/" + valid_time + ".png"
        if not os.path.exists(filename):
            data['values'].append(valid_time)
            values.append(valid_time)
        else:
            print(filename + ' 已存在')
    # 拼接字符串
    data['values'] = ','.join(data['values'])
    res = requests.get(url, params=data, headers=headers)
    print(data['values'])
    # 对json文件求dict
    res = dict(res.json())
    # print (json.dumps(res, sort_keys=True, indent=2))
    res = res['results']
    length = len(values)

    for j in range(length):
        filename = r"./" + module_name + "/" + data['base_time'] + "/" + values[j] + ".png"
        # 获取图片路径
        if values[j] in res:
            img_url = res[values[j]]['url']
            # 获取图片内容
            response = requests.get(img_url).content
        # 保存图片
            with open(filename, 'wb') as f:
                f.write(response)
                print(filename + ' download successfully')
        else:
            print('check the base_time: ' + data['base_time'] + ', valid_time: ' + valid_time + ' exist on the website')

print('Mission Accomplished')