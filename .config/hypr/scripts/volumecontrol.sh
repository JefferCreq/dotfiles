#!/usr/bin/env sh

# define functions

function print_error {
cat << "EOF"
    ./volumecontrol.sh -[device] <action>
    ...valid device options...
        i -- [i]nput device (microphone)
        o -- [o]utput device (speaker)
    ...valid actions are...
        i -- <i>ncrease volume [+5]
        d -- <d>ecrease volume [-5]
        m -- <m>ute [toggle]
EOF
exit 1
}

function notify_vol {
    vol=$(pactl get-$target-volume @DEFAULT_${target^^}@ | grep 'Volume:' | grep -E -o "[0-9]+%" | head -1 | tr -d '%')
    angle="$(( (vol+2)/5 * 5 ))"
    icodir="~/.config/dunst/icons/vol"
    ico="${icodir}/vol-${angle}.svg"
    dunstify $ncolor -a "volctl" "Volume Control" -i "$ico" -r 91190 -t 800 -a "$vol" "$nsink"
}

function notify_mute {
	mute=$(pactl get-$target-mute @DEFAULT_${target^^}@ | awk '/Mute:/ { print $2 }')
    if [ "$mute" == "yes" ] ; then
        dunstify $ncolor -a "volctl" "Muted" -i "${icodir}/muted-${dvce}.svg" -r 91190 -t 800
    else
        dunstify $ncolor -a "volctl" "Unmuted" -i "${icodir}/unmuted-${dvce}.svg" -r 91190 -t 800
    fi
}

# set device source

while getopts "io" SetSrc
do
    case $SetSrc in
    i) nsink="input"
       target="source" 
       dvce="mic" ;;
    o) nsink="output"
       target="sink" 
       dvce="speaker" ;;
    esac
done

shift $((OPTIND -1))
if [ -z "$nsink" ]; then
    print_error
fi

# set device action

vol=$(pactl get-$target-volume @DEFAULT_${target^^}@ | grep 'Volume:' | grep -E -o "[0-9]+%" | head -1 | tr -d '%')
ncolor="-h string:bgcolor:#181825 -h string:fgcolor:#f5e0dc -h string:frcolor:#11111b"
step="${2:-5}"
icodir="~/.config/dunst/icons/vol"

case "$1" in
i)  
  if [[ $vol -lt 100 ]]; then
    pactl set-$target-volume  @DEFAULT_${target^^}@ +${step}%
  else
    pactl set-$target-volume  @DEFAULT_${target^^}@ 100%
  fi
  notify_vol
  ;;
d) pactl set-$target-volume  @DEFAULT_${target^^}@ -${step}%; notify_vol ;;
m) pactl set-$target-mute @DEFAULT_${target^^}@ toggle; notify_mute ;;
    *) print_error ;;
esac

