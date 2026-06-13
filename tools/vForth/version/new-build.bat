: copia da directory di lavoro a directory di GitHub

@ECHO OFF

if "%1"=="" goto NO_PARAM

set BUILD=%1


: verifica che ci sia la directory BUILD
:
cd c:\zx\forth\F18\tools\vForth\version\%BUILD%
if %ERRORLEVEL% NEQ 0 goto ERROR

: per poter chiamare new-build-copy.bat
:
cd c:\zx\forth\F18\tools\vForth\version

: _____________________________________________________

echo   1. Copia verso SD
echo      Copia selettivamente da  c:\Zx\forth\F18\tools\vForth      a   c:\Zx\GitHub\vforth-next\SD\tools\vForth
: pause

: %~dp0 = directory di questo .bat: il call funziona da qualunque CWD
call "%~dp0new-build-copy.bat"     c:\Zx\forth\F18\tools\vForth          c:\Zx\GitHub\vforth-next\SD\tools\vForth   %BUILD%
copy                               c:\zx\forth\F18\tools\vForth\dot\*    c:\Zx\GitHub\vforth-next\SD\dot\


: _____________________________________________________

echo   2. Copia verso /
echo      Copia selettivaemnte da  c:\Zx\forth\F18\tools\vForth      a   c:\Zx\GitHub\vforth-next
: pause

: %~dp0 = directory di questo .bat: il call funziona da qualunque CWD
call "%~dp0new-build-copy.bat"     c:\Zx\forth\F18\tools\vForth          c:\Zx\GitHub\vforth-next                   %BUILD%
copy                               c:\zx\forth\F18\tools\vForth\dot\*    c:\Zx\GitHub\vforth-next\dot\


: _____________________________________________________

echo   _____________________________________________________
echo   " "
echo   3. Crea zip file da SD
echo   _____________________________________________________
echo   " "
: pause

: pulizia SD per zip leggero: doc\previous svuotata, un solo PDF e un solo
: !Blocks txt (quelli della build corrente). La radice del repo conserva tutto.
del /q c:\Zx\GitHub\vforth-next\SD\tools\vForth\doc\previous\*.* 2>nul
del /q c:\Zx\GitHub\vforth-next\SD\tools\vForth\doc\txt\!Blocks-64.bin_*.txt 2>nul
copy c:\Zx\forth\F18\tools\vForth\doc\txt\!Blocks-64.bin_%BUILD%.txt c:\Zx\GitHub\vforth-next\SD\tools\vForth\doc\txt\

cd c:\Zx\GitHub\vforth-next\SD

: zip ricreato da zero: -add su zip esistente non rimuove le voci stantie
if exist c:\Zx\GitHub\vforth-next\download\vForth_18_NextZXOS_%BUILD%.zip del /q c:\Zx\GitHub\vforth-next\download\vForth_18_NextZXOS_%BUILD%.zip

: in download resta solo la build corrente: le precedenti vanno in older\
move c:\Zx\GitHub\vforth-next\download\vForth_18_NextZXOS_*.zip c:\Zx\GitHub\vforth-next\download\older\ 2>nul

pkzip25 -add -rec -times=all -dir=current c:\Zx\GitHub\vforth-next\download\vForth_18_NextZXOS_%BUILD%.zip *


: _____________________________________________________


echo   4. Copia anche i project
: pause

echo : DOT VERSION
copy    c:\Zx\Forth\F18\tools\vForth\project\vForth18_DOT\source\*                  c:\Zx\GitHub\vforth-next\project\MMU7_DOT\source
copy    c:\Zx\Forth\F18\tools\vForth\project\vForth18_DOT\list\*                    c:\Zx\GitHub\vforth-next\project\MMU7_DOT\list
copy    c:\Zx\Forth\F18\tools\vForth\project\vForth18_DOT\output\vforth             c:\Zx\GitHub\vforth-next\project\MMU7_DOT\output

echo : MMU7 VERSION
copy    c:\Zx\Forth\F18\tools\vForth\project\vForth18_DOES\source\*                 c:\Zx\GitHub\vforth-next\project\DIRECT_MMU7\source
copy    c:\Zx\Forth\F18\tools\vForth\project\vForth18_DOES\list\*                   c:\Zx\GitHub\vforth-next\project\DIRECT_MMU7\list
copy    c:\Zx\Forth\F18\tools\vForth\project\vForth18_DOES\output\forth18e.bin      c:\Zx\GitHub\vforth-next\project\DIRECT_MMU7\output
copy    c:\Zx\Forth\F18\tools\vForth\project\vForth18_DOES\output\ram8.bin          c:\Zx\GitHub\vforth-next\project\DIRECT_MMU7\output

