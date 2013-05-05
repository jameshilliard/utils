import urllib2, urllib
import requests
import sys

rack = int(sys.argv[1])
board_begin = int(sys.argv[2])
board_end = int(sys.argv[3])
port = int(sys.argv[4])
worker = sys.argv[5]

boards=range(board_begin,board_end+1)

# def make_two_digit (num):
#     if num >=0 and num < 10:
#         return '0' + str(num)
#     else:
#        return str(num)

for board in boards:
    data = {
        'JMIP' : '192.168.' + str(rack) + '.' + str(board),
        'JMSK' : '255.255.0.0',
        'JGTW' : '192.168.1.1',
        'PDNS' : '8.8.8.8',
        'MURL' : '192.168.0.12,192.168.0.12',
        'MPRT' : str(port)+','+str(port),
        'USPA' : 'realasicminer_' + worker + ':wasabi,realasicminer_' +  worker + ':wasabi',
        'JGTV' : '0',
        }
    print data
    url     = 'http://192.168.'+str(rack)+'.'+str(board)+':8000/Upload_Data'
    try:
        r = requests.post(url, data)
        print r.content
    except:
        print "Cannot connect to rack " + str(rack) + ", board " + str(board)

    
