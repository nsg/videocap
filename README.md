# Videocap

## Install

### Clone and install unit files

```
cd /opt
git clone https://github.com/nsg/videocap.git
cp *.service /etc/systemd/system
```

### Configure

```
cp config.sh.sample config-foo.sh # and edit it!
```

### Start the services

```
# enable & start recording for camera foo
systemctl enable videocap-recorder@foo.service
systemctl start videocap-recorder@foo.service

# enable & start analytics for camera foo
systemctl enable videocap-analyzer@foo.service
systemctl start videocap-analyzer@foo.service
```

## Requirements

Packages installed on Ubuntu 20.04 LTS

```
apt install inotify-tools ffmpeg python3-opencv
```
