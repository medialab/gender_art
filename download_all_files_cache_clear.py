# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 12:07:38 2018

@author: ruta binkyte, Paul Girard
"""


import json
from requests.adapters import HTTPAdapter
import requests_cache
import config
import datetime 
import os

# a function to calculate time remaining to download
def remaining_time(total, start_time, now, doc_num) :  
    duration = now-start_time
    duration_in_s = duration.total_seconds()
    doc_left = total - doc_num
    # time in seconds to download one document
    speed = duration_in_s/doc_num
    time_left = doc_left*speed
    
    	# convert to hours
    if time_left >= 3600:
    	time_left = divmod(time_left, 3600)[0]
    	time_left = str(time_left) + ' hours' + '\n'
    	# convert to days
    elif time_left >= 86400:
    	time_left = divmod(time_left, 86400)[0]
    	time_left = str(time_left) + ' days' + '\n'
    else:
        time_left = str(time_left) + ' seconds' + '\n'
        
    return time_left


clear = False

if clear == True:
    os.remove("cache.sqlite")
    print('Cache is cleared')

with  requests_cache.CachedSession() as s:

    
    # logins from config file 
    SERVERROOT= config.SERVERROOT
    VAULT = config.VAULT
  
    
    if SERVERROOT == None or VAULT == None:
        print('Use config.py file for obtaining login data')
    
    url = '%s/%s/login' % (SERVERROOT, VAULT)
    
    s.mount(url, HTTPAdapter(max_retries=5))

    # login data from config file 
    login_data = {
        "email": config.USERNAME,
        "password": config.PASSWORD
    }
    
  
    if login_data['email'] == None or login_data['password'] == None:
        print('Use config.py file for obtaining login data')
    
    headers = {
    'Content-Type': 'application/json',
    }
    
    
    try:
        response = s.post(url, headers = headers, json = login_data).json()
        
    except Exception as e:
        print(e.message)
        
        
    
    token = response['token']
    
    headers = {
        'X-Token': token,
    }
    

    # go to the firs page
    url = '%s/%s/artworks?size=0' % (SERVERROOT, VAULT) 
    s.mount(url, HTTPAdapter(max_retries=5))
    
    try:
        response = s.get(url, headers = headers, json = login_data).json()
        
    except Exception as e:
        print(e.message)
    
    
    # number of documents to download
    #total = response['totalCount']
    total = 11000
    
    
    if type(total) is not int:
        raise ValueError("Invalid number of documents")
    else:
        print('Total number of documents: ' + str(total) + '\n')
    
    # number of results per page
    size = 1000
    print('Number of documents per page: ' + str(size) + '\n')
    
    # downloading start time
    start_time = datetime.datetime.now()
    # a number of pages to pass for calculating downloading time
    page = 10
    
    
    for i in range(int(total/size)): 
        
        print(i)
        print(page)
        
        if i == page:
            
            doc_num = page*size - 1
            
            page += 10
                        
            now = datetime.datetime.now()
            # calculating time remaining to download all the documents        
            time_left = remaining_time(total, start_time, now, doc_num)
                    
            print(str(now) + '  Documents downloaded: ' + str(doc_num) + '\n')
            print('Downloading time left: ' + time_left + '\n')
                    
        # name for the document indicating number of files it contains   
        start = i*size
        end = start+size-1
        name = os.path.join('data',str(start) + '-' + str(end) + '.json')
        

        url = "%s/%s/artworks?size=%s&from=%s&sort=source.artwork.order_default.keyword:asc" % (SERVERROOT, VAULT, size, start)
        s.mount(url, HTTPAdapter(max_retries=5))
        
        print('The URL is: ' + url + '\n')

        #Check if connection is ok
        response = s.get(url, headers = headers, json = login_data)
        if not response.from_cache:
            try:
                response.raise_for_status()    
                response = response.json()
                
                
                with open(name, 'w') as outfile: 
                    
                    json.dump(response, outfile, ensure_ascii = False, indent = 2)
            except Exception as e :
                print(e)
        else :
            print('Retrieved from cache')    

        
        
    
    
    
    