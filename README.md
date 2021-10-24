# Videocap

## About

I have security cameras installed for about two years. I used the proprietary solution bundled with the product and was quite happy with it. Sure it did not add that much features over "recording movements", but it did filter out "noise" like sunshine, bugs and uninteresting things quite nicely so I was happy with it. The software was abandoned by the company and after a few months is started to get tricky to run it so I started to look around for alternatives.

I had a few requirements:

* FOSS
* Linux based
* It runs on a average computer with only integrated Intel graphics
* Only record movements

I looked around for alternatives but found no one that felt right for me. I found two that looked like they had all the features I needed but documentation lacked and after hours of tinkering I gave up. So I thought, how hard can it be? Compared to these projects I have a much more narrow problem... it would be fun to play a little more with OpenCV... and here we are!

### Who is this for?

Me, and me-like-individuals! If you have RTSP-cameras and like to record movements this may be to some interest for you. It is probably good if you know your way around Python so you can weak the code to your liking to. Pull Requests are welcome, can't promise I merge everything, of course :)

## Design

### Snap package
Ship the application inside a Snap package for easy deployment and management.

### tmpfs
Create a tmpfs filesystem and use it to record files to save write cycles on the storage medium.

### FFmpeg
Use FFmpeg to receive and store the video data. Data is stored in the tmpfs filesystem in 10s chunks.

### Analyze
Watch for file close events, fire of a piece of Python code that do the heavy lifting. At the moment is do this:

* Detect movements, mark them with a green square
* Save movements in a heat map. Use is as a mask to filter out repeating movements
* Require movement at 9-10% of the frames (over 10s) to get rid of noise
* Blend the a frame from the video, the square and heat map to a image
* The top 40 pixels are ignored (contains a timestamp)

Future:

* Maybe: Color matching heuristics (I had this in an earlier version)
* Face detection ("a face" not "who")
* Merge movements from different video frames in to a single image for quick inspection

### Nextcloud
Push the resulting image to a Nextcloud File Drop. In the future the idea it to transmit the actual video.

## Install

```
sudo snap install videocap
```

### Configure

Configure your cameras with a comma separated list like this:

```
sudo snap set videocap rtsp-camera-sources='127.0.0.1:5554/s0,10.0.0.1:1234/f1'
```

Enable recording and video analyzing

```
sudo snap set videocap recorder=enabled
sudo snap set videocap analyzer=enabled
```

Setup your Nextcloud configuration, to get the token. Create a File Drop and copy the share link. The token is part of that URL.

```
sudo snap set videocap nextcloud-server=nextcloud.example.com
sudo snap set videocap nextcloud-token=hUio...
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

The above commands assume you have python3 and the packages specified in [analyzer/setup.py](analyzer/setup.py) installed.

Enable debug mode with `sudo snap set videocap debug=enabled`, that should store masks and jpegs in `$SNAP_COMMON` with movements in a directory called `movements`.
