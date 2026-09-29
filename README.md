# This is My Icon Repo

*[Link to iconjar page](https://y-jar.github.io/icon-jar/)*

**What is in here**

- [iconbin/](./iconbin) - my collected icons (`.ico`, `.png`, ...)
- [pfpbin/](./pfpbin) - my collected profile pictures

**How the page works**

1. Drop an image into `iconbin/` (icons) or `pfpbin/` (profile pictures).
2. From the repo root, run `python3 scripts/gen-index.py`. This rescans both
   bins and rewrites `icons_database.json` (size, ext, auto-tags).
3. `git add` the image and the JSON, commit, push.

**Using it from nix**

This repo is a flake that exposes a hjem module. Point it at wherever you want
the bulk images to land:

```nix
# inside a hjem user module
imports = [ inputs.icon-jar.hjemModules.default ];

jarRes = {
  icons = {
    enable = true;
    dest = "resjar/iconbin"; # home-relative
  };
  pfps = {
    enable = true;
    dest = "resjar/pfpbin"; # home-relative
  };
};
```

`dest` defaults to `resjar/iconbin` and `resjar/pfpbin`, so a nix system can
pick and choose where each bin goes.

> **Disclaimer**: This repo does contain art and screenshots and edits from me. So if you see art that needs sourcing, tell me! `:)`
