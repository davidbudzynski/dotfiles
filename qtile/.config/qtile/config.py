# ==============================================================================
# Qtile configuration by David Budzynski
# ==============================================================================
#
# A minimal, terminal-centric Qtile setup built around:
#   - MonadTall tiling (default) with Columns / TreeTab alternates
#   - Ghostty terminal, firefox-developer-edition, VS Code
#   - A caffeine toggle (systemd-inhibit) that prevents sleep/idle while
#     active - like Amphetamine on macOS - shown as a "☕ ON / ☕ OFF" pill
#     in the bar (left-click to toggle)
#
# Keybinding cheat-sheet (mod = Super/Win):
#   mod+x l/s/r/q/p/b     lock / suspend / reload / quit / poweroff / reboot
#   mod+Return             terminal            mod+w          browser
#   mod+e                  editor              mod+f          yazi file manager
#   mod+t                  toggle floating     mod+g          float window to front
#   mod+Space              next layout         mod+b          toggle bar
#   mod+h/l/j/k            move focus          mod+Shift+h/l/j/k  move window
#   mod+1..0               switch workspace    mod+Shift+1..0 move window to it
#   mod+q                  kill window         mod+Shift+f    fullscreen
#   alt+space              rofi launcher       mod+period     emoji picker
#   mod+d t/m              scratchpad: terminal / mixer
#   Print                  flameshot GUI       XF86* keys     volume & media
# ==============================================================================


# ==============================================================================
# IMPORTS
# ==============================================================================
import os
import re
import signal
import subprocess
from typing import Any

from libqtile import bar, layout, widget, hook
from libqtile.config import (
    Click,
    Drag,
    DropDown,
    Group,
    Key,
    KeyChord,
    Match,
    Screen,
    ScratchPad,
)
from libqtile.lazy import lazy
from libqtile.widget import CurrentLayout, base


# ==============================================================================
# DEFAULT APPLICATIONS & KEY MOD
# ==============================================================================
mod = "mod4"  # Super/Win key - main modifier for all keybindings
terminal = "ghostty"
browser = "firefox-developer-edition"
editor = "code"
home = os.path.expanduser("~")


# ==============================================================================
# THEME - colors, layout and widget styling
# ==============================================================================
colors = {
    "background": "#1d1f21",
    "foreground": "#c4c8c5",
    "highlight": "#313335",
    "inactive": "#545B68",
    "active": "#ecf0ed",
    "red": "#cc6666",
    "blue": "#80a1bd",
    "green": "#b5bd68",
}

layout_theme = {
    "margin": 20,
    "border_width": 5,
    "border_focus": "#cc241d",
    "border_normal": "#282828",
}

widget_defaults = dict(
    font="Cascadia Code",
    fontsize=21,
    padding=3,
    background=colors["background"],
    foreground=colors["foreground"],
)
extension_defaults = widget_defaults.copy()


# ==============================================================================
# HELPER FUNCTIONS & CUSTOM WIDGETS
# ==============================================================================
@lazy.function
def float_to_front(qtile) -> None:
    """Bring all floating windows of the group to the front."""
    for window in qtile.current_group.windows:
        if window.floating:
            window.cmd_bring_to_front()


# --- Caffeine: prevent sleep/idle while active (like Amphetamine on macOS) ---
# A `systemd-inhibit` process holds the lock; the widget polls for its state.
CAFFEINE_PIDFILE = "/tmp/qtile-caffeine.pid"
CAFFEINE_MARKER = "qtile-caffeine"


def caffeine_running() -> bool:
    """True if a systemd-inhibit caffeine process is alive."""
    return (
        subprocess.run(
            ["pgrep", "-f", f"systemd-inhibit.*{CAFFEINE_MARKER}"],
            capture_output=True,
        ).returncode
        == 0
    )


def start_caffeine() -> None:
    """Spawn systemd-inhibit holding a lock on idle and sleep."""
    stop_caffeine()
    proc = subprocess.Popen(
        [
            "systemd-inhibit",
            f"--who={CAFFEINE_MARKER}",
            "--what=idle:sleep",
            "--why=Caffeine toggle",
            "sleep",
            "infinity",
        ],
        start_new_session=True,
    )
    with open(CAFFEINE_PIDFILE, "w") as f:
        f.write(str(proc.pid))


def stop_caffeine() -> None:
    """Kill the caffeine process group and release the lock."""
    try:
        with open(CAFFEINE_PIDFILE) as f:
            pid = int(f.read().strip())
        os.killpg(pid, signal.SIGTERM)
    except (FileNotFoundError, ValueError, ProcessLookupError, PermissionError):
        pass
    finally:
        try:
            os.unlink(CAFFEINE_PIDFILE)
        except FileNotFoundError:
            pass


@lazy.function
def toggle_caffeine(qtile) -> None:
    if caffeine_running():
        stop_caffeine()
    else:
        start_caffeine()


