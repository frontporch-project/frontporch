# GL.iNet Opal Router Setup Checklist

Use this checklist when preparing a GL.iNet Opal router for a FrontPorch pilot house.

The Opal is used as a small private gateway for the ATA. It connects upstream to the household Internet connection and establishes a split-tunnel WireGuard connection back to the PBX network. Do not expose SIP or Asterisk ports publicly.

Keep real hostnames, public IPs, keys, family names, and addresses out of this public repo.

## Inputs

Record these in the private deployment notes before starting:

- Opal inventory name, for example `frontporch-opal-002`
- Assigned house or family
- Unique Opal LAN subnet, for example `192.168.102.0/24`
- WireGuard client tunnel IP, for example `10.4.0.3/32`
- WireGuard server public key
- WireGuard server endpoint hostname, for example `vpn.example.net:51820`
- ATA SIP username, extension, and secret from Django Admin

## Router Baseline

- Upgrade the Opal to the latest stable firmware.
- Set the router name/hostname:

  ```text
  frontporch-opal-NNN
  ```

- Set the admin password.
- Configure the Opal as a Wi-Fi client/repeater of the household Wi-Fi, or connect its WAN port to the household router.
- Confirm a laptop connected to the Opal can reach the Internet before enabling WireGuard.

## LAN Settings

- Set a unique LAN subnet per Opal:

  ```text
  Opal 001: 192.168.101.1/24
  Opal 002: 192.168.102.1/24
  Opal 003: 192.168.103.1/24
  ```

- Keep DHCP enabled on the Opal LAN.
- Do not reuse the same LAN subnet on multiple Opals. Duplicate site subnets make remote debugging and future routed access ambiguous.
- If possible, reserve the ATA address after it appears:

  ```text
  frontporch-ata-NNN: 192.168.10N.10
  ```

## Wi-Fi Settings

- Use the shared FrontPorch SSID and password if the goal is easy admin-device roaming across houses.
- Use separate 2.4 GHz and 5 GHz SSIDs if useful for administration, for example:

  ```text
  frontporch
  frontporch-5g
  ```

- The ATA should use wired Ethernet to the Opal LAN. It should not depend on Wi-Fi.

## WireGuard Client

Configure the Opal as a WireGuard client.

Use split tunnel only:

```ini
[Interface]
PrivateKey = <OPAL_PRIVATE_KEY>
Address = 10.4.0.N/32
MTU = 1420

[Peer]
PublicKey = <WIREGUARD_SERVER_PUBLIC_KEY>
Endpoint = vpn.example.net:51820
AllowedIPs = 10.4.0.0/24
PersistentKeepalive = 25
```

Do not use:

```text
AllowedIPs = 0.0.0.0/0
```

That turns the VPN into a default route and can break normal Internet access behind the Opal when the tunnel is down or misrouted.

## WireGuard Server Peer

On the WireGuard server, create a peer for the Opal:

```text
Name: frontporch-opal-NNN
Public key: <Opal client public key>
Allowed IPs: 10.4.0.N/32
```

Start with only the WireGuard client IP. Add the Opal LAN subnet later only if the PBX/admin side needs routed access to devices behind that Opal:

```text
10.4.0.N/32, 192.168.10N.0/24
```

## Static Route

Some Opal/OpenWrt builds bring up WireGuard but do not install the route for `AllowedIPs`.

After WireGuard connects, test:

```sh
ping -I wgclient1 -c 3 10.4.0.1
ping -c 3 10.4.0.1
```

If the first command works and the second fails, add a static route:

```text
Route type: Unicast
Interface: wgclient1
Target: 10.4.0.0
Netmask: 255.255.255.0
Gateway: blank
```

Expected route:

```sh
ip route get 10.4.0.1
```

```text
10.4.0.1 dev wgclient1 src 10.4.0.N
```

## Verification

From the Opal SSH shell:

```sh
wg show
ip route
ip route get 10.4.0.1
ping -I wgclient1 -c 3 10.4.0.1
ping -c 3 10.4.0.1
```

Expected WireGuard state:

```text
latest handshake: recent
transfer: nonzero received and sent bytes
allowed ips: 10.4.0.0/24
```

From a laptop connected to the Opal:

```sh
ping 1.1.1.1
ping example.com
```

Normal Internet access should still work while WireGuard is enabled.

## ATA Settings

Plug the Grandstream HT802 into the Opal LAN port.

Configure the ATA FXS port:

```text
Primary SIP Server: 10.4.0.1
SIP port: 5060
Transport: UDP
SIP User ID: <device SIP username>
Authenticate ID: <device SIP username>
Authenticate Password: <device SIP secret>
Name: <child or device label>
SIP Registration: Yes
Preferred Vocoder: PCMU / G.711u
Preferred DTMF method: RFC2833
```

On Asterisk, verify registration:

```sh
asterisk -rx "pjsip show contacts"
```

From the phone, test:

```text
100
```

The echo test should work before testing child-to-child or external calls.

## Troubleshooting

If laptops behind the Opal lose Internet when WireGuard is enabled:

- Confirm `AllowedIPs` is not `0.0.0.0/0`.
- Confirm VPN policy is not forcing all traffic through WireGuard.
- Disable WireGuard and verify the Opal repeater/WAN path still has Internet.

If `wg show` has sent bytes but no received bytes:

- Confirm the WireGuard server UDP port forward is correct.
- Confirm the endpoint hostname resolves to the current public IP.
- Confirm the WireGuard server peer has the current Opal public key.
- Confirm the WireGuard server is enabled.

If `ping -I wgclient1 10.4.0.1` works but `ping 10.4.0.1` fails:

- Add or repair the static route for `10.4.0.0/24` through `wgclient1`.

If SIP registration works and `100` echo works but phone-to-phone audio fails:

- Confirm Asterisk endpoints inherit:

  ```ini
  direct_media=no
  rtp_symmetric=yes
  force_rport=yes
  rewrite_contact=yes
  ```

- Reload or restart Asterisk after changing PJSIP configuration.
