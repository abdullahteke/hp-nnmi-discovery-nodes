'''
Created on 24 Mar 2022

@author: ateke
'''
#!/usr/bin/python

import psycopg2
import psycopg2.extras

HOST='localhost'
DBNAME='nnm'
DBUSER='postgres'
DBPASSWD='1qaz2wsx'

def getIdForIP(ip,note):
    try:
        cur.execute("""SELECT id from nms_node where long_name='"""+ip+"""' """)    
    except:
        print "I can't SELECT from bar"    
    rows=cur.fetchall()
    if len(rows)>0:
        nodeid=rows[0][0]
        setNoteForNode(nodeid,note)

def setNoteForNode(id,note):
    #updateStr="UPDATE nms_node_journal SET notes='"+note+"' WHERE id="+str(id)

    try:
        cur.execute("UPDATE nms_node_journal SET notes=(%s) WHERE id=(%s)",(note,str(id)))
        #cur.execute(updateStr)
        print cur.statusmessage
        conn.commit()
        except:
                print "I can't UPDATE notes"

try:
    conn=psycopg2.connect("host="+HOST+" dbname="+DBNAME+" user="+DBUSER+" password="+DBPASSWD)
    cur=conn.cursor()
except:
    print "I am unable to connect to the database."


with open('yeniListe.txt') as fp:
    for line in fp:
        txt=line.split()
        ip= txt[2]
        binaNo= txt[1]
        tesisNo= txt[0]
        note="BINA_NO: "+binaNo+" -|- "+"TESIS_NO: "+tesisNo
        getIdForIP(ip,note)
cur.close()
conn.close()



