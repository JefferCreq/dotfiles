#!/usr/bin/env sh

STATUS_FILE="$HOME/.config/waybar/.waybar_status"

if [ -f "$STATUS_FILE" ]; then
    STATUS=$(cat "$STATUS_FILE")
else
    STATUS="hidden"
fi

killall -SIGUSR1 waybar

if [ "$STATUS" = "hidden" ]; then
    hyprctl keyword general:gaps_out 0,4,2,4
    echo "visible" > "$STATUS_FILE"
else
    hyprctl keyword general:gaps_out 8
    echo "hidden" > "$STATUS_FILE"
fi


