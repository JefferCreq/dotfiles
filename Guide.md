# Personal Guide

## During Installation

```bash
pacman -S --needed dhcpcd sddm bash-completion base-devel git waybar swww \
rofi-wayland pacman -S pacman-contrib alacritty feh ueberzug \
lsd bat npm ranger zathura zathura-pdf-mupdf noto-fonts-emoji \
python python-pip obsidian tk xclip zip unzip dunst playerctl \
upower zsh zsh-syntax-highlighting zsh-autosuggestions \
wget bluez bluez-utils blueman wlsunset cliphist \
pipewire pipewire-alsa pipewire-pulse pipewire-jack \
pavucontrol nemo qt5-wayland qt6-wayland obs-studio \
xdg-desktop-portal-hyprland polkit-kde-agent \
capitaine-cursors adw-gtk-theme \
ttf-dejavu ttf-liberation adobe-source-han-sans-otc-fonts
```

### Installing AUR helper
```bash
cd /opt
sudo git clone https://aur.archlinux.org/yay.git
sudo chown -R <username>:<username> ./yay
cd yay
makepkg -si
```


### Initial AUR pacakages
```bash
yay -S brave-bin ttf-cascadia-code-nerd ttf-montserrat spotify wlogout \
hyprpicker hyprshot gnome-pomodoro-git tela-circle-icon-theme-grey \
```

### Enable Sddm
```bash
systemctl enable sddm.service
```

### Internet connection:
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


