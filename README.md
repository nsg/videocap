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

## Project status

Still early prototyping... 

### Nextcloud
Push the resulting image to a Nextcloud File Drop. In the future the idea it to transmit the actual video.

## Install

```
sudo snap install videocap
```

### Configure

Configure your cameras with a comma separated list like this:

```
sudo snap set videocap rtsp-camera-sources='rtsp://127.0.0.1:5554/s0,rtsp://user:password@10.0.0.1:1234/f1'
```

Setup your Nextcloud configuration, to get the token. Create a File Drop and copy the share link. The token is part of that URL.

```
sudo snap set videocap nextcloud-server=nextcloud.example.com
sudo snap set videocap nextcloud-token=hUio...
```
