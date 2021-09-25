#!/bin/bash

if [ -z $1 ]; then
    echo "Usage: cat myfile1 | videocap.ingest myfile2"
    echo
    echo "Read myfile1 and ingest it, save it as myfile2"
    exit 1
fi

cat - > $VIDEOCAP_DATA/$1
