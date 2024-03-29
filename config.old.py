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

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from Spotify import Spotify

import os
import subprocess
from libqtile import hook

from subprocess import run


def toggle_music(qtitle):
    run(
        "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.chrome /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause",
        shell=True,
    )


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([home])


mod = "mod4"
terminal = "alacritty"
browser = "google-chrome-stable"
promt = "rofi -show run"
musicPlayer = "spotify LD_PRELOAD=/usr/local/lib/spotify-adblock.so"
volumUp = "amixer -q sset Master 5%+"
volumDown = "amixer -q sset Master 5%-"
warpd = "warpd --normal"
code = "code"
screenshot = "flameshot gui"
rofi = "rofi -show drun"

# toggleMpd = "mpc toggle"
toggleMpd = (
    "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause",
)


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "a", lazy.spawn("sh ~/rely.sh"), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.next(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.previous(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new coalsamixer lumn.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If cjurrent window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
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
    Key([mod], "f", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "r", lazy.spawn(promt), desc="Launch promt"),
    Key([mod], "m", lazy.spawn(musicPlayer), desc="Launch music player"),
    Key([mod], "u", lazy.spawn(volumUp), desc="Volumn up"),
    Key([mod], "i", lazy.spawn(volumDown), desc="Volumn down"),
    Key([mod], "y", lazy.function(toggle_music), desc="Toggle mpd"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "t", lazy.reload_config(), desc="Reload the config"),
    Key([mod], "r", lazy.spawn(warpd), desc="Reload the config"),
    Key([mod], "e", lazy.spawn(code), desc="Reload the config"),
    Key([mod], "p", lazy.spawn(screenshot), desc="Reload the config"),
    Key([mod], "o", lazy.spawn(rofi), desc="Move window focus to other window"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

# groups = [Group(i) for i in "123456789"]


groups = [
    Group(
        "1",
        label="一",
    ),
    Group(
        "2",
        label="二",
    ),
    Group(
        "3",
        label="三",
    ),
    Group(
        "4",
        label="四",
    ),
    Group("5", label="五"),
    Group("0", label="愛"),
]


for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4, margin=8),
    layout.Max(margin=12),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(margin=8, ratio=0.75),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="jetbrains mono nerd font",
    fontsize=16,
    padding=2,
)
extension_defaults = widget_defaults.copy()

colors = ["#FF7721", "#FF679A", "#00BBDC", "#0077DD"]

bgColor = "#EE1166"

textColor = "#575279"
# have window open text color
activeColor = "#ffffff"
# does not have window open text color
inactiveColor = "#b3b1b1"
# border/line color
highlightColor = colors[1]
highlightTextColor = "#ffffff"
fontSize = 16


def wrapWidget(widgets, bgColor, icon=""):
    return [
        widget.TextBox(text="", foreground=bgColor, padding=0, fontsize="30"),
        widget.TextBox(
            text=icon,
            background=bgColor,
        ),
        *widgets,
        widget.TextBox(text=" ", foreground=bgColor, padding=0, fontsize="30"),
    ]


def wrapWidget2(widgets, bgColor, fgColor, icon=""):
    return [
        widget.TextBox(
            text=" ", foreground=fgColor, background=bgColor, padding=0, fontsize="30"
        ),
        widget.TextBox(
            text=icon,
            background=fgColor,
        ),
        *widgets,
    ]


screensold = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    fontsize=fontSize,
                    margin_y=3,
                    margin_x=6,
                    padding_y=7,
                    padding_x=6,
                    borderwidth=4,
                    active=activeColor,
                    # does not have window open text color
                    inactive=inactiveColor,
                    rounded=False,
                    highlight_color=inactiveColor,
                    highlight_method="block",
                    this_current_screen_border=highlightColor,
                    block_highlight_text_color=highlightTextColor,
                ),
                widget.Spacer(),
                *(
                    wrapWidget2(
                        [
                            Spotify(
                                fontsize=fontSize,
                                background=colors[1],
                                format="{track}",
                            ),
                        ],
                        "",
                        colors[1],
                        " ",
                    )
                ),
                *(
                    wrapWidget2(
                        [
                            widget.PulseVolume(
                                fontsize=fontSize,
                                background=colors[2],
                            ),
                        ],
                        colors[1],
                        colors[2],
                        "墳",
                    )
                ),
                *(
                    wrapWidget2(
                        [
                            widget.Memory(
                                fontsize=fontSize,
                                background=colors[3],
                            ),
                        ],
                        colors[2],
                        colors[3],
                        "", 
                    )
                ),
                *(
                    wrapWidget2(
                        [
                            widget.Clock(
                                format="%d/%m/%y %H:%M",
                                background=colors[0],
                            ),
                        ],
                        colors[3],
                        colors[0],
                        " ",
                    )
                ),
            ],
            32,
            opacity=0.95,
            background=bgColor,
            # margin=[8,2,0,2]
        ),
    ),
]

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    fontsize=fontSize,
                    margin_y=3,
                    margin_x=6,
                    padding_y=6,
                    padding_x=6,
                    borderwidth=4,
                    active=activeColor,
                    # does not have window open text color
                    inactive=inactiveColor,
                    rounded=False,
                    highlight_color="1F2122",
                    highlight_method="line",
                    this_current_screen_border=highlightColor,
                    block_highlight_text_color=highlightTextColor,
                ),
                widget.Spacer(),
                widget.TextBox(text=" ", foreground="#FF679A" , fontsize="16"),
                Spotify(
                    fontsize=fontSize,
                    format="{track}",
                    foreground="#FF679A"
                ),
                widget.Spacer(),
                widget.TextBox(text="墳 ", foreground="#00BBDC", fontsize="16"),
                widget.PulseVolume(
                    fontsize=fontSize,
                    foreground="#00BBDC"
                ),
                widget.Spacer(length=20),
                widget.TextBox(text="", foreground="#FF7721" , fontsize="16"),
                widget.Memory(
                    fontsize=fontSize,
                    measure_mem="G",
                    foreground="#FF7721"
                ),
                widget.Spacer(length=20),
                widget.TextBox(text=" ", foreground="#0077DD" , fontsize="16"),
                widget.Clock(
                    format="%d/%m/%y %H:%M",
                    foreground="#0077DD"
                ),
            ],
            32,
            opacity=0.95,
            background="1F2122",
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
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
