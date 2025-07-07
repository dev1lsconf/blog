{
  description = "Mi entorno de desarrollo Python";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05"; # Asegúrate de que esta rama exista y sea estable
  };

  outputs = { self, nixpkgs }: {
    # Define la arquitectura de tu sistema (ajusta si es diferente, e.g., aarch64-darwin para Macs M1/M2)
    # Puedes hacer esto para diferentes sistemas, pero para un solo shell, podemos ser más directos.
    # Usaremos x86_64-linux por defecto, ya que es lo más común.
    devShells.x86_64-linux.blog = nixpkgs.legacyPackages.x86_64-linux.mkShell {
      # Aquí, 'nixpkgs.legacyPackages.x86_64-linux' nos da acceso a los paquetes para esa arquitectura
      # de forma más directa, sin la necesidad de un nixosSystem completo.

      packages = with nixpkgs.legacyPackages.x86_64-linux; [
        python311Full
        (python311.withPackages (ps: with ps; [
          textual
          requests
        ]))
        fish
      ];

      shellHook = ''
        export SHELL=${nixpkgs.legacyPackages.x86_64-linux.fish}/bin/fish
        exec fish
      '';

      name = "blog"; # Este nombre es interno al shell, no el que usas para llamarlo
    };
  };
}
