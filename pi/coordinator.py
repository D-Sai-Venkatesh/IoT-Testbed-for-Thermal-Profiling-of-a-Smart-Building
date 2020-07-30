#!/usr/bin/env python
import time
import serial
from serial import Serial
import elk_post
ser = Serial(
    port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1             
 )



# server id
r_id = "03"


# separates the string wrt spaces
# "sai venkatesh" => ["sai","venkatesh"]
def extract_string(temp):
    i=0
    temp1=[]
    while(i<len(temp)):
        temp2=""
        while(i<len(temp) and chr(temp[i])!=' '):
            temp2=temp2+chr(temp[i])
            i=i+1
        temp1.append(temp2)
        i=i+1
    return temp1
# it will try to connect with the arduinos which are not communicating
def adapt_arduino():
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    start = time.time()
    wait = 10
    end = start + wait
    adapted = []
    prev = start
    ser.write(str.encode("hi    "+r_id))
    while(1):
        #print("----------")
        if(time.time()>end):
            break
        if(time.time()-prev>=3):
            ser.write(str.encode("hi    "+r_id))
        x=ser.readline().strip()
        if(x != b''):
            temp=extract_string(x)
            if(len(temp)>=3 and temp[0] == "hello" and temp[2]=="r"+r_id):
                ser.write(str.encode("h "+temp[1]+" "+r_id))
                if(temp[1] not in adapted):
                    print(temp)
                    adapted.append(temp[1])
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    return adapted
# this verifies the connection of adapted arduinos 
# checks if connection is correct or not
def check_connection(adapted):
    print("+++++++++++++++++++++++++++++++++++")
    working=[]
    for a_id in adapted:
        start = time.time()
        end = start + 5
        ser.write(str.encode("s "+a_id+" "+r_id))
        prev = start
        while(1):
            if(time.time()-prev>=2):
                ser.write(str.encode("s "+a_id+" "+r_id))
                prev= time.time()
            x=ser.readline().strip()
            if(x!=b''):
                temp=extract_string(x)
                if(temp[0]=="data" and temp[1]==a_id and temp[2]=="r"+r_id):
                    ser.write(str.encode("a "+a_id+" "+r_id))
                    print("connected with "+temp[1])
                    if(temp[1] not in working):
                        working.append(temp[1])
                    break
            if(time.time()>end):
                ser.write(str.encode("f "+a_id+" "+r_id))
                time.sleep(0.1)
                ser.write(str.encode("f "+a_id+" "+r_id))
                time.sleep(0.1)
                ser.write(str.encode("f "+a_id+" "+r_id))
                time.sleep(0.1)
                print("connction failed with "+a_id)
                break
    print("+++++++++++++++++++++++++++++++++++")
    return working
#it merges 2 stings without repeating
def string_add(str1,str2):
    for x in str2:
        if (x not in str1):
            str1.append(x)
    return str1            
#it collects data from the connected arduinos in roung robin faction
def post_data(arduino_list1,num_trys):   
    for a_id in arduino_list1:
        print("#####################")
        start = time.time()
        wait = 5
        end =start + wait
        ser.write(str.encode("s "+a_id+" "+r_id))
        prev = start
        while(1):
            if(time.time()-prev>=1):
                ser.write(str.encode("s "+a_id+" "+r_id))
            x=ser.readline().strip()
            if(x != b''):
                temp=extract_string(x)
                if(temp[0]=="data" and temp[1] in arduino_list1 and temp[2]=="r"+r_id):
                    #print(temp)
                    ser.write(str.encode("a "+temp[1]+" "+r_id))
                    num_trys[temp[1]]=0
                    elk_post.send_data('1'+temp[3],float(temp[4]))
                    if temp[1] == a_id:
                        print(temp)
                        break
                if(temp[0]=="data" and temp[2]!="r"+r_id):
                    if(temp[1] in arduino_list1):
                        print("deleting "+temp[1])
                        arduino_list1.remove(temp[1])
                    if(temp[1] in num_trys):
                        num_trys.pop(temp[1])
            if(time.time()>end):
                if (a_id not in num_trys):
                    num_trys[a_id] = 1
                else:
                    num_trys[a_id]+=1
                break
        if(a_id in num_trys and num_trys[a_id]>=4):
            print("removing "+a_id)
            arduino_list1.remove(a_id)
            num_trys.pop(a_id)
            ser.write(str.encode("f "+a_id+" "+r_id))
            time.sleep(0.1)
            ser.write(str.encode("f "+a_id+" "+r_id))
            time.sleep(0.1)
            ser.write(str.encode("f "+a_id+" "+r_id))
            time.sleep(0.1)
def run():
    arduino_list = []
    num_trys = {}
    num_loops=0
    while(1):
        print("=====================================================")
        #after every 3 loops it checks for free arduino
        if(num_loops%3 == 0):
            x=adapt_arduino()
            print(x)
            x=check_connection(x)
            arduino_list=string_add(arduino_list,x)
        print("arduino_list "+str(arduino_list))
        print("dictionary " + str(num_trys))
        post_data(arduino_list,num_trys)
        num_loops+=1

run()
