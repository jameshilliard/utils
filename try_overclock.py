import yaml
from urllib2 import urlopen
import re
from time import sleep
import requests
 
f=open('config.yaml')
config=yaml.safe_load(f)
f.close()

def make_range(s):
    return eval('range'+s)

def parse(obj):
    if isinstance(obj,str):
        return make_range(obj)
    else:
        return [obj]

def make_ip(a,b):
    return 'http://192.168.'+str(a)+'.'+str(b)+':8000'

def get_clock(ip):
    try:
        page = urlopen(ip,timeout=2).read()
        find_clock=re.search("Clock selected: ([a-zA-Z]+)",page)
        (status,)=find_clock.groups()
        return status
    except:
        return 'fail to connect '+ip

discon = []
def count_X(ip):
    try:
        page = urlopen(ip,timeout=2).read()
        find_status=re.search("Chip: ([Ox]+)",page)
        (status,)=find_status.groups()
        return status.count("x")
    except:
        print 'fail to connect '+ip
        discon.append(ip)
        return -1
    
def toggle_clock(ip):
    urlopen(ip+'/Sw_Clock')

def reset_board(ip):
    requests.post(ip,{})


def overclock():
    low = 0
    high = 0
    for k in config.keys():
        res=map(parse,config[k])
        domain = [item for sublist in res for item in sublist]
        ips = map(lambda x:make_ip(k,x),domain)
        for ip in ips:
            print ('overclocking node '+ip)
            status = get_clock(ip)
            if( status == 'Low'):
                low+=1
                print 'toggle '+ip+' to High'
                toggle_clock(ip)
                reset_board(ip)
            else:
                if(status == 'High'):
                    high+=1
                else:
                    print status
    print "High:"+str(high)
    print " Low:"+str(low);


failed = []
discon = []

def downclock():
    for k in config.keys():
        res=map(parse,config[k])
        domain = [item for sublist in res for item in sublist]
        ips = map(lambda x:make_ip(k,x),domain)
        for ip in ips:
            print ('checking node '+ip)
            count = count_X(ip)
            status = get_clock(ip)
            if( status == 'High' and count>=4):
                print(str(count)+" ASIC down on "+ip)
                print('downclock '+ip)
                toggle_clock(ip)
                reset_board(ip)
                failed.append(ip)
    print "Failed"
    print failed
    print "Disconnected"
    print discon
                

# print("overclock")
# overclock()
# print("overclock finished")
# sleep(30)
# print("downclock")
# downclock()


