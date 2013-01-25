#!/bin/bash

echo "Updating "  $1  " to version "  $2 

if [ $1 = "CanadaNepal" ]; then
    zip -r repo/plugin.video.canadanepal/plugin.video.canadanepal-$2.zip plugin.video.canadanepal/
    cp plugin.video.einthusan/changelog.txt repo/plugin.video.einthusan/
elif [ $1 = "Einthusan" ]; then
    zip -r repo/plugin.video.einthusan/plugin.video.einthusan-$2.zip plugin.video.einthusan/
    cp plugin.video.canadanepal/changelog.txt repo/plugin.video.canadanepal/
elif [ $1 = "Repo" ]; then
    zip -r repo/repository.humla/repository.humla-$2.zip repository.humla/
    cp repository.humla/changelog.txt repo/repository.humla/
fi