: echo : DOT VERSION
: copy    c:\Zx\Forth\F18\vForth17_DOT\source\*                  c:\Zx\GitHub\vforth-next\project\MMU7_DOT\source
: copy    c:\Zx\Forth\F18\vForth17_DOT\list\*                    c:\Zx\GitHub\vforth-next\project\MMU7_DOT\list
: copy    c:\Zx\Forth\F18\vForth17_DOT\output\forth17            c:\Zx\GitHub\vforth-next\project\MMU7_DOT\output
 
: echo : MMU7 VERSION
: copy    c:\Zx\Forth\F18\vForth17_MMU7\source\*                 c:\Zx\GitHub\vforth-next\project\DIRECT_MMU7\source
: copy    c:\Zx\Forth\F18\vForth17_MMU7\list\*                   c:\Zx\GitHub\vforth-next\project\DIRECT_MMU7\list
: copy    c:\Zx\Forth\F18\vForth17_MMU7\output\forth17d.bin      c:\Zx\GitHub\vforth-next\project\DIRECT_MMU7\output
: copy    c:\Zx\Forth\F18\vForth17_MMU7\output\ram7.bin          c:\Zx\GitHub\vforth-next\project\DIRECT_MMU7\output

: echo : Previous Direct RP
: copy    c:\Zx\Forth\F18\vForth16_DIRECT_RP\source\*            c:\Zx\GitHub\vforth-next\project\DIRECT_RP\source
: copy    c:\Zx\Forth\F18\vForth16_DIRECT_RP\list\*              c:\Zx\GitHub\vforth-next\project\DIRECT_RP\list
: copy    c:\Zx\Forth\F18\vForth16_DIRECT_RP\output\forth16c.bin c:\Zx\GitHub\vforth-next\project\DIRECT_RP\output
: 
: echo : Previous Direct without RP
: copy    c:\Zx\Forth\F18\vForth15_DIRECT\source\*               c:\Zx\GitHub\vforth-next\project\DIRECT\source
: copy    c:\Zx\Forth\F18\vForth15_DIRECT\list\*                 c:\Zx\GitHub\vforth-next\project\DIRECT\list
: copy    c:\Zx\Forth\F18\vForth15_DIRECT\output\forth15f.bin    c:\Zx\GitHub\vforth-next\project\DIRECT\output
: 
: echo : Previous Indirect
: copy    c:\Zx\Forth\F18\vForth15_INDIRECT\source\*             c:\Zx\GitHub\vforth-next\project\INDIRECT\source
: copy    c:\Zx\Forth\F18\vForth15_INDIRECT\list\*               c:\Zx\GitHub\vforth-next\project\INDIRECT\list
: copy    c:\Zx\Forth\F18\vForth15_INDIRECT\output\forth15e.bin  c:\Zx\GitHub\vforth-next\project\INDIRECT\output


: _____________________________________________________

echo   5. Da ultimo: Crea zip file per Microdrive e Disciple ?
: pause

cd c:\Zx\Forth\F18\
: pkzip25 -add -dir=no c:\Zx\GitHub\vforth-next\download\vForth16m_8Microdrives_%BUILD%.zip     c:\Zx\Forth\F18\M?.mdr
: pkzip25 -add -dir=no c:\Zx\GitHub\vforth-next\download\vForth16m_DISCiPLE_%BUILD%.zip         c:\Zx\Forth\F18\Forth?.img

: pkzip25 -add -dir=no c:\Zx\GitHub\vforth-next\download\vForth16m_8Microdrives_%BUILD%.zip     c:\Zx\Forth\F18\!Blocks7.TAP
: pkzip25 -add -dir=no c:\Zx\GitHub\vforth-next\download\vForth16m_DISCiPLE_%BUILD%.zip         c:\Zx\Forth\F18\!Blocks7.TAP


: _____________________________________________________

: pause
goto END_PROG


:ERROR

echo There is no such directory
echo c:\zx\forth\F18\tools\vForth\version\%BUILD%

goto END_PROG

: _____________________________________________________

:NO_PARAM

echo Usage:
echo    new-build YYYYMMDD
echo.

: _____________________________________________________

: END_PROG

cd c:\zx\forth\F18\tools\vForth\version
