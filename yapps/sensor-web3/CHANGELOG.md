### 3.6.1

- Expose following node modules that are compiled into the app bundle
  - express
  - async
  - uid
  - body-parser
  - handlebars

### 3.6.0

- Re-build app bundle with newer toolchain
  - browserify, `13.0.0` to `15.2.0`
  - exorcist, `1.0.0` to `1.0.1`
  - uglify, `2.6.2` to `2.8.29`

### 3.5.9

- Fix the bug when sending sensor data update via wss module.

### 3.5.8

- Fix ps/console-handler crash bug

### 3.5.7

- Improve sensor data emitter to accept dictionary data object, in addition to array of data elements.
- Fix crash issue when websocket client does not want blemo but SensorWeb3 has enabled blemo service.

### 3.5.6

- Add `process-web-command` to PeripheralService

### 3.5.4

- Up a version to export Docker with port 6024

### 3.5.3

- Add one more socket server at port 6024 to broadcast the events of sensor-updated and peripheral-updated that apps (e.g. Ironman2) are interested. By default, only broadcast events with peripheral_type `linux`.

### 3.5.2

- Improve `-o` command-line option to support base64-encoded json string. For example, `-o ^communicator.connections.uno:ewogICJlbmFibGVkIjogdHJ1ZSwKICAidXJsIjogInRjcDovLzEuMS4xLjE6MzAiLAogICJjaGFubmVsIjogbnVsbCwKICAiYnJvYWRjYXN0IjogZmFsc2UKfQo=` is to set `communicator.connections.uno` with following json object:

```json
{
  "enabled": true,
  "url": "tcp://1.1.1.1:30",
  "channel": null,
  "broadcast": false
}
```

### 3.5.1

- Yapps supports `-o` command-line option to assign JSON object into app's configs.

### 3.5.0

