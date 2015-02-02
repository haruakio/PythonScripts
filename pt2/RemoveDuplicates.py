import glob
import os
import argparse

parser = argparse.ArgumentParser(description='Remove all files except the biggest, then rename it for PT2 output')
parser.add_argument('path')
parser.add_argument('filename')
args = parser.parse_args()
print(args)

def listFiles(path, matchStr):
    return glob.glob(path + os.sep + matchStr + '*.*')

def maxSizeFile(files):
    return max(files, key=os.path.getsize)

def removeFiles(files):
    for file in files:
        print('Remove %s' % file)
        os.remove(file)

def renameToTitleOnly(path, ext='.ts'):
    name = os.path.basename(path)
    words = name.split('_')
    os.rename( path, os.path.dirname(path)+os.sep+words[1]+ext)

files = listFiles(args.path, args.filename)
maxFile = maxSizeFile(files)
files.remove(maxFile)
removeFiles(files)
renameToTitleOnly(maxFile)