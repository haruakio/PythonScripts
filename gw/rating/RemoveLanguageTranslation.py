# -*- coding: utf-8 -*-
import codecs

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import argparse



### Main ###
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove all files except the biggest, then rename it for PT2 output')
    parser.add_argument('path')
    args = parser.parse_args()
    print(args)

    file = codecs.open(args.path,'r','utf8')

    glob = file.read()
    glob.sub('<.*_L10N .*</.*_L10N>')
    soup = BeautifulSoup(file, "xml")
    # for child in soup.children:
        # print(child)
    for lang in soup.find_all("language"):
        # print(lang.text)
        if not ('en_US' in lang.text):
            # print (lang.parent)
            lang.parent.decompose()

    print(soup.prettify())
    # tree = ET.parse(args.path)
    # root = tree._root
    # for node in root.findall('.//{http://guidewire.com/pc/exim/import}Language'):
    #     if 'fr' in node.text or 'ja_JP' in node.text:
    #         l10n = node.find('..')
    #         print(l10n)
    #         parent = l10n.find('..')
    #
    #         print(parent)
    #         parent.remove(l10n)

    # for node in tree.iter():
    #     # print(node.tag)
    #     for child in node.iter():
    #         if "_L10N" in child.tag:
    #             lang = child.find('{http://guidewire.com/pc/exim/import}Language')
    #             if lang is not None and 'fr' in lang.text :
    #                 print(lang)
    #                 print(lang.text)
    #                 node.remove(child)
        # if "_L10N" in node.tag :
        #     lang = node.find('{http://guidewire.com/pc/exim/import}Language')
        #     print(node.tag)
        #     if lang is not None and 'fr' in lang.text :
        #         print(lang)
        #         print(lang.text)
        #         node.clear()

    # tree.write(r"c:\tmp\xmlout.txt", default_namespace=False)