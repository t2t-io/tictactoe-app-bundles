### 0.7.5

- Update timeout from 30s to 120s
- Improve hostname retrieval on Mac OS X by removing its `lan` postfix (e.g. `grandia.lan`)

### 0.7.4

- Use yapps to load `package.json` instead of pkginfo

### 0.7.3

- Implement `AGENT_EVENT_HTTP_BY_SERVER`
- Use symbolic link to solve closure issue (cross-directory)

### 0.7.2

- Use hostname and mac address string (upper-case) to compose device unique identity.

### 0.7.1

- Improve pkginfo detection with directly-access to `module` variable by skipping browserify manipulation (storing `module` in the `global.yac-context` variable)

### 0.7.0

- Implement protocol 0.2.0
- Improve network interface information gathering for Mac OS X

### 0.6.0

- Upgrade [socket.io-client](https://github.com/socketio/socket.io-client) from 1.3.7 to 2.0.4, to paired with WsttyServer 0.6.0.

### 0.2.7

- Replace [pty.js](https://github.com/chjj/pty.js) with [node-pty](https://github.com/Tyriar/node-pty).

### 0.2.6

- Generate unique identity from the mac address of ethernet adapter when `/tmp/ttt_system` is unavailable

### 0.2.5

- `restart_agent` event to force agent to restart itself immediately

### 0.2.4

- Add sys output to tty data for notifying server about child process status

### 0.2.3

- Change default restart_timeout (DEFAULT_RESTART_TIMEOUT) from 1 minute to 20 minutes.

### 0.2.2

- Change default restart_timeout from 1 min to 20 minutes.

### 0.2.1

- Restart wstty-agent when disconnected more than `restart_timeout` specified in config.json

### 0.2.0

- Refactor packet protocol in order to support both `pty.spawn` and `child_process.spawn`
- Support "exec" subcommand from wstty-cli

### 0.1.1

- Support `BOARD_PROFILE_ENV` in configuration generation because of https://github.com/yagamy4680/yapps/commit/f74b0736dc01d12e8143a25e5dea9d21241aaabf for wstty-agent

### 0.1.0

- Apply new configuration generation algorithm from https://github.com/yagamy4680/yapps/commit/f74b0736dc01d12e8143a25e5dea9d21241aaabf for wstty-agent

### 0.0.5

- Enable regular-gc

### 0.0.4

- Minor upgrade because of `system-info` plugin bugfix for missing Wifi.

### 0.0.3

- Minor upgrade because of `system-info` plugin update

### 0.0.2

- Enclose `socketio.auth` and `request` modules.

### 0.0.1

Initial version of WebSocket TTY Agent.
