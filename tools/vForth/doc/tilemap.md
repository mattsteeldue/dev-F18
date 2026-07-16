This document is (c) Allen Albright

Distributed under the Attribution-NonCommercial-ShareAlike CC BY-NC-SA license.
-------------------------------------------------------------------------------

=======
TILEMAP
=======

The tilemap is a hardware character oriented display that comes in two 
resolutions:  40x32 (320x256 pixels) and 80x32 (640x256 pixels).  
The display area on screen is the same as the sprite layer, meaning it overlaps
the standard 256x192 area by 32 pixels on all sides.  Vertically this is larger 
than the physical HDMI display which will cut off the top and bottom character 
rows (making the visible area 40x30 or 80x30) but the full area is visible on 
VGA.

The tilemap is defined by two data structures.

========================
DATA STRUCTURE:  TILEMAP
========================

The first data structure is the tilemap itself which indicates what characters 
occupy each cell on screen.  Each tilemap entry is two bytes so for 40x32 
resolution, a full size tilemap will occupy 2560 bytes, and for 80x32 resolution
the space taken is twice that at 5120 bytes.  The tilemap entries are stored in 
X-major order and each two-byte tilemap entry is stored little endian:

  Tilemap Entry

  bits 15-12 : palette offset
  bit     11 : x mirror
  bit     10 : y mirror
  bit      9 : rotate
  bit      8 : ULA over tilemap (if the ula is disabled, bit 8 of tile number)
  bits   7-0 : tile number

The character displayed is indicated by the "tile number" which can be thought 
of as an ascii code.  The tile number is normally eight bits allowing up to 256 
unique tiles to be defined but this can be extended to nine bits for 512 unique 
tiles if the ULA display is disabled.

The other bits are tile attributes that modify how the tile image is drawn.  
Their function is the same as the equivalent sprite attributes for sprites.  
Bits will apply rotation and mirroring and colour can be shifted with a palette
offset.  If the ULA display is enabled, bit 8 will determine if the tile is 
above or below the ULA display.

=================================
DATA STRUCTURE:  TILE DEFINITIONS
=================================

The second data structure is the tile definitions themselves.

Each tile, identified by tile number, is 8x8 pixels in size with each pixel four
bits to select one of 16 colours.  A tile definition occupies 32 bytes and is 
defined in X major order with packing in the X direction in the same way that 
4-bit sprites are defined.  The 4-bit colour of each pixel is augmented by the
4-bit palette offset from the tilemap in the most significant bits to form an 
8-bit colour index that is looked up in the tilemap palette to determine the 
final 9-bit colour sent to the display.  
Tiles are therefore defined using 16 colours with the tilemap palette offset 
able to act as index into the tilemap palette to vary the display colour.

===================================
MEMORY ORGANIZATION & DISPLAY LAYER
===================================

The tilemap is a logical extension of the ULA and its data structures are 
contained in the ULA's 16k bank 5.  If both the ULA and tilemap are enabled, 
this means that the tilemap's map and tile definitions should be arranged within
the 16k to avoid overlap with the display ram used by the ULA.

The tilemap exists on the same display layer as the ULA.  The graphics generated
by the ULA and tilemap are combined before being forwarded to the SLU layer 
system as layer U.

=========================
ULA & TILEMAP COMBINATION
=========================

The combination of the ULA and tilemap output is done in one of two modes: 
the standard mode and the stencil mode.

The standard mode uses bit 8 of a tile's tilemap entry to determine if a tile is
above or below the ULA.  The source of the final pixel generated is then the 
topmost non-transparent pixel.  If the ULA or tilemap is disabled then they are 
treated as transparent.

The stencil mode will only be applied if both the ULA and tilemap are enabled.  
In the stencil mode, the final pixel will be transparent if either the ULA or 
tilemap are transparent.  Otherwise the final pixel is a logical AND of the 
corresponding colour bits.  The stencil mode allows one layer to act as a 
cut-out stencil for the other.

=======================
PROGRAMMING THE TILEMAP
=======================

(R/W) 0x6B (107) => Tilemap Control
  bit 7    = 1 to enable the tilemap
  bit 6    = 0 for 40x32, 1 for 80x32
  bit 5    = 1 to eliminate the attribute entry in the tilemap
  bit 4    = palette select
  bits 3-0 = Reserved set to 0

Bits 7 & 6 enable the tilemap and select resolution.  Bit 4 selects one of two 
tilemap palettes used for final colour lookup.  Bit 5 changes the structure of
the tilemap so that it contains only 8-bit tilemap entries instead of 16-bit 
tilemap entries.  If 8-bit, the tilemap only contains tile numbers and the 
attributes are instead taken from nextreg 0x6C.


(R/W) 0x6C (108) => Default Tilemap Attribute
  bits 7-4 = Palette Offset
  bit 3    = X mirror
  bit 2    = Y mirror
  bit 1    = Rotate
  bit 0    = ULA over tilemap
             (bit 8 of tile id if the ULA is disabled)

If bit 5 of nextreg 0x6B is set, the tilemap's structure is modified to contain 
only 8-bit tile numbers instead of the usual 16-bit tilemap entries.  In this 
case, the tile attributes used are taken from this register instead.


