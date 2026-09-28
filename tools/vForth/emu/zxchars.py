"""
ZX Spectrum character set -> printable text, for the headless emulator.

The Spectrum uses a near-standard 7-bit ASCII set ($7F is the copyright sign);
codes >= $80 are graphics, not text:

    $80-$8F  block graphics: a 2x2 grid of quadrants, bit 0 = top-right,
             bit 1 = top-left, bit 2 = bottom-right, bit 3 = bottom-left
    $90-...  user-defined graphics (UDG A, B, ...) and, on the ROM side,
             BASIC keyword tokens

Handing chr(b) of such a byte to the console is wrong twice: chr($80..$9F)
is a C1 control character, and a cp1252 console cannot encode it at all --
sys.stdout.write() raised UnicodeEncodeError and took the REPL down (e.g. on
WORDS, which lists the null word whose one-byte name is $00|END_BIT = $80).

zx_char() renders block graphics as the Unicode quadrant glyphs when the
output stream can encode them, as an ASCII approximation otherwise; every
other code >= $90 becomes a visible <$NN> escape, since its shape is either
user-defined or a token.
"""
import sys

# index = code - $80 (bit 0 TR, bit 1 TL, bit 2 BR, bit 3 BL)
QUADRANTS = (" \u259d\u2598\u2580\u2597\u2590\u259a\u259c"
             "\u2596\u259e\u258c\u259b\u2584\u259f\u2599\u2588")
# 7-bit fallback: ' top only, . bottom only, # full, : any other mix
QUADRANTS_ASCII = " '''.:::.:::.::#"


def _can_encode(text, encoding):
    try:
        text.encode(encoding or "ascii")
        return True
    except (UnicodeEncodeError, LookupError):
        return False


def zx_char(b, encoding=None):
    """Printable text for Spectrum character code b (0-255).

    encoding: the target stream's encoding; defaults to sys.stdout's."""
    if b == 0x7F:
        return "(c)"
    if b < 0x80:
        return chr(b)
    if b < 0x90:
        if encoding is None:
            encoding = getattr(sys.stdout, "encoding", None)
        glyph = QUADRANTS[b - 0x80]
        return glyph if _can_encode(glyph, encoding) else QUADRANTS_ASCII[b - 0x80]
    return "<$%02X>" % b
