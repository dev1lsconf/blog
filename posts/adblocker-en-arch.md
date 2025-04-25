---
title: AdBlocker en Arch
publish_date: 2025-04-25
summary: Configurar UFW como AdBlocker en Arch Linux
---

Para usar UFW (Uncomplicated Firewall) como un bloqueador de anuncios en Arch Linux, puedes seguir estos pasos:

## Instalar UFW


```bash
sudo pacman -S ufw
```

## Habilitar y iniciar UFW

```bash
sudo systemctl enable --now ufw
sudo ufw enable
```
## Instalar dependencias para el bloqueo de anuncios

```bash
sudo pacman -S curl python
```
## Crear un script para generar reglas de bloqueo
Crea un archivo llamado ufw-adblock.sh:

```bash
#!/bin/bash

# Listas de hosts para bloquear (puedes añadir más)
HOSTS_URLS=(
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
    "https://mirror1.malwaredomains.com/files/justdomains"
    "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext"
)

# Archivo temporal
TMP_FILE=$(mktemp)

# Descargar y procesar listas
for url in "${HOSTS_URLS[@]}"; do
    echo "Descargando $url"
    curl -s "$url" | grep -E '^0\.0\.0\.0|^127\.0\.0\.1' | awk '{print $2}' >> "$TMP_FILE"
done

# Ordenar y eliminar duplicados
sort -u "$TMP_FILE" -o "$TMP_FILE"

# Generar reglas UFW
echo "Generando reglas UFW..."
while read -r domain; do
    # Ignorar localhost y dominios vacíos
    [[ "$domain" == "localhost" || -z "$domain" ]] && continue
    
    # Añadir regla para bloquear
    sudo ufw deny out to any port 80,443 comment "AdBlock: $domain"
done < "$TMP_FILE"

# Limpiar
rm "$TMP_FILE"

echo "Bloqueo de anuncios configurado con UFW"
```

## Hacer el script ejecutable

```bash
chmod +x ufw-adblock.sh
```
## Ejecutar el script

```bash
sudo ./ufw-adblock.sh
```
## Verificar las reglas

```bash
sudo ufw status numbered
```
## (Opcional) Programar actualización periódica
Puedes agregar el script a cron para que se actualice regularmente:

```bash
(crontab -l 2>/dev/null; echo "0 3 * * * /ruta/al/script/ufw-adblock.sh") | crontab -
```

## Notas importantes:

UFW bloquea las conexiones a nivel de red, no filtra contenido dentro de páginas web.
Esto puede afectar el rendimiento si tienes muchas reglas.
Algunas páginas web podrían no funcionar correctamente.
Para deshacer los cambios, puedes usar: sudo ufw reset y luego reconfigurar tus reglas normales.
