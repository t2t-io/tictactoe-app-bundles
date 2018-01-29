### 0.2.3

- Disable `onUpload` when sensorweb-uploader is disabled

### 0.2.2

- Fix missing sensor data issue

### 0.2.1

- Support to enable/disable TOE-DG3 data uploading
- Support to enable/disable TOE-DG1 data uploading

### 0.2.0

- Add TOE-DG3 experimental feature

### 0.1.3

- Change the implementation of timer helper class to decreasing counter (relative time instead of absolute time)
- Use process.uptime() to replace moment() in onUpload() function of sensorweb-uploader plugin

### 0.1.2

- Improve sensorweb-uploader to submit local timezone when uploading sensor archives.

### 0.1.1

- Improve sensorweb-uploader to submit local timestamp when uploading sensor archives.

### 0.1.0

Initial version of DhvacAgent on yapps framework with following default plugins:

- `system-info`
- `registry-client`
- `filecollector-client`
- `system-helpers`
- `profile-storage`
- `sensorweb-client`
- `sensorweb-uploader`
