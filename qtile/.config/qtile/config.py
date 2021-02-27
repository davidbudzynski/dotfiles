# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import CurrentLayoutIcon
import os
import subprocess

# startup apps 

@hook.subscribe.startup_once

def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

mod = "mod4"
terminal = 'alacritty'
browser = "firefox"
editor = "emacsclient -n -c -a emacs"

keys = [
    # this toggles the floating / tiling window mode
    # Key([mod], "n", lazy.window.toggle_floating()),

    # Switch between windows in current stack pane
    Key([mod], "h", lazy.layout.left(),
        desc = "move focus in stack pane to the left"),
    Key([mod], "l", lazy.layout.right(),
        desc = "move focus in stack pane to the right"),
    Key([mod], "j", lazy.layout.down(),
        desc = "move focus down in stack pane"),
    Key([mod], "k", lazy.layout.up(),
        desc = "move focus up in the stack pane"),

    #  Move windows in current stack
    Key([mod, "shift"], "h", lazy.layout.swap_left(),
        desc = "move window left in current stack"),
    Key([mod, "shift"], "l", lazy.layout.swap_right(),
        desc = "move window right in current stack"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc = "move window down in current stack"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(),
        desc = "move window up in current stack"),

    # customize window sizes
    Key([mod], "i", lazy.layout.grow(),
        desc = "increase size of window in focus"),
    Key([mod], "m", lazy.layout.shrink(),
        desc = "decrease size of window in focus"),
    Key([mod], "n", lazy.layout.reset(),
        desc = "reset window sized back to default"),
    Key([mod], "o", lazy.layout.maximize(),
        desc = "maximize the size of the focused window"),
    Key([mod, "shift"], "space", lazy.layout.flip(),
        desc = "flip master/stack positions"),

    # Switch window focus to other pane(s) of stack
    Key([mod], "Tab", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"),

    # Swap panes of split stack
    # Key([mod, "shift"], "space", lazy.layout.rotate(),
    #    desc="Swap panes of split stack"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key(["mod1"], "space", lazy.spawn("rofi -show drun -show-icons -theme-str 'element-icon {size: 2.5ch;}'"), desc="Launch rofi"),
    Key([mod], "e", lazy.spawn(editor), desc="Launch emacs"),
    Key([mod], "w", lazy.spawn(browser), desc="Launch Firefox"),
    # Key([mod], "f", lazy.spawn("alacritty -e ranger"), desc="Launch Ranger"),
    # fix for issues with ranger opening and resizing
    # described here: https://groups.google.com/g/qtile-dev/c/mjMKB533GNA/m/f0UGhBxpDgAJ
    Key([mod], "f", lazy.spawn("alacritty -e /home/david/.config/qtile/ranger-startup-fix.sh"), desc="Launch Ranger"),
    Key([mod, "control"], "l", lazy.spawn("/home/david/.config/qtile/lock-and-suspend.sh"), desc="sleep and suspend"),

    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),

    # toggle the status bar
    Key([mod], "b", lazy.hide_show_bar(), desc = "toggle the status bar"),

    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc = "turn off the bar and go full screen mode"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.MonadTall(
        margin = 5,
        border_width = 2,
        # revert to default so the layout icon can work
        # name = "[]=",
        border_focus = "cc241d",
        border_normal = "#282828"
        ),
    layout.Max(
       # name = "[M]"
    ),
    # layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    layout.MonadWide(
        # name = "TTT"
    ),
    # layout.RatioTile(),
    layout.Tile(
        # name = 'floating'
    ),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    # font = 'Source Code Pro Bold',
    font = 'SFMono Nerd Font Mono Bold',
    fontsize = 12,
    padding = 3,
    # atom one dark colorscheme
    # background = "#282C34",
    # foreground = "#ABB2BF",
    background = "#282828",
    foreground = "#ebdbb2",
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    active = "#ebdbb2",
                    highlight_method = "block",
                    rounded = False,
                    this_current_screen_border = "#98971a",
                    use_mouse_wheel = False
                ),
                CurrentLayoutIcon(
                    scale = 0.7
                ),
                widget.WindowName(),
                widget.Systray(),
                widget.Clock(format='%b %d %A %H:%M:%S'),
            ],
            size = 23,
            opacity = 0.90,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
    # {'wmclass': 'mpv'},  # mpv
    # firefox closing tab prompt (change?)
    {'wname': 'Quit and close tabs?'},
    {'wname': 'Close tabs?'},
    {"wmclass": "flameshot"},
    {"wname": "Picture-in-Picture"}
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
