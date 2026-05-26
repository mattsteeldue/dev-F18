:
: new-build-copy.bat
:
: copia da directory di lavoro a directory di GitHub

: @ECHO OFF

cd c:\zx\forth\F18\tools\vForth\version

if "%1"=="" goto NO_PARAM
if "%2"=="" goto NO_PARAM
if "%3"=="" goto NO_PARAM

: _____________________________________________________

: Source directory 
set SOURCE=%1

set DEST=%2
set BUILD=%3

: _____________________________________________________

echo Change Directory to %SOURCE%
cd %SOURCE%

: _____________________________________________________

echo Copy LICENSE.md
copy  LICENSE.md                            %DEST%
copy  LICENSE.tap                           %DEST%
copy  LICENSE.txt                           %DEST%

: _____________________________________________________

echo Copy !Blocks-64.bin
copy  !Blocks-64.bin                        %DEST%

: echo Copy Forth15
: copy  forth15e.bin                          %DEST%
: copy  forth15f.bin                          %DEST%
: copy  Forth15_loader.bas                    %DEST%
: copy  Forth15_direct.bas                    %DEST%
: copy  Forth15_indirect.bas                  %DEST%
: copy  Forth15.bas                           %DEST%

: echo Copy Forth16
: copy  Forth16_loader.bas                    %DEST%
: copy  Forth16_golden.bas                    %DEST%
: copy  forth16c.bin                          %DEST%
: copy  Forth16.bas                           %DEST%

: echo Copy Forth17
: copy  Forth17_loader.bas                    %DEST%
: copy  forth17d.bin                          %DEST%
: copy  Forth17.bas                           %DEST%
: copy  ram7.bin                              %DEST%

echo Copy Forth18
copy  Forth18_loader.bas                    %DEST%
copy  forth18e.bin                          %DEST%
copy  Forth18.bas                           %DEST%
copy  ram8.bin                              %DEST%

echo Copy other
copy  Standard-Loader.bas                   %DEST%

: pause

: _____________________________________________________


echo Change Directory to c:\Zx\forth\F18\tools\vForth
cd c:\Zx\forth\F18\tools\vForth

echo Moving older docs to previous
move  %DEST%\doc\*.*                                     %DEST%\doc\previous 
move  %DEST%\doc\previous\vForth1.*-core-en-%BUILD%.pdf  %DEST%\doc\
move  %DEST%\doc\previous\vForth1.*-core-en-%BUILD%.odt  %DEST%\doc\

echo Copying new docs
copy  doc\vForth1.*-core-en-%BUILD%.pdf     %DEST%\doc
copy  doc\txt\!Blocks-64.bin_%BUILD%.txt    %DEST%\doc\txt

: pause

: _____________________________________________________

echo Copying inc
copy  inc\*.f                               %DEST%\inc
copy  inc\README.txt                        %DEST%\inc 
: pause

: _____________________________________________________

echo Copying lib
copy  lib\*.f                               %DEST%\lib
copy  lib\*.bin                             %DEST%\lib
: pause

: _____________________________________________________

echo Copying src
copy  src\F18e.f                            %DEST%\src
: copy  src\F17e.f                            %DEST%\src
: copy  src\F16m.f                            %DEST%\src
copy  src\Z80N-Assembler-Dictionary.txt     %DEST%\src
copy  src\Z80N-asm.f                        %DEST%\src
copy  src\FP-OPT.f                          %DEST%\src
copy  src\z80-test.txt                      %DEST%\src
copy  src\Z80-TEST.f                        %DEST%\src
: pause

: _____________________________________________________

echo Copying test
copy  test\*.f                              %DEST%\test
copy  test\README.txt                       %DEST%\test
: pause

: _____________________________________________________

echo Copying demo
copy  demo\*.f                              %DEST%\demo
copy  demo\*.bin                            %DEST%\demo
copy  demo\README.txt                       %DEST%\demo
copy  demo\chomp-chomp\*.*                  %DEST%\demo\chomp-chomp\*.*
: pause

: _____________________________________________________

echo Copying util
copy  util\putscr.pl                        %DEST%\util
copy  util\blocks2txt.pl                    %DEST%\util        
: pause

: _____________________________________________________

pause
goto END_PROG

: _____________________________________________________

:NO_PARAM

echo Uso:
echo    new-build-copy SOURCE DEST BUILD
echo.

: _____________________________________________________

: END_PROG

cd c:\zx\forth\F18\tools\vForth\version
