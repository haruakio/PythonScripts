rem @ECHO off
setlocal

SET TS_HD_DIR=F:\PT2_HD_video
SET MP4_DIR=F:\FFmpegOut
SET BAT_DIR=C:\Users\hogawa\PT2

SET CUT_TIME=0
SET SIZE=1920x1080
SET CRF=23.0
SET AUDIO2=
SET ACODEC=copy
SET VPRE=libx264-hq2
SET DELOGO=

:optioncheck
IF NOT "%~x1" == ""        goto optionCheckFinished
IF "%~1" == "-s"           (SET SIZE=%~2 & shift & shift & goto optioncheck)
IF "%~1" == "-2audio"      (SET AUDIO2=-map 0:v -map 0:a:0 -map 0:a:1 & shift & goto optioncheck)
IF "%~1" == "-crf"         (SET CRF=%~2 & shift & shift & goto optioncheck)
IF "%~1" == "-acodec"      (SET ACODEC=%~2 & shift & shift & goto optioncheck)
IF "%~1" == "-vpre"        (SET VPRE=%~2 & shift & shift & goto optioncheck)
IF "%~1" == "-delogo_wowow" (SET DELOGO=true & shift & goto optioncheck)

:optionCheckFinished
IF NOT "%DELOGO%" == "" (
   SET DELOGO=
   IF "%SIZE%" == "1920x1080" SET DELOGO=-vf delogo=1670:55:150:40:4)
   IF "%SIZE%" == "1280x720"  SET DELOGO=-vf delogo=1110:30:110:30:4)
)

:start
IF "%~1" == "" GOTO finish
IF "%~x1" == ".ts"  GOTO encode
IF "%~x1" == ".mp4" GOTO encode
IF "%~x1" == ".mkv" GOTO encode
IF "%~x1" == ".m4v" GOTO encode
IF "%~x1" == ".avi" GOTO encode
IF "%~x1" == ".mpg" GOTO encode
IF "%~x1" == ".mpeg" GOTO encode
goto next

:encode
SET SRC_DIR=%~d1%~p1
SET SRC_EXT=%~x1
SET SRC_FILE="%SRC_DIR%%~n1%SRC_EXT%"
SET SRC_FILE_FIXED="%SRC_DIR%%~n1_fixed%SRC_EXT%"
SET DES_FILE="%MP4_DIR%\%~n1.mp4"
IF "%~x1" == ".ts" (SET DES_FILE="%MP4_DIR%\%~n1 [AAC 2ch %SIZE%].mp4")
SET DES_FILE6="%~n1 [AAC 5.1ch %SIZE%].mp4"
SET AUDIO_STREAM=1
	

FOR /f "usebackq tokens=1" %%i in (`%BAT_DIR%\CountAacStream.bat %SRC_FILE%`) do (set AUDIO_STREAM=%%i)

IF %AUDIO_STREAM% == 2 (SET AUDIO2=-map 0:v -map 0:a:0 -map 0:a:1 & SET DES_FILE="%MP4_DIR%\%~n1[AAC デュアル音声 %SIZE%].mp4")

IF %SRC_FILE% == %DES_FILE% ( echo "エラー: 元ファイルとエンコード後のファイルが同一です" & goto next)

FOR /f "usebackq tokens=1" %%i in (`%BAT_DIR%\SearchAudioChangePoint.bat %SRC_FILE%`) do (set CUT_TIME=%%i)

%BAT_DIR%\ffmpeg  -i %SRC_FILE% %AUDIO2% -preset fast -s %SIZE% -crf %CRF% %DELOGO% -aspect 16:9 -vcodec libx264 -acodec %ACODEC% -absf aac_adtstoasc -deinterlace -ss %CUT_TIME% %DES_FILE%

REM TsRepair.batが動作するのであれば以下の1行(goto rename)は削除する
goto rename

IF not ERRORLEVEL 1 goto rename

call %BAT_DIR%\TsRepair.bat %SRC_FILE%

SET SRC_FILE=%SRC_FILE_FIXED% 

%BAT_DIR%\ffmpeg  -i %SRC_FILE% %AUDIO2% -vpre %VPRE% -s %SIZE% -crf %CRF% %DELOGO% -aspect 16:9 -vcodec libx264 -acodec %ACODEC% -absf aac_adtstoasc -deinterlace -ss %CUT_TIME% %DES_FILE%

:rename

FOR /f "usebackq tokens=1" %%i in (`%BAT_DIR%\GetAudioChannels.bat %DES_FILE%`) do (set CH=%%i)
IF %CH% == 6 (rename %DES_FILE% %DES_FILE6%)

IF EXIST "%SRC_DIR%\done\." move %SRC_FILE% "%SRC_DIR%\done"

:next

SHIFT
GOTO start

:finish