(R/W) 0x6E (110) => Tilemap Base Address
  bits 7-6 = Read back as zero, write values ignored
  bits 5-0 = MSB of address of the tilemap in Bank 5

This register determines the tilemap's base address in bank 5.  The base address
is the MSB of an offset into the 16k bank, allowing the tilemap to begin at any
multiple of 256 bytes in the bank.  Writing a physical MSB address in 0x40-0x7f 
or 0xc0-0xff, corresponding to traditional ULA physical addresses, is permitted.
The value read back should be treated as a fully significant 8-bit value.

The tilemap will be 40x32 or 80x32 in size depending on the resolution selected
in nextreg 0x6B.  Each entry in the tilemap is normally two bytes but can be one
byte if attributes are eliminated by setting bit 5 of nextreg 0x6B.


(R/W) 0x6F (111) => Tile Definitions Base Address
  bits 7-6 = Read back as zero, write values ignored
  bits 5-0 = MSB of address of tile definitions in Bank 5

This register determines the base address of tile definitions in bank 5.  As 
with nextreg 0x6E, the base address is the MSB of the an offset into the 16k 
bank, allowing tile definitions to begin at any multiple of 256 bytes in the 
bank.  Writing a physical MSB address in 0x40-0x7f or 0xc0-0xff, corresponding 
to traditional ULA physical addresses, is permitted.  The value read back should
be treated as a fully significant 8-bit value.

Each tile definition is 32 bytes in size and is located at address:

  Tile Def Base Addr + 32 * (Tile Number)


(R/W) 0x4C (76) => Transparency index for the tilemap
  bits 7-4 = Reserved, must be 0
  bits 3-0 = Set the index value (0xF after reset)

Defines the transparent colour index for tiles.  The 4-bit pixels of a tile 
definition are compared to this value to determine if they are transparent.


(R/W) 0x43 (67) => Palette Control
  bit 7 = '1' to disable palette write auto-increment.
  bits 6-4 = Select palette for reading or writing:
     000 = ULA first palette
     100 = ULA second palette
     001 = Layer 2 first palette
     101 = Layer 2 second palette
     010 = Sprites first palette 
     110 = Sprites second palette
	  011 = Tilemap first palette
	  111 = Tilemap second palette
  bit 3 = Select Sprites palette (0 = first palette, 1 = second palette)
  bit 2 = Select Layer 2 palette (0 = first palette, 1 = second palette)
  bit 1 = Select ULA palette (0 = first palette, 1 = second palette)
  bit 0 = Enabe ULANext mode if 1. (0 after a reset)

The tilemap has its own pair of palettes for looking up 9-bit colours.  Each 
tile definition pixel is 4-bits which is combined with the 4-bit palette offset
from the tilemap entry in the most significant 8-bits.  This 8-bit value is 
passed through the tilemap palette to generate the final 9-bit colour for the 
pixel.


(R/W) 0x1B (27) => Clip Window Tilemap
  bits 7-0 = Coord. of the clip window
  1st write = X1 position
  2nd write = X2 position
  3rd write = Y1 position
  4rd write = Y2 position
  The values are 0,159,0,255 after a Reset
  Reads do not advance the clip position

The tilemap display surface extends 32 pixels around the central 256x192 
display.  
The origin of the clip window is the top left corner of this area 32 pixels to 
the left and 32 pixels above the central 256x192 display.  The X coordinates are
internally doubled to cover the full 320 pixel width of the surface.  The clip
window indicates the portion of the tilemap display that is non-transparent and 
its indicated extent is inclusive; it will extend from X1*2 to X2*2+1 
horizontally and from Y1 to Y2 vertically.


(R/W) 0x2F (47) => Tilemap Offset X MSB
  bits 7-2 = Reserved, must be 0
  bits 1-0 = MSB X Offset
  Meaningful Range is 0-319 in 40 char mode, 0-639 in 80 char mode

(R/W) 0x30 (48) => Tilemap Offset X LSB
  bits 7-0 = LSB X Offset
  Meaningful range is 0-319 in 40 char mode, 0-639 in 80 char mode

(R/W) 0x31 (49) => Tilemap Offset Y
  bits 7-0 = Y Offset (0-191)

These are scroll registers for scrolling the tilemap area.  As with other 
layers, the scroll region wraps.


(R/W) 0x68 (104) => ULA Control
  bit 7    = 1 to disable ULA output
  bit 6    = 0 to select the ULA colour for blending in SLU modes 6 & 7
           = 1 to select the ULA/tilemap mix for blending in SLU modes 6 & 7
  bits 5-1 = Reserved must be 0
  bit 0    = 1 to enable stencil mode when both the ULA and tilemap are enabled
            (if either are transparent the result is transparent otherwise the
				 result is a logical AND of both colours)

Bit 0 can be set to choose stencil mode for the combined output of the ULA and 
tilemap.  Bit 6 determines what colour is used in SLU modes 6 & 7 where the ULA 
is combined with Layer 2 to generate highlighting effects.