class CaffeineToggle(base.InLoopPollText):
    """Pill-style bar widget; left-click to toggle caffeine on/off."""

    defaults = [
        ("update_interval", 2, "Poll interval in seconds"),
        ("on_text", "☕ ON", "Text when caffeine is active"),
        ("off_text", "☕ OFF", "Text when caffeine is inactive"),
        ("on_color", colors["green"], "Foreground color when active"),
        ("off_color", colors["inactive"], "Foreground color when inactive"),
    ]

    def __init__(self, **config):
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(CaffeineToggle.defaults)
        self.add_callbacks({"Button1": toggle_caffeine})

    def poll(self):
        if caffeine_running():
            self.foreground = self.on_color
            return self.on_text
        self.foreground = self.off_color
        return self.off_text


# ==============================================================================
# KEYBINDINGS
# ==============================================================================
keys = [
    # --- System & power (mod+x, then one of these) ---
    KeyChord(
        [mod],
        "x",
        [
            Key([], "l", lazy.spawn("betterlockscreen -s blur"), desc="Lock screen"),
            Key([], "s", lazy.spawn("systemctl suspend"), desc="Suspend system"),
            Key([], "r", lazy.reload_config(), desc="Reload Qtile config"),
            Key([], "q", lazy.shutdown(), desc="Shutdown/logout Qtile"),
            Key([], "p", lazy.spawn("poweroff"), desc="Power off machine"),
            Key([], "b", lazy.spawn("reboot"), desc="Reboot machine"),
        ],
    ),
    # --- Workspace switching ---
    # Quick back-and-forth between current and previous workspace
    Key(
        [mod],
        "BackSpace",
        lazy.screen.toggle_group(),
        desc="Switch to last visited workspace",
    ),
    # Cycle to next/previous workspace
    Key(
        [mod, "control"],
        "h",
        lazy.screen.prev_group(),
        desc="Move to workspace on left",
    ),
    Key(
        [mod, "control"],
        "l",
        lazy.screen.next_group(),
        desc="Move to workspace on right",
    ),
    # Shift focused window to next/previous workspace
    Key(
        [mod, "control", "shift"],
        "h",
        lazy.window.togroup_prev(),
        desc="Move window to workspace on left",
    ),
    Key(
        [mod, "control", "shift"],
        "l",
        lazy.window.togroup_next(),
        desc="Move window to workspace on right",
    ),
    # --- Window focus & floating ---
    Key(
        [mod],
        "g",
        float_to_front,
        desc="Bring buried floating window to the front",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating mode"),
    # Switch focus in current stack
    Key([mod], "h", lazy.layout.left(), desc="Move focus left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "c", lazy.window.center(), desc="Center floating window"),
    # Move windows in current stack
    Key([mod, "shift"], "h", lazy.layout.swap_left(), desc="Move window left"),
    Key([mod, "shift"], "l", lazy.layout.swap_right(), desc="Move window right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # --- Window sizing & layout management ---
    Key([mod], "equal", lazy.layout.grow(), desc="Increase window size"),
    Key([mod], "minus", lazy.layout.shrink(), desc="Decrease window size"),
    Key([mod], "n", lazy.layout.reset(), desc="Reset window size"),
    Key([mod], "o", lazy.layout.maximize(), desc="Maximize window size"),
    Key([mod, "shift"], "space", lazy.layout.flip(), desc="Flip master/stack"),
    Key([mod], "Tab", lazy.layout.next(), desc="Switch window focus"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle split/unsplit stack",
    ),
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "b", lazy.hide_show_bar(), desc="Toggle the status bar"),
    Key(
        [mod, "shift"],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen mode",
    ),
    # --- Spawning applications ---
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key(
        ["mod1"],
        "space",
        lazy.spawn(
            "rofi -show drun -show-icons -theme-str 'element-icon {size: 2.5ch;}'"
        ),
        desc="Launch rofi",
    ),
    Key([mod], "period", lazy.spawn("rofi -show emoji"), desc="Launch emoji selector"),
    Key([mod], "e", lazy.spawn(editor), desc="Launch code editor"),
    Key([mod], "w", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "f", lazy.spawn(f"{terminal} -e yazi"), desc="Launch yazi file manager"),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Take a screenshot"),
    # --- Scratchpad dropdowns (mod+d, then one of these) ---
    KeyChord(
        [mod],
        "d",
        [
            Key([], "m", lazy.group["scratchpad"].dropdown_toggle("mixer")),
            Key([], "t", lazy.group["scratchpad"].dropdown_toggle("term")),
        ],
    ),
    # --- Volume (PipeWire / PulseAudio) ---
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
        desc="Mute audio",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -2%"),
        desc="Volume down",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +2%"),
        desc="Volume up",
    ),
    # --- Media keys ---
    Key(
        [], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Audio play-pause"
    ),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Audio next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Audio previous"),
]


# ==============================================================================
# GROUPS & WORKSPACES
# ==============================================================================
# Scratchpads are togglable dropdown windows, available from any workspace
groups: list[Group] = [
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "term",
                terminal,
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

# Workspace definitions: name, group-switch key and windows that auto-match
workspaces: list[dict[str, Any]] = [
    {"name": "1", "key": "1", "matches": [Match(wm_class="firefoxdeveloperedition")]},
    {"name": "2", "key": "2", "matches": [Match(wm_class="emacs")]},
    {
        "name": "3",
        "key": "3",
        "matches": [
            Match(wm_class=re.compile(r"thunderbird", re.IGNORECASE)),
            Match(wm_class=re.compile(r"Mail", re.IGNORECASE)),
            Match(wm_class=re.compile(r"org.mozilla.Thunderbird", re.IGNORECASE)),
        ],
    },
    {"name": "4", "key": "4", "matches": [Match(wm_class="code")]},
    {"name": "5", "key": "5", "matches": []},
    {"name": "6", "key": "6", "matches": []},
    {"name": "7", "key": "7", "matches": []},
    {"name": "8", "key": "8", "matches": []},
    {"name": "9", "key": "9", "matches": []},
    {"name": "10", "key": "0", "matches": [Match(wm_class="signal")]},
]

# Build one Group per workspace plus its mod+key / mod+shift+key bindings
for workspace in workspaces:
    matches = workspace.get("matches", None)
    groups.append(Group(workspace["name"], matches=matches, layout="monadtall"))
    keys.extend(
        [
            Key([mod], workspace["key"], lazy.group[workspace["name"]].toscreen()),
            Key(
                [mod, "shift"],
                workspace["key"],
                lazy.window.togroup(workspace["name"], switch_group=True),
            ),
        ]
    )


# ==============================================================================
# MOUSE BINDINGS - drag and resize floating windows
# ==============================================================================
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod],
        "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size(),
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]


