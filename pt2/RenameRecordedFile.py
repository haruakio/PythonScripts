import unicodedata
import os
import argparse
import re

parser = argparse.ArgumentParser(description='Strip unneeded Date, Network, brackets from PT2 file name')
parser.add_argument('file')
args = parser.parse_args()
print(args)

def renameToTitleOnly(path):
    ext = os.path.splitext(path)[1]
    name = os.path.basename(path)
    words = name.split('_')
    if len(words) > 1 :
        str = re.compile(u"【.*】")
        newName = re.sub(str, '',  words[1])
    else:
        newName = words[0]
        ext = ''
    newName = unicodedata.normalize('NFKC',newName)
    os.rename( path, os.path.dirname(path)+os.sep+newName+ext)

renameToTitleOnly(args.file)