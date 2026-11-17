<h1 align="center">lunele-cli</h1>

<p align="center"><strong>English</strong> · <a href="./README.es.md">Español</a></p>

<p align="center">
The command line of <a href="https://github.com/iMacnucintosh/lunele-shell">Lunele</a>, a Material You desktop for Hyprland: start the shell, change the colour scheme and the wallpaper, take screenshots and recordings, manage the extensions and keep everything up to date. The command is <code>lunele</code>.
</p>

<details><summary id="dependencies">External dependencies</summary>

- [`libnotify`](https://gitlab.gnome.org/GNOME/libnotify) - sending notifications
- [`swappy`](https://github.com/jtheoof/swappy) - screenshot editor
- [`grim`](https://gitlab.freedesktop.org/emersion/grim) - taking screenshots
- [`dart-sass`](https://github.com/sass/dart-sass) - discord theming
- [`wl-clipboard`](https://github.com/bugaevc/wl-clipboard) - copying to clipboard
- [`slurp`](https://github.com/emersion/slurp) - selecting an area
- [`gpu-screen-recorder`](https://git.dec05eba.com/gpu-screen-recorder/about) - screen recording
- `glib2` - closing notifications
- [`cliphist`](https://github.com/sentriz/cliphist) - clipboard history
- [`fuzzel`](https://codeberg.org/dnkl/fuzzel) - clipboard history/emoji picker
- [`ffmpeg`](https://ffmpeg.org) - video wallpaper detection and colour generation

</details>

## Installation

It comes with Lunele: [its installer](https://github.com/iMacnucintosh/lunele-shell#installation) installs this
CLI (the `lunele-cli-git` package) along with the shell, and keeps it up to date. On its own, on Arch Linux, add the
[Lunele package repository](https://github.com/iMacnucintosh/lunele-packages) and install it with pacman:

```sh
sudo pacman -S lunele-cli-git
```

### Build from source

Install all [dependencies](#dependencies), then install
[`python-build`](https://github.com/pypa/build),
[`python-installer`](https://github.com/pypa/installer),
[`python-hatch`](https://github.com/pypa/hatch) and
[`python-hatch-vcs`](https://github.com/ofek/hatch-vcs).

e.g. via an AUR helper (yay)

```sh
yay -S libnotify swappy grim dart-sass wl-clipboard slurp gpu-screen-recorder ffmpeg glib2 cliphist fuzzel python-build python-installer python-hatch python-hatch-vcs
```

Now, clone the repo, `cd` into it, build the wheel via `python -m build --wheel` and install it via
`python -m installer dist/*.whl`. Then, to install the `fish` completions, copy the
`completions/lunele.fish` file to `/usr/share/fish/vendor_completions.d/lunele.fish`.

```sh
git clone https://github.com/iMacnucintosh/lunele-cli.git
cd lunele-cli
python -m build --wheel
sudo python -m installer dist/*.whl
sudo cp completions/lunele.fish /usr/share/fish/vendor_completions.d/lunele.fish
```

### Additional steps

#### Auto folder colour theming

For automatic Papirus folder icon colour syncing, you must have
[`papirus-folders`](https://github.com/PapirusDevelopmentTeam/papirus-folders) installed, and
`papirus-folders` must be able to run with `sudo` without a password prompt.

You can allow this by creating a sudoers file:

```sh
echo "$USER ALL=(ALL) NOPASSWD: $(which papirus-folders)" | sudo tee /etc/sudoers.d/papirus-folders
sudo chmod 440 /etc/sudoers.d/papirus-folders
```

#### Chromium-based browser theming

For live Chromium-based browser theming, the CLI must be allowed to create certain directories in
`/etc` and write to them via `sudo` without a password prompt.

You can allow this by creating a sudoers file:

```fish
# Fish shell
for dir in /etc/chromium/policies/managed /etc/brave/policies/managed /etc/opt/chrome/policies/managed
    echo "$USER ALL=(ALL) NOPASSWD: $(which mkdir) -p $dir" | sudo tee -a /etc/sudoers.d/lunele-chromium
    echo "$USER ALL=(ALL) NOPASSWD: $(which tee) $dir/lunele.json" | sudo tee -a /etc/sudoers.d/lunele-chromium
end
sudo chmod 440 /etc/sudoers.d/lunele-chromium
```

```sh
# Bash/other shells
for dir in /etc/chromium/policies/managed /etc/brave/policies/managed /etc/opt/chrome/policies/managed; do
    echo "$USER ALL=(ALL) NOPASSWD: $(which mkdir) -p $dir" | sudo tee -a /etc/sudoers.d/lunele-chromium
    echo "$USER ALL=(ALL) NOPASSWD: $(which tee) $dir/lunele.json" | sudo tee -a /etc/sudoers.d/lunele-chromium
done
sudo chmod 440 /etc/sudoers.d/lunele-chromium
```

## Usage

All subcommands/options can be explored via the help flag.

```
$ lunele -h
usage: lunele [-h] [-v] COMMAND ...

Main control script for the Lunele Shell

options:
  -h, --help     show this help message and exit
  -v, --version  print the current version

subcommands:
  valid subcommands

  COMMAND        the subcommand to run
    shell        start or message the shell
    toggle       toggle a special workspace
    scheme       manage the colour scheme
    screenshot   take a screenshot
    record       start a screen recording
    clipboard    open clipboard history
    emoji        emoji/glyph utilities
    wallpaper    manage the wallpaper
    resizer      window resizer daemon
    install      install Lunele: what is missing on this computer (`lunele install --help`)
    update       bring Lunele and what it installed up to date (`lunele update --help`)
    ext          manage the shell's extensions or run their commands
```

`lunele install` and `lunele update` run the shell's own installer (`scripts/installer.py`); `lunele ext` runs its
extension tool (`scripts/ext.py`). Their options are the ones of those scripts.

### User templates

Custom user templates can be defined in `~/.config/lunele/templates/`.

#### Template syntax

`{{ <color>.<format> }}`

- `<color>` is a theme color role derived from the Material You color system (e.g. `primary`, `secondary`, `background`)
- `<format>` is the output format: `hex`, `rgb`, `hsl`, or a single channel (`red`, `green`, `blue`, `hue`, `saturation`, `lightness`)

#### Examples

- `{{ primary.hex }}` outputs `3f4ba2`
- `{{ primary.rgb }}` outputs `rgb(193, 132, 207)`
- `{{ primary.red }}` outputs `193`
- `{{ primary.hsl }}` outputs `hsl(268,41%,66%)`
- `{{ primary.hue }}` outputs `268`

Output files are written to `~/.local/state/lunele/theme/`. You can symlink them to your desired
locations.

## Configuring

All configuration options are in `~/.config/lunele/cli.json`.

<details><summary>Example configuration</summary>

```json
{
    "record": {
        "extraArgs": []
    },
    "wallpaper": {
        "postHook": "echo $WALLPAPER_PATH $SCHEME_NAME $SCHEME_FLAVOUR $SCHEME_MODE $SCHEME_VARIANT $SCHEME_COLOURS"
    },
    "theme": {
        "enableTerm": true,
        "enableHypr": true,
        "enableDiscord": true,
        "enableSpicetify": true,
        "enablePandora": true,
        "enableFuzzel": true,
        "enableBtop": true,
        "enableNvtop": true,
        "enableHtop": true,
        "enableGtk": true,
        "enableQt": true,
        "enableWarp": true,
        "enableChromium": true,
        "enableZed": true,
        "enableCava": true,
        "iconTheme": "Papirus-Dark",
        "iconThemeLight": "Papirus-Light",
        "iconThemeDark": "Papirus-Dark",
        "postHook": "echo $SCHEME_NAME $SCHEME_FLAVOUR $SCHEME_MODE $SCHEME_VARIANT $SCHEME_COLOURS"
    },
    "toggles": {
        "communication": {
            "discord": {
                "enable": true,
                "match": [{ "class": "discord" }],
                "command": ["discord"],
                "move": true
            },
            "whatsapp": {
                "enable": true,
                "match": [{ "class": "whatsapp" }],
                "move": true
            }
        },
        "music": {
            "spotify": {
                "enable": true,
                "match": [{ "class": "Spotify" }, { "initialTitle": "Spotify" }, { "initialTitle": "Spotify Free" }],
                "command": ["spicetify", "watch", "-s"],
                "move": true
            }
        },
        "sysmon": {
            "btop": {
                "enable": true,
                "match": [{ "class": "btop", "title": "btop", "workspace": { "name": "special:sysmon" } }],
                "command": ["kitty", "-a", "btop", "-T", "btop"]
            }
        },
        "todo": {
            "todoist": {
                "enable": true,
                "match": [{ "class": "Todoist" }],
                "command": ["todoist"],
                "move": true
            }
        }
    }
}
```

</details>

## Coming from Caelestia

The CLI of Lunele started as [`caelestia-dots/cli`](https://github.com/caelestia-dots/cli). If you used that one, this is what is named differently here:

| Caelestia | Lunele |
| --- | --- |
| command `caelestia` | command `lunele` |
| package `caelestia` | package `lunele` |
| `~/.config/caelestia` | `~/.config/lunele` |
| `~/.local/state/caelestia` | `~/.local/state/lunele` |
| `~/.cache/caelestia` | `~/.cache/lunele` |
| `CAELESTIA_*` env vars | `LUNELE_*` (old ones still read) |
| Quickshell instance `caelestia` | Quickshell instance `lunele` |
| theme files `caelestia.*` | theme files `lunele.*` |

`install` and `update` no longer deploy the Caelestia dotfiles: they run Lunele's installer.

## License

GPL-3.0-only. Original work © the Caelestia contributors.
