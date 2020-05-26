# -*- coding: utf-8 -*-
from xml.dom.minidom import *
import urllib
import http.client
from xml.etree import ElementTree


def extraxt_data(str_xml):
    tree = ElementTree.fromstring(str_xml)

    items = tree.iter('itemList')
    name = []
    x, y = [], []

    for i in items:
        name.append(i.find('poiNm').text)
        x.append(eval(i.find('gpsX').text)), y.append(eval(i.find('gpsY').text))

    return name, x, y


key = '8zvGJaRxZX2%2Fr%2BWKMJ5jvbJstf1HYfg3vKs%2FTZaSBSXcJkPVoz7b1i4f4Dut5B8cZePVHygCmITymwMx2VeW0w%3D%3D'
url = '/api/rest/pathinfo/getLocationInfo?ServiceKey='+key+'&stSrch=%서울'

connection = http.client.HTTPConnection('ws.bus.go.kr')
korean = urllib.parse.quote("서울")
connection.request('GET', '/api/rest/pathinfo/getLocationInfo?serviceKey=8zvGJaRxZX2%2Fr%2BWKMJ5jvbJstf1HYfg3vKs%2FTZaSBSXcJkPVoz7b1i4f4Dut5B8cZePVHygCmITymwMx2VeW0w%3D%3D&stSrch='+korean)

req = connection.getresponse()
data = req.read().decode('utf-8')

n, x, y = extraxt_data(data)

print(n)
print(x)
print(y)
