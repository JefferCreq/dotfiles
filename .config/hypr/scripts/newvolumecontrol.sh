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
    vol=$(pactl get-$type-volume $target | grep 'Volume:' | grep -E -o "[0-9]+%" | head -1 | tr -d '%')
    angle="$(( (vol+2)/5 * 5 ))"
    icodir="~/.config/dunst/icons/vol"
    ico="${icodir}/vol-${angle}.svg"
    dunstify $ncolor -a "volctl" "Volume Control" -i "$ico" -r 91190 -t 800 -a "$vol" "$nsink"
}

function notify_mute {
	mute=$(pactl get-$type-mute $target | awk '/Mute:/ { print $2 }')
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
       type="source"
       target="@DEFAULT_SOURCE@" 
       dvce="mic" ;;
    o) nsink="output"
       type="sink"
       target=$(pactl list sinks | awk '/State: RUNNING/{getline; print $2; exit}') 
       dvce="speaker" ;;
    esac
done

shift $((OPTIND -1))
if [ -z "$nsink" ]; then
    print_error
fi

# set device action

vol=$(pactl get-$type-volume $target | grep 'Volume:' | grep -E -o "[0-9]+%" | head -1 | tr -d '%')
ncolor="-h string:bgcolor:#181825 -h string:fgcolor:#f5e0dc -h string:frcolor:#11111b"
step="${2:-5}"
icodir="~/.config/dunst/icons/vol"

case "$1" in
i)  
  if [[ $vol -lt 100 ]]; then
    pactl set-$type-volume $target +${step}%
  else
    pactl set-$type-volume $target 100%
  fi
  notify_vol
  ;;
d) pactl set-$type-volume $target -${step}%; notify_vol ;;
m) pactl set-$type-mute $target toggle; notify_mute ;;
    *) print_error ;;
esac

