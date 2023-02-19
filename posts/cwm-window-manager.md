---
title: CWM Window Manager 
publish_date:  2023-02-18
summary: 'cwm: un administrador de ventanas liviano y eficiente para X11'
---

[![My CWM pimp](/my-cwm-openbsd.png)](https://man.openbsd.org/cwm.1)


cwm es un administrador de ventanas para X11 que contiene muchas características que se concentran 
en la eficiencia y transparencia de la administración de ventanas, manteniendo la estética más simple 
y agradable.

Viene incluido en OpenBSD asi com fvwm y twm.

Aqui te dejo mi sencillo pero elegante configuracion..


```
borderwidth 1
color inactiveborder "#ebdbb2"
color activeborder "#ebdbb2"
color font "#ebdbb2"
color selfont "#282828"
color menubg "#282828"
color menufg "#ebdbb2"
color groupborder "#686868"
color ungroupborder "#7c7c7c"
unbind-key all

gap 10 40 10 10

bind-key 4-1  group-only-1
bind-key 4-2  group-only-2
bind-key 4-3  group-only-3
bind-key 4-4  group-only-4
bind-key 4-5  group-only-5
bind-key 4-f window-fullscreen
bind-key 4S-x xlock
bind-key 4-x scratchterm
bind-key 4C-q dsession
bind-key 4-i window-cycle
bind-key 4-h window-move-left
bind-key 4-j window-move-down
bind-key 4-k window-move-up
bind-key 4-l window-move-right
bind-key 4-t "st -g 110x30"
bind-key 4-c window-close
bind-key 4-d "dmenu_run"
bind-key 4-w "rofi -show window"
bind-key 4-space "rofi -show run"
bind-key 4C-h window-resize-left
bind-key 4C-j window-resize-down
bind-key 4C-k window-resize-up 
bind-key 4C-l window-resize-right
bind-key 4S-h window-move-left-big
bind-key 4S-j window-move-down-big
bind-key 4S-k window-move-up-big
bind-key 4S-l window-move-right-big
bind-key 4S-Up window-htile
bind-key 4S-Left window-vtile
bind-key 4S-Right window-snap-down-right
bind-key 4C-r restart
bind-key 4S-q "pkill cwm"
bind-mouse M-3 window-resize
bind-mouse M-2 window-lower
bind-mouse M-1 window-move

autogroup 1 "urxvt,URxvt"
autogroup 2 "Navigator,Firefox"

ignore lemonbar
ignore dunst

window-hmaximize 11 
window-vmaximize 34

moveamount 5
snapdist 5
sticky yes

command "           terminal -" "st -g 100x30"
command "            firefox -" "firefox"
command "               lock -" "xlock -mode pacman & zzz"
command "            suspend -" "zzz"
command "               exit -" "pkill cwm"

```

[My cwmrc en Github](https://gist.github.com/dev1lsconf/cae520cbb960d346d9aba1ec71b597b3)
