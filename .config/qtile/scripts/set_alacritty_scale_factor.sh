#!/bin/sh

monitorCount=$(xrandr -q | grep -w "connected" | wc -l)

if [ "$monitorCount" -eq 1 ]; then
  sed -i "s/WINIT_X11_SCALE_FACTOR: '1.0'/WINIT_X11_SCALE_FACTOR: '2.0'/g" /home/jeffer/.config/alacritty/alacritty.yml
else
  sed -i "s/WINIT_X11_SCALE_FACTOR: '2.0'/WINIT_X11_SCALE_FACTOR: '1.0'/g" /home/jeffer/.config/alacritty/alacritty.yml
fi
