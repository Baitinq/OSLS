{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  nativeBuildInputs = with pkgs; [
    python3
    python3Packages.numpy
    python3Packages.pygame
    python3Packages.matplotlib
  ];
}
