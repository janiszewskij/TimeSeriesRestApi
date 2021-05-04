# -*- coding: utf-8 -*-
"""
Created on Sun May  2 08:12:17 2021

@author: DomJJ
"""
import os
import json
import pyodbc

import pandas as pd

import rpy2
from rpy2.robjects.packages import importr

#import R objects into python
import rpy2.robjects.packages as rpackages
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri

#Main VAriables
os.environ['R_HOME']=r'C:\Users\DomJJ\Anaconda3\pkgs\r-base-3.6.1-hf18239d_1\lib\R\bin\x64'


class API():
    def __init__(self):
        
        print("API Instance created")
        
    def insert_JSON_db(self,JSON_list):
        
        conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-GOBO5ON\SQLEXPRESS;'
                      'Database=SampleDb;'
                      'Trusted_Connection=yes;')
        
        cursor = conn.cursor()
        for item in JSON_list:
            #str_item = "'" + str(item) + "'"

            sql = "insert into SampleValues Values('%s', '%i', '%f')" % \
                (item["name"], item["t"] , item["v"])
            excute = cursor.execute(sql)
            conn.commit()
            
        conn.close()
        
        return(200)
        
    def get_db_records(self,start_timestamp,end_timestamp):
        
        conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-GOBO5ON\SQLEXPRESS;'
                      'Database=SampleDb;'
                      'Trusted_Connection=yes;')
        
        cursor = conn.cursor()
        
        cursor.execute("SELECT v FROM dbo.SampleValues WHERE t between ? and ?",[start_timestamp,start_timestamp])
        deteretreived=[]
        for row in cursor.fetchall():
            for field in row:
                deteretreived.append(float(str(field)))
            #for field in row:
            
        conn.close()
        self.deteretreived =deteretreived
        return(deteretreived)
        
    def get_engine_results(self,fetched_list=None):
        if fetched_list is None:
            fetched_list = self.deteretreived
        
        
        pandas2ri.activate()
        
        #activate R envinronment
        Imported_R_Envinronment=ro.r('source("D:/Volue/calcEngine.R")')
        R_FUN_Loaded=ro.r('engine_call')
        
        #get result from calculation engine
        r_results =R_FUN_Loaded(pd.DataFrame(fetched_list))
        
        #Json wrapper
        json_out ={"avg": r_results[0], 
                   "sum": r_results[1]}
        
        return(json.dumps(json_out))
        
#---------------------------Main---------------------------------
     
        #json insert sample
json_sample_list =[
    { "name": "example1", "t": 13515551, "v": 1.1 },
    { "name": "example1", "t": 13515552, "v": 2.4 },
    { "name": "example1", "t": 13515553, "v": 3.5 },
    { "name": "example2", "t": 13515554, "v": 1.5 },
    { "name": "example2", "t": 13515555, "v": 2.5 },
]

#Create instance
AP=API()
#Insert sample json for 2 clinets
AP.insert_JSON_db(json_sample_list)
#Filter recods by timestamp
records = AP.get_db_records(13515552,13515554)
#Extract calculation engib=ne results in json format
results = AP.get_engine_results(records)