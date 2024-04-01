#!/bin/sh
# wallpaper
feh --bg-scale --randomize ~/Pictures/wallpapers/*
# network applet
nm-applet &
disown
blueman-applet &
disown
# clipboard manager
# QT_SCALE_FACTOR=0.75
copyq &
disown
# screenshot utility
flameshot &
disown
# gnome polkit
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
disown
# x11 compositor
picom &
disown
# emacs daemon
emacs --daemon &
disown
# conky system monitor
#conky &
# music player daemon
# mpd &
# playerctl daemon (to enable play/pause with media keys)
# playerctld daemon
# enable changing play/pause for mpd clients
# mpDris2 &
# mouse software if logitech is used
# solaar -w=hide -b=solaar & disown
# notifications
dunst &
disown
# blue screen reduction, automatically get location
redshift-gtk -l $(curl -s "https://location.services.mozilla.com/v1/geolocate?key=geoclue" | awk 'OFS=":" {print $3,$5}' | tr -d ',}') &
disown
# power manager
xfce4-power-manager &
disown
# run caffeine to prevent sleep when playing media
caffeine &
disown
firefox-developer-edition &
disown
signal-desktop &
disown
code &
disown

# fix keyboard settings (decrease delay and increase repeat)
#xset r rate 200 30
