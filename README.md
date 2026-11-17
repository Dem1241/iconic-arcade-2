# iconic-arcade

Custom stuff for my Raspberry Pi 4 arcade cabinet running Batocera 39.

## Install / update on the arcade

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USER/iconic-arcade/main/install.sh | bash
```

## What's in here

| Path | What it is |
|---|---|
| `ports/IconicFun.sh` | Launcher that shows up under **Ports** in the arcade menu |
| `ports/iconicfun/main.py` | The pygame app (currently a control tester) |
| `install.sh` | Downloads this repo and copies it into `/userdata/roms/ports` |

## Controls

Exit any time: hold 2 buttons for 2 seconds, or ESC on a keyboard.
