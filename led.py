import datetime
import subprocess
import time

import pymobitec_flipdot as flipdot
import serial

intf = "wlan0"
intf_ip = subprocess.Popen(
    "ip address show dev " + intf, shell=True, stdout=subprocess.PIPE
).stdout.read()
print(intf_ip.decode())
intf_ip = intf_ip.decode().split()
host_ip = intf_ip[intf_ip.index("inet") + 1].split("/")[0]

print("trying to open uart")
with serial.Serial("/dev/ttyS0", 4800, timeout=1) as ser:
    print("uart open")
    # msg2 = flipdot.set_text("TAMPERE HACKLAB HELLO WORLD!", 00, 0x00, flipdot.Fonts.text_9px)
    msg_ip = flipdot.Text("IP: {}".format(host_ip), 00, 0x00, flipdot.Fonts.text_9px)
    msg_host = flipdot.Text(
        "trehacklab@trehacklabled.local", 20, 0, flipdot.Fonts.text_9px
    )
    msg = flipdot.set_texts([msg_ip, msg_host])
    ser.write(msg)
    print("message send!")
    time.sleep(10)
    while True:
        # print("Time loop")
        time_now = datetime.datetime.now()
        time_str = time_now.strftime("%H:%M:%S")
        timestuff = flipdot.Text(time_str, 0, 0, flipdot.Fonts.text_16px_bold)
        hellotext = flipdot.Text("Dev me hard!", 65, 0, flipdot.Fonts.text_16px_bold)
        textstuff = flipdot.Text("TAMPERE HACKLAB", 0, 25, flipdot.Fonts.text_7px_bold)
        msg = flipdot.set_texts([timestuff, hellotext, textstuff])
        # print(msg)
        ser.write(msg)
        time.sleep(1)
