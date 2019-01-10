# Installation

1. Configure Pi for Static IP

Edit `/etc/dhcpcd.conf`

```bash
# give pi static ethernet ip
interface eth0

static ip_address=192.168.0.10/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1
```

2. Install deps

```bash
sudo apt-get install x11-xserver-utils
```

3. Edit startup commands

Edit `~/.config/lxsession/LXDE-pi/autostart`

```bash
# open browser in kiosk and incognito mode
@chromium-browser -kiosk -incognito https://url.to.your.site/

# keep screen on indefinitely
@xset s noblank
@xset s off
@xset -dpms
```
