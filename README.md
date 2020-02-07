# Lab bus led screen software

WIP

https://tampere.hacklab.fi/led-matriisin%c3%a4ytt%c3%b6/

# setup for now (raspi zerow)

```
cd ~

# our user needs access to serial
sudo usermod -a -G dialout trehacklab

# activate serial (raspi-config, interfacing options, no login, enable serial hardware). requires reboot

# some pre requisities
sudo apt-get install pipenv libatlas-base-dev python3-numpy python3-serial

# clone
mkdir git
cd git
git clone https://github.com/TampereHacklab/trehacklabled.git
cd ~/git/trehacklabled

# test that it works
python3 led.py

# setup autostartup stuff
cp autoupdate.sh startup.sh ~/

mkdir -p ~/.config/systemd/user/
cp ledmatrix.service ~/.config/systemd/user/
cp autoupdate.service ~/.config/systemd/user/
systemctl --user daemon-reload

systemctl --user enable ledmatrix
systemctl --user enable autoupdate

reboot
```

autoupdate will check for new code in the repo every 15 minutes and restart the services if required
