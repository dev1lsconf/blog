---
title: vger + OpenBSD  
publish_date:  2023-09-27
summary: 'Gemini is a new internet technology supporting an electronic library of interconnected text documents. Thats not a new idea, but its not old fashioned either.'
---

# Install Packages

```
$ pkg_add vger
$ echo "# it works" >> /var/gemini/index.gmi
```

# Configure inetd

inetd(8) is a super server. It works by listening for incoming connections and launches a specific program when it receives one. Since no one actually uses gemini, this approach to services is better. Instead of running constantly, the gemini server only runs when someone sends it a packet.

```
127.0.0.1:11965 stream tcp nowait _vger /usr/local/bin/vger vger
```

# Configure relayd

relayd(8) is proxying service. In this example, I've set it up to proxy requests on :1965 to :11965. The tls keypair line is important because tls is a mandatory component of the gemini protocol.

```
log connection
tcp protocol "gemini" {
        tls keypair "example.com:1965"
}

relay "genimi" {
        listen on example.com port 1965 tls
        protocol "gemini"
        forward to 127.0.0.1 port 11965
}

```

# Get Certs

Since I'm also running httpd, I just symlinked my existing ssl certs. The name is important here. After much fiddling around, I read the documentation and relalized that the name of the cert and key must be identical to hostname:port.{key,crt}.

```
$ ln -s /etc/ssl/example.com.fullchain.pem /etc/ssl/example.com\:1965.crt
$ ln -s /etc/ssl/private/example.com.key /etc/ssl/private/example.com\:1965.key
```

# Configure pf

pf(4) is the firewall on OpenBSD. Thsis is a fairly basic configuration. Skip on the loopback device, use a macro to list services, block all incoming traffic unless it's in the list, pass all traffic out. The last line is was included in /etc/examples/pf.conf so I thought it was worthwhile to keep it.

```
set skip on lo
tcp_services="{ssh, http, https, 1965}"

block in all

pass in proto tcp to any port $tcp_services keep state
pass out all

block return in on ! lo0 proto tcp to port 6000:6010
```

# Smoke Test

```
$ pfctl -f /etc/pf.conf
$ rcctl enable inetd relayd
$ rcctl start inetd relayd
```

# test if it works

```
$ pkg_add bombadillo
$ bombadillo gemini://example.com
```

Eventually, I will write a script that converts html to the gemini markdown format. I will likely set it up as a cron job so that I can serve this website over gemini and never have to touch it again. 

source: https://0x19.org/posts/2022-01-02.php
