---
title: Doas My Friends! 
publish_date:  2023-06-30
summary: 'doas es un programa para ejecutar comandos como otro usuario, generalmente como root.doas fue desarrollado por Ted Unangst para OpenBSD como un reemplazo de sudo más simple y seguro.'
---

doas es el comando predeterminado de OpenBSD para ejecutar otros comandos con privilegios, funciona como Linux sudo y se introdujo en OpenBSD 5.8.

Al instalar OpenBSD, debe haber establecido una contraseña de cuenta raíz y su cuenta de usuario. Ahora deberá iniciar sesión en la cuenta raíz con el nombre de usuario raíz y la contraseña que eligió anteriormente.

OpenBSD proporciona una configuración predeterminada para doas en su carpeta /etc/examples, solo necesitamos copiarla en:

|   cp /etc/examples/doas.conf /etc/doas.conf

Con el archivo en su lugar, podemos editarlo y permitir que nuestro usuario normal lo use, puede usar vi o mg como vienen con el sistema.

En las últimas líneas del archivo debería ver una línea como permit keepenv :wheel debajo de ella puede configurar su acceso de usuario al grupo doas:

|   permitir keepenv nopass usuario

El permiso de comando le dará acceso a su usuario al grupo de ruedas, lo que le permitirá usar doas. Los otros dos son:

    keepenv: mantenga las variables ambientales de sus usuarios cuando use doas
    nopass: no pida una contraseña cuando use doas

Ambos argumentos se pueden mantener fuera de la línea, elige el que prefieras.

El archivo final se verá así:

# Permitir usuario por defecto
permiso keepenv :usuario
permitir keepenv nopass usuario

Ahora puede volver a iniciar sesión con su usuario y probar el comando doas, puede hacerlo de la siguiente manera:

gato doas /etc/doas.conf

Si se le solicita que ingrese su contraseña o se imprime el texto dentro del archivo, ¡Doas se ha configurado correctamente!

Fuente: https://bluesden.gitlab.io/the-code-den/posts/openbsd_doas/
