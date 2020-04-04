import xml.etree.ElementTree
from urllib.request import urlopen
import collections
import gevent
import datetime


def func(str, map):

    index = 0
    for iter in list(map):
        while True:
            index = str.find(iter, index + 1)
            if index != -1:
                map[iter] += 1
            else:
                break
        index = 0


def outXml(map):
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
            subLoc2.text = str(map[iter] * (-1))

    STR = xml.etree.ElementTree.tostring(root, "utf-8")
    document = '<?xml version="1.0" encoding="UTF-8"?>' + STR.decode("utf-8")
    out = open("/home/liffert/Prog/NoRepo/out.xml", "w")
    out.write(document)

    STR = xml.etree.ElementTree.tostring(root2, "utf-8")
    document = '<?xml version="1.0" encoding="UTF-8"?>' + STR.decode("utf-8")
    out2 = open("/home/liffert/Prog/NoRepo/outWithoutZero.xml", "w")
    out2.write(document)


def mythread(rssXml, map):
    for i in rssXml.iterfind("channel/item"):
        title = i.findtext('title')
        if not isinstance(title, type(None)):
            title = title.upper()
            func(title, map)
        fulltext = i.findtext('fulltext')
        if not isinstance(fulltext, type(None)):
            fulltext = fulltext.upper()
            func(fulltext, map)
        descr = i.findtext('description')
        if not isinstance(descr, type(None)):
            descr = descr.upper()
            func(descr, map)


def main():
    ListMap = []
    urlL = xml.etree.ElementTree.parse("/home/liffert/Prog/NoRepo/rssUrl.xml")
    urlLRoot = urlL.getroot()

    file = open("/home/liffert/Prog/NoRepo/list.txt")
    for iter in range(len(list(urlLRoot))):
        ListMap.append(collections.Counter())
        for line in file:
            line = line.replace("\n", "")
            ListMap[iter][line] = 0
        file = open("/home/liffert/Prog/NoRepo/list.txt")

    threads = []
    start = datetime.datetime.now()
    counter = 0
    for iter in list(urlLRoot):
        rssF = urlopen(iter.text)
        rssXml = xml.etree.ElementTree.parse(rssF)
        threads.append(gevent.spawn(mythread, rssXml, ListMap[counter]))
    gevent.joinall(threads)
    print(datetime.datetime.now() - start)
    OutMap = collections.Counter()
    for iter in ListMap:
        OutMap.subtract(iter)
    outXml(OutMap)


if __name__ == "__main__":
    main()
