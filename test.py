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


