#!/usr/bin/env sh

STATUS_FILE="$HOME/.config/waybar/.waybar_status"

if [ -f "$STATUS_FILE" ]; then
    STATUS=$(cat "$STATUS_FILE")
else
    STATUS="hidden"
fi

# killall -SIGUSR1 waybar
# killall -SIGUSR1 ags quit || ags run

if [ "$STATUS" = "hidden" ]; then
    hyprctl keyword general:gaps_in 1
    hyprctl keyword general:gaps_out 2
    hyprctl keyword decoration:rounding 4
    echo "visible" > "$STATUS_FILE"
else
    hyprctl keyword general:gaps_in 0
    hyprctl keyword general:gaps_out 0
    hyprctl keyword decoration:rounding 0
    echo "hidden" > "$STATUS_FILE"
fi


ags run || ags quit

