# -*- coding: utf-8 -*-
from xml.dom.minidom import *
import urllib
import http.client
from xml.etree import ElementTree

# 지하철 정보 서비스 API
connection = http.client.HTTPConnection('openapi.tago.go.kr')
# 인증키
key = '8zvGJaRxZX2%2Fr%2BWKMJ5jvbJstf1HYfg3vKs%2FTZaSBSXcJkPVoz7b1i4f4Dut5B8cZePVHygCmITymwMx2VeW0w%3D%3D'
# url
get_station_id_url = '/openapi/service/SubwayInfoService/getKwrdFndSubwaySttnList?serviceKey='
get_station_timetable_url = '/openapi/service/SubwayInfoService/getSubwaySttnAcctoSchdulList?serviceKey='


def get_station_info(keyword_string):
    global key, get_station_id_url, connection
    station_name = urllib.parse.quote(keyword_string)
    connection.request('GET', get_station_id_url + key + '&subwayStationName=' + station_name)
    req = connection.getresponse()
    xml = req.read().decode('utf-8')

    tree = ElementTree.fromstring(xml)

    items = tree.iter('item')
    route, name, station_id  = [], [], []

    for i in items:
        route.append(i.find('subwayRouteName').text)
        name.append(i.find('subwayStationName').text)
        station_id.append(i.find('subwayStationId').text)

    return route, name, station_id


def get_up_line_timetable(station_id):
    global key, get_station_id_url, connection
    station_id = urllib.parse.quote(station_id)
    connection.request('GET', get_station_timetable_url + key + '&subwayStationId=' + station_id
                       + '&dailyTypeCode=01&upDownTypeCode=U')
    req = connection.getresponse()
    xml = req.read().decode('utf-8')

    tree = ElementTree.fromstring(xml)

    items = tree.iter('item')
    departure_time, end_station_name = [], []

    for i in items:
        departure_time.append(i.find('depTime').text)
        end_station_name.append(i.find('endSubwayStationNm').text)

    return departure_time, end_station_name


def get_down_line_timetable(station_id):
    global key, get_station_id_url, connection
    station_id = urllib.parse.quote(station_id)
    connection.request('GET', get_station_timetable_url + key + '&subwayStationId=' + station_id
                       + '&dailyTypeCode=01&upDownTypeCode=D')
    req = connection.getresponse()
    xml = req.read().decode('utf-8')

    tree = ElementTree.fromstring(xml)

    items = tree.iter('item')
    departure_time, end_station_name = [], []

    for i in items:
        departure_time.append(i.find('depTime').text)
        end_station_name.append(i.find('endSubwayStationNm').text)

    return departure_time, end_station_name


'''r,n,i = get_station_id('서울')
print(r,n,i)

d, e = get_up_line_timetable('SUB133', '서울 1호선')
print(e[0]+'행 열차 ' + d[0][0]+d[0][1]+'시'+d[0][2]+d[0][3]+'분'+ ' 출발')'''

import spam
lst =[0]
arr = spam.sort_by_transfer_time(lst)
print(arr)
