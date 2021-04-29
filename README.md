# DOT INSTALL

Installing dependencies for dotfiles
```
sudo pacman -S kitty firefox htop sxhkd nitrogen vim picon zathura rofi pcmanfm sxhkd nitrogen bluez-utils
```

Install yay 

```
cd /opt
sudo git clone https://aur.archlinux.org/yay-git.git
sudo chown -R USER:USER ./yay-git/
cd yay-git
makepkg -si
```

Install polybar and fonts
```
yay -S picom-jonaburg-git polybar ttf-iosevka-ss08 ttf-font-awesome
```
