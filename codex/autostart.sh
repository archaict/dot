#!/bin/sh
mpd &
dunst &
sxhkd &
locker &
tilda &
# xfce4-power-manager &
polybar -r bar &
dropbox &
# unclutter &
light -S 20 &
xset b off &
xset r rate 200 &
nitrogen --restore &
picom --experimental-backend &
emacs --daemon &
systemctl --user enable --now emacs &
setxkbmap -option caps:super &
xmodmap ~/.Xmodmap &
xfce4-clipman &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
