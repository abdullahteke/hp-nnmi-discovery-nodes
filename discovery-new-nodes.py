#!/usr/bin/python
 
import netsnmp
import Queue
import threading
import subprocess
 
def checkSysName(ip):
    res = netsnmp.snmpget(sysName,
                                      Version= 2,
                                      DestHost=ip,
                                      Community='snmpcommunity',
                                      Timeout=1000000,
                                      Retries=0)
    name= str(res[0])
    #print name
    if name != "None":
        resultFile.write(str(ip)+"\n")
 
 
def getSysName():
    while True:
        ip=q.get()
        if ip is None:
            break
        checkSysName(ip)
        q.task_done()
 
resultFile = open('resultFile.txt', 'w')
q = Queue.Queue(maxsize=0)
num_threads=512
sysName= netsnmp.Varbind('sysName.0')
threads=[]
 
for i in range(num_threads):
    t = threading.Thread(target=getSysName )
    t.start()
    threads.append(t)
 
 
 
for i in range (0,256):
    for j in range (0,256):
        ip="172.22."+str(i)+"."+str(j)
        q.put(ip)        
 
q.join()
 
for i in range(num_threads):
    q.put(None)
 
for t in threads:
    t.join()
 
resultFile.close()
subprocess.call('/opt/OV/bin/nnmloadseeds.ovpl -f resultFile.txt', shell=True)