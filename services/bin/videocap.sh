#!/bin/bash

die() {
    echo "$@"
    exit 1
}

DISK_USAGE_LIMIT_MB=512
VIDEO_SAVE_DAYS=1
VIDEO_REMOVE_SMALLER_THAN=32k
RTSP_CAMERA_SOURCES="$(snapctl get rtsp-camera-sources)"

if [ -z "$RTSP_CAMERA_SOURCES" ]; then
    die "Please specify an array of RTSP camera sources: snap set videocap rtsp-camera-sources='rtsp://10.0.0.1:554/s0,rtsp://user:password@10.0.0.2:554/s0'"
fi

clean_files() {
    DISK_USAGE="$(du -ms $SNAP_COMMON | cut -f1)"
    if [[ $DISK_USAGE -gt $DISK_USAGE_LIMIT_MB ]]; then
        REMOVE="$(ls -t $1 | tail -1)"
        echo "Remove: $REMOVE"
        rm "$1/$REMOVE"
    fi

    find $1 -type f -mtime +${VIDEO_SAVE_DAYS} -delete
    find $1 -type f -size -${VIDEO_REMOVE_SMALLER_THAN}
}

while [ 1 ]; do
    for CAMERA in $(echo $RTSP_CAMERA_SOURCES | tr ',' ' '); do
        CAMERA_FILTERED=${CAMERA/*@}
        SCORE_NAME="$(echo $CAMERA_FILTERED | sed 's/[^a-z0-9]/_/g')"
        STORDIR="$SNAP_COMMON/$SCORE_NAME"
        FILENAME="$(date +%F_%H)"
        mkdir -p "$STORDIR"

        echo "Camera $CAMERA_FILTERED found"
        echo "Movements will be stored to $STORDIR"
        echo "Filename $FILENAME"

        clean_files "$STORDIR"
        $SNAP/bin/videocap --camera "$CAMERA" --output "$STORDIR/$FILENAME" &
    done
    wait
done
