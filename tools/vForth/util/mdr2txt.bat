:
: extract from Microdrive file Blocks! files and to  M2-M7.txt 
:

perl    \zx\mdr\mdr.pl  /zx/forth/F15/tools/vForth/M2.mdr  get=!Blocks  text=M2.tmp.txt 
perl    \zx\mdr\mdr.pl  /zx/forth/F15/tools/vForth/M3.mdr  get=!Blocks  text=M3.tmp.txt 
perl    \zx\mdr\mdr.pl  /zx/forth/F15/tools/vForth/M4.mdr  get=!Blocks  text=M4.tmp.txt 
perl    \zx\mdr\mdr.pl  /zx/forth/F15/tools/vForth/M5.mdr  get=!Blocks  text=M5.tmp.txt 
perl    \zx\mdr\mdr.pl  /zx/forth/F15/tools/vForth/M6.mdr  get=!Blocks  text=M6.tmp.txt 
perl    \zx\mdr\mdr.pl  /zx/forth/F15/tools/vForth/M7.mdr  get=!Blocks  text=M7.tmp.txt 
perl    \zx\mdr\mdr.pl  /zx/forth/F15/tools/vForth/M8.mdr  get=!Blocks  text=M8.tmp.txt 
perl  mdrDump2txt.pl  M2-M8.txt  M2.tmp.txt  M3.tmp.txt  M4.tmp.txt  M5.tmp.txt  M6.tmp.txt  M7.tmp.txt  M8.tmp.txt 

: pause
del   M2.tmp.txt 
del   M3.tmp.txt 
del   M4.tmp.txt 
del   M5.tmp.txt 
del   M6.tmp.txt 
del   M7.tmp.txt 
del   M8.tmp.txt 
: pause

: extract from IMG file Blocks! 

perl  mgtDump2txt.pl    \Zx\forth\F15\tools\vForth\Forth2.IMG  
move    \Zx\forth\F15\tools\vForth\Forth2.IMG.txt    \Zx\forth\F15\tools\vForth\Util
: pause

: extract from Next file Blocks! 

perl  blocks2txt.pl    \Zx\forth\F15\tools\vForth\!Blocks-64.bin   16383
move    \Zx\forth\F15\tools\vForth\!Blocks-64.bin.txt    \Zx\forth\F15\tools\vForth\util
: pause
