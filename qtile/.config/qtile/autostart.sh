#!/bin/sh
# wallpaper
feh --bg-scale ~/Downloads/jeremy-bishop-2e3hgvDnCpM-unsplash.jpg &
# clipboard manager
copyq &
# screenshot utility
flameshot &
# network applet
nm-applet &
# xfce settings GUI daemon
xfsettingsd &
# gnome polkit
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
# power management and power icon
xfce4-power-manager &
# volume icon
volumeicon &
# x11 compositor
picom &
# notifications
dunst &
# emacs daemon
emacs --daemon &
# conky system monitor
conky &
