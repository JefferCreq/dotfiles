# █▀█ ▀█▀ █ █░░ █▀▀
# ▀▀█ ░█░ █ █▄▄ ██▄

# Imports {{{
import os
import subprocess

from libqtile.config import Group, Key, Match, Screen, Click, Drag
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal, send_notification
from libqtile import qtile, hook, layout, widget, bar
# from qtile_extras import bar, widget
# from qtile_extras.widget import modify
from themes import Theme
from widgets.spotify import Spotify, SpotifyIcon
from widgets.pomodoro import Pomodoro, PomoIcon
from widgets.gmail import Gmail, GmailIcon
# from widgets.arcobattery import BatteryIcon
from widgets.groupbox import CustomGroupBox
from widgets.network import WiFiIcon
from widgets.upower import UPowerWidget

# import psutil
# import socket
# }}}

# Definitions {{{
home = os.path.expanduser('~')
MOD = "mod4"
terminal = guess_terminal()
theme = Theme["catppuccin_mocha"]
SCALE_QTILE = 2

DEFAULT_FONT = 'CaskaydiaCove Nerd Font SemiBold'
ICON_FONT = 'Symbols Nerd Font Mono'
ICON_AWESOME_FONT = 'Font Awesome 6 Free'
ICON_FONT_SIZE = 13*SCALE_QTILE
ITALIC_FONT = 'CaskaydiaCove Nerd Font Mono Bold Italic'

BAR_SIZE = 25*SCALE_QTILE
BAR_SEP = 12*SCALE_QTILE

ACCENT_COLOR = theme['magenta']
BAR_BG = theme['background']
# }}}

# Keybindings {{{

# Lazy functions {{{
@lazy.function
def change_layout(qtile):
    send_notification("Layout", message=str(
        qtile.current_layout.name), urgent=False, timeout=1200)


LEVEL_VOL = 0.05

@lazy.function
def change_spotify_volume(qtile, level):
    c = '+' if level == "up" else '-'
    subprocess.run(["playerctl", "volume", str(
        LEVEL_VOL) + c, "-p", "spotify"])
    volume = subprocess.run(["playerctl", "volume", "-p", "spotify"],
                            stdout=subprocess.PIPE, text=True)
    current_vol = float(volume.stdout) * 100
    subprocess.run(["dunstify", "-a", 'spotifyvolume', '-u', 'low',
                    '-r', '9993', '-h', 'int:value:' + str(current_vol),
                    'Volume:' + f' {current_vol:.0f}%', '-t', '2000', '-i', 'spotify'])


launch_rofi = 'rofi -show drun'
launch_rofi_powermenu = 'rofi -show power-menu -modi power-menu:~/.config/rofi/scripts/rofi-power-menu'

if SCALE_QTILE > 1:
    launch_rofi += ' -dpi 192'
    launch_rofi_powermenu += ' -dpi 192'



# }}}

