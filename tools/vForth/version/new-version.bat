: crea alberatura
@ECHO OFF

if "%1"=="" goto NO_PARAM

: _____________________________________________________

mkdir %1

cd %1

mkdir src
mkdir test
mkdir lib
mkdir inc
mkdir doc
mkdir doc\txt
mkdir forum
mkdir util
mkdir demo
mkdir help
mkdir dev
mkdir tutorial

mkdir dot

cd ..

goto END_PROG

: _____________________________________________________

:NO_PARAM
echo Uso:
echo    new-version YYYYMMDD
echo.

: _____________________________________________________

: END_PROG



