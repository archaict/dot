import os, subprocess, psutil, socket

from typing import List
from libqtile import qtile,hook, bar, layout, widget
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.config import Click, Drag, Group, Screen, KeyChord, Key, Match

#============================= VARIABLES =============================#

# Dependencies [ KMONAD ]

TERM = "kitty"
FILE = "pcmanfm"
WEB = "firefox"
EMC = "emacsclient -c -a 'emacs'"
ROFI = "rofi -show "

# DefineMe

MTL = "monadtall" ; MAX = "max"
APA ="XF86AudioPause"; APL ="XF86AudioPlay"

MTT = "F1" ; MDN = "F2" ; MUP = "F3"  ; MIC = "F4"
REF = "F5" ; LCK = "F9" ; LUP = "F11" ; LDN = "F12"
UPS = "Up" ; DWN = "Down" ; LFT = "Left" ; RGT = "Right"

ALT = "mod1"      ; MOD = "mod4"
ESC = "Escape"    ; CTL = "control"; GRV = "grave"
BPC = "BackSpace" ; TAB = "Tab"    ; SHF = "shift"
SML = "semicolon" ; MIN = "minus"  ; EQL = "equal"
DEL = "Delete"    ; RET = "Return" ; INS = "Insert"
BSL = "backslash" ; SLS = "slash"  ; SPC = "space"
MSHF = [MOD,SHF]  ; MODS = [MOD]   ; MCTL = [MOD,CTL]
CCTL = [CTL]      ; AALT = [ALT]   ; MALT = [MOD,ALT]
MALS = [MOD,SHF,ALT]  ; EMPY = []

# Colors

BLACK  = "#222222"
GREY   = "#8B8B8B"

# Layouts

layouts = [
    layout.Max(),
    layout.MonadTall(
        margin = 8, ratio = 0.4979, change_ratio = 0.05,
        border_focus = GREY, border_normal = BLACK, border_width=3,
        single_margin = None, single_border_width = None )
]

groups        = [                                       ]
group_names   = [ "a"   , "s"   , "d"   , "o"   , "p"   ]
group_labels  = [ "DEV" , "WWW" , "BOX" , "MSC" , "VMS" ]
group_layouts = [ MTL   , MTL   , MTL   , MAX   , MAX   ]

for i in range(len(group_names)):
    groups.append( Group(
        name   = group_names[i],
        label  = group_labels[i],
        layout = group_layouts[i].lower()))

# Definition

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
widget_defaults = dict( font="Iosevka Bold", fontsize = 12,  background = BLACK, padding=2 )

#=========================== EOF VARIABLES ===========================#

keys = [

    # Navigation [ can be exposed through shell "qtile cmd-obj" ]
    Key( MODS , GRV , lazy.window.bring_to_front()),
    Key( MODS , "j" , lazy.layout.down()),
    Key( MODS , "k" , lazy.layout.up()),
    Key( MODS , "l" , lazy.layout.grow_main()),
    Key( MODS , "h" , lazy.layout.shrink_main()),
    Key( MODS , DWN , lazy.layout.shuffle_down()),
    Key( MODS , UPS , lazy.layout.shuffle_up()),
    Key( MODS , LFT , lazy.screen.prev_group()),
    Key( MODS , RGT , lazy.screen.next_group()),
    Key( MODS , "f" , lazy.next_layout()),
    Key( MCTL , "f" , lazy.window.toggle_floating()),
    Key( MODS , "q" , lazy.window.kill()),
    Key( MCTL , "r" , lazy.restart()),
    Key( MCTL , ESC , lazy.shutdown()),

    Key( MODS , SPC , lazy.spawn( ROFI + "run" )),
    Key( MODS , BSL , lazy.spawn( ROFI + "window" )),

]

for i in groups:
    keys.extend([
        Key( MODS , i.name, lazy.group[i.name].toscreen()),
        Key( MCTL , i.name, lazy.window.togroup(i.name))])

main = None
wmname = "LG3D"
cursor_warp = False
auto_fullscreen = False
dgroups_app_rules = []
dgroups_key_binder = None
follow_mouse_focus = True
bring_front_click = False
focus_on_window_activation = "smart"
extension_defaults = widget_defaults.copy()
screens = [ Screen (top=bar.Bar ([ ],0, background=BLACK ))] # Use polybar instead;

mouse = [

    Drag( MODS  , "Button3" , lazy.window.set_size_floating()     , start=lazy.window.get_size()),
    Drag( MODS  , "Button1" , lazy.window.set_position_floating() , start=lazy.window.get_position()),
    Click( MODS , "Button2" , lazy.window.bring_to_front() )

]

for key, x, y in [("h", -20, 0),
                  ("l", 20, 0),
                  ("k", 0, -20),
                  ("j", 0, 20)]:
    keys.append(Key( MALT, key, lazy.window.move_floating(x, y)))
    keys.append(Key( MALS, key, lazy.window.resize_floating(x, y)))

floating_layout = layout.Floating(
    border_focus = BLACK,
    float_rules=[
    {'wmclass' : 'confirm'},
    {'wmclass' : 'dialog'},
    {'wmclass' : 'download'},
    {'wmclass' : 'error'},
    {'wmclass' : 'file_progress'},
    {'wmclass' : 'notification'},
    {'wmclass' : 'splash'},
    {'wmclass' : 'toolbar'},
    {'wmclass' : 'confirmreset'},
    {'wmclass' : 'makebranch'},
    {'wmclass' : 'maketag'},
    {'wname'   : 'Picture-in-Picture'},
    {'wname'   : 'branchdialog'},
    {'wname'   : 'pinentry'},
    {'wname'   : 'Quit and close tabs?'},
    {'wname'   : 'Save Image'},
    {'wmclass' : 'polkit-gnome-authentication-agent-1'},
    {'wmclass' : 'ssh-askpass'},
    {'wmclass' : 'tilda'},
    Match(wm_class='steam')])

# Autostart

@hook.subscribe.startup_once    # [ Autostart ]
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/autostart.sh'])

@hook.subscribe.client_new      # [ Swallow ]
def _swallow(window):
    pid = window.window.get_net_wm_pid()
    ppid = psutil.Process(pid).ppid()
    cpids = {c.window.get_net_wm_pid(): wid for wid, c in window.qtile.windows_map.items()}
    for i in range(5):
        if not ppid:
            return
        if ppid in cpids:
            parent = window.qtile.windows_map.get(cpids[ppid])
            parent.minimized = True
            window.parent = parent
            return
        ppid = psutil.Process(ppid).ppid()

@hook.subscribe.client_killed
def _unswallow(window):
    if hasattr(window, 'parent'):
        window.parent.minimized = False
