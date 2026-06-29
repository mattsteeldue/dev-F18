#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
ARCHIVE_DIR="$SCRIPT_DIR/logs/archive"
KEEP_DAYS=7
DELETE_DAYS=30

mkdir -p "$LOG_DIR" "$ARCHIVE_DIR"

TODAY=$(date '+%Y-%m-%d')
OUT="$LOG_DIR/last_sign_${TODAY}.txt"

# --- rilevamento reboot ---
UPTIME_SECS=$(awk '{print int($1)}' /proc/uptime)
REBOOT_FLAG=""
if [ "$UPTIME_SECS" -lt 120 ]; then
    REBOOT_FLAG="  *** REBOOT RILEVATO (uptime ${UPTIME_SECS}s) ***"
fi

TIMESTAMP=$(date +"%Y-%m-%d %H")
UPTIME="$(uptime -p)"
MEMORY=$(free -h | perl -ne 'print $3 if /^Mem:\s+(\w+)\s+(\w+)\s+(\w+)/')
TEMPERATURE=$(cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf "%.1fC\n", $1/1000}')
PROCESS=$(ps aux --sort=-%cpu | awk 'NR==2' | awk '{printf "%-10s %5s %5s %s\n", $1, $3, $4, $11}')
USERS="$(who | grep -v matteo)"
# 
echo "$TIMESTAMP $UPTIME $MEMORY $TEMPERATURE $PROCESS $USERS" >> "$OUT"

# --- copia in parent directory dopo reboot ---
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
PARENT_COPY="$PARENT_DIR/alive_${TODAY}.txt"
if [ -n "$REBOOT_FLAG" ] && [ ! -f "$PARENT_COPY" ]; then
    cp "$OUT" "$PARENT_COPY"
fi

# --- archiviazione log vecchi ---
find "$LOG_DIR" -maxdepth 1 -name "last_sign_*.txt" \
    -mtime +"$KEEP_DAYS" | while read -r f; do
    gzip -f "$f" && mv "${f}.gz" "$ARCHIVE_DIR/"
done

find "$ARCHIVE_DIR" -name "last_sign_*.gz" -mtime +"$DELETE_DAYS" -delete

# in crontab
# * * * * * ~/last_sign/last_sign.sh
