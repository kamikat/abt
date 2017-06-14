# a2torrent

BitTorrent workflow with [aria2][aria2].

## Overview

a2torrent is a workflow managing BT tasks on local filesystem.

```
<storage-root>
├── .abt/
├── Title-of-Task-1/
│   ├── eedf66261594f8af6d703d3f8481f3feb8647c01.torrent
│   └── ...
└── Title-of-Task-2/
    ├── 338d555de5702d49a51963bbc1e2ee9408ebb362.torrent
    └── ...
```

`.abt/` folder stores metadata and running config of the workflow. `abt` command will searches for `.abt/` folder recursively.

## Usage

To create a storage root:

```shell
abt init Downloads
```

Or init an existing filder as storage root:

```shell
abt init
```

By default, abt connects to `http://localhost:6800/jsonrpc`. To change the RPC setting:

```shell
abt config rpc.endpoint http://localhost:6800/jsonrpc
```

If the connection to RPC server is secured with a self-assigned certificate, the certificate file is required:

```shell
abt config rpc.certpath /path/to/cert.pem
```

Run `abt status` to test your config.

## CLI Reference

#### `abt init [<name>]`

Create a storage root. If _name_ parameter is omitted, a storage root is initialized at current directory.

#### `abt config <section>.<name> [<value>] | -e`

Change configuration.

- `rpc` section sets how RPC service is connected
- `task` section sets default options for new tasks (see [aria2 manual][options])

#### `abt add [--title=<title>] [OPTIONS] <torrent>|<torrent_uri>|<magnet_uri>|<task_folder>`

Add download task from torrent file, magnet or link to torrent file.

When `--title` is omitted, title of torrent is used to name the task folder.

Here's a full list of _OPTIONS_ available in [aria2 manual][options].

#### `abt ps [--format=<pattern>]`

Print task list with summary information (id/size/progress/upload/sr/...).

#### `abt status [<task_folder>|<task_id>]`

Summary of current storage root.

When running in task folder, the command prints file and peer informations of current task.

#### `abt logs [-f]`

Show event logs in current storage root.

#### `abt start`

Start download/seeding task.

#### `abt stop`

Stop download/seeding task.

#### `abt update`

Update task options.

#### `abt rm [--purge] <task_folder>|<task_id>`

Remove task. Add `--purge` flag if you want the task folder being erased from disk.

Removed task can be added back for seeding with `abt add <task_folder>`.

#### `abt rehash`

Re-index storage root.

#### `abt new-torrent [-i] [<task_folder>]`

Generate torrent file for files in `<task_folder>`. When `<task_folder>` is omitted, a torrent file will be created for current directory. For security, `abt` will refuse to create a torrent for storage root.

The `-i` option opens an editor to edit torrent information.

## Development

- Python 2.7
- better-bencode
- jsonrpclib

## License

(The MIT License)

[aria2]: https://aria2.github.io/
[options]: https://aria2.github.io/manual/en/html/aria2c.html#input-file
