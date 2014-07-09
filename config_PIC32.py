import urllib2, urllib
import requests
import sys

rack = int(sys.argv[1])
board_begin = int(sys.argv[2])
board_end = int(sys.argv[3])

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
        'JGTW' : '192.168.0.1',
        'PDNS' : '192.168.0.1',
        'SDNS' : '114.114.114.114',
        'MURL' : 'us1.ghash.io',
        'MPRT' : '3333',
        'USEF' : 'naituida.' + str(rack) + str(board),
        'PASO' : '123',
        'GCLK' : '270'
        }
    print data
    url     = 'http://192.168.'+str(rack)+'.'+str(board)+':8000/Settings/Upload_Data'
    try:
        r = requests.post(url, data)
        print r.content
    except:
        print "Cannot connect to rack " + str(rack) + ", board " + str(board)

    
