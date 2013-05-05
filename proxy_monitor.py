import time
import subprocess
import os
import string
import psutil


def cur_time():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

# TODO: more accurate criteria 
def is_stuck(proc):
    return proc.get_cpu_percent(interval=1)>98

def is_low(proc):
    return proc.get_cpu_percent(interval=1)<2


# 54.235.91.242  btcguild
# mint.bitminter.com bitminter
# us.ozco.in     ozcoin
def build_cmd(server,port):
    return 'python ~/stratum-mining-proxy/mining_proxy.py -o '+ server + ' -gp ' + port + ' >/dev/null 2>/dev/null &'

def get_proxy_pids():
    pids = []
    for p in psutil.process_iter():
        if p.status == psutil.STATUS_RUNNING and "-gp" in p.cmdline:
            pids.append(p.pid)
    return pids


while(True):
    procs = map(psutil.Process,get_proxy_pids())
    for proc in procs:
        if (is_stuck(proc) or is_low(proc)):
            port = proc.cmdline[-1]
            server = proc.cmdline[3]
            # restart process
            print 'port ' + port + ' is stuck!'
            os.kill(proc.pid,9)
            print 'killed process '+ str(proc.pid)
            respawn = build_cmd(server,port)
            print respawn
            subprocess.Popen(respawn,shell=True)
            print 'restart port '+port
        else:
            continue
        
print '=================' + cur_time() + '=================='
time.sleep(30)
   




