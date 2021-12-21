#!/bin/bash

die() {
    echo "$@"
    exit 1
}

while [ 1 ]; do
    for CAMERA in $(echo $RTSP_CAMERA_SOURCES | tr ',' ' '); do
        CAMERA_FILTERED=${CAMERA/*@}
        SCORE_NAME="$(echo $CAMERA_FILTERED | sed 's/[^a-z0-9]/_/g')"
        STORDIR="$SNAP_COMMON/$SCORE_NAME"

        echo "Process $STORDIR"
        cd $STORDIR
        for f in *.avi; do
            MODE="$(stat --format=%a $f)"
            SIZE="$(stat --format=%s $f)"
            if [[ $MODE == ??4 ]] && [[ $SIZE -gt 32768 ]]; then
                echo "I will upload $f"
                $SNAP/bin/push-nextcloud.sh "$f" && chmod o-r $f
            fi
        done
    done

    sleep 60
done
