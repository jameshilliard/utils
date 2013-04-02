import time
import subprocess
import os
import string

def cur_time():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

# TODO: more accurate criteria 
def is_stuck(proc):
    return proc['cpu'] > '98'

proxy_stub = 'python ~/stratum-mining-proxy/mining_proxy.py -o 192.95.29.175 -gp '


while(True):
    procs = []
    cmd = 'shelltop -n1 -c -b | grep proxy | grep -v grep | awk \'{print $1,$9,$NF}\''
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True)
    while True:
        line = p.stdout.readline()
        if line != '':
            p_info = line.split()
            proc = {'pid':p_info[0],'cpu':p_info[1],'port':p_info[2]}
            procs.append(proc)
        else:
            break    

    p.wait()
       
    for proc in procs:
        if is_stuck(proc):
            # restart process
            print 'port ' + proc['port'] + ' is stuck!'
            os.kill(string.atoi(proc['pid']),9)
            print 'killed process '+proc['pid']
            respawn = proxy_stub + proc['port'] + ' > /dev/null 2> /dev/null &'
            print respawn
            subprocess.Popen(respawn,shell=True)
            print 'restart port '+proc['port']
        else:
            continue
            
    print '=================' + cur_time() + '=================='
    time.sleep(5)
   
