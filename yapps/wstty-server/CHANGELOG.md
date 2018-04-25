### 0.7.3

- Implement `AGENT_EVENT_HTTP_BY_SERVER`
- Use yapps to load `package.json` instead of pkginfo

### 0.7.1

- Improve pkginfo detection with directly-access to `module` variable by skipping browserify manipulation (storing `module` in the `global.yac-context` variable)

### 0.7.0

- Implement protocol 0.2.0
- Improve mac address and ip address detection
- Improve web UI with humanized uptime and protocol information

### 0.6.3

- Add passport for HTTP Basic Authentication

### 0.6.2

- Replace `prelude-ls` with lodash
- Remove unused module dependencies
  - `jade`
  - `serve-favicon`
  - `multer`
  - `method-override`
  - `express-partial-response`
- Upgrade `pug` from 2.0.0-rc4 to 2.0.3

### 0.6.1

- Upgrade socketio-auth from 0.0.4 to 0.1.0
- Replace [jade](http://jade-lang.com/) with [pug](https://github.com/pugjs/pug)

### 0.6.0

- Upgrade [socket.io](https://github.com/socketio/socket.io) from 1.3.7 to 2.0.4

### 0.5.6

- Update system metrics to sysadmin database

### 0.5.5

- Update settings for replacing web0/monitor with hub000

### 0.5.4

- Slightly change the UI styles for web-terminal
  - `SourceCodePro-ExtraLight` is added to the 1st element of default fonts
  - Change font size to 10px
  - Change FG and BG colors for terminal

### 0.5.3

- Correctly clean up resources for duplicate agent error
- Submit `[db]:/[id]/tic/wstty/agent/duplicate` data every 60s

### 0.5.2

- Use incremental uptime updater
- Force underlying socket connection to be closed when duplicated agent exists (close the newer one)
- Dump more information when duplicate agent takes place

### 0.5.1

- Fix state-updater bug

### 0.5.0

- Add more metrics with iw-client to update influxdb.
  - `[db]:/[id]/tic/wstty/user.[username]/uptime`
  - `[db]:/[id]/tic/wstty/user.[username]/state`
  - `api:/[site]/wstty/system/agents/total`
  - `api:/[site]/wstty/system/agents/onlines`
  - `api:/[site]/wstty/system/agents/offlines`
- Improve verbose messages

### 0.4.3

- Ensure the index of short-connection instance is printed out when disconnection.

### 0.4.2

- Fix short disconnection issue

### 0.4.1

- Add index and username of web terminal pairing

### 0.4.0

- Improve logging messages
- Add system websocket channel for monitoring and management purpose
- Add sensorweb-client to update number of connected agents and the uptime of each agent session

### 0.2.2

- Fix a critical bug that is caused by mis-deleting the listener `me-on-depair` in agent-mgr

### 0.2.1

- Improve state consistency when `disconnect` event takes place before `pair` event

### 0.2.0

- Refactor packet protocol in order to support both `pty.spawn` and `child_process.spawn`

### 0.1.6

- Disable pretty-json outputs

### 0.1.5

- Replace uart-board with communicator
- Replace parser with legacy.ls

### 0.1.0

Initial version of SensorWeb on yapps-tt framework.
