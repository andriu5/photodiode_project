#!/usr/bin/python2.7
'''
Para Arduino UNO, firmware para Arduino: 

\nAuthor: Andres Alvear, Enero 2015.
'''
 
import time
import serial
import numpy as np
import math,Gnuplot, Gnuplot.funcutils, array
import fnmatch

max_valid_read = 1023
reference_voltage = 5.000
update_interval = 2e-4
rate = 5000 #samples/second


def auto_detect_serial_unix(preferred_list=['*']):
    '''try to auto-detect serial ports on win32'''
    import glob
    glist = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
    ret = []

    # try preferred ones first
    for d in glist:
        for preferred in preferred_list:
            if fnmatch.fnmatch(d, preferred):
                ret.append(d)
    if len(ret) > 0:
        return ret
    # now the rest
    for d in glist:
        ret.append(d)
    return ret

def port():
    available_ports = auto_detect_serial_unix()
    ser = serial.Serial(available_ports[0], 115200)
    port = available_ports[0]
    print "port = " +str(port)+ " (1)"
    time.sleep(0.1)
    print "port = "+ str(ser) + "!!!"
    return port

port = port()
ser = serial.Serial(port,baudrate = 115200)

def get_data(ser):
    
    #ser = serial.Serial(port,baudrate = 115200)
    #ser.write('2')
    
    r = 0
    r_time = 0
    i = 0
    analog_reads = 0.000
    analog_buffer_data = [] # 0 .. n-1  (!)
    #analog_buffer_time = np.linspace(0, update_interval, rate*update_interval)  #start, end, num-points FIX!!
    
  
    for i in range(1024):

        b1 = ord(ser.read())
        #print ser.read()
        b2 = ord(ser.read())
        #print ser.read()
        #r = b1 + b2*256
        r = np.float16(b1)+np.float16(b2)*256.000
        
        analog_reads = (r*reference_voltage)/(max_valid_read)
        print "dato = " +str(analog_reads)+ " volts"

        analog_buffer_data.append(analog_reads) #STATIC LIST!!!

    return analog_buffer_data#, analog_buffer_time

def continuous_plot(ser):
    #ser = serial.Serial(port,baudrate = 115200)
    #ser.write('2')
    ok=1
    bw = rate/2

    g0.clear()    
    g0.title('ADC A0 Max frequency = ' +str(bw)+'Hz')
    g0.xlabel('2e-4*[time unit]  ')
    g0.ylabel('Samples in Volts [v]')
    g0('set style data linespoints')
    g0('set yrange [*:*]')
    g0('set xrange [-5:1024]')
    g0('set ytics 0.01')# * invalid! 
    #g0('set xtics *')# * invalid!
    g0('set grid y')
    g0('set grid x')

    #ser = serial.Serial(port,baudrate = 115200)
    #time.sleep(0.1)
    print 'ok'

    while ok==1: #r <= max_valid_read

    	#get the data...
        ser.write('2')
        time.sleep(0.1)  
        #analog_buffer_data, analog_buffer_time = get_data()
        
        analog_buffer_data = get_data(ser)
        
        g0.title('ADC A0 Max frequency = ' +str(bw)+'Hz')
        #g0.plot(analog_buffer_data, analog_buffer_time)
        g0.plot(analog_buffer_data)


if __name__=='__main__':

    print "\n\n"     
    print "        .--. "
    print "       |o_o | "
    print "       |:_/ | "
    print "      //   \ \ "
    print "     (|     | ) "
    print "    /`\_   _/'\ "
    print "    \___)=(___/ "
    print "                 by aalvear@das.uchile.cl"
    print "\n\n"

    time.sleep(0.25) 

    #port=port()
    #print "port = " +str(port)+ " (2)"
    #ser = serial.Serial(port,baudrate = 115200)
    #ser = serial.Serial(port = '/dev/ttyACM0',baudrate = 115200)
    
    time.sleep(1.5)
    ser.flush()

    #set up the figure with a subplot to be plotted
    g0 = Gnuplot.Gnuplot(debug=1)    

    continuous_plot(ser)
    print 'Plot started.'


    try:
        user_input = input()
        sys.exit(0)
    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(0)


    #try:
    #    sys.exit(0)
    #except KeyboardInterrupt:
    #    print 'Interrupted'
    #    sys.exit(0)
    #try:
    #    sys.exit(0)
    #except SystemExit:
    #    os._exit(0)
