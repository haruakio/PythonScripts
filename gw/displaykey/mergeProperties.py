# -*- coding: utf-8 -*-

import argparse
import re
import codecs

parser = argparse.ArgumentParser(description='Merge two properties files(e.g. display.properties). If the same key exists the second file content will win.')
parser.add_argument('baseFile')
parser.add_argument('newFile')
args = parser.parse_args()
print(args)

def readFileToMap(file, dic=None):
    if dic is None:
        properties = dict()
    else:
        properties = dic

    for line in codecs.open(file, 'r', 'utf8'):
        arr = re.compile(r' ?= ?').split(line)

        if len(arr) != 2:
            continue
        if arr[0] in properties and properties[arr[0]].rstrip() != arr[1].rstrip():
            print('Duplicate key %s, old=%s new=%s' % (arr[0], properties[arr[0]], arr[1]))
        properties[arr[0]] = arr[1]
    return properties

def printMap(dic):
    print('--------------------START-----------------')
    for k, v in sorted(dic.items()):
        print(k + ' = ' + v.rstrip())

d = readFileToMap(args.baseFile)
printMap(readFileToMap(args.newFile, d))