keys = [
    # Switch between windows
    Key([MOD], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([MOD], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([MOD], "j", lazy.layout.down(), desc="Move focus down"),
    Key([MOD], "k", lazy.layout.up(), desc="Move focus up"),
    Key([MOD], "Tab", lazy.layout.next(),
        desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([MOD, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([MOD, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([MOD, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([MOD, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([MOD, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([MOD, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([MOD, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([MOD, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([MOD], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([MOD], "b", lazy.hide_show_bar(), desc="Toggle bar"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [MOD, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([MOD], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([MOD, "shift"], "Tab", lazy.next_layout(),
        change_layout, desc="Toggle between layouts"),
    Key([MOD, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([MOD, "mod1"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([MOD, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([MOD, "mod1"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([MOD], "t", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),


    # Audio

    Key([], 'XF86AudioLowerVolume', lazy.spawn(
        home + '/.local/bin/volume down')),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn(home + '/.local/bin/volume up')),
    Key([], 'XF86AudioMute', lazy.spawn(home + '/.local/bin/volume mute')),
    Key([], 'XF86AudioPrev', lazy.spawn('playerctl previous -p spotify')),
    Key([], 'XF86AudioNext', lazy.spawn('playerctl next -p spotify')),
    Key([], 'XF86AudioPlay', lazy.spawn('playerctl play-pause -p spotify')),

    # window

    Key([MOD], 'space', lazy.spawn(launch_rofi)),
    Key([MOD], 'r', lazy.spawn(
        'alacritty -t "Ranger" -e ranger ' + home)),
    Key([MOD], 'w', lazy.spawn('brave --profile-directory="Default"')),
    Key([MOD, "shift"], 'w', lazy.spawn(
        'brave --profile-directory="Default" --incognito')),
    Key([MOD], 'p', lazy.spawn(
        'brave --profile-directory="Profile 1"')),
    Key([MOD, "shift"], 's', lazy.spawn(home + '/.local/bin/screenshot')),
    Key(["mod1"], 'F4', lazy.spawn(launch_rofi_powermenu)),
    Key([MOD], 's', lazy.window.toggle_floating()),


    Key([MOD], 'quoteleft', lazy.screen.toggle_group(),
        desc="Move to the last visited group"),
    Key([MOD, "shift"], 'quoteleft', lazy.next_screen(),
        desc="Move to the last visited group"),
    Key([MOD, "mod1"], "space", lazy.widget["keyboardlayout"].next_keyboard(),
        desc="Next keyboard layout."),
    Key([MOD, "control"], "equal", change_spotify_volume("up")),
    Key([MOD, "control"], "minus", change_spotify_volume("down")),

    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("light -A 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("light -U 5")),
]
# }}}

# Groups {{{
# groups = [
#     Group('1', label="", layout='columns'),
#     Group('2', label="", layout='columns'),
#     Group('3', label="", matches=[Match(wm_class='obsidian')], layout='tile'),
#     Group('4', label="", matches=[Match(wm_class='obs')]),
#     Group('5', label="", matches=[Match(wm_class='zoom ')], layout='max'),
#     # Group('6', label="", layout='max'),
#     Group('6', label="", matches=[Match(wm_class='spotify')], layout='max'),
# ]

groups = [
    Group('1', label="ﱣ", layout='columns'),
    Group('2', label="ﱣ", layout='columns'),
    Group('3', label="ﱣ", matches=[Match(wm_class='obsidian')], layout='tile'),
    Group('4', label="ﱣ", matches=[Match(wm_class='obs')]),
    Group('5', label="ﱣ", matches=[Match(wm_class='zoom ')], layout='max'),
    Group('6', label="ﱣ", matches=[Match(wm_class='spotify')], layout='max'),
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [MOD],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [MOD, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(
                    i.name),
            ),
        ]
    )

# }}}

# Layouts {{{
layout_defaults = {
    "border_focus": theme["white"],
    "border_normal": theme["background"],
    "border_width": 2,
    "margin": 4,
}

layouts = [
    layout.Columns(**layout_defaults),
    layout.Max(
        border_width=0,
               ),
    layout.MonadTall(**layout_defaults),
    layout.MonadWide(**layout_defaults,),
    layout.Tile(**layout_defaults,),
]


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
        Match(title="Settings"),
        Match(title="Ranger"),
    ],
    border_focus=theme["red"],
    border_normal=theme["black"]
)
# }}}

# Screens {{{

# Bar options {{{

widget_defaults = dict(
    font=DEFAULT_FONT,
    fontsize=14*SCALE_QTILE,
    padding=3,
    background=BAR_BG,
    foreground=theme["foreground"],
)

extension_defaults = widget_defaults.copy()

# }}}

# Mouse Callbacks {{{
def open_gmail():
    qtile.cmd_spawn(
        'google-chrome-stable --profile-directory="Profile 2" https://mail.google.com/')


def spotify_action():
    if ("spotify" in (i.name() for i in psutil.process_iter())):
        qtile.cmd_spawn('playerctl play-pause -p spotify')
    else:
        qtile.cmd_spawn('spotify')
# }}}

# Widgets {{{
def groupBox(bg):
    return [
        CustomGroupBox(
            active=theme["black"],
            inactive=theme["black"],
            this_current_screen_border=ACCENT_COLOR,
            this_screen_border=ACCENT_COLOR,
            other_current_screen_border=theme["white"],
            other_screen_border=theme["white"],
            highlight_method='text',
            font=ICON_FONT,
            padding_x=6*SCALE_QTILE,
            margin_x=0,
            fontsize=ICON_FONT_SIZE,
            background=bg,
            disable_drag=True,
        ),
    ]


def windowName(bg, fg):
    return [
        widget.WindowName(
            font=ITALIC_FONT,
            fontsize=13*SCALE_QTILE,
            foreground=fg,
            background=bg,
            max_chars=80,
            for_current_screen=True,
            padding=20,
        ),
        # widget.Chord(
        #     chords_colors={
        #         "launch": ("#F28FAD", "#D9E0EE"),
        #     },
        #     name_transform=lambda name: name.upper(),
        # ),
        # widget.Prompt(),
        # widget.Systray(
        #     background=bg,
        #     icon_size=15,
        #     padding=10,
        #     # **decor3,
        # ),
        # widget.Spacer(length=BAR_SEP+8, background=bg),
    ]


def gmail_widget(bg, fg):
    gmail_list = [
        my_gmail := Gmail(
            font=DEFAULT_FONT,
            foreground=fg,
            background=bg,
            padding=2,
            fontsize=13*SCALE_QTILE,
            mouse_callbacks={"Button1": open_gmail},
        ),
        GmailIcon(
            font=DEFAULT_FONT,
            foreground=fg,
            background=bg,
            color_active=fg,
            color_inactive=theme["black"],
            fontsize=16*SCALE_QTILE,
            padding=7,
            mouse_callbacks={"Button1": open_gmail},
            gmail_object=my_gmail,
        ),
    ]
    return reversed(gmail_list)


def pomodoro_wdiget(bg, fg):
    pomodoro_list = [
        my_pomdoro := Pomodoro(
            font=DEFAULT_FONT,
            background=bg,
            padding=2,
            fontsize=13*SCALE_QTILE,
            color_active=fg,
            color_break=theme["black"],
            color_inactive=theme["black"],
        ),
        PomoIcon(
            font=DEFAULT_FONT,
            background=bg,
            color_active=fg,
            color_break=theme["black"],
            color_inactive=theme["black"],
            fontsize=17*SCALE_QTILE,
            padding=6,
            pomo_object=my_pomdoro,
        ),
    ]
    return reversed(pomodoro_list)


def customWidgets(bg:str, fg:str, spotify:bool = True, gmail:bool = True,
        pomodoro:bool = True):
    widgetlist = []
    if spotify:
        widgetlist.extend([
            widget.Spacer(length=BAR_SEP, background=bg),
            SpotifyIcon(
                   font=ICON_FONT,
                   foreground=theme["green"],
                   background=bg,
                   fontsize=ICON_FONT_SIZE,
                   padding=8,
                   mouse_callbacks={
                    "Button1": lazy.spawn('playerctl play-pause -p spotify'),
                    "Button3": lazy.spawn('killall spotify')},
                   ),
            Spotify(
                   name='spotify',
                   objname="org.mpris.MediaPlayer2.spotify",
                   display_metadata=['xesam:title', 'xesam:artist'],
                   scroll_chars=18,
                   scroll_interval=1,
                   scroll_wait_intervals=0,
                   stop_pause_text='',
                   foreground=fg,
                   mouse_callbacks={"Button1": lazy.spawn(
                       'playerctl play-pause -p spotify'), },
                   background=bg,
                   ),
            widget.Spacer(length=BAR_SEP, background=bg)])

    if pomodoro:
        widgetlist.extend([*pomodoro_wdiget(bg, fg),
            widget.Spacer(length=BAR_SEP, background=bg)])

    if gmail:
        widgetlist.extend([
            *gmail_widget(bg, fg),
            widget.Spacer(length=BAR_SEP, background=bg),
        ])

    widgetlist.extend([
        widget.TextBox(
            text='',
            foreground=theme["yellow"],
            background=bg,
            fontsize=ICON_FONT_SIZE,
            font=ICON_AWESOME_FONT,
        ),
        widget.KeyboardLayout(
                          foreground=fg,
                          background=bg,
                          configured_keyboards=['us', 'us intl'],
                          display_map={'us': 'us', 'us intl': 'in'}
                          ),
        widget.Spacer(length=BAR_SEP, background=bg),
        widget.TextBox(
                text='',
                padding=6,
                foreground=theme["red"],
                background=bg,
                fontsize=ICON_FONT_SIZE,
                font=ICON_AWESOME_FONT,
            ),

        # widget.WidgetBox(widgets=[
            widget.CheckUpdates(
                update_interval=900,
                custom_command="checkupdates",
                display_format="{updates}",
                foreground=fg,
                background=bg,
                colour_have_updates=fg,
                no_update_string='0',
                colour_no_updates=fg,
            ),
        # ],
        #     text_closed='',
        #     text_open='',
        #     foreground=theme["blue"],
        #     background=bg,
        #     fontsize=ICON_FONT_SIZE+2,
        #     font=ICON_FONT,
        # ),
        # widget.Spacer(length=BAR_SEP, background=bg),
        ])
    return widgetlist

def widgetBox(bg, fg):
    return [
        widget.Spacer(length=BAR_SEP, background=bg),
        widget.WidgetBox(widgets=[
            # widget.Spacer(length=BAR_SEP, background=bg),
            # widget.TextBox(  # **decor,
            #     text='',
            #     padding=6,
            #     foreground=theme["green"],
            #     background=bg,
            #     fontsize=ICON_FONT_SIZE,
            #     font=ICON_AWESOME_FONT,
            # ),
            # widget.Net(#**decor1,
            #        interface="enp4s0f3u1u1u3",
            #        # interface="enp4s0f3u1u4",
            #        format='{down} ↓↑ {up}',
            #        ),
            # widget.Spacer(length=BAR_SEP, background=bg),
            widget.TextBox(
                text='',
                padding=6,
                foreground=theme["magenta"],
                background=bg,
                fontsize=ICON_FONT_SIZE,
                font=ICON_AWESOME_FONT
            ),
            widget.Memory(#**decor1,
                    format='{MemUsed:.2f}{mm}',
                    measure_mem='G',
                    background=bg,
                    ),
            widget.Spacer(length=BAR_SEP, background=bg),
            widget.TextBox(
                text='',
                padding=6,
                foreground=theme["cyan"],
                background=bg,
                fontsize=ICON_FONT_SIZE,
                font=ICON_AWESOME_FONT
            ),
            widget.CPU(
                       format='{load_percent:04}%',
                        background=bg,
                       ),
            widget.Spacer(length=BAR_SEP, background=bg),
        ],
            close_button_location='right',
            text_closed='  ',
            text_open=' ',
            foreground=theme["black"],
            background=bg,
            fontsize=ICON_FONT_SIZE,
            font=ICON_FONT,
        ),
    ]


def clockWidget(bg, fg):
    return [
        widget.TextBox(
            text='',
            foreground=fg,
            background=bg,
            fontsize=ICON_FONT_SIZE,
            font=ICON_AWESOME_FONT,
            padding=8,
        ),
        widget.Clock(
            # format="%a %d/%m %I:%M %p",
            format="%I:%M %p",
            foreground=fg,
            background=bg,
            width=bar.CALCULATED,
        ),
        widget.Spacer(length=8*SCALE_QTILE, background=bg),
    ]

def laptopWidgets(bg, fg):
    return [
        # widget.Spacer(length=BAR_SEP-(4*SCALE_QTILE), background=bg),
        # widget.Backlight()
        widget.Systray(
            background=bg,
            icon_size=16*SCALE_QTILE,
            padding=10*SCALE_QTILE,
        ),
        widget.Spacer(length=BAR_SEP-(4*SCALE_QTILE), background=bg),
        WiFiIcon(
            active_colour=theme["white"],
            inactive_colour=theme["black"],
            foreground=fg,
            padding=12,
        ),
        widget.Spacer(length=BAR_SEP-(6*SCALE_QTILE), background=bg),
        UPowerWidget(
            border_charge_colour=theme["blue"],
            border_colour=theme["white"],
            border_critical_colour=theme["red"],
            fill_critical=theme["red"],
            fill_low=theme["magenta"],
            fill_normal=theme["white"],
            foreground=fg,
            battery_height=10*SCALE_QTILE,
            battery_width=20*SCALE_QTILE,
        ),
        widget.Spacer(length=BAR_SEP-(6*SCALE_QTILE), background=bg),
    ]

# }}}

# KikaiBar {{{
kikaiBar = bar.Bar(
    [
        *groupBox(theme["background"]),
        *windowName(theme["background"], theme["white"]),
        *customWidgets(theme["background"], theme["foreground"]),
        *widgetBox(theme["background"], fg=theme["foreground"]),
        *clockWidget(theme["background"], fg=theme["foreground"]),
    ],
    BAR_SIZE,
    border_width=[0, 0, 0, 0],  # Draw top and bottom borders
    border_color=[theme["background"], "000000", theme["background"], "000000"],
    opacity=1,
)
# }}}
# DellBar {{{
dellBar = bar.Bar(
    [
        *groupBox(BAR_BG),
        *windowName(bg=BAR_BG, fg=theme["white"]),
        widget.Spacer(),
        *clockWidget(bg=BAR_BG, fg=theme["foreground"]),
        widget.Spacer(),
        *widgetBox(bg=BAR_BG, fg=theme["foreground"]),
        *customWidgets(bg=BAR_BG, fg=theme["foreground"],
                       pomodoro=False, gmail=False),
        *laptopWidgets(bg=BAR_BG, fg=theme["foreground"]),
    ],
    BAR_SIZE,
    border_width=[0, 0, 0, 0],  # Draw top and bottom borders
    border_color=[BAR_BG, "000000", BAR_BG, "000000"],
)
# }}}

# topBar = dellBar if (socket.gethostname() == "creq") else kikaiBar
screens = [Screen(top=dellBar), ]
# screens = [Screen(), ]
# }}}

# Mouse {{{
mouse = [
    Drag([MOD], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([MOD], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([MOD], "Button2", lazy.window.bring_to_front()),
]
# }}}

# Additional configs {{{
dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "LG3D"

execCommands = [
    "feh --bg-fill /home/jeffer/.config/.wallpaper &",
    # "xrandr --output eDP-1 --mode 1440x900 &",
    # "picom --config ~/.config/picom/picom.conf &",
    "picom &",
    # "redshift -P -O 3500 &",
]

# if (socket.gethostname() == "ArchSUS"):
    # execcommands.append("xrandr --output edp-1 --mode 1440x900 &")


for x in execCommands:
    os.system(x)
# }}}

# hooks {{{


@hook.subscribe.startup_once
def autostart():
    subprocess.run([home + '/.config/qtile/autostart.sh'])


@hook.subscribe.focus_change
def float_to_front():
    """
    Bring floating Ranger window to front
    """
    for window in qtile.current_group.windows:
        if window.floating and window.name == "Ranger":
            window.cmd_bring_to_front()
            window.focus()
            break


@lazy.function
def _show_current_layout(qtile):
    subprocess.run(["dunstify", "-a", 'Layout', '-u', "normal",
                   "Layout", str(qtile.current_layout.name)],)


@hook.subscribe.layout_change
def show_current_layout():
    _show_current_layout()
# }}}

# Reload config from terminal:
# qtile cmd-obj -o cmd -f reload_config
# qtile cmd-obj -o cmd -f restart

# vim:foldmethod=marker
