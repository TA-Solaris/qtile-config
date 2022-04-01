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

import os
import json

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
#from libqtile.utils import guess_terminal

with open("{}/.config/qtile/config/settings.json".format(os.getenv("HOME"))) as file:
    settings = json.load(file)

looks: dict = settings["looks"]

with open("{}/.config/qtile/config/colours.json".format(os.getenv("HOME"))) as file:
    colours_json = json.load(file)

colours = colours_json

mod = "mod4"
terminal = "alacritty"
browser = "opera"
filemanager = "pcmanfm"
editor = "code"
launcher = "rofi -show run"
snip = "ksnip --rectarea"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "j", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "k", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "i", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "j", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "i", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "j", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "k", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "i", lazy.layout.grow_up(), desc="Grow window up"),
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
    Key([mod], "g", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "e", lazy.spawn(filemanager), desc="Launch filemanager"),
    Key([mod], "v", lazy.spawn(editor), desc="Launch editor"),
    # Toggle between different layouts as defined belowR
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "x", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([mod], "a", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "a", lazy.spawn(launcher), desc="Spawn an application using launcher"),
    Key([mod, "shift"], "s", lazy.spawn(snip), desc="Use snipping tool"),
]

groups = [Group(f"circle{i}", layout="max", label="circle") for i in "123456789"]

for i, group in enumerate(groups):
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                str(i+1),
                lazy.group[group.name].toscreen(),
                desc="Switch to group {}".format(group.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                str(i+1),
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme = {
    "border_width": 2,
    "margin": 24,
    "border_focus": colours["border_focus"],
    "border_normal": colours["border_normal"],
}

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    # layout.Floating(**layout_theme)
]

widget_defaults = dict(
    font=looks["main_font"],
    fontsize=15,
    padding=3,
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
        widget.Sep(
            linewidth = 0,
            padding = 6,
            foreground=colours["fg"],
            background=colours["bg"],
        ),
        widget.WindowName(
            foreground=colours["fg"],
            background=colours["bg"],
            padding=10,
        ),
        widget.Spacer(
            foreground=colours["fg"],
            background=colours["bg"],
        ),
        widget.TextBox(
            text = "chevron-left",
            font = looks["caret_font"],
            foreground=colours["fg"],
            background=colours["bg"],
            padding = 12,
            fontsize = 20
        ),
        widget.GroupBox(
            font=looks["caret_font"],
            borderwidth=3,
            active=colours["active"],
            inactive=colours["inactive"],
            rounded=False,
            highlight_method="line",
            highlight_color=colours["bg"],
            this_current_screen_border=colours["current_screen_tab"],
            this_screen_border=colours["fg"],
            other_screen_border=colours["bg"],
            foreground=colours["fg"],
            background=colours["bg"],
            max_chars=1,
        ),
        widget.TextBox(
            text = "chevron-right",
            font = looks["caret_font"],
            foreground=colours["fg"],
            background=colours["bg"],
            padding = 12,
            fontsize = 20
        ),
        widget.Spacer(
            foreground=colours["fg"],
            background=colours["bg"],
        ),
        widget.TextBox(
            text = "chevron-left",
            font = looks["caret_font"],
            foreground=colours["fg"],
            background=colours["bg"],
            padding = 12,
            fontsize = 20
        ),
        widget.CurrentLayout(
            foreground=colours["fg"],
            background=colours["bg"],
            padding = 10
        ),
        widget.Sep(
            linewidth = 0,
            padding = 20,
            foreground=colours["fg"],
            background=colours["bg"],
        ),
        widget.TextBox(
            text = "atlassian", #looks close enough to arch idc
            font = looks["brands_font"],
            foreground=colours["fg"],
            background=colours["bg"],
            padding = 0
        ),
        widget.CheckUpdates(
            update_interval = 1800,
            distro = "Arch_checkupdates",
            display_format = "Updates: {updates} ",
            no_update_string = "Up to date",
            foreground=colours["fg"],
            background=colours["bg"],
            colour_have_updates = colours["colour2"],
            colour_no_updates = colours["colour1"],
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + " -e sudo pacman -Syu")},
            padding = 5,
        ),
        widget.Sep(
            linewidth = 0,
            padding = 20,
            foreground=colours["fg"],
            background=colours["bg"],
        ),
        widget.TextBox(
            text = "headphones",
            font = looks["caret_font"],
            foreground=colours["fg"],
            background=colours["bg"],
            padding = 0
        ),
        widget.PulseVolume(
            foreground=colours["fg"],
            background=colours["bg"],
            padding = 5,
            fmt = "{}"
        ),
        widget.Sep(
            linewidth = 0,
            padding = 20,
            foreground=colours["fg"],
            background=colours["bg"],
        ),
        widget.TextBox(
            text = "battery-full",
            font = looks["caret_font"],
            foreground=colours["fg"],
            background=colours["bg"],
            padding = 0
        ),
        widget.Battery(
            foreground=colours["fg"],
            background=colours["bg"],
            padding = 5,
            format = "{percent:2.0%}"
        ),
        widget.Sep(
            linewidth = 0,
            padding = 10,
            foreground=colours["fg"],
            background=colours["bg"],
        ),
        widget.TextBox(
            text = "chevron-left",
            font = looks["caret_font"],
            foreground=colours["fg"],
            background=colours["bg"],
            padding = 12,
            fontsize = 20
        ),
        widget.Clock(
            foreground=colours["fg"],
            background=colours["bg"],
            format="%a, %b %y %H:%M:%S ",
            padding = 10
        )
    ]
    return widgets_list

bar_margin = 0

screens = [
    Screen(
        top=bar.Bar(
            init_widgets_list(),
            int(looks["panel-size"]),
            background=colours["bg"],
            opacity=float(looks["panel-opacity"]),
            margin=bar_margin,
        ),
    ),
    Screen(
        top=bar.Bar(
            init_widgets_list(),
            int(looks["panel-size"]),
            background=colours["bg"],
            opacity=float(looks["panel-opacity"]),
            margin=bar_margin,
        ),
    ),
    Screen(
        top=bar.Bar(
            init_widgets_list(),
            int(looks["panel-size"]),
            background=colours["bg"],
            opacity=float(looks["panel-opacity"]),
            margin=bar_margin,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
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
