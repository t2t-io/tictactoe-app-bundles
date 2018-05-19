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
