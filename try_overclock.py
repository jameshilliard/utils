import yaml
from urllib2 import urlopen
import re
from time import sleep
import request

 
f=open('config.yaml')
config=yaml.safe_load(f)
f.close()

def make_range(s):
    r = eval('range'+s)
    r.append(r[-1]+1)
    return r

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

def count_X(ip):
    try:
        page = urlopen(ip).read()
        find_status=re.search("([OX]+)",page)
        status=find_clock.group()
        return status.count("X")
    except:
        return 'fail to connect '+ip
    
def toggle_clock(ip):
    urlopen(ip+'/Sw_Clock')

def reset_board(ip):
    requests.post(ip,{})

def overclock():
    for k in config.keys():
        res=map(parse,config[k])
        domain = [item for sublist in res for item in sublist]
        ips = map(lambda x:make_ip(k,x),domain)
        for ip in ips:
            print ('overclocking node '+ip)
            status = get_clock(ip)
            if( status == 'Low'):
                print 'toggle '+ip+' to High'
                toggle_clock(ip)
                reset_board(ip)
            else:
                if(status == 'High'):
                    high+=1
                else:
                    print status

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
                print('downclock '+ip)
                toggle_clock(ip)
                

overclock()
print "Low:"+str(low)
print "High:"+str(high)
sleep(60)
downclock()


