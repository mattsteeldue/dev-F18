<#
.SYNOPSIS
    Fill one or more BLOCK ranges in a vForth blocks file with BL (0x20),
    matching the Forth word BLANK (BL FILL). File size is never changed.

.PARAMETER File
    Path to the blocks file (usually "!Blocks-64.bin").

.PARAMETER Ranges
    Comma-separated list of "start-end" BLOCK ranges (512 bytes each,
    BLOCK n at byte offset n*512).

.EXAMPLE
    .\blank-blocks.ps1 -File "!Blocks-64.bin" -Ranges "24-197,32000-32040,32048-32175,32200-32240,32248-32375"
#>
param(
    [Parameter(Mandatory=$true)][string]$File,
    [Parameter(Mandatory=$true)][string]$Ranges
)

$BBUF = 512
$parsed = @()
foreach ($part in $Ranges -split ',') {
    $bounds = $part -split '-'
    $a = [int]$bounds[0]
    $b = [int]$bounds[1]
    if ($a -gt $b) { throw "Invalid range $part (start > end)" }
    $parsed += ,@($a, $b)
}

$size = (Get-Item $File).Length
$maxBlock = ($parsed | ForEach-Object { $_[1] } | Measure-Object -Maximum).Maximum
$needed = ([int64]$maxBlock + 1) * $BBUF
if ($needed -gt $size) {
    throw "$File is $size bytes, too small for BLOCK $maxBlock (needs at least $needed)"
}

$blank = [byte[]]::new($BBUF)
for ($i = 0; $i -lt $BBUF; $i++) { $blank[$i] = 0x20 }

$fs = [System.IO.File]::Open($File, 'Open', 'ReadWrite')
try {
    $total = 0
    foreach ($r in $parsed) {
        for ($blk = $r[0]; $blk -le $r[1]; $blk++) {
            $fs.Seek([int64]$blk * $BBUF, 'Begin') | Out-Null
            $fs.Write($blank, 0, $BBUF)
            $total++
        }
    }
} finally {
    $fs.Close()
}

Write-Output "OK: blanked $total BLOCK(s) ($BBUF bytes each, filled with 0x20) in $File"
