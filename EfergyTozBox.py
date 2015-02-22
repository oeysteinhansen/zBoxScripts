#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib2
import cookielib
import time
import json



def grab_data_with_cookie(cookie_jar, url):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
        data = opener.open(url)
        return data

def grab_data_from_efergy():
        #Efergy Urls
        url = "https://engage.efergy.com/user/login?username=yourusername&password=yourpassword";
        url2 = 'https://engage.efergy.com/proxy/getCurrentValuesSummary'

        cj = cookielib.CookieJar()

        #grab the data
        data1 = grab_data_with_cookie(cj, url)

        #the second time we do this, we get back the excel sheet.
        data2 = grab_data_with_cookie(cj, url2)

        KWH = data2.read()
        KWH = json.loads(KWH)

        # Change the incomming data to be more Python friendly.
        for rec in KWH:
                for d in rec["data"]:
                        keylist = d.keys()
                        d["timestamp"]=int(keylist[0])
                        d["value"]=d[keylist[0]]
                        d.pop(keylist[0])

        #print KWH
        return KWH



def zipatoWeb_Efergy_SetValue(value, index=1):
        # Send to Zipabox
        urlprefix =  "Paste your long Http address you copyed from Efergymeter in here, remove the &value1= it is added on the next line."
        urlpostfix = "&value%d=%f" % (index,value) 
        #print "Read Url: " + urlprefix + urlpostfix
        urllib2.urlopen(urlprefix + urlpostfix).read()

def workerLoop():
        while 1:
                kwh = grab_data_from_efergy()
                print("####")
                print("  Age: ", kwh[0]["age"])
                print("  Tim: ", kwh[0]["data"][0]["timestamp"])
                print("  kWm: ", kwh[0]["data"][0]["value"])
                zipatoWeb_Efergy_SetValue(kwh[0]["data"][0]["value"])
                time.sleep(30.0)



if __name__ == "__main__":
        workerLoop()
