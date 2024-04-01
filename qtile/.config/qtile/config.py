# Config by David Budzynski

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

from posixpath import expanduser
from typing import List  # noqa: F401
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import (
    Click,
    Drag,
    Group,
    Key,
    KeyChord,
    Screen,
    ScratchPad,
    DropDown,
    Match,
)
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import CurrentLayoutIcon
import os, subprocess, psutil

# startup apps


@hook.subscribe.startup_once
def autostart():
    autostart_path = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.call([autostart_path])


# swallow windows
# taken from https://github.com/qtile/qtile/issues/1771
# @hook.subscribe.client_new
# def _swallow(window):
#     pid = window.window.get_net_wm_pid()
#     ppid = psutil.Process(pid).ppid()
#     cpids = {
#         c.window.get_net_wm_pid(): wid for wid, c in window.qtile.windows_map.items()
#     }
#     for i in range(5):
#         if not ppid:
#             return
#         if ppid in cpids:
#             parent = window.qtile.windows_map.get(cpids[ppid])
#             parent.minimized = True
#             window.parent = parent
#             return
#         ppid = psutil.Process(ppid).ppid()


# @hook.subscribe.client_killed
# def _unswallow(window):
#     if hasattr(window, "parent"):
#         window.parent.minimized = False
# window swallow ends here


mod = "mod4"
terminal = "alacritty"
browser = "firefox-developer-edition"
# editor = "emacsclient -n -c -a emacs"
editor = "code"
home = os.path.expanduser("~")


@lazy.function
def float_to_front(qtile) -> None:
    """Bring all floating windows of the group to front"""
    for window in qtile.current_group.windows:
        if window.floating:
            window.cmd_bring_to_front()


# key names for keys other than letters are weird they are all described here:
# https://github.com/qtile/qtile/blob/master/libqtile/xkeysyms.py
keys = [
    Key(
        [mod],
        "g",
        float_to_front(),
        desc="if a floating window becomes buried under tiled windows, bring it to the front",
    ),
    # this toggles the floating / tiling window mode
    Key([mod], "t", lazy.window.toggle_floating()),
    # Switch between windows in current stack pane
    Key([mod], "h", lazy.layout.left(), desc="move focus in stack pane to the left"),
    Key([mod], "l", lazy.layout.right(), desc="move focus in stack pane to the right"),
    Key([mod], "j", lazy.layout.down(), desc="move focus down in stack pane"),
    Key([mod], "k", lazy.layout.up(), desc="move focus up in the stack pane"),
    Key([mod], "c", lazy.window.center(), desc="center floating window"),
    #  Move windows in current stack
    Key(
        [mod, "shift"],
        "h",
        lazy.layout.swap_left(),
        desc="move window left in current stack",
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.swap_right(),
        desc="move window right in current stack",
    ),
    Key(
        [mod, "shift"],
        "j",
        lazy.layout.shuffle_down(),
        desc="move window down in current stack",
    ),
    Key(
        [mod, "shift"],
        "k",
        lazy.layout.shuffle_up(),
        desc="move window up in current stack",
    ),
    # for column stack layout
    # TODO maybe figure out a different keybinding becasue it clashes with
    # monad tall shink/grow
    # Key([mod, "control"], "n", lazy.layout.grow_left()),
    # Key([mod, "control"], "m", lazy.layout.grow_right()),
    # column stack layout end
    # customize window sizes
    Key([mod], "equal", lazy.layout.grow(), desc="increase size of window in focus"),
    Key([mod], "minus", lazy.layout.shrink(), desc="decrease size of window in focus"),
    Key([mod], "n", lazy.layout.reset(), desc="reset window sized back to default"),
    Key(
        [mod],
        "o",
        lazy.layout.maximize(),
        desc="maximize the size of the focused window",
    ),
    Key(
        [mod, "shift"], "space", lazy.layout.flip(), desc="flip master/stack positions"
    ),
    # Switch window focus to other pane(s) of stack
    Key(
        [mod],
        "Tab",
        lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack",
    ),
    # Swap panes of split stack
    # Key([mod, "shift"], "space", lazy.layout.rotate(),
    #    desc="Swap panes of split stack"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key(
        ["mod1"],
        "space",
        lazy.spawn(
            "rofi -show drun -show-icons -theme-str 'element-icon {size: 2.5ch;}'"
        ),
        desc="Launch rofi",
    ),
    Key([mod], "period", lazy.spawn("rofi -show emoji"), desc="launch emoji selector"),
    Key([mod], "e", lazy.spawn(editor), desc="Launch code editor"),
    Key([mod], "w", lazy.spawn(browser), desc="Launch Firefox"),
    # Key([mod], "f", lazy.spawn("alacritty -e ranger"), desc="Launch Ranger"),
    # fix for issues with ranger opening and resizing
    # described here: https://groups.google.com/g/qtile-dev/c/mjMKB533GNA/m/f0UGhBxpDgAJ
    # Key(
    #     [mod],
    #     "f",
    #     # lazy.spawn("alacritty -e /home/david/.config/qtile/ranger-startup-fix.sh"),
    #     # finally relative paths are working!
    #     # for spawning an app with its own window  in a script or a script that
    #     #  won't need to run in a window, simply use home + "whatever path to script"
    #     lazy.spawn(
    #         "" + terminal + " -e " + home + "/.config/qtile/ranger-startup-fix.sh"
    #     ),
    #     desc="Launch Ranger",
    # )
    Key(
        [mod],
        "f", 
        lazy.spawn("wezterm -e yazi"),
        desc = "Launch yazi (better ranger alternative) in wezterm (perhaps better default terminal alternative)"
    ),
    Key(
        [mod, "control"],
        "l",
        lazy.spawn("betterlockscreen -s blur"),
        desc="lock using betterclockscreen with blur effect and suspend",
    ),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="take a screenshot"),
    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),
    # toggle the status bar
    Key([mod], "b", lazy.hide_show_bar(), desc="toggle the status bar"),
    Key(
        [mod, "shift"],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="turn off the bar and go full screen mode",
    ),
    # dropdown apps
    KeyChord(
        [mod],
        "d",
        [
            Key([], "m", lazy.group["scratchpad"].dropdown_toggle("mixer")),
            Key([], "t", lazy.group["scratchpad"].dropdown_toggle("term")),
        ],
    ),
    # volume and media keys
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn(home + "/.config/qtile/volume-control.sh toggle"),
        # lazy.spawn("amixer -D pulse sset Master toggle"),
        desc="Mute audio",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn(home + "/.config/qtile/volume-control.sh down"),
        # lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -2%"),
        desc="Volume down",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn(home + "/.config/qtile/volume-control.sh up"),
        # lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +2%"),
        desc="Volume up",
    ),
    # Brightness - not working yet
    # Key([], "XF86MonBrightnessDown",
    #     lazy.spawn(home + "/.local/bin/statusbar/brightnesscontrol down"),
    #     desc='Brightness down'
    #     ),
    # Key([], "XF86MonBrightnessUp",
    #     lazy.spawn(home + "/.local/bin/statusbar/brightnesscontrol up"),
    #     desc='Brightness up'
    #     ),
    # Media keys - not wokring yet (need to get them to work on bare metal)
    Key(
        [],
        "XF86AudioPlay",
        lazy.spawn("playerctl play-pause"),
        desc="Audio play-pause toggle",
    ),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Audio next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl next"), desc="Audio previous"),
]

