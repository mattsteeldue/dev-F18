DIM rr(320)
FOR i=0 TO 320
  rr(i)=193
NEXT i
xp=144
xr=4.171238905
xf=xr/xp
FOR zi=64 TO -64 STEP -2
  zt=zi*2.25
  zs=zt*zt
  xl=INT(SQR(20736-zs)+0.5)
  FOR xi=0-xl TO xl step .5
    xt=SQR(xi*xi+zs)*xf
    yy=(SIN(xt)+SIN(xt*3)*0.4)*56
    x1=xi+zi+160
    y1=90-yy+zi
    IF x1<0 THEN GOTO 180
    IF rr(x1)<=y1 THEN GOTO 180
    rr(x1)=y1
    PLOT 69,x1*4,850-y1*4+32
  NEXT xi ; row 180
NEXT zi
