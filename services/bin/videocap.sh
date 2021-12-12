#!/bin/bash

die() {
    echo "$@"
    exit 1
}

RTSP_CAMERA_SOURCES="$(snapctl get rtsp-camera-sources)"

if [ -z "$RTSP_CAMERA_SOURCES" ]; then
    die "Please specify an array of RTSP camera sources: snap set videocap rtsp-camera-sources='rtsp://10.0.0.1:554/s0,rtsp://user:password@10.0.0.2:554/s0'"
fi

for CAMERA in $(echo $RTSP_CAMERA_SOURCES | tr ',' ' '); do
    CAMERA_FILTERED=${CAMERA/*@}
    SCORE_NAME="$(echo $CAMERA_FILTERED | sed 's/[^a-z0-9]/_/g')"
    STORDIR="$SNAP_COMMON/$SCORE_NAME"
    mkdir -p "$STORDIR"

    echo "Camera $CAMERA_FILTERED found"
    echo "Movements will be stored to $STORDIR"

    $SNAP/bin/videocap --camera "$CAMERA" --output "$STORDIR/video" &
done

wait
