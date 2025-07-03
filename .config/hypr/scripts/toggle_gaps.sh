#!/usr/bin/env sh

GAPS_IN=$(hyprctl getoption general:gaps_in | sed -n '1p' | awk '{print $3}')

if [ "$GAPS_IN" = "0" ]; then
    # Cambiar a gaps pequeños
    hyprctl keyword general:gaps_in 1
    hyprctl keyword general:gaps_out 2
    hyprctl keyword decoration:rounding 4
elif [ "$GAPS_IN" = "1" ]; then
    # Cambiar a gaps grandes
    hyprctl keyword general:gaps_in 6
    hyprctl keyword general:gaps_out 16
    hyprctl keyword decoration:rounding 8
else
    # Cambiar a sin gaps
    hyprctl keyword general:gaps_in 0
    hyprctl keyword general:gaps_out 0
    hyprctl keyword decoration:rounding 0
fi
