# -*- coding: utf-8 -*-

import os
import argparse
import zipfile
import codecs
import re
import urllib.request

parser = argparse.ArgumentParser(description='Unzip accelerator zip file to targetDir. Merge *.properties file. TargetDir must be root dir contains modules folder.')
parser.add_argument('-i', '--input', required=True, help=r'zip file path or build url. e.g.) -i c:\tmp\base-module.zip or -i http://thfiles/builds/PC/8.0/8.0.3.270_20150527.0303_618017/')
parser.add_argument('-m', '--modules', help='Required if input is url. Multiple modules should be comma separated without space e.g.) base,gl')
parser.add_argument('-o', '--out', required=True, help=r'output directory c:\tmp\pc803')
args = parser.parse_args()
print(args)


# Make zip url from build url http://thfiles/builds/PC/8.0/8.0.3.270_20150527.0303_618017/
def makeZipURLFromBuild(url, module):
    return  url + 'jrdc/' + module + '-module.zip'

def downloadFromWeb(url):
    local_filename, headers =urllib.request.urlretrieve(url)
    return local_filename

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

# main
configuration = 'modules/configuration'
modules = args.modules.split(',')
target = os.path.join(args.out, configuration)
if args.input.startswith('http'):
    for module in modules:
        #make each url then download zip
        zipPath = downloadFromWeb(makeZipURLFromBuild(args.input, module))
        print('Temp file save at ' + zipPath)
        unzip(zipPath)
        print('Remove temp file : '+ zipPath)
        os.remove(zipPath)
else:
    unzip(args.zipFile)
