# abt

[![PyPI version](https://badge.fury.io/py/abt.svg)](https://badge.fury.io/py/abt)

BitTorrent workflow with [aria2][aria2].

## Installation

Using [pip](https://pip.pypa.io/en/stable/installing/):

```shell
pip install abt
```

## Usage

Run `abt` shows basic usage and available sub-commands.

Add a BitTorrent task form local torrent file:

```
abt add ubuntu-17.04-desktop-amd64.iso.torrent
```

Use `--uri` to add a torrent file on web:

```
abt add --uri "http://releases.ubuntu.com/17.04/ubuntu-17.04-desktop-amd64.iso.torrent"
```

And you can add additional options to task:

```
abt add ubuntu-17.04-desktop-amd64.iso.torrent \
  --dir=/media/Downloads/ubuntu \
  --seed-ratio=1.0
```

To save files to `/media/Downloads/ubuntu` and stop seeding on seed ratio reaching `1.0`
(see [full list of options][options]).

Run `abt status` to show task status.

### Customized RPC service

abt connects to aria2 RPC on http://localhost:6800 by default. You can change that by specifying `--jsonrpc` option.
If you're using HTTPS with certificate signed by self-signed CA. You can add CA certificate with `--ca-certificate` (for CA certificate only).
There's a `--no-verify` option for self-signed root certificate which is considered insecure and should better be avoided.

## aria2.conf

abt connects to RPC server created by aria2. To enable RPC on port 6800 (by default):

```
enable-rpc=true

rpc-listen-port=6800
rpc-allow-origin-all=true
```

Here's some session control options help tasks surviving the restart of aria2 daemon.

```
max-concurrent-downloads=999 # controls number of tasks in downloading/seeding state
force-save=true              # save completed tasks for seeding
bt-seed-unverified=true      # resume seeding without verify files (start seeding faster)
input-file=.aria2.session    # load session from .aria2.session (file must exists)
save-session=.aria2.session  # save session to .aria2.session
save-session-interval=60     # save session every 60 seconds
async-dns=false              # turn-off asynchronous dns (which does not work well with ipv6-only domains)
```

BitTorrent options:

```
seed-ratio=0                 # seed forever (or stop when reaches specified seed-ratio)
bt-max-peers=96
bt-tracker-connect-timeout=1
bt-tracker-interval=0
bt-tracker-timeout=10
```

Work with Private Tracker (PT):

```
user-agent=uTorrent/341(109279400)(30888)
                             # override user agent string
peer-id-prefix=-UT341-       # override peer id
enable-dht=false
enable-peer-exchange=false
bt-enable-lpd=false
bt-exclude-tracker=*         # when you want to override trackers
bt-tracker=...               # your tracker assigned by PT service (do NOT add double/single quotes)
```

## License

(The MIT License)

[aria2]: https://aria2.github.io/
[options]: https://aria2.github.io/manual/en/html/aria2c.html#input-file
