# Step 1. Setup a udev rule

Installation (Linux): Before using a SpaceMouse in the system, you need to install: 1) hidapi python package and 2) udev system (to avoid running as sudo). You might need to install libmotif-dev.

## Find your SpaceMouse USB IDs
First, identify the actual vendor and product IDs on your machine (VID always `256f` for 3Dconnexion; PID varies by model / firmware):

```bash
lsusb | grep -i 256f        # Example: 256f:c635 3Dconnexion SpaceMouse Compact
```

Alternatively (from Python, after installing hidapi in your environment):

```python
import hid
[ (hex(d['vendor_id']), hex(d['product_id']), d.get('product_string')) for d in hid.enumerate() if d.get('vendor_id') == 0x256f ]
```

## Create udev rules for your device (replace <PID> with your product ID)
Create a rule file under `/etc/udev/rules.d/` (use a number ≥ 50). The example below uses `60-spacemouse.rules` and includes both `plugdev` group and a `uaccess` tag for desktop sessions. Use `printf | sudo tee` to avoid interactive hangs:

```bash
printf '%s\n' \
'KERNEL=="hidraw*", ATTRS{idVendor}=="256f", ATTRS{idProduct}=="<PID>", MODE="0666", GROUP="plugdev", TAG+="uaccess"' \
'SUBSYSTEM=="usb",   ATTRS{idVendor}=="256f", ATTRS{idProduct}=="<PID>", MODE="0666", GROUP="plugdev", TAG+="uaccess"' | \
sudo tee /etc/udev/rules.d/60-spacemouse.rules
```

Example for SpaceMouse Compact observed as `256f:c635`:

```bash
printf '%s\n' \
'KERNEL=="hidraw*", ATTRS{idVendor}=="256f", ATTRS{idProduct}=="c635", MODE="0666", GROUP="plugdev", TAG+="uaccess"' \
'SUBSYSTEM=="usb",   ATTRS{idVendor}=="256f", ATTRS{idProduct}=="c635", MODE="0666", GROUP="plugdev", TAG+="uaccess"' | \
sudo tee /etc/udev/rules.d/60-spacemouse.rules
```

## Reload rules and replug the device

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
# Unplug and replug the SpaceMouse
```

## Verify the rule is applied

```bash
ls -l /dev/hidraw*
# Optionally, identify which hidraw node is the SpaceMouse and check IDs:
udevadm info -a -n /dev/hidrawX | grep -E 'idVendor|idProduct' -m1 -A1
```

Your user should be in the `plugdev` group:

```bash
groups | grep plugdev || sudo usermod -aG plugdev "$USER"
```

# Step 2. Install hidapi in your environment

Install hidapi inside your virtualenv/conda env:

```bash
pip install hidapi
```

# Step 3. Enumerate and test

From Python, confirm the device is visible (replace `<PID>` as above):

```python
import json, hid
print(json.dumps([{'vid':hex(d['vendor_id']),'pid':hex(d['product_id']),'product':d.get('product_string')} for d in hid.enumerate(0x256f, 0x<PID>)], indent=2))
```

If you see the SpaceMouse entry and still get `OSError: open failed` when running examples, re-check that the udev rule uses your exact PID and that you replugged the device after reloading rules. As a permissions sanity check, the example should run with sudo; if it does with sudo but not without, the udev rule is the culprit.