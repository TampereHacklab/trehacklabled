#! /bin/bash

# polls github and if there are changes available pulls them and restarts the service
#

while true
do
	cd ~/git/trehacklabled
	git fetch
	LOCAL=$(git rev-parse HEAD);
	REMOTE=$(git rev-parse @{u});

	if [ $LOCAL != $REMOTE ]; then
	        git pull origin master
		systemctl --user stop ledmatrix.service
		systemctl --user start ledmatrix.service
	fi
sleep 900
done