# ==============================================================================
# LAYOUTS - the first layout (monadtall) is the default
# ==============================================================================
layouts = [
    layout.MonadTall(
        **layout_theme,
        new_client_position="bottom",
        single_border_width=0,
        single_margin=0,
    ),
    layout.Max(),
    layout.Columns(
        border_width=5,
        num_columns=3,
        border_on_single=True,
        insert_position=1,
    ),
    layout.MonadWide(**layout_theme),
    layout.MonadThreeCol(**layout_theme),
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
    layout.Floating(),
]


# ==============================================================================
# SCREENS & STATUS BAR
# ==============================================================================
# Bar layout: [left: screen/workspaces] [center: window name]
#             [right: tray, volume, caffeine, keyboard, clock]
screens = [
    Screen(
        top=bar.Bar(
            [
                # --- Left: screen indicator, workspaces, layout icon ---
                widget.Spacer(length=5),
                widget.CurrentScreen(
                    fontsize=55,
                    active_text="",
                    inactive_text="",
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
                    fontsize=21,
                    borderwidth=5,
                    disable_drag=True,
                ),
                CurrentLayout(scale=0.7, mode="icon"),
                widget.Spacer(length=10),
                # --- Center: focused window name ---
                widget.WindowName(),
                widget.Spacer(length=10),
                # --- Right: tray, volume/disk, caffeine, keyboard, clock ---
                widget.Systray(icon_size=28),
                widget.Spacer(length=10),
                widget.WidgetBox(
                    text_closed="...",
                    close_button_location="right",
                    text_open="...",
                    widgets=[
                        widget.Spacer(length=10),
                        # Native PipeWire / PulseAudio widget
                        widget.Volume(
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
                            format="💾 {uf:.2f}{m}",
                        ),
                        widget.Spacer(length=10),
                    ],
                ),
                widget.Spacer(length=10),
                # Caffeine: click to keep the PC awake while downloading etc.
                CaffeineToggle(fontsize=21),
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
                        "Button1": lazy.spawn(
                            f"{terminal} -e emacs -nw --eval '(progn (calendar))'"
                        )
                    },
                ),
                widget.Spacer(length=10),
            ],
            size=40,
            opacity=1,
        ),
    ),
]


# ==============================================================================
# FLOATING WINDOW RULES - dialogs, prompts and misc apps float by default
# ==============================================================================
floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
        Match(wm_class="flameshot"),
        Match(title="Picture-in-Picture"),
        Match(title="Secure CRAN mirrors"),
        Match(wm_class="r_x11"),
        Match(wm_class="Signal"),
    ],
)


# ==============================================================================
# MISC SETTINGS - window management behaviour
# ==============================================================================
dgroups_key_binder = None                    # dgroups disabled (no key rules)
dgroups_app_rules: list[Any] = []            # no automatic app-to-group rules
follow_mouse_focus = True                    # focus follows the mouse pointer
bring_front_click = False                    # don't raise windows on click
cursor_warp = True                           # warp pointer to focused window
auto_fullscreen = True                       # windows requesting fullscreen get it
focus_on_window_activation = "smart"         # only steal focus when needed
reconfigure_screens = True                   # re-evaluate screens on hotplug
auto_minimize = True                         # minimize floating windows on focus loss
wmname = "LG3D"                              # compatibility with Java applications


# ==============================================================================
# STARTUP - run autostart.sh once when Qtile starts
# ==============================================================================
@hook.subscribe.startup_once
def autostart():
    autostart_path = os.path.expanduser("~/.config/qtile/autostart.sh")
    if os.path.exists(autostart_path):
        subprocess.Popen([autostart_path])
