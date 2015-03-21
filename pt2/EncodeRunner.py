# -*- coding: utf-8 -*-

import subprocess
import argparse
import os
from pt2.RemoveDuplicates import removeDuplicates

def runSplitter(path):
    cmd = "TsSplitter.exe"
    option = "-EIT -ECM -EMM -SD -1SEG -OUT tmp -SEP -SEPA " + path
    ret  =  subprocess.check_output( [cmd, option] )
    return ret

def checkBSChannels(path):
    BSChannels = ["ＷＯＷＯＷ", "スターチャンネル"]
    for channel in BSChannels:
        if channel in path:
            return True
    return False

def callHandBrake(path):
    cmd = "hb_matome.bat"
    option = ""
    ret  =  subprocess.check_output( [cmd, option] )
    return ret


### Main ###
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Encode TS file to MP4. Change behavior depending on channel name in filename then move to directory.')
    parser.add_argument('TSFile')
    parser.add_argument('targetDir')
    args = parser.parse_args()
    print(args)


    filePath = args.TSFile

    # If channel requires split, call splitter
    if checkBSChannels(filePath):
        runSplitter(filePath)
        filePath = removeDuplicates(os.path.dirname(filePath), os.path.basename(filePath))

    # Call handbrake
    callHandBrake(filePath)
