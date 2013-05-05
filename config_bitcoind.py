import urllib2, urllib
import requests
import sys

racks_begin = int(sys.argv[1])
racks_end = int(sys.argv[2])+1
port = int(sys.argv[3])
racks = range(racks_begin,racks_end)

# def make_two_digit (num):
#     if num >=0 and num < 10:
#         return '0' + str(num)
#     else:
#        return str(num)

for rack in racks:
    for board in range(1,13):
        data = {
            'JMIP' : '192.168.' + str(rack) + '.' + str(board),
            'JMSK' : '255.255.0.0',
            'JGTW' : '192.168.1.1',
            'PDNS' : '8.8.8.8',
            'MURL' : '192.168.0.10,192.168.0.10',
            'MPRT' : str(port)+','+str(port),
            'USPA' : 'asicminer_' + str(rack) + ':wasabi,asicminer_' +  str(rack) + ':wasabi',
            'JGTV' : '0',
            }
        print data
        url     = 'http://192.168.'+str(rack)+'.'+str(board)+':8000/Upload_Data'
        try:
            r = requests.post(url, data)
            print r.content
        except:
            print "Cannot connect to rack " + str(rack) + ", board " + str(board)

    
