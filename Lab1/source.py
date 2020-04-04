import xml.etree.ElementTree
from urllib.request import urlopen
import collections
import datetime
import os
import sys

map = collections.Counter()


def func(str):

    index = 0
    for iter in list(map):
        while True:
            index = str.find(iter, index + 1)
            if index != -1:
                map[iter] += 1
            else:
                break
        index = 0


def outXml():
    root = xml.etree.ElementTree.Element("names")
    root2 = xml.etree.ElementTree.Element("names")
    for iter in list(map):
        loc = xml.etree.ElementTree.SubElement(root, "location")
        loc.text = iter
        subLoc = xml.etree.ElementTree.SubElement(loc, "count")
        subLoc.text = str(map[iter])
        if map[iter] != 0:
            loc2 = xml.etree.ElementTree.SubElement(root2, "location")
            loc2.text = iter
            subLoc2 = xml.etree.ElementTree.SubElement(loc2, "count")
            subLoc2.text = str(map[iter])

    STR = xml.etree.ElementTree.tostring(root, "utf-8")
    document = '<?xml version="1.0" encoding="UTF-8"?>' + STR.decode("utf-8")
    out = open("out/out.xml", "w")
    out.write(document)

    STR = xml.etree.ElementTree.tostring(root2, "utf-8")
    document = '<?xml version="1.0" encoding="UTF-8"?>' + STR.decode("utf-8")
    out2 = open("out/outWithoutZero.xml", "w")
    out2.write(document)


def main():
    os.chdir(sys.path[0])
    file = open("resources/list.txt")
    for line in file:
        line = line.replace("\n", "")
        map[line] = 0

    urlL = xml.etree.ElementTree.parse("resources/rssUrl.xml")
    urlLRoot = urlL.getroot()

    start = datetime.datetime.now()
    for iter in list(urlLRoot):
        rssF = urlopen(iter.text)
        rssXml = xml.etree.ElementTree.parse(rssF)
        for i in rssXml.iterfind("channel/item"):
            title = i.findtext('title')
            if not isinstance(title, type(None)):
                title = title.upper()
                func(title)
            fulltext = i.findtext('fulltext')
            if not isinstance(fulltext, type(None)):
                fulltext = fulltext.upper()
                func(fulltext)
            descr = i.findtext('description')
            if not isinstance(descr, type(None)):
                descr = descr.upper()
                func(descr)

    print(datetime.datetime.now() - start)
    outXml()
