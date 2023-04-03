
{
  description = "github_issue_retriever";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-21.11";
    flake-utils.url = "github:numtide/flake-utils";
    axiom-utils.url = "github:ford-perfect/axiom-utils";
  };


  outputs = { self, nixpkgs, flake-utils, axiom-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonEnv = pkgs.python39.withPackages (ps: with ps; [
          requests
          urllib3
          configargparse
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          name = "github_issue_retriever";
          buildInputs = [
            pythonEnv
          ];
          shellHook = axiom-utils.eyeCandy.colorPrompt "github_issue_retriever" + ''
            source .env
          '';
        };

        defaultPackage = pythonEnv;
      }
    );
}
