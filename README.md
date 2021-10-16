# Videocap

## Install

```
sudo snap install videocap
```

### Configure

```
sudo snap set videocap nextcloud-server=nextcloud.example.com
sudo snap set videocap nextcloud-token=hUio...
sudo snap set videocap rtsp-camera-sources='127.0.0.1:5554/s0,10.0.0.1:1234/f1'
```

## Develop

### Manually run the analyzer

```
VIDEOCAP_DATA=foo/1/ python3 analyzer/analyzer.py ffmpeg_capture-0.mp4
```

... or this is probably easier:

```
analyzer() { VIDEOCAP_DATA="${1%/*}" python3 analyzer/analyzer.py "${1##*/}"; }
analyzer foo/1/ffmpeg_capture-0.mp4
```
