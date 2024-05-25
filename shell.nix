let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.pyqt5
    ]))
  ];
  buildInputs = [
    pkgs.qt5.full
  ];
}
