---
title: My NixOS Setup 
publish_date:  2022-12-20
summary: 'NixOS es una distribución de Linux construida sobre el administrador de paquetes Nix. Utiliza configuración declarativa y permite actualizar de manera confiable el sistema. Ofrece varios "canales" de paquetes oficiales, incluida la versión estable actual y la versión inestable que aún continúa en pruebas. '
---

![My NixOS Setup](/nixos.jpeg)

Despues de estar muy comodo usando Archlinux.. llego NixOS.. hhaaha..  luego hare un post sobre lo que me gusto y me atrajo de NixOS..

Hasta el momento aqui te dejo mi configuration.nix


```bash
# Edit this configuration file to define what should be installed on
# your system.  Help is available in the configuration.nix(5) man page
# and in the NixOS manual (accessible by running ‘nixos-help’).

{ config, pkgs, ... }:

{
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix 
    ];

  # Bootloader.
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;
  boot.loader.efi.efiSysMountPoint = "/boot/efi";

  networking.hostName = "fsociety"; # Define your hostname.
  # networking.wireless.enable = true;  # Enables wireless support via wpa_supplicant.

  # Configure network proxy if necessary
  # networking.proxy.default = "http://user:password@proxy:port/";
  # networking.proxy.noProxy = "127.0.0.1,localhost,internal.domain";

  # Enable networking
  networking.networkmanager.enable = true;
  networking.extraHosts =
  ''
    192.168.86.244 mini.lan mini.arpa mini.local
    192.168.86.243 puffy.lan puffy.arpa puffy.local
  '';

  # Set your time zone.
  time.timeZone = "America/Santo_Domingo";

  # Select internationalisation properties.
  i18n.defaultLocale = "en_US.utf8";

  i18n.extraLocaleSettings = {
    LC_ADDRESS = "es_DO.utf8";
    LC_IDENTIFICATION = "es_DO.utf8";
    LC_MEASUREMENT = "es_DO.utf8";
    LC_MONETARY = "es_DO.utf8";
    LC_NAME = "es_DO.utf8";
    LC_NUMERIC = "es_DO.utf8";
    LC_PAPER = "es_DO.utf8";
    LC_TELEPHONE = "es_DO.utf8";
    LC_TIME = "es_DO.utf8";
  };

  # Enable the X11 windowing system.
  services.xserver.enable = true;

  # Enable the GNOME Desktop Environment.
  services.xserver.displayManager.gdm.enable = true;
  services.xserver.desktopManager.gnome.enable = true;
  
  # enable xfce
  services.xserver.desktopManager.xfce.enable = true;

  # BSPWM
  services.xserver.windowManager.bspwm.enable = true;

  # Picom enable
  services.picom = {
  enable = true;
  fade = true;
  inactiveOpacity = 0.9;
  shadow = true;
  fadeDelta = 4;
  };

  # Configure keymap in X11
  services.xserver = {
    layout = "latam";
    xkbVariant = "";
  };

  # Configure console keymap
  console.keyMap = "la-latin1";

  # Enable CUPS to print documents.
  services.printing.enable = true;

  # Enable sound with pipewire.
  sound.enable = true;
  hardware.pulseaudio.enable = false;
  security.rtkit.enable = true;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;
    pulse.enable = true;
    # If you want to use JACK applications, uncomment this
    #jack.enable = true;

    # use the example session manager (no others are packaged yet so this is enabled by default,
    # no need to redefine it in your config for now)
    #media-session.enable = true;
  };
  
  # bluethooth
  hardware.bluetooth.enable = true;

  # GVFS
  services.gvfs.enable = true ;

  # Enable touchpad support (enabled default in most desktopManager).
  services.xserver.libinput.enable = true;

   #Virtualisation
     virtualisation.libvirtd.enable = true;
     virtualisation.virtualbox.host.enable = true;
     users.extraGroups.vboxusers.members = [ "user-with-access-to-virtualbox" ];

  # Define a user account. Don't forget to set a password with ‘passwd’.
  users.users.dev1ls = {
    isNormalUser = true;
    shell = pkgs.fish;
    description = "dev1ls";
    extraGroups = [ "networkmanager" "wheel" "sudo" "vboxusers" "libvirtd" ];
    packages = with pkgs; [
      firefox
      chromium
      brave
      vorta
      fish
      aria2
      fzf
      fd
      sshfs-fuse
      lynx
      spotify-tui
      popcorntime
      tootle
      termscp
      toot
      tuir
      duf
      sakura
      glances
      blueberry
      hydra-check
      nerdfonts
      ripgrep
      virt-manager
      st
      luakit
      alacritty
      thunderbird
      invidious
      nitter
    ];
  };

  # Allow unfree packages
  nixpkgs.config.allowUnfree = true;

  # List packages installed in system profile. To search, run:
  # $ nix search wget
  environment.systemPackages = with pkgs; [
    vim # Do not forget to add an editor to edit configuration.nix! The Nano editor is also installed by default.
    wget
    neovim
    tmux
    dt-shell-color-scripts
    git
    neofetch
    htop
    kakoune
    firejail
    wget
    firefox
    neovim
    pfetch
    git
    feh
    picom
    sxhkd
    polybar
    rofi
    w3m
    scrot
    killall
    xclip
    ffmpeg
    mpv
    gimp
    nodejs
    nodePackages.npm
    ntfs3g
    pasystray
    qogir-icon-theme
    qogir-theme
    lxappearance
    youtube-dl
    vscodium
    unzip
    luajit
    lf
    pulseaudio
    pulseaudio-ctl
    rclone
    scrot
    tty-clock
    sxiv
    tdesktop
    xorg.xev
    font-awesome
  ];


  #fonts.fonts = [ ];

   fonts.fonts = with pkgs; [
      (nerdfonts.override { fonts = [ "Iosevka" "FiraCode" "Hack" ]; })
   ];

  # Flakes
  nix.settings.experimental-features = [ "nix-command" "flakes" ];
  
  #garbage collector
  nix.settings.auto-optimise-store = true;
  nix.gc.automatic = true;

  #automatic update
  system.autoUpgrade.enable = true;

  # Some programs need SUID wrappers, can be configured further or are
  # started in user sessions.
  # programs.mtr.enable = true;
  # programs.gnupg.agent = {
  #   enable = true;
  #   enableSSHSupport = true;
  # };

  # List services that you want to enable:

  # Enable the OpenSSH daemon.
  services.openssh.enable = true;

  # Open ports in the firewall.
  networking.firewall.allowedTCPPorts = [ 22 12345 12346 ];
  networking.firewall.allowedUDPPorts = [ ];
  # Or disable the firewall altogether.
  networking.firewall.enable = true;

  # Hardened Nixos ( Solene )
  # disable coredump that could be exploited later
  # and also slow down the system when something crash
  systemd.coredump.enable = false;

  # required to run chromium
  security.chromiumSuidSandbox.enable = true;

  # enable firejail
  programs.firejail.enable = true;

  # create system-wide executables firefox and chromium
  # that will wrap the real binaries so everything
  # work out of the box.
  programs.firejail.wrappedBinaries = {
      firefox = {
          executable = "${pkgs.lib.getBin pkgs.firefox}/bin/firefox";
          profile = "${pkgs.firejail}/etc/firejail/firefox.profile";
      };
      chromium = {
          executable = "${pkgs.lib.getBin pkgs.chromium}/bin/chromium";
          profile = "${pkgs.firejail}/etc/firejail/chromium.profile";
      };
  };


  services.invidious = {
      enable = true;
      nginx.enable = false;
      port = 12345;

      # if you want to disable recommended videos
      settings = {
        default_user_preferences = {
          "related_videos" = false;
        };
      };
  };  
  
  services.nitter = {
      enable = true;
      server.port = 12346;
      server.address = "127.0.0.1";
  };

  # This value determines the NixOS release from which the default
  # settings for stateful data, like file locations and database versions
  # on your system were taken. It‘s perfectly fine and recommended to leave
  # this value at the release version of the first install of this system.
  # Before changing this value read the documentation for this option
  # (e.g. man configuration.nix or on https://nixos.org/nixos/options.html).
  system.stateVersion = "22.05"; # Did you read the comment?

}
```


