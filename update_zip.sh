#!/bin/bash

if [ $1 = "CanadaNepal" ]; then
    zip -r repo/plugin.video.canadanepal/plugin.video.canadanepal-$2.zip plugin.video.canadanepal/
    cp plugin.video.einthusan/changelog.txt repo/plugin.video.einthusan/
elif [ $1 = "Einthusan" ]; then
    zip -r repo/plugin.video.einthusan/plugin.video.einthusan-$2.zip plugin.video.einthusan/
     cp plugin.video.canadanepal/changelog.txt repo/plugin.video.canadanepal/
fi
