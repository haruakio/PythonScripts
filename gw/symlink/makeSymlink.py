# -*- coding: utf-8 -*-

import os
import argparse

parser = argparse.ArgumentParser(description='Output mklink commands for Windows batch file. Originally created for making symlink for PC Product model.')
parser.add_argument('sourceDir')
parser.add_argument('targetDir')
args = parser.parse_args()
print(args)

def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        # yield root
        for file in files:
            yield os.path.join(root, file)

def findCommonPath(wordA, wordB):
    i = 0
    text = ''
    listA = wordA.split('\\')
    listB = wordB.split('\\')
    for a in listA:
        #print(wordB[i])
        if a == listB[i]:
            text = text + a + os.path.sep
        else:
            diffA = listA[i]
            diffB = listB[i]
            break
        i += 1

    return [text, diffA, diffB]

def replacePath(file, commonPath):
    relative = os.path.abspath(file).replace(commonPath, '')
    dirs = relative.split(os.path.sep)
    text = ''
    dirs.pop(0)
    for n in dirs:
        text = text + '..' + os.path.sep
    return text + relative

[cPath, diffA, diffB] = findCommonPath(args.sourceDir,args.targetDir)
print("common path is %s, diffA is %s, diffB is %s" % (cPath, diffA, diffB))
for file in find_all_files(args.sourceDir):
    # Comment out if you want to make directory
    os.makedirs(os.path.dirname(file).replace(cPath + diffA, cPath + diffB), exist_ok=True)
    print('cd '+ os.path.dirname(file).replace(cPath + diffA, cPath + diffB))
    # print('del /F ' + os.path.basename(file))
    rPath =replacePath(file, cPath)
    print('mklink ' + os.path.basename(file) + ' ' + rPath)
    # print('p4 edit -t symlink '+os.path.basename(file))