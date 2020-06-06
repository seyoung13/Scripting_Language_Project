# -*- coding: utf-8 -*-
from xml.dom.minidom import *
import urllib
import http.client
from xml.etree import ElementTree

# 대중교통 환승정보 서비스 API
# 인증키
key = '8zvGJaRxZX2%2Fr%2BWKMJ5jvbJstf1HYfg3vKs%2FTZaSBSXcJkPVoz7b1i4f4Dut5B8cZePVHygCmITymwMx2VeW0w%3D%3D'
# 환승정보 api의 공통 url
url = '/api/rest/pathinfo/getLocationInfo?ServiceKey='
connection = http.client.HTTPConnection('ws.bus.go.kr')


def search_location(keyword_string):
    # 사용자가 입력한 문자열을 받아와서 api에 넘겨줌
    global key, url, connection
    location_name = urllib.parse.quote(keyword_string)
    connection.request('GET', url+key+'&stSrch='+location_name)
    req = connection.getresponse()
    xml = req.read().decode('utf-8')
    # api에서 이름, x좌표, y좌표 리스트를 받은 후 GUI에 넘겨줌
    n, x, y = get_location_info(xml)
    return n, x, y


def get_location_info(api_xml):
    # 사용자가 입력한 문자열을 포함한 장소들의 리스트를 반환
    tree = ElementTree.fromstring(api_xml)

    items = tree.iter('itemList')
    name = []
    gps_x, gps_y = [], []

    for i in items:
        name.append(i.find('poiNm').text)
        gps_x.append(eval(i.find('gpsX').text)), gps_y.append(eval(i.find('gpsY').text))

    return name, gps_x, gps_y


def search_path_info_bus_n_subway(x1, y1, x2, y2):
    global key, url, connection
    connection.request('GET'+url+key+'&startX'+x1+'&startY'+y1+'&endX'+x2+'&endY')
    req = connection.getresponse()
    xml = req.read().decode('utf-8')


def get_path(api_xml):
    # 입력받은 출발지 ~ 목적지 사이의 경로 리스트 반환
    tree = ElementTree.fromstring(api_xml)

    items = tree.iter('itemList')
    name = []