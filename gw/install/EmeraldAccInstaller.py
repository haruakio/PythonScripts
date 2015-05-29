# -*- coding: utf-8 -*-

import os
import argparse
import zipfile
import codecs
import re
import urllib.request
from logging import getLogger,StreamHandler,DEBUG,INFO
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(INFO)
logger.addHandler(handler)

parser = argparse.ArgumentParser(description='Unzip accelerator zip file to targetDir. Merge *.properties file. TargetDir must be root dir contains modules folder.')
parser.add_argument('-i', '--input', required=True, help=r'zip file path or build url. e.g.) -i c:\tmp\base-module.zip or -i http://thfiles/builds/PC/8.0/8.0.3.270_20150527.0303_618017/')
parser.add_argument('-m', '--modules', help='Required if input is url. Multiple modules should be comma separated without space e.g.) base,gl')
parser.add_argument('-o', '--out', required=True, help=r'output directory c:\tmp\pc803')
args = parser.parse_args()
print(args)


# Make zip url from build url http://thfiles/builds/PC/8.0/8.0.3.270_20150527.0303_618017/
def makeZipURLFromBuild(url, module):
    jrdc = '/jrdc/'
    if url.endswith('/'):
        jrdc = 'jrdc/'
    return  url + jrdc + module + '-module.zip'

def downloadFromWeb(url):
    logger.info('download file: '+ url)
    local_filename, headers =urllib.request.urlretrieve(url)
    return local_filename

def readFileToMap(file, dic=None):
    if dic is None:
        properties = dict()
    else:
        properties = dic

    for line in codecs.open(file, 'r', 'utf8'):
        arr = re.compile(r' ?= ?').split(line, maxsplit=1)

        if len(arr) != 2:
            logger.warn('Cannot parse the line: '+ line)
            continue
        if arr[0] in properties and properties[arr[0]].rstrip() != arr[1].rstrip():
            logger.info('Duplicate key %s, old=%s new=%s' % (arr[0], properties[arr[0]], arr[1]))
        properties[arr[0]] = arr[1]
    return properties

def readLinesToMap(chunk, dic=None):
    if dic is None:
        properties = dict()
    else:
        properties = dic

    for line in chunk.splitlines():
        arr = re.compile(r' ?= ?').split(line, maxsplit=1)

        if len(arr) != 2:
            logger.warn('Cannot parse the line: '+ line)
            continue
        if arr[0] in properties and properties[arr[0]].rstrip() != arr[1].rstrip():
            logger.info('Duplicate key %s, old=%s new=%s' % (arr[0], properties[arr[0]], arr[1]))
        properties[arr[0]] = arr[1]
    return properties

def writeMap(file, dic):
    logger.info('dic count is %d' % len(dic))
    for k, v in sorted(dic.items()):
        file.write(bytes(k + ' = ' + v.rstrip() + os.linesep, 'utf8'))

def unzip(zip_filename):
    zip_file = zipfile.ZipFile(zip_filename, "r")
    for filename in zip_file.namelist():
        if not os.path.basename(filename):
            logger.debug('makedir '+ filename)
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
target = os.path.join(args.out, configuration)
if args.input.startswith('http'):
    if args.modules is None:
        exit('modules parameter is required for url')
    modules = args.modules.split(',')
    for module in modules:
        #make each url then download zip
        zipPath = downloadFromWeb(makeZipURLFromBuild(args.input, module))
        logger.info('Temp file save at ' + zipPath)
        unzip(zipPath)
        logger.info('Remove temp file : '+ zipPath)
        os.remove(zipPath)
else:
    unzip(args.input)
