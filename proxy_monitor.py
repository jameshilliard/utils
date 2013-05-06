import time
import subprocess
import os
import string
import psutil


def cur_time():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

# TODO: more accurate criteria 
def is_stuck(proc):
    usage = proc.get_cpu_percent(interval=1)
    print usage
    return (
        usage>98 
        # or usage<2
        )

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

def collect_info(procs):
    info = {}
    for proc in procs:
        server = proc.cmdline[3]
        port = proc.cmdline[-1]
        info[port]=server
    return info



procs = map(psutil.Process,get_proxy_pids())
print "Start watching ports:"
info = collect_info(procs)
print info

count = 0

while(True):
    count = count + 1
    
    print '=================' + cur_time() + '=================='

    # check low and high cpu usage
    procs = map(psutil.Process,get_proxy_pids())

    for proc in procs:
        print "Checking PID:"+str(proc.pid)
        if is_stuck(proc):
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

    # time.sleep(30)

    # # check if port exists
    # procs = map(psutil.Process,get_proxy_pids())

    # print "Check Ports:"+str(info)
    # cur_ports = collect_info(procs).keys()
    # flag = True
    # for port in info.keys():
    #     if(not port in cur_ports):
    #         respawn = build_cmd(info[port],port)
    #         print respawn
    #         subprocess.Popen(respawn,shell=True)
    #         print 'restart port '+port
    #         flag = False
    # if(flag):
    #     print "All ports alive"

        
    # restart all every 100 round
    if(count>120):
        print "restart all"
        count = 0
        procs = map(psutil.Process,get_proxy_pids())
        for proc in procs:
            print 'killed process '+ str(proc.pid)
            os.kill(proc.pid,9)
        time.sleep(10)
        for port in info.keys():
            respawn = build_cmd(info[port],port)
            print respawn
            subprocess.Popen(respawn,shell=True)
            print 'restart port '+port

    time.sleep(30)

   




