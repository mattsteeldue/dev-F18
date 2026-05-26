\
\ aydemo.f
\ 
needs ay
needs interrupts
needs ms
needs [']

needs afxframe

\ include lib/afxframe-asm.f

decimal

aysetup

: silence
    isr-off
    1 ayselect shh 
    2 ayselect shh 
    3 ayselect shh 
;  


: display-block ( u -- )
    cr dup .                \  u
    block 2+                \  a
    c/l 2-                  \  a
    -trailing type          \    
;    



: play-block  ( u1 u2 -- )   \  u1:block number, u2:slot
    2* 2* >R                \  u1
    block                   \  a
    c/l + 0 swap            \  0 a1
    afx-ch-desc R> +        \  0 a1 a3
    2!  
;


needs dump
: aystatus
  AFX-CH-DESC 56 dump
;


decimal

: delay 300 ms ;

: ay-demo
    isr-off
    ['] afxframe isr-xt !   
    isr-on

    4490 4400 do

        i 0 + display-block 
        i 1 + display-block 
        i 2 + display-block 
        i 3 + display-block 
        i 4 + display-block 
        i 5 + display-block 

        i 0 + 0 play-block 
        i 1 + 1 play-block 
        i 2 + 2 play-block 
        i 3 + 3 play-block 
        i 4 + 4 play-block 
        i 5 + 5 play-block 

        delay delay delay
        delay delay delay

        ?terminal if leave then

    6 +loop

    4638 4500 do

        i 0 + display-block 
        i 1 + display-block 
        i 2 + display-block 
        i 3 + display-block 
        i 4 + display-block 
        i 5 + display-block 

        isr-off
        i 0 + 0 play-block 
        i 1 + 1 play-block 
        i 2 + 2 play-block 
        i 3 + 3 play-block 
        i 4 + 4 play-block 
        i 5 + 5 play-block 
        isr-on

        delay delay delay
        delay delay delay

        ?terminal if leave then

    6 +loop

    isr-off

    1 ayselect shh 
    2 ayselect shh 
    3 ayselect shh 
;

quit

isr-off
' afxframe isr-xt !   
isr-on


4400 0 play-block delay
4401 1 play-block delay
4402 2 play-block delay
4403 3 play-block delay
4404 4 play-block delay

4405 0 play-block delay
4406 1 play-block delay
4407 2 play-block delay
4408 3 play-block delay
4409 4 play-block delay

4410 0 play-block delay
4411 1 play-block delay
4412 2 play-block delay
4413 3 play-block delay
4414 4 play-block delay

4415 0 play-block delay
4416 1 play-block delay
4417 2 play-block delay
4418 3 play-block delay
4419 4 play-block delay
4420 5 play-block delay

4421 0 play-block delay
4422 1 play-block delay
4423 2 play-block delay
4424 3 play-block delay
4425 4 play-block delay
4426 5 play-block delay

4427 0 play-block delay
4428 1 play-block delay
4429 2 play-block delay
4430 3 play-block delay

4431 0 play-block delay
4432 1 play-block delay
4433 2 play-block delay
4434 3 play-block delay

4435 0 play-block delay
4436 1 play-block delay
4437 2 play-block delay
4438 3 play-block delay
4439 4 play-block delay
4440 5 play-block delay

4441 0 play-block delay
4442 1 play-block delay
4443 2 play-block delay
4444 3 play-block delay

4445 0 play-block delay
4446 1 play-block delay
4447 2 play-block delay
4448 3 play-block delay

4449 0 play-block delay
4450 1 play-block delay
4451 2 play-block delay
4452 3 play-block delay
4453 4 play-block delay

4454 0 play-block delay
4455 1 play-block delay

4456 0 play-block delay
4457 1 play-block delay
4458 2 play-block delay
4459 3 play-block delay
4460 4 play-block delay

4461 0 play-block delay
4462 1 play-block delay
4463 2 play-block delay
4464 3 play-block delay

4465 0 play-block delay
4466 1 play-block delay
4467 2 play-block delay
4468 3 play-block delay

4469 0 play-block delay
4470 1 play-block delay
4471 2 play-block delay
4472 3 play-block delay
4473 4 play-block delay
4474 5 play-block delay

4475 0 play-block delay
4476 1 play-block delay
4477 2 play-block delay
4478 3 play-block delay

4479 0 play-block delay
4480 1 play-block delay
4481 2 play-block delay
4482 3 play-block delay
4483 4 play-block delay
4484 5 play-block delay

4485 0 play-block delay
4486 1 play-block delay
4487 2 play-block delay
4488 3 play-block delay
4489 4 play-block delay
4490 0 play-block delay
4491 1 play-block delay
4492 2 play-block delay
4493 3 play-block delay

isr-off
1 ayselect shh 
2 ayselect shh 
3 ayselect shh 

