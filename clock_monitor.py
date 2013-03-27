import yaml
from urllib2 import urlopen

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
    return '192.168.'+str(a)+'.'+str(b)

def get_clock(ip):
    # page = urlopen(ip).read()
    return 1


def toggle_clock(ip):
    urlopen(ip+'/Sw_Clock')


for k in config.keys():
    res=map(parse,config[k])
    domain = [item for sublist in res for item in sublist]
    ips = map(lambda x:make_ip(k,x),domain)
    for ip in ips:
        if(get_clock(ip) = 0):
            toggle_clock(ip)
        else:
            continue






