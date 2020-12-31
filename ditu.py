'''调用百度地图API，批量输入地址查询坐标经纬度
'''
 
import pandas as pd
import json
import requests
# kehu.xlsx是存放地址信息的表格文件
data = pd.read_excel("kehu.xlsx")
 
 
from urllib.request import urlopen
from urllib.parse import quote
import requests
 
 
def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoding/v3'
    output = 'json'
    ak = 'cGsZKyqIcrGnE4pwlzGRwQeISKjnG6Gh'
    address = quote(address)
    uri = url + '?' + 'address=' + address + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode()
    temp = json.loads(res)
    lat = temp["result"]["location"]["lat"]
    lng = temp["result"]["location"]["lng"]
    return lat, lng
'''
{"status":"1","info":"OK","infocode":"10000","count":"1","geocodes":[{"formatted_address":"北京市朝阳区阜通东大街|6号","country":"中国","province":"北京市","citycode":"010","city":"北京市","district":"朝阳区","township":[],"neighborhood":{"name":[],"type":[]},"building":{"name":[],"type":[]},"adcode":"110105","street":"阜通东大街","number":"6号","location":"116.483038,39.990633","level":"门牌号"}]}
'''
 
for indexs in data.index:
    location = data.loc[indexs, "公司地址"] #公司地址是存放地址信息的列第一行内的文字
    print(indexs)
    print(location)
    get_location = getlnglat(location)
    get_lat = get_location[0]
    get_lng = get_location[1]
    data.loc[indexs, "经度"] = get_lng+0.0125
    data.loc[indexs, "纬度"] = get_lat+0.0077
    print(get_lat, get_lng)
 
data.to_excel("kehu1.xlsx", sheet_name='sheet1') #保存经纬度信息到新的excl表格
 
data_html = pd.DataFrame(columns=["location", "address"])
# 批量处理经纬度信息，生成html代码
for indexs in data.index:
    data_html.loc[indexs, "location"] = "new BMap.Point(" + str(data.loc[indexs, "经度"]) + "," + str(
        data.loc[indexs, "纬度"]) + "),"
    data_html.loc[indexs, "address"] = "'" + data.loc[indexs, "公司名称"] + "',"
 
data_html.to_csv("kehu_location.csv", encoding="gbk") #导出合成html代码到excel表格内
 
print(data_html)