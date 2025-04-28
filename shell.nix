{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = [
    pkgs.poetry  # Install Poetry
    pkgs.python3  # Base Python

    pkgs.python312Packages.nbdime # Merging Jupyter Notebooks
  ];

  shellHook = ''
    export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH
  '';
}

