#! /bin/bash
monitors=$(hyprctl monitors | tr '\n' '\a')
activemonitor=$(grep -Po 'Monitor((?!Monitor).)*?focused: yes' <<<"$monitors" | tr '\a' '\n' | awk 'NR==1 {print $2}')
passivemonitor=$(grep -Po 'Monitor((?!Monitor).)*?focused: no' <<<"$monitors" | tr '\a' '\n' | awk 'NR==1 {print $2}')
passivews=$(grep -Po 'Monitor((?!Monitor).)*?focused: no' <<<"$monitors" | tr '\a' '\n' | awk '/active workspace/ {print $3}')
activews=$(grep -Po 'Monitor((?!Monitor).)*?focused: yes' <<<"$monitors" | tr '\a' '\n' | awk '/active workspace/ {print $3}')


if [[ -z $1 ]]; then
  workspace="$passivews"
else
  workspace="$1"
fi

# workspace="$1"

if [[ $workspace -eq $passivews ]] && [[ $activemonitor != "$passivemonitor" ]]; then
  hyprctl dispatch moveworkspacetomonitor "$activews" "$passivemonitor"
fi

hyprctl dispatch moveworkspacetomonitor "$workspace" "$activemonitor"
hyprctl dispatch workspace "$workspace"
