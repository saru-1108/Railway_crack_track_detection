from machine import Pin, UART 
import utime 
 
buz = Pin(3, Pin.OUT) 
lm1, lm2, rm1, rm2 = Pin(10, Pin.OUT), Pin(11, Pin.OUT), Pin(12, 
Pin.OUT), Pin(13, Pin.OUT) 
ls, Rs, rf , rf1= Pin(9, Pin.IN), Pin(8, Pin.IN), Pin(26, Pin.OUT), 
Pin(27, Pin.OUT) 
wifi = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) 
 
buff = bytearray(255) 
 
TIMEOUT = False 
FIX_STATUS = False 
 
latitude = "" 
longitude = "" 
satellites = "" 
GPStime = "" 
 
def getGPS(wifi): 
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, 
GPStime 
     
17 | Page 
 
    timeout = time.time() + 8  
    while True: 
        gpsModule.readline() 
        buff = str(gpsModule.readline()) 
        parts = buff.split(',') 
     
        if (parts[0] == "b'$GPGGA" and len(parts) == 15): 
            if(parts[1] and parts[2] and parts[3] and parts[4] and 
parts[5] and parts[6] and parts[7]): 
                print(buff) 
                 
                latitude = convertToDegree(parts[2]) 
                if (parts[3] == 'S'): 
                    latitude = -latitude 
                longitude = convertToDegree(parts[4]) 
                if (parts[5] == 'W'): 
                    longitude = -longitude 
                satellites = parts[7] 
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + 
parts[1][4:6] 
                FIX_STATUS = True 
                break 
                 
        if (time.time() > timeout): 
            TIMEOUT = True 
            break 
18 | Page 
 
        utime.sleep_ms(500) 
         
def convertToDegree(RawDegrees): 
 
    RawAsFloat = float(RawDegrees) 
    firstdigits = int(RawAsFloat/100)  
    nexttwodigits = RawAsFloat - float(firstdigits*100)  
     
    Converted = float(firstdigits + nexttwodigits/60.0) 
    Converted = '{0:.6f}'.format(Converted)  
    return str(Converted) 
def setup(): 
    utime.sleep(1) 
    ls.init(Pin.IN) 
    Rs.init(Pin.IN) 
    lm1.init(Pin.OUT) 
    lm2.init(Pin.OUT) 
    rf.init(Pin.OUT) 
    rm1.init(Pin.OUT) 
    rm2.init(Pin.OUT) 
    buz.init(Pin.OUT) 
    lm1.value(0) 
    lm2.value(0) 
    rm1.value(0) 
    rm2.value(0) 
19 | Page 
 
    rf.value(1) 
    rf1.value(1) 
cnt=0 
def loop(): 
    utime.sleep(0.2) 
    global cnt 
 
    if ls.value() == 0 and Rs.value() == 0: 
        sts=0 
        lm1.value(1) 
        lm2.value(0) 
        rm1.value(1) 
        rm2.value(0) 
        rf.value(1) 
        rf1.value(0) 
 
    if ls.value() == 1 and Rs.value() == 0: 
        sts=1 
        lm1.value(0) 
        lm2.value(0) 
        rm1.value(0) 
        rm2.value(0) 
        buz.value(1) 
        rf.value(0) 
        rf1.value(1) 
20 | Page 
 
 
         
         
        utime.sleep(2) 
        buz.value(0) 
 
    if ls.value() == 0 and Rs.value() == 1: 
        sts=1 
        lm1.value(0) 
        lm2.value(0) 
        rm1.value(0) 
        rm2.value(0) 
        buz.value(1) 
        rf.value(0) 
        rf1.value(1) 
         
         
        utime.sleep(2) 
        buz.value(0) 
 
    if ls.value() == 1 and Rs.value() == 1: 
        sts=1 
        lm1.value(0) 
        lm2.value(0) 
        rm1.value(0) 
21 | Page 
 
        rm2.value(0) 
        buz.value(1) 
        rf.value(0) 
        rf1.value(1) 
        
        #print("Crack detected AT 
,https://www.google.com/maps/search/?api=1&query=" + 
str(flat) + "," + str(flon) + "^0") 
        utime.sleep(2) 
        buz.value(0) 
         
    cnt=cnt+1 
    print(cnt) 
    if(cnt>20): 
        cnt=0; 
        wifi.write("700155,408HHB11CXV5WZEE,0,0,SRC 
24G,src@internet," + str(sts)+","+ str(16.4971) + "," + str(80.4991) 
+ ",^0") 
        print("700155,408HHB11CXV5WZEE,0,0,SRC 
24G,src@internet," + str(sts)+","+ str(16.4971) + "," + str(80.4991) 
+ ",^0") 
 
setup() 
while True: 
    loop() 