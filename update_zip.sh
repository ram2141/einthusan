#!/bin/bash

echo "Looking for addons to update"

for plugin in `ls -d *`
do
    if [ -f $plugin/addon.xml ]
    then
        if [ ! -f  $plugin/pre_release ]
        then 
            echo "Checking addon" $plugin
            latest_version_number=`cat $plugin/addon.xml | grep "  version=" | awk -F\" '{print $2}'`
            repo_version_number=`ls repo/$plugin/*.zip |  awk -F\- '{print $2}' | sed 's/.zip//'`
            echo "Dev version=" $latest_version_number " VS Repo Version=" $repo_version_number

            if [ $latest_version_number != $repo_version_number ] ; then
                echo "[UPDATE FOUND]: Updating to version " $latest_version_number
                rm -rf repo/$plugin/*.zip
		        git archive --format=zip --prefix=$plugin/ HEAD:$plugin/ > repo/$plugin/$plugin-$latest_version_number.zip
                cp $plugin/changelog.txt repo/$plugin
            fi
        fi
    echo '------------------------------------------------'
    fi
done
