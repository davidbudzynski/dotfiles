#!/bin/sh
XDG_SEAT_PATH="/org/freedesktop/DisplayManager/Seat0" dm-tool lock && systemctl suspend
