#!/bin/bash

echo "Looking for addons to update"

for plugin in `ls -d *`
do
    if [ -f $plugin/addon.xml ]
    then
        if [ ! -f  $plugin/pre_release ]
        then 
            echo "Checking addon" $plugin
            latest_version_number=`cat $plugin/addon.xml | grep "  version=" | grep -Po '(?<=")[^"]+(?=")'`
            repo_version_number=`ls repo/$plugin/*.zip |  grep -Po '\d.\d.\d'`
            echo "Dev version=" $latest_version_number " VS Repo Version=" $repo_version_number

            if [ $latest_version_number != $repo_version_number ] ; then
                echo "Update found..... Updating to version " $latest_version_number
                rm -rf repo/$plugin/*.zip
                zip -rq repo/$plugin/$plugin-$latest_version_number.zip $plugin/
                cp $plugin/changelog.txt repo/$plugin
            fi
        fi
    echo '------------------------------------------------'
    fi
done
