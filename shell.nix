{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  # Define los paquetes que quieres en tu entorno
  packages = with pkgs; [
    python311Full # Puedes especificar la versión de Python que prefieras (e.g., python310, python311, etc.)
    (python311.withPackages (ps: with ps; [
      textual
      requests
    ]))
    fish # Incluimos fish en el entorno
  ];

  # Establece el shell por defecto dentro de este entorno
  shellHook = ''
    export SHELL=${pkgs.fish}/bin/fish
    exec fish
  '';

  # Opcional: Si quieres darle un nombre al entorno de tu shell
  name = "Publicar blog";
}
