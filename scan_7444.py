from urllib2 import urlopen
import re


def make_ip(a,b):
    return 'http://192.168.'+str(a)+'.'+str(b)+':8000'

fuck = []

for a in range(100,145):
    print a
    for b in range(1,13):
        try:
            ip=make_ip(a,b)
            page = urlopen(ip,timeout=2).read()
            if(re.search("(7444)",page)==None):
                continue
            else:
                fuck.append(ip)
                print ip
        except:
            continue

print fuck

