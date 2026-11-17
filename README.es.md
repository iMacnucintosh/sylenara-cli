<h1 align="center">sylphrena-cli</h1>

<p align="center"><a href="./README.md">English</a> · <strong>Español</strong></p>

<p align="center">
La línea de comandos de <a href="https://github.com/iMacnucintosh/sylphrena-shell">Sylphrena</a>, un escritorio Material You para Hyprland: arranca la shell, cambia el esquema de colores y el fondo, hace capturas y grabaciones, gestiona las extensiones y mantiene todo al día. El comando es <code>sylph</code>.
</p>

<details><summary id="dependencias">Dependencias externas</summary>

- [`libnotify`](https://gitlab.gnome.org/GNOME/libnotify) - enviar notificaciones
- [`swappy`](https://github.com/jtheoof/swappy) - editor de capturas (opcional)
- [`grim`](https://gitlab.freedesktop.org/emersion/grim) - hacer capturas
- [`dart-sass`](https://github.com/sass/dart-sass) - tema de Discord
- [`wl-clipboard`](https://github.com/bugaevc/wl-clipboard) - copiar al portapapeles
- [`slurp`](https://github.com/emersion/slurp) - elegir una zona
- [`gpu-screen-recorder`](https://git.dec05eba.com/gpu-screen-recorder/about) - grabar la pantalla
- `glib2` - cerrar notificaciones
- [`cliphist`](https://github.com/sentriz/cliphist) - historial del portapapeles
- [`fuzzel`](https://codeberg.org/dnkl/fuzzel) - historial del portapapeles / selector de emojis
- [`ffmpeg`](https://ffmpeg.org) - detectar fondos de vídeo y generar colores

</details>

## Instalación

Viene con Sylphrena: [su instalador](https://github.com/iMacnucintosh/sylphrena-shell/blob/main/README.es.md#instalación) instala esta CLI (el paquete `sylphrena-cli-git`) junto con la shell y la mantiene al día. Por separado, en Arch Linux, añade el [repositorio de paquetes de Sylphrena](https://github.com/iMacnucintosh/sylphrena-packages) e instálala con pacman:

```sh
sudo pacman -S sylphrena-cli-git
```

### Compilar desde el código

Instala todas las [dependencias](#dependencias), y después [`python-build`](https://github.com/pypa/build), [`python-installer`](https://github.com/pypa/installer), [`python-hatch`](https://github.com/pypa/hatch) y [`python-hatch-vcs`](https://github.com/ofek/hatch-vcs).

Por ejemplo, con un ayudante del AUR (yay):

```sh
yay -S libnotify swappy grim dart-sass wl-clipboard slurp gpu-screen-recorder ffmpeg glib2 cliphist fuzzel python-build python-installer python-hatch python-hatch-vcs
```

Ahora clona el repositorio, entra en él, construye el wheel con `python -m build --wheel` e instálalo con `python -m installer dist/*.whl`. Después, para instalar las completaciones de `fish`, copia `completions/sylph.fish` en `/usr/share/fish/vendor_completions.d/sylph.fish`.

```sh
git clone https://github.com/iMacnucintosh/sylphrena-cli.git
cd sylphrena-cli
python -m build --wheel
sudo python -m installer dist/*.whl
sudo cp completions/sylph.fish /usr/share/fish/vendor_completions.d/sylph.fish
```

### Pasos adicionales

#### Color automático de las carpetas

Para sincronizar el color de los iconos de carpetas de Papirus tienes que tener instalado [`papirus-folders`](https://github.com/PapirusDevelopmentTeam/papirus-folders), y `papirus-folders` debe poder ejecutarse con `sudo` sin pedir contraseña.

Puedes permitirlo creando un fichero de sudoers:

```sh
echo "$USER ALL=(ALL) NOPASSWD: $(which papirus-folders)" | sudo tee /etc/sudoers.d/papirus-folders
sudo chmod 440 /etc/sudoers.d/papirus-folders
```

#### Tema de los navegadores basados en Chromium

Para tematizar en vivo los navegadores basados en Chromium, la CLI debe poder crear ciertos directorios en `/etc` y escribir en ellos con `sudo` sin pedir contraseña.

Puedes permitirlo creando un fichero de sudoers:

```fish
# Fish shell
for dir in /etc/chromium/policies/managed /etc/brave/policies/managed /etc/opt/chrome/policies/managed
    echo "$USER ALL=(ALL) NOPASSWD: $(which mkdir) -p $dir" | sudo tee -a /etc/sudoers.d/sylphrena-chromium
    echo "$USER ALL=(ALL) NOPASSWD: $(which tee) $dir/sylphrena.json" | sudo tee -a /etc/sudoers.d/sylphrena-chromium
end
sudo chmod 440 /etc/sudoers.d/sylphrena-chromium
```

```sh
# Bash/other shells
for dir in /etc/chromium/policies/managed /etc/brave/policies/managed /etc/opt/chrome/policies/managed; do
    echo "$USER ALL=(ALL) NOPASSWD: $(which mkdir) -p $dir" | sudo tee -a /etc/sudoers.d/sylphrena-chromium
    echo "$USER ALL=(ALL) NOPASSWD: $(which tee) $dir/sylphrena.json" | sudo tee -a /etc/sudoers.d/sylphrena-chromium
done
sudo chmod 440 /etc/sudoers.d/sylphrena-chromium
```

## Uso

Todos los subcomandos y opciones se pueden explorar con la ayuda.

```
$ sylph -h
usage: sylph [-h] [-v] COMMAND ...

Main control script for the Sylphrena Shell

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
    install      install Sylphrena: what is missing on this computer (`sylph install --help`)
    update       bring Sylphrena and what it installed up to date (`sylph update --help`)
    ext          manage the shell's extensions or run their commands
```

`sylph install` y `sylph update` ejecutan el instalador de la shell (`scripts/installer.py`); `sylph ext` ejecuta su herramienta de extensiones (`scripts/ext.py`). Sus opciones son las de esos scripts.

### Plantillas de usuario

Puedes definir tus propias plantillas en `~/.config/sylphrena/templates/`.

#### Sintaxis de las plantillas

`{{ <color>.<formato> }}`

- `<color>` es un rol de color del tema derivado del sistema de color de Material You (p. ej. `primary`, `secondary`, `background`)
- `<formato>` es el formato de salida: `hex`, `rgb`, `hsl`, o un solo canal (`red`, `green`, `blue`, `hue`, `saturation`, `lightness`)

#### Ejemplos

- `{{ primary.hex }}` da `3f4ba2`
- `{{ primary.rgb }}` da `rgb(193, 132, 207)`
- `{{ primary.red }}` da `193`
- `{{ primary.hsl }}` da `hsl(268,41%,66%)`
- `{{ primary.hue }}` da `268`

Los ficheros de salida se escriben en `~/.local/state/sylphrena/theme/`. Puedes enlazarlos simbólicamente donde los quieras.

## Configuración

Todas las opciones están en `~/.config/sylphrena/cli.json`.

<details><summary>Configuración de ejemplo</summary>

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

## Si vienes de Caelestia

La CLI de Sylphrena empezó como [`caelestia-dots/cli`](https://github.com/caelestia-dots/cli). Si usabas esa, esto es lo que se llama distinto aquí:

| Caelestia | Sylphrena |
| --- | --- |
| comando `caelestia` | comando `sylph` |
| paquete `caelestia` | paquete `sylphrena` |
| `~/.config/caelestia` | `~/.config/sylphrena` |
| `~/.local/state/caelestia` | `~/.local/state/sylphrena` |
| `~/.cache/caelestia` | `~/.cache/sylphrena` |
| variables `CAELESTIA_*` | `SYLPHRENA_*` (las antiguas se siguen leyendo) |
| instancia de Quickshell `caelestia` | instancia de Quickshell `sylphrena` |
| ficheros de tema `caelestia.*` | ficheros de tema `sylphrena.*` |

`install` y `update` ya no despliegan los dotfiles de Caelestia: ejecutan el instalador de Sylphrena.

## Licencia

GPL-3.0-only. Obra original © los colaboradores de Caelestia.
