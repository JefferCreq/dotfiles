# git
alias gcl 'git clone --depth 1'
alias gi 'git init'
alias ga 'git add'
alias gc 'git commit -m'
alias gp 'git push origin master'

# editar configs
alias vi nvim

alias r ranger
alias code 'code --enable-features=UseOzonePlatform --ozone-platform-hint=auto 2>/dev/null'

# cd shortcut
alias cdwrk 'cd /data/Workspace/'

# For .dotfiles
alias config '/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'

# Grub update
alias update-grub 'sudo grub-mkconfig -o /boot/grub/grub.cfg'

# otros
alias .. 'cd ..'
alias nf 'clear; neofetch'
alias mv 'mv -i'
alias rm 'rm -I'
# alias grep 'grep --color=auto'
alias wlan0_up 'sudo ip link set wlan0 up'
alias wlan0_down 'sudo ip link set wlan0 down'

# sincronizar hora
alias timesync 'sudo systemctl restart systemd-timesyncd'

