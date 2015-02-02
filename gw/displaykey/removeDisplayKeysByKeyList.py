# -*- coding: utf-8 -*-

#import os
import argparse
import codecs
import re

parser = argparse.ArgumentParser(description='Remove display keys in the list from display.properties file. Mostly used when you try to apply old langualge module to newer app version.')
parser.add_argument('display')
parser.add_argument('list')
args = parser.parse_args()
print(args)

f=codecs.open(args.display,'r','utf8')
listFile=open(args.list, 'r')
removeKeys = set()
for w in listFile.readlines():
    removeKeys.add(w.rstrip())
listFile.close()

outFile = codecs.open(args.display + '.new', 'w', 'utf8')

reg = re.compile("=.*\n")
for i in f.readlines():
    line = re.sub(reg,'',i)
    if line in removeKeys:
        print("Remove : ", i.rstrip())
    else:
        outFile.write(i.rstrip()+"\n")
f.close()