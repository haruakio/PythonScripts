# -*- coding: utf-8 -*-

import os
import argparse
import zipfile
import codecs
import re

parser = argparse.ArgumentParser(description='Unzip accelerator zip file to targetDir. Merge *.properties file. TargetDir must be root dir contains modules folder.')
parser.add_argument('zipFile')
parser.add_argument('targetDir')
args = parser.parse_args()
print(args)

configuration = 'modules/configuration'
target = os.path.join(args.targetDir, configuration)

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

def readLinesToMap(chunk, dic=None):
    if dic is None:
        properties = dict()
    else:
        properties = dic

    for line in chunk.splitlines():
        arr = re.compile(r' ?= ?').split(line)

        if len(arr) != 2:
            continue
        if arr[0] in properties and properties[arr[0]].rstrip() != arr[1].rstrip():
            print('Duplicate key %s, old=%s new=%s' % (arr[0], properties[arr[0]], arr[1]))
        properties[arr[0]] = arr[1]
    return properties

def writeMap(file, dic):
    for k, v in sorted(dic.items()):
        file.write(bytes(k + ' = ' + v.rstrip() + os.linesep, 'utf8'))

def unzip(zip_filename):
    zip_file = zipfile.ZipFile(zip_filename, "r")
    for filename in zip_file.namelist():
        if not os.path.basename(filename):
            print('makedir '+ filename)
            path = os.path.join(target,filename)
            if not os.path.exists(path):
                os.mkdir(path)
        else:
            if filename.endswith('.properties'):
                if os.path.isfile( os.path.join(target,filename) ):
                    org_dic = readFileToMap(os.path.join(target,filename))
                    merged_dic = readLinesToMap(zip_file.read(filename).decode('utf8'), org_dic)
                else:
                    merged_dic = readLinesToMap(zip_file.read(filename).decode('utf8'))
                unzip_file = codecs.open(os.path.join(target,filename), "wb")
                writeMap(unzip_file, merged_dic)
            else:
                unzip_file = open(os.path.join(target,filename), "wb")
                unzip_file.write(zip_file.read(filename))

            unzip_file.close()
    zip_file.close()

unzip(args.zipFile)
