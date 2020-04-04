import source
import source2
import source2_2
import xml.etree.ElementTree
import os
import sys


def main():
    os.chdir(sys.path[0])
    conf = xml.etree.ElementTree.parse("resources/conf.xml")
    state = conf.findtext("program")
    if state == "0":
        source.main()
    elif state == "1":
        source2.main()
    elif state == "2":
        source2_2.main()


if __name__ == "__main__":
    main()
