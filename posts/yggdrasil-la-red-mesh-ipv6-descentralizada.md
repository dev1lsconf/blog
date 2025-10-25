---
title: Yggdrasil - La Red Mesh IPv6 Descentralizada
publish_date: 2025-10-25
summary: ¿Pero qué pasaría si pudieras tener tu propia red global, cifrada de extremo a extremo, sin servidores centrales y accesible desde cualquier lugar? Eso es exactamente lo que propone Yggdrasil, una fascinante red mesh construida sobre los cimientos de IPv6
---

![ipv6 yggdrasil](/yggdrasil0.png)

# La Red Mesh IPv6 Descentralizada 

En este post, exploraremos qué es Yggdrasil, por qué es una idea tan poderosa y, lo más importante, cómo puedes implementarla de forma increíblemente sencilla usando NixOS.

## ¿Qué es Yggdrasil y por qué usa IPv6?

Yggdrasil es un proyecto de software libre que crea una red superpuesta (overlay network) global. Funciona como una red mesh: en lugar de depender de unos pocos proveedores de internet (ISPs) y servidores raíz, cada participante (o "nodo") en la red Yggdrasil se conecta a otros nodos que conoce. El tráfico puede "saltar" de nodo en nodo hasta encontrar su destino.

La clave de su funcionamiento es IPv6. Mientras que el internet que la mayoría usamos (IPv4) se está quedando sin direcciones, IPv6 ofrece un espacio de direcciones casi infinito. Yggdrasil aprovecha esto para asignar a cada nodo una dirección IPv6 única y estática (dentro del rango `200::/7`).

Esta dirección es tuya, permanente, y te identifica en la red Yggdrasil sin importar si estás conectado en casa, en una cafetería o en otro país.

![ipv6 explicacion](/yggdrasil2.png)

## Puntos Fuertes de Yggdrasil

Lo que hace a Yggdrasil tan atractivo no es solo su arquitectura, sino sus beneficios prácticos:

*   🔒 **Totalmente Cifrado (E2EE)**: Toda la comunicación a través de la red Yggdrasil está cifrada de extremo a extremo. Nadie en medio (ni tu ISP, ni otros nodos) puede espiar tu tráfico.
*   🌳 **Descentralizado y Resiliente**: Como el árbol mítico del que toma su nombre, la red no tiene un tronco central. Si un nodo o un grupo de nodos cae, el tráfico simplemente busca una ruta alternativa. No hay un "interruptor" central que se pueda apagar.
*   🌍 **Accesible Globalmente**: Tu dirección IPv6 de Yggdrasil es tu identidad. Puedes conectarte a tus dispositivos desde cualquier parte del mundo como si estuvieran en tu red local, sin configurar VPNs complejas ni lidiar con NATs.
*   🚀 **Fácil de Usar**: Una vez instalado, Yggdrasil simplemente funciona. Te proporciona una nueva interfaz de red y tú (y tus aplicaciones) solo tenéis que usar las direcciones IPv6 correspondientes.

![Implementación en NixOS] (/yggdrasil1.png)

## Implementación en NixOS: La Vía Declarativa

Aquí es donde la magia de NixOS brilla. En lugar de compilar código, gestionar dependencias o editar archivos de configuración manualmente, podemos habilitar Yggdrasil con unas pocas líneas en nuestro `configuration.nix`.

Solo tienes que añadir el siguiente módulo a tu configuración:

```nix
# /etc/nixos/configuration.nix

services.yggdrasil = {
  enable = true;

  # Opcional: Puedes configurar un nombre de nodo para identificarlo
  # settings = {
  #   NodeInfo = {
  #     name = "mi-servidor-nixos";
  #   };
  # };

  # Opcional: Conectarte a "peers" públicos si no encuentras nodos automáticamente
  # settings.Peers = [
  #   "tcp://example.public.peer:12345"
  # ];
};
```

Después de añadir esto, simplemente reconstruye tu sistema como de costumbre:

```bash
sudo nixos-rebuild switch
```

¡Y ya está! NixOS descargará, compilará y configurará el servicio. Puedes verificar que está funcionando ejecutando `ip a` (deberías ver una nueva interfaz `ygg-` o similar) o usando la herramienta de control de Yggdrasil:

```bash
$ yggdrasilctl getSelf
{
  "build_name": "...",
  "build_version": "...",
  "key": "...",
  "coords": "[...]",
  "address": "200:abcd:ef01:..."
}
```

La `address` que ves ahí es tu nueva IP permanente en la red Yggdrasil. ¡Guárdala bien!

## Usos Cotidianos y Ejemplos Prácticos

Ahora que tienes tu dirección, ¿qué puedes hacer con ella? Básicamente, cualquier cosa que harías en una red local, pero a escala global y de forma segura.

### 1. Alojar una Web "Oculta" (Pero Accesible)

Puedes correr un servidor web (como Nginx o Caddy) en tu máquina NixOS y hacerlo accesible solo a través de Yggdrasil. Es perfecto para un blog personal, un portafolio o una wiki familiar.

En Caddy, por ejemplo, tu `Caddyfile` sería tan simple como:

```caddyfile
[200:abcd:ef01:...]:80 {
    root * /srv/mi-web
    file_server
}
```
(Reemplaza la IP con la tuya). Ahora, cualquiera en Yggdrasil puede visitar `http://[200:abcd:ef01:...]` y ver tu web, sin necesidad de dominios, DNS públicos ni abrir puertos en tu router.

### 2. Montar una Radio Online P2P

¿Quieres compartir tu música? Puedes montar un servidor de streaming como Icecast o Azuracast y configurarlo para que "escuche" en tu dirección de Yggdrasil.

Tus amigos solo necesitarían un reproductor (como VLC) y la URL de tu stream: `http://[tu-ip-yggdrasil]:8000/stream`. Será una radio P2P sin intermediarios.

### 3. SSH y Servicios Privados (El uso estrella)

Este es quizás el uso más práctico. ¿Tienes un servidor en casa, una Raspberry Pi o tu propio portátil? Puedes acceder a ellos por SSH desde cualquier lugar del mundo de forma segura:

```bash
ssh miusuario@[200:abcd:ef01:...]
```

Esto reemplaza la necesidad de servicios como Tailscale o ZeroTier, pero de una forma completamente descentralizada. También funciona para otros servicios:

*   **Syncthing**: Sincroniza archivos entre tus dispositivos usando sus IPs de Yggdrasil.
*   **Servidores de Juegos**: Monta un servidor de Minecraft o Minetest para tus amigos.
*   **Copias de Seguridad**: Haz copias de seguridad remotas a un NAS en casa de forma segura.

## Conclusión

Yggdrasil es un vistazo a un futuro de internet más privado, resiliente y controlado por el usuario. Combina el poder de las redes mesh con la escala de IPv6. Y gracias a la naturaleza declarativa de NixOS, ponerlo en marcha es trivial.

Es un proyecto experimental, pero increíblemente funcional. Si te gusta la idea de construir redes alternativas y explorar la descentralización, ¡anímate a probarlo!
