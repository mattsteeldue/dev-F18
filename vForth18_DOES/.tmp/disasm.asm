L8130:       equ  8130h


             org 8104h


8104 L8104:
8104 37           SCF         
8105 C3 4F 96     JP   L964F  


8108 L8108:
8108 01           defb 01h    
8109 01           defb 01h    
810A 00           defb 00h    
810B E0           defb E0h    
810C A3           defb A3h    
810D A3           defb A3h    
810E 0C           defb 0Ch    
810F 00           defb 00h    
8110 50           defb 50h    
8111 B2           defb B2h    


8112 L8112:
8112 E8           defb E8h    
8113 D0           defb D0h    


8114 L8114:
8114 88           defb 88h    
8115 D1           defb D1h    
8116 E8           defb E8h    
8117 D0           defb D0h    
8118 1F           defb 1Fh    


             org 964Fh


964F L964F:
964F DD 21 34 81  LD   IX,8134h 
9653 D9           EXX         
9654 E5           PUSH HL     
9655 D9           EXX         
9656 ED 73 08 81  LD   (L8108),SP 
965A ED 7B 12 81  LD   SP,(L8112) 
965E 00           NOP         
965F 2A 14 81     LD   HL,(L8114) 
9662 00           NOP         
9663 22 30 81     LD   (L8130),HL 
9666 01 49 96     LD   BC,9649h 
9669 38 02        JR   C,L966D 
966B 03           INC  BC     
966C 03           INC  BC     
966D L966D:
966D DD E9        JP   (IX)   


966F 85           defb 85h    
9670 42           defb 42h    
9671 41           defb 41h    
9672 53           defb 53h    
9673 49           defb 49h    
9674 C3           defb C3h    
9675 F2           defb F2h    
9676 95           defb 95h    
9677 79           defb 79h    
9678 96           defb 96h    
9679 C1           defb C1h    
967A 21           defb 21h    
967B 00           defb 00h    
967C 00           defb 00h    
967D 39           defb 39h    
967E ED           defb EDh    
967F 7B           defb 7Bh    
9680 08           defb 08h    
9681 81           defb 81h    
9682 00           defb 00h    
9683 22           defb 22h    
9684 08           defb 08h    
9685 81           defb 81h    
9686 D9           defb D9h    
9687 E1           defb E1h    
9688 D9           defb D9h    
9689 C9           defb C9h    
968A 82           defb 82h    
968B 2B           defb 2Bh    
968C AD           defb ADh    
968D 6F           defb 6Fh    
968E 96           defb 96h    
968F CB           defb CBh    
9690 89           defb 89h    
9691 FF           defb FFh    
9692 86           defb 86h    
9693 7F           defb 7Fh    
9694 81           defb 81h    
9695 04           defb 04h    
9696 00           defb 00h    
9697 9E           defb 9Eh    
9698 87           defb 87h    
9699 95           defb 95h    
969A 86           defb 86h    
969B 83           defb 83h    
969C 44           defb 44h    
969D 2B           defb 2Bh    
969E AD           defb ADh    
969F 8A           defb 8Ah    
96A0 96           defb 96h    
96A1 CB           defb CBh    
96A2 89           defb 89h    
96A3 FF           defb FFh    
96A4 86           defb 86h    
96A5 7F           defb 7Fh    
96A6 81           defb 81h    
96A7 04           defb 04h    
96A8 00           defb 00h    
96A9 B3           defb B3h    
96AA 87           defb 87h    
96AB 95           defb 95h    
96AC 86           defb 86h    
96AD 83           defb 83h    
96AE 41           defb 41h    
96AF 42           defb 42h    
96B0 D3           defb D3h    
96B1 9B           defb 9Bh    
96B2 96           defb 96h    