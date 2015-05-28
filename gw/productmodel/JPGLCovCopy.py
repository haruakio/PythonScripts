# -*- coding: utf-8 -*-

import fileinput
import argparse
import re
import os
import codecs
from logging import getLogger,StreamHandler,DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

parser = argparse.ArgumentParser(description='Merge two properties files(e.g. display.properties). If the same key exists the second file content will win.')
parser.add_argument('baseFile')
args = parser.parse_args()
print(args)

# Change here
original = "JPGLFL"
prefix = "JPGLEVL"
covTerm = "PD"
localizationPath = r'C:\eng\emerald\pc\rdc\jp\stable\app-pc\pc-gl-JP\config\locale'


wordLen = len(prefix + covTerm)
logger.debug("wordLen is %i" % wordLen)
regex = 'public-id="z\w{'+ str(wordLen -1) + '}'
covOpt = '<CovTermOptCode>\w{'+ str(wordLen)+'}'
logger.debug("regex = "+ regex)

newFileName = args.baseFile.replace(original, prefix)
newFile = open(newFileName, mode='w')
for line in fileinput.input():
    newLine = line.replace(original, prefix)
    newLine = re.sub(regex, 'public-id="'+ prefix + covTerm, newLine)
    newLine = re.sub(covOpt, '<CovTermOptCode>'+prefix + covTerm, newLine)
    newFile.write(newLine)

lookupName = args.baseFile.replace('.xml', '-lookups.xml')
newLookupName = lookupName.replace(original, prefix)
newLookupFile = open(newLookupName, mode='w')

for line in fileinput.input(lookupName):
    newLine = line.replace(original, prefix)
    newLine = re.sub(regex, 'public-id="'+ prefix + covTerm, newLine)
    newLine = re.sub(covOpt, '<CovTermOptCode>'+prefix + covTerm, newLine)
    newLookupFile.write(newLine)

covTermOpt = 'CovTermOpt_\w{'+ str(wordLen)+'}'
enPath = os.path.join(localizationPath,'en_US','productmodel.display.properties')
jaPath = os.path.join(localizationPath,'ja','productmodel.display.properties')

def uniq(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

def addProdModelProperties(path) :
    lines = codecs.open(path, 'r', 'utf8').readlines()
    newKeys = []
    for line in lines:
        if line.startswith('PolicyLine_JPGLLine.CoveragePattern_' + original + covTerm):
            newLine = line.replace(original, prefix,2)
            newLine = re.sub(covTermOpt, 'CovTermOpt_'+ prefix + covTerm, newLine)
            lines.append(newLine)
    lines_uniq = list(set(lines))
    lines_uniq.sort()
    keyFile = codecs.open(path,'w', 'utf8')
    keyFile.writelines(lines_uniq)

addProdModelProperties(enPath)
addProdModelProperties(jaPath)
