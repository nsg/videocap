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
        NUM_FILES="$(ls $1 | wc -l)"
        LAST_FILE="$(ls -t $1 | tail -1)"
        if [[ $NUM_FILES -gt 1 ]]; then
            echo "Remove: $LAST_FILE"
            rm "$1/$LAST_FILE"
        fi
    fi

    find $1 -type f -mtime +${VIDEO_SAVE_DAYS} -delete -print
    find $1 -type f -size -${VIDEO_REMOVE_SMALLER_THAN} -delete -print
}

while [ 1 ]; do
    START_TS="$(date +%s)"
    for CAMERA in $(echo $RTSP_CAMERA_SOURCES | tr ',' ' '); do
        CAMERA_FILTERED=${CAMERA/*@}
        SCORE_NAME="$(echo $CAMERA_FILTERED | sed 's/[^a-z0-9]/_/g')"
        STORDIR="$SNAP_COMMON/$SCORE_NAME"
        FILENAME="$(date +%F_%H)"
        mkdir -p "$STORDIR"
        clean_files "$STORDIR"
        echo "Start camera $CAMERA"
        $SNAP/bin/videocap --camera "$CAMERA" --output "$STORDIR/$FILENAME" &
    done
    wait
    END_TS="$(date +%s)"
    if [[ $(($END_TS - $START_TS )) -lt 60 ]]; then
        echo "Last run took less than 60s, backoff and sleep for 60s"
        sleep 60
    fi
done
