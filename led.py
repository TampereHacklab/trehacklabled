import datetime
import time

import pymobitec_flipdot as flipdot
import serial

with serial.Serial("/dev/ttyS0", 4800, timeout=1) as ser:
    while True:
        time_now = datetime.datetime.now()
        time_str = time_now.strftime("%H:%M:%S")
        timestuff = flipdot.Text(time_str, 0, 0, flipdot.Fonts.text_16px_bold)
        hellotext = flipdot.Text("Dev me more!", 65, 0, flipdot.Fonts.text_16px_bold)
        textstuff = flipdot.Text("TAMPERE HACKLAB", 0, 25, flipdot.Fonts.text_7px_bold)
        msg = flipdot.set_texts([timestuff, hellotext, textstuff])
        ser.write(msg)
        time.sleep(1)
