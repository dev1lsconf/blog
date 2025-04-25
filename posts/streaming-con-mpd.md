---
title: Streaming con MPD
publish_date: 2025-04-25
summary: hacer stream directo con MPD, algo que ni me imaginaba que existia, pero mirando un poco en la configuracion me encontre con esta joya!
---

## hacer stream sin icecast o algun programa de streaming radio online
 

Claro que si se puede.. lo encontre casi por mera coincidencia.. buscando en la wiki ayudando a un amigo con algo que me pedia sobre mpd y conectarlo a un icecast, encontre esto y me parecio curioso e interesante.

Aqui te dejo una idea de lo que puse en mi ~/.mpd/mpd.conf

```
music_directory "~/Music"
playlist_directory "~/.mpd/playlists"
db_file "~/.mpd/mpd.db"
log_file "~/.mpd/mpd.log"
pid_file "~/.mpd/mpd.pid"
state_file "~/.mpd/mpdstate"

audio_output {
        type "pulse"
        name "pulse audio"
}

audio_output {
	type                    "fifo"
	name                    "my_fifo"
	path                    "/tmp/mpd.fifo"
	format                  "44100:16:2"
}

audio_output {
    type        "httpd"
    name        "MPD HTTP Stream"
    encoder     "vorbis"       # Formato Ogg Vorbis
    port        "8000"
    bind_to_address "0.0.0.0"  # Permite conexiones desde otras máquinas
    bitrate     "192"
    format      "44100:16:2"
}

bind_to_address "127.0.0.1"
port "6600"
```
