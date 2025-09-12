# SSH Setup Guide for Remote Access to the 3D-printer

## Step 1: Generate SSH Keys

### Create a key for the Raspberry Pi (Klipper)
```bash
ssh-keygen -t ed25519 -f ~/.ssh/[RPI_KEY_NAME]
```
**Replace `[RPI_KEY_NAME]` with a descriptive name** (e.g., `rpi_klipper_key`)

**Important:** After generating the key, email the contents of `~/.ssh/[RPI_KEY_NAME].pub` to `tsauren@uio.no`

### Create a key for UiO login (if you don't have one)
```bash
ssh-keygen -t ed25519 -f ~/.ssh/[UIO_KEY_NAME]
```
**Replace `[UIO_KEY_NAME]` with a descriptive name** (e.g., `uio_login_key`)

## Step 2: Configure SSH Client

Save the following configuration to `~/.ssh/config` on your computer:

```ssh
# Main UiO login gateway
Host uio
    Hostname login.uio.no
    User [UIO_USER]
    IdentityFile ~/.ssh/[UIO_KEY_NAME]
    IdentitiesOnly yes
    ForwardAgent yes
    AddKeysToAgent yes

# Robin cluster machines
# Note: xinzhao is the primary machine for this project
Host dancer dunder rudolph deepthinker comet cupid xinzhao
    Hostname %h.ifi.uio.no
    User [UIO_USER]
    ProxyJump uio

# Ender3 3D printer with Klipper firmware
Host ender3_klipper
    Hostname klipper.labnet
    User in5490
    IdentityFile ~/.ssh/[RPI_KEY_NAME]
    ProxyJump xinzhao  # Routes through xinzhao (on both labnet and public network)
    LocalForward 7125 localhost:7125  # Moonraker API
    LocalForward 8080 localhost:80     # Mainsail web interface (nginx)
    # LocalForward 7136 localhost:7136 # Fluidd interface (commented - using Mainsail instead)
```

### Required Replacements
Make sure to replace these placeholders in the config file:
- `[UIO_USER]` → Your UiO username
- `[UIO_KEY_NAME]` → The name you used for your UiO SSH key
- `[RPI_KEY_NAME]` → The name you used for your Raspberry Pi SSH key

## Step 3: Connect to the System

Once everything is configured, connect using:
```bash
ssh ender3_klipper
```

### Authentication Notes
- You may need to enter your UiO password and 2FA code depending on your location
- The connection will automatically route through the UiO gateway and xinzhao

## Access to Web Interfaces

After connecting, you can access these services locally:
- **Moonraker API:** http://localhost:7125
- **Mainsail Web Interface:** http://localhost:8080

Note that the ssh session must be active for these to work.


## Additional Robin Machines

While `xinzhao` is the primary machine for this project, you have access to other Robin cluster machines:
- dancer
- dunder
- rudolph
- deepthinker
- comet
- cupid

Connect to any of them using: `ssh [machine_name]`

## Troubleshooting

### Permission Denied
- Ensure your public key has been sent to `tsauren@uio.no`
- Verify the correct key paths in your SSH config
- Check that your key files have proper permissions: `chmod 600 ~/.ssh/[KEY_NAME]`

### Connection Timeout
- Verify you're connected to the internet
- Check if you need to be on VPN for external access
- Ensure 2FA is properly configured for your UiO account

## Notes
- The Raspberry Pi is on the labnet WLAN, requiring proxy through a dual-network machine (xinzhao)
- If xinzhao lacks computational power, we may switch to another desktop computer
