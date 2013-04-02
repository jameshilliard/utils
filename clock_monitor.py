import sys
import yaml
from urllib2 import urlopen
import re
import time


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
        page = urlopen(ip).read()
        find_clock=re.search("Clock selected: ([a-zA-Z]+)",page)
        (status,)=find_clock.groups()
        return status
    except:
        return 'fail to connect '+ip


def toggle_clock(ip):
    urlopen(ip+'/Sw_Clock')


while(True):
    high = 0
    low = 0
    
    for k in config.keys():
        res=map(parse,config[k])
        domain = [item for sublist in res for item in sublist]
        ips = map(lambda x:make_ip(k,x),domain)
        for ip in ips:
            print('checking node '+ip)
            status = get_clock(ip)
            if( status == 'Low'):
                print 'toggle '+ip+' to High'
                toggle_clock(ip)
                low+=1
            else:
                if(status == 'High'):
                    high+=1
                else:
                    print status

    print "Low:"+str(low)
    print "High:"+str(high)
    time.sleep(3600)



