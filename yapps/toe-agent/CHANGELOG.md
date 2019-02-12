### 0.9.5

- Update node/peripherals with single HTTP POST request in dm-po-uploader.
- Update Node with following information
  - macaddr_eth, from environment variable `YAPPS_DM_NODE_MACADDR_ETH`
  - macaddr_usb, from environment variable `YAPPS_DM_NODE_MACADDR_USB`
  - macaddr_wlan, from environment variable `YAPPS_DM_NODE_MACADDR_WLAN`
  - macaddr_ble, from environment variable `YAPPS_DM_NODE_MACADDR_BLE`
  - macaddr_blemo, from peripheral object `blemo` if available
  - version, from environment variable `BOARD_BASE_VERSION`

### 0.9.2

- Support restart timer in dg-ts-uploader. By default, the restart timeout is `http_operation_timeout` + 5 seconds.

### 0.9.1

- Fix infinite timer when tcp-connection is always failed to establish

### 0.9.0

- Fix crash when id equals to sn in dm-po-uploader.

### 0.8.9

- API: `/api/v3/a` to list all active agents.

### 0.8.8

- DG: uploader supports finalization by flushing memory cached data to backend storage with serialization
- DM: uploader supports finalization by flushing memory cached data to backend storage with serialization

### 0.8.7

- DG: uploader supports dynamic pack-interval based on the number of local cache files for time-series data
  - min interval of packing sensor archive is 30s
  - max interval of packing sensor archive is 1200s
  - incremental ratio is 20%
