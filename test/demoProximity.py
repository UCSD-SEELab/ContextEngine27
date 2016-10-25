import subprocess
import MySQLdb
import threading
import time
import multiprocessing
import requests
import datetime
import time


status_dgp = 0
status_ivan = 0

def test(plugip1,plugip2,status):
    #print "Hi"
    if status == "off":
        data=subprocess.check_output(["bash","hs100.sh",plugip1,"9999","off"])
        data=subprocess.check_output(["bash","hs100.sh",plugip2,"9999","off"])
    else:
        cd = MySQLdb.Connect(host="localhost", port=3306, user="beaconuser", passwd="seelab", db="BeaconDatabase")
        cur = cd.cursor()
        sql = 'SELECT STATUS FROM ProximityData WHERE UID = 1234 ORDER BY TIME DESC LIMIT 1'
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                status_dgp = int(row[0])
                #print (row)
            cd.commit()
        except:
            cd.rollback()
        sql = 'SELECT STATUS FROM ProximityData WHERE UID = 5555 ORDER BY TIME DESC LIMIT 1'
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                status_ivan = int(row[0])
                #print (row)
            cd.commit()
        except:
            cd.rollback()
        cd.close()
        
        if(status_dgp==1 and status_ivan == 0):
            print "Hello Dhanesh"
            data=subprocess.check_output(["bash","hs100.sh",plugip1,"9999","on"])
            data=subprocess.check_output(["bash","hs100.sh",plugip2,"9999","off"])
        elif(status_ivan==1 and status_dgp == 0):
            print "Hello Ivan"
            data=subprocess.check_output(["bash","hs100.sh",plugip1,"9999","off"])
            data=subprocess.check_output(["bash","hs100.sh",plugip2,"9999","on"])
        elif(status_dgp==1 and status_ivan==1):
            print "Hello Dhanesh and Ivan "
            data=subprocess.check_output(["bash","hs100.sh",plugip1,"9999","on"])
            data=subprocess.check_output(["bash","hs100.sh",plugip2,"9999","on"])
        else:
            print " No one present near plug load"
    #        print "Off","   ",status_dgp,"   ",status_ivan
            data=subprocess.check_output(["bash","hs100.sh",plugip1,"9999","off"])
            data=subprocess.check_output(["bash","hs100.sh",plugip2,"9999","off"])


    
