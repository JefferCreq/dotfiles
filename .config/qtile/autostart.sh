#!/bin/sh

hostname=$(cat /proc/sys/kernel/hostname)

monitorCount=$(xrandr -q | grep -w "connected" | wc -l)

if [ "$monitorCount" -eq 2 ]; then
    xrandr --output eDP-1 --mode 2880x1800 --pos 3840x0 --rotate normal --output HDMI-1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --scale 2x2
fi

# $HOME/.config/qtile/themes/polybar.sh
light -S 100 &
redshift -P -O 4500 &
exec mpd &
feh --bg-fill /home/jeffer/.config/.wallpaper &
picom --config ~/.config/picom/picom.conf &
