---
title: Fish Shell 
publish_date:  2022-05-24
summary: 'Friendly interactive shell es el nombre de una shell de Unix que pretende ser interactiva y amigable para el usuario, al contrario de otras shells.'
---

[![My Fish Shell](/fish.png)](https://fishshell.com)]

 La meta de diseño de ***fish*** es dar al usuario un conjunto diverso de poderosas características de una manera fácil de descubrir, recordar y usar ***fish*** es considerado un ***"shell exótica"***, ya que su sintaxis no deriva ni de una ***Bourne shell (ksh, bash, zsh)*** ni de alguna ***C shell (csh, tcsh)***. También, al contrario de otras shells, que desabilitan algunas características para cuidar los recursos del sistema, ***fish*** habilita todas las características por defecto.
 
 ### con opciones como:
* Autosugerencias
* 256 colores de terminal
* Configuración basada en la web
* Mejoras en el rendimiento (al disponer de más módulos integrados).

Te voy a dar un ejempo de ***Arch*** de como uso fish en mi terminal.

### Instalar Fish

```bash
pacman -S fish
```

o usando yay

```bash
yay -S fish
```

en OpenBSD

```ksh
pkg_add fish
```

## Configurar Fish

En mis maquinas suelo utilizar un lanzador ya sea con un Launcher o usando Keybindings.

Ejemplo:

```bash
alacritty -e fish
```

### Instalar Fisher  
plugin manager para ***Fish*** Administra funciones, finalizaciones, enlaces y fragmentos desde la línea de comandos. Amplíe sus capacidades de shell, cambie el aspecto de su indicador y cree configuraciones repetibles en diferentes sistemas sin esfuerzo.

```bash
curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source && fisher install jorgebucaran/fisher
```


### Plugins Recomendados:

* [fzf.fish](https://github.com/PatrickF1/fzf.fish)

* [Z - Directory Jumper](https://github.com/jethrokuan/z)

* [Fish logo](https://github.com/laughedelic/fish_logo)

#### Aqui te dejo lista oficial de plugins:

[Listado de Plugins](https://git.io/awesome.fish)

### Themes
aqui te dejo el equivalente a ohmyzsh o framework manager para ***Fish***, de varios que eh usado como "ohmyfish" en cambio uso el que instalamos fisher, aqui te dejo el que yo uso.

[SpaceFish GitHub](https://github.com/matchai/spacefish)

y para instalarlo:

```bash
$ fisher install matchai/spacefish
```

### Automatico con Tmux
Realmente asi es como uso fish con tmux y lo que hago es que automaticamente abro tmux ya tengo mi fish y las funciones que sin mucho esfuerzo hacen de la terminal un espacio hasta mas comodo de trabajar.

agrega esto en tu .tmux.conf

```bash
# SHELL
set-option -g default-shell /bin/fish
```
