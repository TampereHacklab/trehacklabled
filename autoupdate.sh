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
		sudo systemctl stop ledmatrix.service
		sudo systemctl start ledmatrix.service
	fi
sleep 60
done
