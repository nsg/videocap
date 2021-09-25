#!/bin/bash

die() {
    echo "$@"
    exit 1
}

RTSP_CAMERA_SOURCES="$(snapctl get rtsp-camera-sources)"

[ -z "$RTSP_CAMERA_SOURCES" ] && die "Please specify an array of RTSP camera sources: snap set videocap rtsp-camera-sources='10.0.0.1:554/s0,10.0.0.2:554/s0'"

# TODO: This is not a prefect solution, a single camera may fail and the script will not detect this
for camera in $(echo $RTSP_CAMERA_SOURCES | tr ',' ' '); do
    SCORE_NAME="$(echo $camera | sed 's/[^a-z0-9]/_/g')"
    $SNAP/command-ffmpeg.wrapper \
        -rtsp_transport tcp \
        -i rtsp://$camera \
        -reconnect 1 \
        -vcodec copy \
        -acodec copy \
        -map 0 \
        -f segment \
        -segment_time 10 \
        -segment_format mp4 \
        -segment_wrap 10 \
        -reset_timestamps 1 \
        "/var/videocap/${SCORE_NAME}-%01d.mp4" &
done

wait
