#!/usr/bin/python

import psycopg2
import psycopg2.extras
import os
import subprocess

# --------------------------------------- ADD CUSTOM ATTRIBUTE --------------------------------------------

HOST='localhost'
DBNAME='nnm'
DBUSER='postgres'
DBPASSWD='1qaz2wsx'


# --------------------------------------- GET NEW DEVICES ------------------------------------------------- 

def getNodeCreatedForLast15Minutes():
    try:
        #query="select id,long_name,reg_created from nms_node where reg_created >= now()-interval '15 minute'"
        #query="select id,long_name,reg_created from nms_node"
        query="select n.id,n.long_name from nms_node as n, nms_node_journal as j where j.id=n.id and j.notes is null"
        cur.execute(query)
    except:
        print "test"
            #print "I can't SELECT from bar"
    rows=cur.fetchall()

    if len(rows)>0:
        for node in rows:
            nodeID=node[0]
            nodeIP=node[1]
            note=createNoteForNode(nodeID,nodeIP)
            if note!="bos":
                setNoteForNode(nodeID,note)


# --------------------------------------- CREATE NOTE FOR NODE --------------------------------------------

def createNoteForNode(nodeID,nodeIP):
    note="bos"

    with open('allDevice.txt') as fp:
            for line in fp:
                       txt=line.split("\t")
                       tesisNo= txt[0]
            bolge=txt[1]
            sehir=txt[2]
            binaNo=txt[3]
            ipAdr=txt[4]

            if ipAdr.split("\n")[0]==nodeIP:
                f.write(nodeIP+",BOLGE,"+bolge+"\n")
                f.write(nodeIP+",SEHIR,"+sehir+"\n")
                f.write(nodeIP+",ENTEGRATOR,INNOVA\n")
                f.write(nodeIP+",MUSTERI\n")
                f.write(nodeIP+",TESIS_NO,"+tesisNo+"\n")
                f.write(nodeIP+",TEMOS_NO,"+binaNo+"\n")
                f.write(nodeIP+",VPN_ID,65138\n")

                           note="TEMOS_NO: "+binaNo+" -|- "+"TESIS_NO: "+tesisNo
                print note
                break
    return note

# -------------------------------------------- ADD NOTE METHOD --------------------------------------------

def setNoteForNode(id,note):

    try:
        cur.execute("UPDATE nms_node_journal SET notes=(%s) WHERE id=(%s)",(note,str(id)))
        conn.commit()
        except:
                print "I can't UPDATE notes"


# -------------------------------------------- MAIN METHOD -----------------------------------------------

os.chdir("/root/scripts/")


try:
    conn=psycopg2.connect("host="+HOST+" dbname="+DBNAME+" user="+DBUSER+" password="+DBPASSWD)
    cur=conn.cursor()
except:
    print "I am unable to connect to the database."

f= open("customAtributes.csv","w")
getNodeCreatedForLast15Minutes()
f.close()

return_code = subprocess.call("/opt/OV/bin/nnmloadattributes.ovpl -r true -t node -f customAtributes.csv", shell=True)  

print "ReturnCode"+str(return_code)


cur.close()
conn.close()