- DG: uploader supports boost mode.
  - At boost mode, the interval of packing sensor archive is always 10s
  - The max period for boost mode is 25 minutes ([Pomodoros](https://en.wikipedia.org/wiki/Pomodoro_Technique))
  - Web-api: `http :6040/api/v3/ticc/uploaders/dg-ts/perform/boost-upload period:=62`

### 0.8.6

- Rollback to use profile_version as version of the peripheral object `linux_boot`.

### 0.8.5

- Post `linux_boot` peripheral object update to TIC DM server.

### 0.8.4

- Drop data job when it's failed to load from disk or memory, to prevent consuming same job forever due to load error.

### 0.8.3

- Yapps improve the handling of shutdown re-entrance
- Yapps move _optimist_ from BaseApp to yapps.ls as entry
- Yapps move yap-simple-logger in, and code refactorying
- Yapps add `logger` commands to command-unixsock

### 0.8.1

- Yapps upgrade tcp-socket and unix-socket servers.

### 0.8.0

- Yapps upgrade with pidfile / ppidfile supports

### 0.7.5

- Support DM peripheral object's state/metadata with offline cache and time calibration with uptime

### 0.7.2

- Fix preference merge bug.

### 0.7.1

- Support DM peripheral object's state/metadata. No cache implementation yet.

### 0.7.0

- Support DG offline cache for TimeSeries data
  - No dynamic pack interval
  - No dynamic upload interval
  - No circular buffer in queue implementation (for entire disk size quota management)
  - No dynamic priority (oldest first, latest first, largest first, ...).

### 0.6.3

- Add new api `list-peripheral-types-in-details` to jarvis in order to read actuator/sensor spec for each peripheral_type.

### 0.6.2

- Upgrade [request](https://github.com/request/request/blob/master/CHANGELOG.md) from 2.72.0 to 2.87.0

### 0.6.1

- Use new package.json to install node_modules from scratch, and bundle.

### 0.6.0

- Add/Expose following node modules that are compiled into the app bundle
  - [prettyjson](https://www.npmjs.com/package/prettyjson), 1.1.3
  - [semver](https://www.npmjs.com/package/semver), 5.5.0
  - [yaml_loader](https://github.com/nodeca/js-yaml/blob/master/lib/js-yaml/loader.js), 3.11.0
  - [yaml_safeLoad](https://github.com/nodeca/js-yaml/blob/master/lib/js-yaml/loader.js#L1598)
  - [uuid_v1](https://github.com/kelektiv/node-uuid/blob/master/v1.js), 3.2.1
  - [uuid_v4](https://github.com/kelektiv/node-uuid/blob/master/v4.js)

### 0.5.6

- Expose following node modules that are compiled into the app bundle
  - express
  - async
  - uid
  - body-parser
  - handlebars

### 0.5.5

- Re-build app bundle with newer toolchain
  - browserify, `13.0.0` to `15.2.0`
  - exorcist, `1.0.0` to `1.0.1`
  - uglify, `2.6.2` to `2.8.29`

### 0.5.1

- Add socketio-namespace and frontend-asset to agent/jarvis
- Add CORS in web/socket.io settings

### 0.5.0

- Add socket.io namespace api to Agent/Jarvis
- Add frontend page handler for Agent
- Fix run script

### 0.4.6

- Upgrade nodejs from 4.4.7 to 8.11.1 in Docker container.

### 0.4.5

- Externalize `request` node module.

### 0.4.4

- Use fullname of agent instance to show warning messages.

### 0.4.3

- Update config.json with t2t servers.

### 0.4.2

- Yapps supports `-o` command-line option to assign JSON object into app's configs.

### 0.4.1

- Fix dm-client crash when missing token in `/tmp/ttt.system` (as system information).
- Enable more checkings before enabling dm-client.

### 0.4.0

- Support DM (device-management) client in `tic-client` plugin.

### 0.3.9

- Jarvis supports `sys-get-system-info`

### 0.3.8

- Implement Agent's `at-blemo-cmd-queue-dequeued` and `at-blemo-raw-queue-dequeued` callbacks.

### 0.3.7

- Fix critical bug, need to use Agent's context to invoke `at-sensor-updated()` callback

### 0.3.6

-  Upgrade [socket.io](https://socket.io) (including client) from 1.3.7 to 2.0.4.

### 0.3.5

- Jarvis supports Sensor tree apis (from snapshot storage)
  - `sensortree-list-peripheral-types`
  - `sensortree-list-peripheral-ids`
  - `sensortree-list-sensor-types`
  - `sensortree-list-sensor-ids`
  - `sensortree-get-sensor-data`
  - `sensortree-get-snapshot`

### 0.3.4

- Jarvis correctly implements attach() and detach() semantics

### 0.3.3

- Jarvis supports `get-peripheral-object-info`.

### 0.3.2

- Fix `blemo-modem-reset` missing callback issue

### 0.3.1

- Jarvis supports `list-peripheral-types` and `list-peripheral-ids`

### 0.3.0

- Fix sensor upload interval issue (tic-client)
- Fix class name (the constructor.name) is changed after obfuscation when accessing BluetoothModem constructor

### 0.2.9

- Reset bluetooth modem when Blemo transmission is closed

### 0.2.8

- Add bluetooth modem apis to Agent/Jarvis
- Use bluetooth modem to transfer files via `&` and `*` Command Channels

### 0.2.7

- Fix missing blemo event issue (as side-effect of 0.2.5 release)

### 0.2.6

- Fix crash caused by empty name string from `YAPPS_EXTRA_AGENTS`

### 0.2.5

- Support DG and upload with simplest algorithm

### 0.2.4

- Remove pug node module dependency

### 0.2.3

- Support blemo push direct/command channel APIs in Agent/Jarvis

### 0.2.2

- Support blemo command packet dispatch to different agent based agent's preferences

### 0.2.1

- Refactor Agent's blemo events

### 0.2.0

- Support blemo partially (with incoming packets and state updates)

### 0.1.6

- Yapps removes `extendify`

### 0.1.5

- Support web command processing in Agent with `process-web-command` callback

### 0.1.3

- Fix typo of callback 'at-sensor-updated'

### 0.1.2

- Add multiple verbose levels to sensorweb3-client
- Broadcast sensor data from tcp client when wss client is ready

### 0.1.1

- Implement `jarvis::perform-actuator-action()`

### 0.1.0

Initial version of ToeAgent on yapps framework with following default plugins:

- `system-info`
- `system-helpers`
- `profile-storage`
- `sensorweb3-client`
