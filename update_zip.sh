#!/bin/bash

echo "Updating "  $1  " to version "  $2 

if [ $1 = "CanadaNepal" ]; then
	echo "Packaging to a zip file"  
    zip -r repo/plugin.video.canadanepal/plugin.video.canadanepal-$2.zip plugin.video.canadanepal/
    echo "Now copying the changelog file"
    cp plugin.video.einthusan/changelog.txt repo/plugin.video.einthusan/
elif [ $1 = "Einthusan" ]; then
	echo "Packaging to a zip file" 
    zip -r repo/plugin.video.einthusan/plugin.video.einthusan-$2.zip plugin.video.einthusan/
    echo "Now copying the changelog file"
    cp plugin.video.canadanepal/changelog.txt repo/plugin.video.canadanepal/
fi
