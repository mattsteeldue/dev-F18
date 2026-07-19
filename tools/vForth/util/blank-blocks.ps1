<#
.SYNOPSIS
    Fill one or more BLOCK ranges in a vForth blocks file with BL (0x20),
    matching the Forth word BLANK (BL FILL). File size is never changed.

.PARAMETER File
    Path to the blocks file (usually "!Blocks-64.bin").

.PARAMETER Ranges
    Comma-separated list of "start-end" BLOCK ranges (512 bytes each).
    BLOCK numbers are 1-based, matching the vForth core (R/W does "1-"
    before BLK-SEEK): BLOCK n lives at byte offset (n-1)*512. BLOCK 1 is
    therefore the file's first 512 bytes.

.PARAMETER CheckOnly
    Only report which BLOCK(s) in the given ranges are already blank; do
    not write. A BLOCK counts as already blank if every byte is 0x20
    (space) or 0x00 (inert NUL mixed in among the spaces is admissible --
    it does not disqualify the BLOCK from being considered blank).

.EXAMPLE
    Dry-run check before touching anything:
    .\blank-blocks.ps1 -File "!Blocks-64.bin" -Ranges "24-197" -CheckOnly

.EXAMPLE
    Actual write (also prints the same pre-check report first):
    .\blank-blocks.ps1 -File "!Blocks-64.bin" -Ranges "24-197,32000-32040,32048-32175,32200-32240,32248-32375"
#>
param(
    [Parameter(Mandatory=$true)][string]$File,
    [Parameter(Mandatory=$true)][string]$Ranges,
    [switch]$CheckOnly
)

$BBUF = 512

function Parse-Ranges([string]$spec) {
    $parsed = @()
    foreach ($part in $spec -split ',') {
        $bounds = $part -split '-'
        $a = [int]$bounds[0]
        $b = [int]$bounds[1]
        if ($a -gt $b) { throw "Invalid range $part (start > end)" }
        $parsed += ,@($a, $b)
    }
    return $parsed
}

function Test-BlockBlank([byte[]]$buf) {
    foreach ($b in $buf) {
        if ($b -ne 0x20 -and $b -ne 0x00) { return $false }
    }
    return $true
}

$parsed = Parse-Ranges $Ranges

$size = (Get-Item $File).Length
$maxBlock = ($parsed | ForEach-Object { $_[1] } | Measure-Object -Maximum).Maximum
$needed = [int64]$maxBlock * $BBUF
if ($needed -gt $size) {
    throw "$File is $size bytes, too small for BLOCK $maxBlock (needs at least $needed)"
}

# Pre-check: which BLOCK(s) in the requested ranges are NOT already blank
# (i.e. contain a byte other than 0x20/0x00) -- run before any write.
$fsCheck = [System.IO.File]::OpenRead($File)
$notBlank = @()
$checked = 0
try {
    foreach ($r in $parsed) {
        for ($blk = $r[0]; $blk -le $r[1]; $blk++) {
            $fsCheck.Seek([int64]($blk - 1) * $BBUF, 'Begin') | Out-Null
            $buf = New-Object byte[] $BBUF
            $fsCheck.Read($buf, 0, $BBUF) | Out-Null
            $checked++
            if (-not (Test-BlockBlank $buf)) { $notBlank += $blk }
        }
    }
} finally {
    $fsCheck.Close()
}

Write-Output "Pre-check: $checked BLOCK(s) esaminati, $($notBlank.Count) NON gia' blank (contengono byte diversi da 0x20/0x00)."
if ($notBlank.Count -gt 0) {
    Write-Output ("BLOCK con contenuto reale: " + ($notBlank -join ', '))
}

if ($CheckOnly) {
    return
}

$blank = [byte[]]::new($BBUF)
for ($i = 0; $i -lt $BBUF; $i++) { $blank[$i] = 0x20 }

$fs = [System.IO.File]::Open($File, 'Open', 'ReadWrite')
try {
    $total = 0
    foreach ($r in $parsed) {
        for ($blk = $r[0]; $blk -le $r[1]; $blk++) {
            $fs.Seek([int64]($blk - 1) * $BBUF, 'Begin') | Out-Null
            $fs.Write($blank, 0, $BBUF)
            $total++
        }
    }
} finally {
    $fs.Close()
}

Write-Output "OK: blanked $total BLOCK(s) ($BBUF bytes each, filled with 0x20) in $File"