groups = [
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "term",
                "alacritty",
                on_focus_lost_hide=True,
                height=0.65,
                opacity=0.95,
                warp_pointer=True,
            ),
            DropDown(
                "mixer",
                "pavucontrol",
                height=0.6,
                width=0.4,
                on_focus_lost_hide=True,
                opacity=1,
                warp_pointer=True,
                x=0.3,
                y=0.2,
            ),
        ],
    ),
]

workspaces = [
    # exmaple of matching workspace with an app
    # {"name": "1", "key": "1", "matches": [Match(wm_class="firefox")]},
    {"name": "1", "key": "1", "matches": [Match(wm_class="firefoxdeveloperedition")]},
    {"name": "2", "key": "2", "matches": [Match(wm_class="code")]},
    {"name": "3", "key": "3", "matches": []},
    {"name": "4", "key": "4", "matches": []},
    {"name": "5", "key": "5", "matches": []},
    {"name": "6", "key": "6", "matches": []},
    {"name": "7", "key": "7", "matches": []},
    {"name": "8", "key": "8", "matches": []},
    {"name": "9", "key": "9", "matches": []},
    {"name": "10", "key": "0", "matches": [Match(wm_class="Signal")]},
]

for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    groups.append(Group(workspace["name"], matches=matches, layout="monadtall"))
    keys.append(Key([mod], workspace["key"], lazy.group[workspace["name"]].toscreen()))
    keys.append(
        Key(
            [mod, "shift"],
            workspace["key"],
            lazy.window.togroup(workspace["name"], switch_group=True),
        )
    )


layout_theme = {
    "margin": 20,
    "border_width": 5,
    "border_focus": "#cc241d",
    "border_normal": "#282828",
}

colors = {
    "background": ["#1d1f21"],
    "foreground": ["#c4c8c5"],
    "highlight": ["#313335"],
    "inactive": ["#545B68"],
    "active": ["#ecf0ed"],
    "red": ["#cc6666"],
    "blue": ["#80a1bd"],
    "green": ["#b5bd68"],
}

