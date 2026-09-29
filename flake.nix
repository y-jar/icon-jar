{
  description = "icon-jar - jar's collected icons and profile pictures";

  # No inputs needed: this flake only ships a hjem module whose `lib`/`config`
  # come from the evaluating system.
  outputs =
    { self }:
    {
      hjemModules.default =
        {
          config,
          lib,
          ...
        }:
        {
          options.jarRes = {
            icons = {
              enable = lib.mkEnableOption "icon-jar icons (iconbin)";
              dest = lib.mkOption {
                type = lib.types.str;
                default = "resjar/iconbin";
                description = "Home-relative directory the iconbin contents are symlinked into.";
              };
            };
            pfps = {
              enable = lib.mkEnableOption "icon-jar profile pictures (pfpbin)";
              dest = lib.mkOption {
                type = lib.types.str;
                default = "resjar/pfpbin";
                description = "Home-relative directory the pfpbin contents are symlinked into.";
              };
            };
          };

          config = {
            files = lib.mkMerge [
              (lib.mkIf config.jarRes.icons.enable {
                "${config.jarRes.icons.dest}".source = ./iconbin;
              })
              (lib.mkIf config.jarRes.pfps.enable {
                "${config.jarRes.pfps.dest}".source = ./pfpbin;
              })
            ];
          };
        };
    };
}
