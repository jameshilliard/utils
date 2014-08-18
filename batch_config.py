import requests
import sys
import csv

argc = len(sys.argv)

csvfile = sys.argv[1] if argc>1 else "config.csv"

data = {
    # IP
    'JMIP' : '192.168.0.100',
    # MASK
    'JMSK' : '255.255.0.0',
    # Gateway
    'JGTW' : '192.168.0.1',
    # Primary DNS
    'PDNS' : '192.168.0.1',
    # Secondary DNS
    'SDNS' : '114.114.114.114',
    # Pool
    'MURL' : 'us1.ghash.io',
    # Port from pool
    'MPRT' : '3333',
    # Worker
    'USEF' : 'bitquan.1',
    # Worker Password
    'PASO' : '123',
    # Default Clock
    'GCLK' : '270'
}

print "Loading CSV File %s ..." % csvfile

failed = []

try:
    with open(csvfile) as configs:
        reader = csv.DictReader(configs, delimiter=',')
        for config in reader:
            ip = config["IP"]
            pool = config["POOL"]
            worker = config["WORKER"]
            url = "http://%s:8000/Settings/Upload_Data" % ip
            print url
            data["JMIP"] = ip
            data["MURL"] = pool
            data["USEF"] = worker
            print data
            try:
                req = requests.post(url,data,timeout=3)
                print req.content
            except:
                print "Cannot connect to %s" % ip
                failed.append(ip)
except:
    print "Cannot open \"%s\"" % csvfile

if(len(failed)>0):
    print "Failed to connect:"
    print failed
    
