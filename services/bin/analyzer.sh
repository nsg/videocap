#!/bin/bash

if [[ "$(snapctl get analyzer)" != "enabled" ]] && [[ "$ANALYZER" != "enabled" ]]; then
    echo "Analytics service not enabled, shutting down service"
    snapctl stop videocap.analyzer-service
    exit 0
fi

RAMDISK=/var/videocap

analyzer() {
    local file="$2/$1"
    local camera="$2"

    echo "ANALYZE: $file"
    if $SNAP/bin/analyzer "$file"; then
        echo "Found movement in $file, push image"

        if [[ "$(snapctl get debug)" == "enabled" ]]; then
            mkdir -p $SNAP_COMMON/movements
            echo "[DEBUG] Save video and jpegs to $SNAP_COMMON/movements"
            cp "$RAMDISK/$file" $RAMDISK/$camera/*.jpg $SNAP_COMMON/movements
        fi

        UNT="$(date +%s%N)"
        mv $RAMDISK/$camera/{match,$UNT}.jpg
        $SNAP/bin/push-nextcloud.sh $RAMDISK/$camera/$UNT.jpg && rm $RAMDISK/$camera/$UNT.jpg
    elif [[ "$(snapctl get debug)" == "enabled" ]]; then
        echo "[DEBUG] Save jpegs to $SNAP_COMMON"
        cp $RAMDISK/$camera/*.jpg $SNAP_COMMON
    fi
}

watch_for_new_file() {
    inotifywait -qe close_write --format "%f" $1
}

RTSP_CAMERA_SOURCES="$(snapctl get rtsp-camera-sources)"
for camera in $(echo $RTSP_CAMERA_SOURCES | tr ',' ' '); do
    SCORE_NAME="$(echo $camera | sed 's/[^a-z0-9]/_/g')"
    echo "Analyzer started for camera $camera ($SCORE_NAME)"
    while sleep 1; do
        analyzer "$(watch_for_new_file $RAMDISK/$SCORE_NAME)" "$SCORE_NAME"
    done &
done

wait
