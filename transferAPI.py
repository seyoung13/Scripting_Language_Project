# -*- coding: utf-8 -*-
from xml.dom.minidom import *
import urllib
import http.client
from xml.etree import ElementTree

# 대중교통 환승정보 서비스 API
connection = http.client.HTTPConnection('ws.bus.go.kr')
# 인증키
key = '8zvGJaRxZX2%2Fr%2BWKMJ5jvbJstf1HYfg3vKs%2FTZaSBSXcJkPVoz7b1i4f4Dut5B8cZePVHygCmITymwMx2VeW0w%3D%3D'
# 환승정보 api의 url
get_location_url = '/api/rest/pathinfo/getLocationInfo?ServiceKey='
get_path_bus_url = '/api/rest/pathinfo/getPathInfoByBus?ServiceKey='
get_path_sub_url = '/api/rest/pathinfo/getPathInfoBySubway?ServiceKey='
get_path_bus_N_sub_url = '/api/rest/pathinfo/getPathInfoByBusNSub?serviceKey='


def search_location(keyword_string):
    # 사용자가 입력한 문자열을 받아와서 api에 넘겨줌
    global key, get_location_url, connection
    location_name = urllib.parse.quote(keyword_string)
    connection.request('GET', get_location_url+key+'&stSrch='+location_name)
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


def search_path_info_bus(x1, y1, x2, y2):
    global key, get_path_bus_N_sub_url, connection
    connection.request('GET', get_path_bus_url+key+'&startX='+str(x1)+'&startY='+str(y1)+'&endX='+str(x2)+'&endY='+str(y2))
    req = connection.getresponse()
    xml = req.read().decode('utf-8')

    path = get_path(xml)
    return path


def search_path_info_sub(x1, y1, x2, y2):
    global key, get_path_bus_N_sub_url, connection
    connection.request('GET', get_path_sub_url+key+'&startX='+str(x1)+'&startY='+str(y1)+'&endX='+str(x2)+'&endY='+str(y2))
    req = connection.getresponse()
    xml = req.read().decode('utf-8')

    path = get_path(xml)
    return path


def search_path_info_bus_N_sub(x1, y1, x2, y2):
    global key, get_path_bus_N_sub_url, connection
    connection.request('GET', get_path_bus_N_sub_url+key+'&startX='+str(x1)+'&startY='+str(y1)+'&endX='+str(x2)+'&endY='+str(y2))
    req = connection.getresponse()
    xml = req.read().decode('utf-8')

    path = get_path(xml)
    return path


def get_path(api_xml):
    # 입력받은 출발지 ~ 목적지 사이의 경로 리스트 반환
    tree = ElementTree.fromstring(api_xml)

    items = tree.iter('itemList')
    fname, fx, fy, tname, tx, ty, route = [], [], [], [], [], [], []
    time = []

    j = 0
    for i in items:
        path_list = i.iter('pathList')
        fname.append([]), fx.append([]), fy.append([]), tname.append([]), tx.append([]), ty.append([]), route.append([])
        for p in path_list:
            fname[j].append(p.find('fname').text)
            fx[j].append(p.find('fx').text)
            fy[j].append(p.find('fy').text)
            tname[j].append(p.find('tname').text)
            tx[j].append(p.find('tx').text)
            ty[j].append(p.find('ty').text)
            route[j].append(p.find('routeNm').text)
        time.append(i.find('time').text)
        j += 1

    return fname, fx, fy, tname, tx, ty, route, time


'''
a1, b1 = 126.7813931846, 37.483320789
a2, b2 = 126.8131640173, 37.4847018435

f, t, r, time = search_path_info_bus(a1, b1, a2, b2)

print(f)
print(t)
print(r)
print(time)
'''
