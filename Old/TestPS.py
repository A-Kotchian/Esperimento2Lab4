#!python

import pyvisa
import time
rm = pyvisa.ResourceManager()
inst=rm.open_resource('GPIB0::18::INSTR')

inst.write(':SENS:FUNC "CURR"')
inst.write(":OUTP:STAT 1")

for i in range(10):
    inst.write(("SOUR:VOLT %d" % (10+5*i)))
    data=inst.query(':READ? "defbuffer1", DATE, SOUR, READ')
    print(data)
    time.sleep(2)

inst.write("SOUR:VOLT 0")
inst.write(":OUTP:STAT 0")
