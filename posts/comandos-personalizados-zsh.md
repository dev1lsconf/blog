---
title: Personalizando comandos en zsh
summary: 'Z shell es un potente intérprete de comandos para sistemas operativos de tipo Unix, como por ejemplo los BSD o GNU/Linux.​ La primera versión de zsh fue escrita por Paul Falstad en 1990, cuando era estudiante en la Universidad de Princeton. Zsh se diseñó para poder usarse interactivamente.'
publish_date: '2022-05-10'
tags: ['terminal', 'ZSH', 'Hack']
---

Siempre fui usuario de [Bash](https://es.wikipedia.org/wiki/Bash), pero luego de ser usuario de mac por algunos años pues le di una oportunidad a zsh y ya es algo esencial en mi entorno de trabajo y de mi uso cotidiano.

zsh, Tiene la particularidad de tener muchas modificaciones y alta colaboracion en plugins de aspecto como tambien de ulitidades muy de moda actualmentes como [PowerLevel10k](https://github.com/romkatv/powerlevel10k) y otras funciones muy elegantes algunas practicas otras puras monerias.

Pero hoy vengo a explicar algo muy simple y es como crear un comando personalizado para tu terminal zsh.
Lo primero es que vamos abrir el rc del zsh para agregar nuestras lineas personalizadas en algunos casos como en el mio el archivo a modificar en .zshrc-personal para no hacer estos comandos globales.
**_( me gusta vim o neovim pero el ejemplo lo haremos con nano.. hahahaha )_**

```bash
nano ~/.zshrc
```

y al final de la configuracion agregaremos nuestra lineas bien comentadas. En mi caso usaremos el ejemplo de Simples Aliases.. puedes verificar otras opciones dependiendo tu comando y la escala del mismo. [CheatSheet](https://github.com/ohmyzsh/ohmyzsh/wiki/Cheatsheet)

```bash
alias <custom-alias>=”<command>”
```

es la referencia segun el man de zsh, asi que vamos a crear nuestro comando en mi caso sera [Browsh](https://www.brow.sh/) ya que no me gusto el metodo de instalacion nativa en Arch/linux ( use yay ) asi que buscando en el github de browsh veo que puedo correr un docker que usa la aplicacion demo que esta disponible online y como es solo para buscar cosas rapido en consola sin tener que moverme de entorno, asi que mi comando perzonalizado seria:

```bash
docker run --rm -it browsh/browsh
```

AL final nuesta modificacion deberia quedar asi.

```
# Comandos Personalizados Dev1ls
alias browshy="docker run --rm -it browsh/browsh"
```

y luego de cerrar y guardar nuestro archivo podemos abrir una nueva terminal y probar nuestro archivo.
