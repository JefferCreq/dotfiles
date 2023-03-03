# Personal Guide

## During Installation

```bash
pacman -S dhcpcd lightdm lightdm-gtk-greeter bash-completion
```

Internet connection:
- List network interfaces with `ip link`.
- With `systemctl list-units | grep dhcp` we can see if DHCP client is already runnig.
- Start the client by `systemctl start dhcpcd@*interface*`.
- Check the adapter properties with `ip address`.

## After Installation
### Wired connection
First internet conection :
- List network interfaces with `ip link`.
- Start the client by `systemctl start dhcpcd@*interface*` (wired connection dynamic ip).
- Check the internet with `ping google.com`.
- Enable the client by `systemctl enable dhcpcd@*interface*` (wired connection dynamic ip).

### Wireless connection with iwd
```bash
sudo systemctl start iwd
sudo systemctl start systemd-resolved.service
```

Edit `/etc/iwd/main.conf`
```
[General]
EnableNetworkConfiguration=true

[Network]
NameResolvingService=systemd
```

Try `ping google.com`, if everything work:
```bash
sudo systemctl enable iwd
sudo systemctl enable systemd-resolved.service
```

### Additional pacakages
```bash
pacman -S pacman-contrib alacritty feh ueberzug \
rofi light lsd bat neofetch npm ranger zathura \
zathura-pdf-mupdf ttf-font-awesome redshift python \
python-pip obsidian tk xclip zip unzip dunst playerctl \
upower zsh zsh-syntax-highlighting zsh-autosuggestions \
nvidia-lts xf86-input-libinput
```

### Installing AUR helper
```bash
pacman -S --needed git base-devel && git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si
```

General pacakages
```bash
yay -S brave-bin nerd-fonts-jetbrains-mono \
ttf-material-design-icons spotify picom-git
```

Lightdm:
```bash
systemctl enable lightdm
```
### Preparing the Configuration File for bspwm and sxhkd
```bash
mkdir -p ~/.config/bspwm
mkdir -p ~/.config/sxhkd
cp /usr/share/doc/bspwm/examples/bspwmrc ~/.config/bspwm
cp /usr/share/doc/bspwm/examples/sxhkdrc ~/.config/sxhkd
```

We have to change the terminal emulator in `~/.config/sxhkd`
```
# terminal emulator
super + Return
    alacritty
```
Then we reboot.

### Installing Dotfiles

[The best way to store your dotfiles: A bare Git repository](https://www.atlassian.com/git/tutorials/dotfiles)

```bash
echo ".dotfiles" >> .gitignore
git clone --bare https://github.com/JefferCreq/dotfiles.git $HOME/.dotfiles
function config {
   /usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME $@
}
mkdir -p .config-backup
config checkout
config config status.showUntrackedFiles no
```

### Touchpad config
`xf86-input-libinput` must be intalled.
``` bash
➜  ~ cat /etc/X11/xorg.conf.d/30-touchpad.conf
Section "InputClass"
    Identifier "devname"
    MatchIsTouchpad "true"
    Driver "libinput"
    Option "Tapping" "on"
    Option "NaturalScrolling" "true"
EndSection
```

