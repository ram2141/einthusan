#!/bin/bash

if [ $1 = "Canada" ]; then
    zip -r repo/plugin.video.canadanepal/plugin.video.canadanepal-$2.zip plugin.video.canadanepal/
elif [ $1 = "Ein" ]; then
    zip -r repo/plugin.video.einthusan/plugin.video.einthusan-$2.zip plugin.video.einthusan/
fi