- Fix DefaultAuthenticator crash bug for client other than 127.0.0.1. ([c958ac2dc83251b271e4a1c65a9a4825aef58b74](https://github.com/yagamy4680/yapps/commit/c958ac2dc83251b271e4a1c65a9a4825aef58b74))

### 3.4.9

- Fix crash when blemo service is disabled.

### 3.4.8

- Add wireless adapter information (iwconfig).
- Use OUI database to get manufacturer information for access point that current wireless adapter connects to.

### 3.4.7

- Support peripheral state update via port 6023

### 3.4.6

- Support array of payloads (buffers) in `blemo-push-command-channel`

### 3.4.5

- Support LED trigger in Blemo service

### 3.4.4

- Support `blemo_cmd_queue_dequeued` and `blemo_raw_queue_dequeued` events.

### 3.4.3

- Upgrade [socket.io](https://socket.io) (including client) from 1.3.7 to 2.0.4.
- Delete following modules from `node_modules` directory
  - extendify
  - influx
  - jade
  - lodash.assign
  - lodash.find
  - lodash.findindex
  - lodash.merge
  - lodash.sum
  - passport
  - passport-http
  - prelude-ls
  - pty.js
  - request-debug
- Add prettyjson bundle

### 3.4.2

- Support sensor snapshort api `/api/v3/d`
- Support sensor tree data api `/api/v3/s`

### 3.4.1

- Refactor to simplify webapi get query.
  - remove `list-peripheral-types`
  - remove `list-peripheral-ids`
  - add `wsrr_perform_webapi_get`
- Add `GET_PERIPHERAL_OBJECT_INFO`

### 3.4.0

- Add `list-peripheral-types` and `list-peripheral-ids` to client-websocket.

### 3.3.9

- Support connect action in `linux-wireless` peripheral service

### 3.3.8

- Add command channel `&` for blemo
- Add command channel `*` for blemo
- Replace `yapps-utils` with `yapps_utils`

### 3.3.7

- Add results of `actuator-perform-action` to webapi response

### 3.3.6

- Fix communicator connection listener bug
- Add `excluded_p_types` to `ps-evt-handler/console` to exclude sensor events from given types of peripheral

### 3.3.5

- blemo: websocket client supports `push-command-channel` and `push-direct-channel`

### 3.3.4

- blemo: add `%` to default channel list

### 3.3.2

- blemo: broadcast channel event properly

### 3.3.1

- Yapps removes `extendify`

### 3.3.0

- Add blemo service to manage Nordic board
- Support connection state and notification state of Nordic board as sensor data updates

### 3.2.0

- Ignore plugin path with empty string

### 3.1.9

- Add `client` websocket channel with minimal functionality: `perform-actuator-request`

### 3.1.8

- Add `system-info`

### 3.1.7

- Disable reconnect in communicator/tcp and communicator/unixsock when shutting down

### 3.1.6

- Update yapps with peaceful shutdown mechanism
- Implement communicator with peaceful shutdown, especially for `linux-stats` with python child process
- Remove `extendify` from communicator/exec

### 3.1.5

- Disable all communicator connections by default
- `tcp-proxy` initiates each bridge when its associated communicator connection is available
- `linux-stats` peripheral service is initiated when `communicator[stats]` is available

### 3.1.4

- Guess physical device from symbolic link in TcpProxy
- Fix null-pointer in tcp-proxy plugin correctly: Register data listener after metadata guessing to ensure `DataFormatter` object is initiated before any incoming data

```text
/Users/yagamy/Works/workspaces/t2t/yapps-tt/apps/sensor-web3/lib/tcp-proxy.ls:201
    formatter.pre-format data, from-remote
             ^
TypeError: Cannot read property 'preFormat' of undefined
    at Bridge.prototype.log (/Users/yagamy/Works/workspaces/t2t/yapps-tt/apps/sensor-web3/lib/tcp-proxy.ls:201:14)
    at Bridge.prototype.from_cc_data (/Users/yagamy/Works/workspaces/t2t/yapps-tt/apps/sensor-web3/lib/tcp-proxy.ls:188:7)
    at /Users/yagamy/Works/workspaces/t2t/yapps-tt/apps/sensor-web3/lib/tcp-proxy.ls:106:63
    at ConnectionWrapper.prototype.emit (/Users/yagamy/Works/workspaces/t2t/yapps-tt/plugins/communicator/lib/communicator.ls:81:12)
    at ConnectionWrapper.prototype.atData (/Users/yagamy/Works/workspaces/t2t/yapps-tt/plugins/communicator/lib/communicator.ls:34:14)
    at /Users/yagamy/Works/workspaces/t2t/yapps-tt/plugins/communicator/lib/communicator.ls:71:40
    at Stream.write (/Users/yagamy/Works/workspaces/t2t/yapps-tt/plugins/communicator/lib/tcp.ls:91:7)
    at Stream.stream.write (/conscious/current/apps/sensor-web3/sensor-web/node_modules/through/index.js:26:1)
    at Socket.ondata (_stream_readable.js:542:20)
    at emitOne (events.js:77:13)
```

### 3.1.3

- Fix null-pointer in tcp-proxy plugin

```text
TypeError: Cannot read property 'preFormat' of undefined
    at t.n.log (/conscious/current/apps/sensor-web3/app/bundle.js:22:16264)
    at t.n.from_cc_data (/conscious/current/apps/sensor-web3/app/bundle.js:22:16026)
    at /conscious/current/apps/sensor-web3/app/bundle.js:22:13634
    at t.n.emit (/conscious/current/apps/sensor-web3/app/bundle.js:24:14806)
    at t.n.atData (/conscious/current/apps/sensor-web3/app/bundle.js:24:13391)
    at /conscious/current/apps/sensor-web3/app/bundle.js:24:14661
    at Stream.m (/conscious/current/apps/sensor-web3/app/bundle.js:24:22833)
    at Stream.u.write (/conscious/current/apps/sensor-web3/app/bundle.js:21:1561)
    at Socket.ondata (_stream_readable.js:542:20)
    at emitOne (events.js:77:13)
```

### 3.1.2

- Improve communicator/exec to support data listener, in order to bride linux-stats data to socket server at port 10020
- Add `linux-wireless` peripheral service
- Automatically disable TcpProxy when Communicator is disabled

### 3.1.1

- Fix wireless signal sensors
  - from `linux/7F000001/wireless_quality/quality` to `linux/7F000001/wireless_quality/wlan0`
  - from `linux/7F000001/wireless_discarded/discarded` to `linux/7F000001/wireless_discarded/wlan0`

### 3.1.0

- Improve httpstat sensor by grouping values with same prefix

### 3.0.9

- Support Linux Stats sensors.

### 3.0.8

- Broadcast sensor data with [JSON Lines](http://jsonlines.org/) format via tcp-port 6022.

```text
$ socat - tcp-connect:127.0.0.1:6022
[0,80221,1511115205467,"sensorboard","ttySENSOR0","humidity","_",{"temperature":23.1,"humidity":73.2}]
[0,80324,1511115205570,"sensorboard","ttySENSOR0","barometric_pressure","_",{"pressure":1020}]
[0,80426,1511115205672,"sensorboard","ttySENSOR0","ndir_co2","_",{"co2":511}]
...
```

```json
// $ socat - tcp-connect:127.0.0.1:6022 | jq .
[
  0,
  7306,
  1511115132553,
  "sensorboard",
  "ttySENSOR0",
  "humidity",
  "_",
  {
    "temperature": 23.2,
    "humidity": 73
  }
]
[
  0,
  7404,
  1511115132652,
  "sensorboard",
  "ttySENSOR0",
  "barometric_pressure",
  "_",
  {
    "pressure": 1020.1
  }
]
...
```

### 3.0.7

- Fix remote peripheral-service's `null` unregistration due to authentication failure via websocket

### 3.0.6

- Support monitor in tcp-proxy with data dump

### 3.0.5

- Support **multiple** pipes in single peripheral-service, and give pipe's `metadata` to peripheral-service when init
- Extend websocket client to support multiple pipes in single peripheral-service

### 3.0.4

- Size reduction
  - Use latest Yapps module that removes the dependency to [prelude-ls](http://www.preludels.com/) library.
  - Use lodash_sum from Yapps.

### 3.0.3

- Disable communicator by default

### 3.0.2

- Support peripheral-service with PIPE mode, in both local and remote (websocket)

### 3.0.1

- Add tcp-proxy feature

### 3.0.0

Intial version of SensorWeb3.