layouts = [
    layout.MonadTall(
        **layout_theme,
        new_client_position="bottom",
        single_border_width=0,
        single_margin=0,
    ),
    layout.Max(),
    # layout.Stack(
    # **layout_theme,
    # num_stacks=2
    # ),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    layout.Columns(
        # **layout_theme,
        border_width=5,
        num_columns=3,
        border_on_single=True,
        insert_position=1,
    ),
    # layout.Matrix(),
    layout.MonadWide(**layout_theme),
    layout.MonadThreeCol(**layout_theme),
    # layout.RatioTile(),
    # layout.Tile(),
    layout.TreeTab(
        fontsize=21,
        sections=[""],
        section_fontsize=0,
        section_top=0,
        section_bottom=0,
        border_width=5,
        bg_color=colors["background"],
        active_bg=colors["highlight"],
        active_fg=colors["active"],
        inactive_bg=colors["background"],
        inactive_fg=colors["inactive"],
        padding_left=0,
        padding_x=0,
        padding_y=5,
        level_shift=8,
        vspace=3,
        panel_width=400,
    ),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    # layout.Slice(),
    layout.Floating(),
]

widget_defaults = dict(
    # font="Source Code Pro Bold",
    font="Cascadia Code",
    fontsize=21,
    padding=3,
    background=colors["background"],
    foreground=colors["foreground"],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(length=5),
                widget.CurrentScreen(
                    fontsize=30,
                    active_text="",
                    inactive_text="",
                    active_color=colors["active"],
                    inactive_color=colors["foreground"],
                    padding=10,
                ),
                widget.Spacer(length=5),
                widget.GroupBox(
                    active=colors["foreground"],
                    inactive=colors["inactive"],
                    urgent_border=colors["red"],
                    urgent_text=colors["foreground"],
                    highlight_color=colors["background"],
                    this_current_screen_border=colors["foreground"],
                    this_screen_border=colors["foreground"],
                    other_current_screen_border=colors["blue"],
                    other_screen_border=colors["blue"],
                    highlight_method="line",
                    rounded=False,
                    use_mouse_wheel=False,
                    fontsize=20,
                    borderwidth=4,
                    disable_drag=True,
                ),
                CurrentLayoutIcon(scale=0.6),
                widget.WindowName(),
                # instead of title for a focused window, you can opt in for a
                # list of windows and their icons
                # widget.TaskList(title_width_method="uniform"),
                widget.Spacer(length=10),
                widget.Systray(icon_size=28),
                widget.Spacer(length=10),
                widget.WidgetBox(
                    text_closed="...",
                    close_button_location="right",
                    text_open="...",
                    widgets=[
                        widget.Spacer(length=10),
                        # note that when adding widgets emojis push the text more to
                        # the center so clock appears to be a bit lower than widgets.
                        widget.Wttr(
                            location={"Droylsden": "Droylsden"},
                            # json=False,
                            # if format removed it will include default
                            # format="MAN: %t",
                            #
                            # see this link for details:
                            # https://github.com/chubin/wttr.in#one-line-output
                            format="2",
                        ),
                        widget.Spacer(length=10),
                        widget.Volume(
                            # fmt="\U0001f50a {}",  # speaker emoji and percentage
                            fmt="🔊 {}",
                            mute_command="amixer -D pulse sset Master toggle",
                            volume_app="pavucontrol",
                            get_volume_command="amixer -D pulse get Master".split(),
                            volume_up_command="pactl set-sink-volume @DEFAULT_SINK@ +2%",
                            volume_down_command="pactl set-sink-volume @DEFAULT_SINK@ -2%",
                            padding=0,
                        ),
                        widget.Spacer(length=10),
                        widget.DF(
                            visible_on_warn=False,
                            format="💾 {uf}{m}",
                        ),
                        widget.Spacer(length=10),
                    ],
                ),
                # widget.Sep(linewidth=3, padding=20, size_percent=40),
                widget.Spacer(length=10),
                widget.KeyboardLayout(
                    configured_keyboards=["us", "us intl", "pl"],
                    display_map={"us": "🇺🇸", "us intl": "🇪🇺", "pl": "🇵🇱"},
                    fontsize=30,
                    mouse_callbacks={
                        "Button1": lazy.widget["keyboardlayout"].next_keyboard()
                    },
                ),
                widget.Spacer(length=10),
                widget.Clock(
                    format="%Y-%m-%d %A %H:%M:%S",
                    mouse_callbacks={
                        "Button1": lambda: qtile.cmd_spawn(
                            "alacritty -e emacs -nw --eval '(progn (calendar))'"
                        )
                    }
                    # mouse_callbacks={
                    # "Button1": lambda: qtile.cmd_spawn("alacritty --hold -e cal -3")
                    # },
                ),
                widget.Spacer(length=10),
            ],
            size=40,
            opacity=1,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True

floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="flameshot"),
        Match(title="Picture-in-Picture"),
        Match(title="Secure CRAN mirrors"),
        Match(wm_class="r_x11"),
        Match(wm_class="Signal"),
    ],
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.

wmname = "LG3D"
