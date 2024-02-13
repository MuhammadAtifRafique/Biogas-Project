import pandas as pd
from io import StringIO
from flask import Flask, jsonify, send_file, redirect, url_for, request
from flask_cors import CORS, cross_origin
import threading
import pymysql
import json
from config import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
CORS(app)
app.app_context().push()
# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

class MyDataBase:
    def __init__(self):
        self.connection = pymysql.connect(host='169.46.39.69',
                      user='analyze_dev55',
                      password='bhaih@dev55',
                      db='analyzer',
                      charset='utf8mb4',
                      cursorclass=pymysql.cursors.DictCursor)
        
        pass

    def fetchTableData(self, tableName):
         self.cursor = self.connection.cursor()
         self.cursor.execute(f""" SELECT * from {tableName}""")
         self.cursor.connection.commit()
         output = self.cursor.fetchall()
         #print(f"data:{output}")
         #for i in output:
         #   print(f" Data is = {i}")
         self.cursor.close() #Closing the cursor
         return output # end of fetchTableData function
    def fetchSettingsWithGroupID(self, tableName,GroupID):
         self.cursor = self.connection.cursor()
         self.cursor.execute(f""" SELECT * from {tableName} WHERE GroupID={GroupID}""")
         self.cursor.connection.commit()
         output = self.cursor.fetchall()
         self.cursor.close() #Closing the cursor
         return output # end of fetchTableData function
    def fetchSelectedData(self, tableName,CsvfileID):
         self.cursor = self.connection.cursor()
         self.cursor.execute(f""" SELECT * from {tableName} WHERE CsvfileID = {CsvfileID}""")
         self.cursor.connection.commit()
         output = self.cursor.fetchall()
         self.cursor.close() #Closing the cursor
         return output # end of fetchSelectedData function

    def insertToDB(self, query, values, table_name):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query, values)
        self.cursor.connection.commit()
        self.cursor.execute(f""" SELECT * from {table_name}""")
        output = self.cursor.fetchall()
        
        lastRow = None
        for i in output:
            lastRow = i
        self.cursor.close() #Closing the cursor
        return lastRow # end of insertToDB function
    def fetchFromDB(self, query):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query)
        self.cursor.connection.commit()
        output = self.cursor.fetchall()
        
        self.cursor.close() #Closing the cursor
        return output # end of insertToDB function
    def updateToDB(self, query,table_name):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query)
        self.cursor.connection.commit()
        self.cursor.execute(f""" SELECT * from {table_name}""")
        output = self.cursor.fetchall()
        
        data = None
        for i in output:
            data = i
        self.cursor.close() #Closing the cursor
        return data # end of insertToDB function
  
@app.route("/api/get_post_notes" , methods=['POST'])
def get_post_notes():
    db = MyDataBase()
    if request.method == 'POST':
        parsedJson = request.get_json() # json should be like : {"CsvfileID":}
        CsvfileID = parsedJson["CsvfileID"]
        #print(CsvfileID)
        query = (f"""SELECT post_notes FROM csvtbl WHERE CsvfileID={CsvfileID}""")
        strData = db.fetchFromDB(query)[0]["post_notes"] # query, values, table_name
        #strData = fetchedData[0]["post_notes"]

    return jsonify({"response": False,"result": strData})

@app.route("/api/post_post_notes" , methods=['POST'])
def post_post_notes():
    db = MyDataBase()
    
    if request.method == 'POST':
        table_name = 'csvtbl'
        parsedJson = request.get_json()
        CsvfileID = parsedJson["CsvfileID"]
        post_notes = json.dumps(parsedJson)
        query = """UPDATE csvtbl SET post_notes=%s WHERE CsvfileID=%s"""
        values = (post_notes,CsvfileID)
        lastSavedData = db.insertToDB(query, values,table_name) # query, values, table_name
        #print(lastSavedData)

    return jsonify({"response": False,"result": f"Saved Successfully in CsvfileID {CsvfileID}"})

@app.route("/api/get_pre_notes" , methods=['POST'])
def get_pre_notes():
    db = MyDataBase()
    
    if request.method == 'POST':
        parsedJson = request.get_json() # json should be like : {"CsvfileID":}
        CsvfileID = parsedJson["CsvfileID"]
        print(CsvfileID)
        query = (f"""SELECT pre_notes FROM csvtbl WHERE CsvfileID={CsvfileID}""")
        strData = db.fetchFromDB(query)[0]["pre_notes"] # query, values, table_name
        #strData = fetchedData[0]["pre_notes"]

    return jsonify({"response": False,"result": strData})    

@app.route("/api/post_pre_notes" , methods=['POST'])
def post_pre_notes():
    db = MyDataBase()
    
    if request.method == 'POST':
        table_name = 'csvtbl'
        parsedJson = request.get_json()
        CsvfileID = parsedJson["CsvfileID"]
        pre_notes = json.dumps(parsedJson)
        query = """UPDATE csvtbl SET pre_notes=%s WHERE CsvfileID=%s"""
        values = (pre_notes,CsvfileID)
        lastSavedData = db.insertToDB(query, values,table_name) # query, values, table_name
        #print(lastSavedData)

    return jsonify({"response": False,"result": f"Saved Successfully in CsvfileID {CsvfileID}"})

@app.route("/api/save_csv_meta_data" , methods=['POST'])
def save_csv_meta_data():
    db = MyDataBase()
    metadata = MetaData()
    csvtbl = "csvtbl"
    tableName = "metadatatbl2"
    rpi_id = 1

    if request.method == 'POST':
        file = request.files['file']
        fileName = file.filename
        date_time = request.form.get('dateTime')
        sample_num = request.form.get('csvSampleNum')
        print(f"Coming csv file date : {date_time}")
        print(f"Coming csv file name : {file.filename}")
        if file.mimetype != 'text/csv': # Check if csv file
            return 'Only CSV files are allowed!', 400
        if file.filename == '': # Check if no file selected 
            return 'No file selected!', 400
        
        df = pd.read_csv(file)
        dicData = df.to_dict(orient='records')

        _data= json.dumps(dicData)
        query  =  (f"""INSERT INTO {csvtbl} (RPIID, CsvfileDirectory,sample_num,date_time)  VALUES (%s, %s, %s, %s)""")
        values = (rpi_id,fileName,sample_num,date_time)
        lastRow = db.insertToDB(query, values,csvtbl)
        CsvfileID = lastRow[metadata.CsvfileID]
        
        query = ("""INSERT INTO metadatatbl2 (CsvfileID, CSV_DATA) VALUES
                                    (%s, %s) """) 
        values = (CsvfileID,_data)
            
        db.insertToDB(query, values, tableName)
           # print(f"[INFO] Data_Point {x[metadata.Data_Point]} && Sample_Num {x[metadata.Sample_Num]}                  Saved Successfully  !!!!!")
    return jsonify({"response": True,"result": "Success"})


@app.route("/api/add_group" , methods=['POST'])
def add_group():
    db = MyDataBase()
    CsvfileID = 5
    table_name = 'grouptbl'
    if request.method == 'POST':
        parsedJson = request.get_json()
        query = """INSERT INTO grouptbl (CsvfileID,GroupName) VALUES(%s,%s)"""
        values = (CsvfileID,parsedJson['group_name'])
        db.insertToDB(query, values, table_name) # query, values, table_name
        #print(parsedJson['group_name'])

    return jsonify({"response": False,"result": ["Success"]})
@app.route("/api/save_fav_setting" , methods=['POST'])
def save_fav_settings():
    db = MyDataBase()
    group_fav_settings_tbl = 'group_fav_settings_tbl'
    if request.method == 'POST':
        parsedjson = request.get_json()
        GroupID = parsedjson['GroupID']
        SettingsName = parsedjson['Fav_setting_name']
        query = """INSERT INTO group_fav_settings_tbl (GroupID,SettingsName,SettingObj) VALUES (%s,%s,%s)"""
        values = (GroupID,SettingsName,str(json.dumps(parsedjson)))
        NewID = db.insertToDB(query,values,group_fav_settings_tbl) # Query , Value , Table

        print(f"DATA SAVED : {NewID}")
        savedData = db.fetchTableData(group_fav_settings_tbl)
        gfsid = {'GFSID':savedData[len(savedData)-1]['GFSID']}
        print(f"Saved data is with GFSID : {savedData}")
    return jsonify({"response": False,"result": gfsid})

@app.route("/api/check_login", methods=['GET', 'POST'])
def check_login():
    db = MyDataBase()
    loginData = db.fetchTableData("Usertbl")
    #[{'UserID': 1, '_username': 'acenxion', '_password': 'acxbio', 'role': 'admin', 'last_login_date_time': '0000-00-00 00:00:00', 'last_logout_date_time': '0000-00-00 00:00:00'}]
    _dn_uname = loginData[0]["_username"]
    _dn_password = loginData[0]["_password"]
    return jsonify({"uname":_dn_uname, "pass":_dn_password})

@app.route("/api/get_list_of_fav_settings" , methods=['POST'])
def get_setting_list():
    db = MyDataBase()
    group_fav_settings_tbl = "group_fav_settings_tbl"
    if request.method == 'POST':
        parsedjson = request.get_json()
        GroupID = parsedjson[0]['GroupID']
        print(f"Fetching data of group ID is: {GroupID}")
        group_fav_settings_Data = db.fetchSettingsWithGroupID(group_fav_settings_tbl,GroupID)
    return jsonify({"response": False,"result": group_fav_settings_Data})

@app.route("/api/get_list_of_group" , methods=['GET'])
def get_group_list():
    db = MyDataBase()
    
    if request.method == 'GET':
        grouptblData = db.fetchTableData("grouptbl")

    return jsonify({"response": False,"result": [grouptblData]})

@app.route("/api/get_graph_meta_data" , methods=['POST', 'GET'])
def get_graph_meta_data():
    metadata = MetaData()
    db = MyDataBase()
    tableName = "metadatatbl2"
    data = []
    totalData = []

    if request.method == 'GET':
        return jsonify({"response": False,"result": "Please Send Post request here!"})
    elif request.method == 'POST':
        postJson = request.get_json()
        client_csvFileID = postJson[metadata.CsvfileID]
        print(f"[INFO] You are getting the data of CsvfileID = {client_csvFileID}")
        Data_Point = postJson[metadata.Data_Point]
        _data = db.fetchSelectedData(tableName,client_csvFileID)[0] # Fetch data and ignore list
        RPI_DataID =  _data[metadata.RPI_DataID]
        CsvfileID = _data[metadata.CsvfileID]
        csv_dict_data = json.loads(_data['CSV_DATA'])
        df = pd.DataFrame(csv_dict_data)
        for dp in Data_Point:
            Data_Point_Data = df.loc[df[metadata.Data_Point]==dp].to_dict("records")
            rawDataPoint = None
            for x in Data_Point_Data:
                row = {metadata.RPI_DataID:RPI_DataID, metadata.CsvfileID:CsvfileID, metadata.Data_Point:x[metadata.Data_Point],metadata.Sample_Num:x[metadata.Sample_Num], metadata.Time_Stamp:str(x[metadata.Time_Stamp]) , metadata.Time_Per:x[metadata.Time_Per] , metadata.Temp:x[metadata.Temp], metadata.Gain:x[metadata.Gain], metadata.Int_Time:x[metadata.Int_Time], metadata.Allowable_Dev:x[metadata.Allowable_Dev],
                                    metadata.Raw_Used_Vio:x[metadata.Raw_Used_Vio],metadata.Raw_Values_Vio_450nm:x[metadata.Raw_Values_Vio_450nm] , metadata.Raw_Selected_Vio_450nm:x[metadata.Raw_Selected_Vio_450nm] , metadata.Raw_Avg_Vio_450nm:x[metadata.Raw_Avg_Vio_450nm] , metadata.Raw_StdDev_Vio:x[metadata.Raw_StdDev_Vio] , metadata.Cal_Used_Vio:x[metadata.Cal_Used_Vio] , metadata.Cal_Values_Vio_450nm:x[metadata.Cal_Values_Vio_450nm], metadata.Cal_Selected_Vio_450nm:x[metadata.Cal_Selected_Vio_450nm], metadata.Cal_Avg_Vio_450nm:x[metadata.Cal_Avg_Vio_450nm], metadata.Cal_StdDev_Vio:x[metadata.Cal_StdDev_Vio], 
                                    metadata.Raw_Used_Blu:x[metadata.Raw_Used_Blu],metadata.Raw_Values_Blu_500nm:x[metadata.Raw_Values_Blu_500nm] , metadata.Raw_Selected_Blu_500nm:x[metadata.Raw_Selected_Blu_500nm] , metadata.Raw_Avg_Blu_500nm:x[metadata.Raw_Avg_Blu_500nm] , metadata.Raw_StdDev_Blu:x[metadata.Raw_StdDev_Blu] , metadata.Cal_Used_Blu:x[metadata.Cal_Used_Blu] , metadata.Cal_Values_Blu_500nm:x[metadata.Cal_Values_Blu_500nm], metadata.Cal_Selected_Blu_500nm:x[metadata.Cal_Selected_Blu_500nm], metadata.Cal_Avg_Blu_500nm:x[metadata.Cal_Avg_Blu_500nm], metadata.Cal_StdDev_Blu:x[metadata.Cal_StdDev_Blu],  
                                    metadata.Raw_Used_Grn:x[metadata.Raw_Used_Grn],metadata.Raw_Values_Grn_550nm:x[metadata.Raw_Values_Grn_550nm] , metadata.Raw_Selected_Grn_550nm:x[metadata.Raw_Selected_Grn_550nm] , metadata.Raw_Avg_Grn_550nm:x[metadata.Raw_Avg_Grn_550nm] , metadata.Raw_StdDev_Grn:x[metadata.Raw_StdDev_Grn] , metadata.Cal_Used_Grn:x[metadata.Cal_Used_Grn] , metadata.Cal_Values_Grn_550nm:x[metadata.Cal_Values_Grn_550nm], metadata.Cal_Selected_Grn_550nm:x[metadata.Cal_Selected_Grn_550nm], metadata.Cal_Avg_Grn_550nm:x[metadata.Cal_Avg_Grn_550nm], metadata.Cal_StdDev_Grn:x[metadata.Cal_StdDev_Grn],  
                                    metadata.Raw_Used_Yel:x[metadata.Raw_Used_Yel],metadata.Raw_Values_Yel_570nm:x[metadata.Raw_Values_Yel_570nm] , metadata.Raw_Selected_Yel_570nm:x[metadata.Raw_Selected_Yel_570nm] , metadata.Raw_Avg_Yel_570nm:x[metadata.Raw_Avg_Yel_570nm] , metadata.Raw_StdDev_Yel:x[metadata.Raw_StdDev_Yel] , metadata.Cal_Used_Yel:x[metadata.Cal_Used_Yel] , metadata.Cal_Values_Yel_570nm:x[metadata.Cal_Values_Yel_570nm], metadata.Cal_Selected_Yel_570nm:x[metadata.Cal_Selected_Yel_570nm], metadata.Cal_Avg_Yel_570nm:x[metadata.Cal_Avg_Yel_570nm], metadata.Cal_StdDev_Yel:x[metadata.Cal_StdDev_Yel], 
                                    metadata.Raw_Used_Org:x[metadata.Raw_Used_Org],metadata.Raw_Values_Org_600nm:x[metadata.Raw_Values_Org_600nm] , metadata.Raw_Selected_Org_600nm:x[metadata.Raw_Selected_Org_600nm] , metadata.Raw_Avg_Org_600nm:x[metadata.Raw_Avg_Org_600nm] , metadata.Raw_StdDev_Org:x[metadata.Raw_StdDev_Org] , metadata.Cal_Used_Org:x[metadata.Cal_Used_Org] , metadata.Cal_Values_Org_600nm:x[metadata.Cal_Values_Org_600nm], metadata.Cal_Selected_Org_600nm:x[metadata.Cal_Selected_Org_600nm], metadata.Cal_Avg_Org_600nm:x[metadata.Cal_Avg_Org_600nm], metadata.Cal_StdDev_Org:x[metadata.Cal_StdDev_Org], 
                                    metadata.Raw_Used_Red:x[metadata.Raw_Used_Red],metadata.Raw_Values_Red_650nm:x[metadata.Raw_Values_Red_650nm] , metadata.Raw_Selected_Red_650nm:x[metadata.Raw_Selected_Red_650nm] , metadata.Raw_Avg_Red_650nm:x[metadata.Raw_Avg_Red_650nm] , metadata.Raw_StdDev_Red:x[metadata.Raw_StdDev_Red] , metadata.Cal_Used_Red:x[metadata.Cal_Used_Red] , metadata.Cal_Values_Red_650nm:x[metadata.Cal_Values_Red_650nm], metadata.Cal_Selected_Red_650nm:x[metadata.Cal_Selected_Red_650nm], metadata.Cal_Avg_Red_650nm:x[metadata.Cal_Avg_Red_650nm], metadata.Cal_StdDev_Red:x[metadata.Cal_StdDev_Red]}
                data.append(row)
                #print(f"[INFO] Length of Rows : {len(row)}")
                rawDataPoint = x[metadata.Data_Point]
            singleDataPointData = {"Data_Point": rawDataPoint,"Samples": data}
            totalData.append(singleDataPointData)
            print(f"[INFO] Sending Data Point is : {rawDataPoint}")
            print(f"[INFO] Sending Data Rows are : {len(data)}")
            data = []
    return jsonify({"response": False,"result": totalData})


@app.route("/api/get_list_of_csv" , methods=['GET'])
def get_csv_list():
    db = MyDataBase()
    csvtblData = db.fetchTableData("csvtbl")

    return jsonify({"response": False,"result": csvtblData})

@app.route("/api/get_grid_meta_data" , methods=['POST', 'GET'])
def get_grid_meta_data():
    metadata = MetaData()
    db = MyDataBase()
    tableName = "metadatatbl2"
    data = []
    if request.method == 'GET':
        return jsonify({"response": False,"result": "Please Send Post request here!"})
    elif request.method == 'POST':
        client_data = request.get_json()
        print(client_data)
        client_csvFileID = client_data['CsvfileID']
        _data = db.fetchSelectedData(tableName,client_csvFileID)[0] # Fetch data and ignore list
        RPI_DataID =  _data[metadata.RPI_DataID]
        CsvfileID = _data[metadata.CsvfileID]
        csv_dict_data = json.loads(_data['CSV_DATA'])
        for x in csv_dict_data:
            row = [RPI_DataID, CsvfileID, x[metadata.Data_Point], x[metadata.Sample_Num], str(x[metadata.Time_Stamp]) , x[metadata.Time_Per] , x[metadata.Temp], x[metadata.Gain], x[metadata.Int_Time], x[metadata.Allowable_Dev],
                                x[metadata.Raw_Used_Vio],x[metadata.Raw_Values_Vio_450nm] , x[metadata.Raw_Selected_Vio_450nm] , x[metadata.Raw_Avg_Vio_450nm] , x[metadata.Raw_StdDev_Vio] , x[metadata.Cal_Used_Vio] , x[metadata.Cal_Values_Vio_450nm], x[metadata.Cal_Selected_Vio_450nm], x[metadata.Cal_Avg_Vio_450nm], x[metadata.Cal_StdDev_Vio], 
                                x[metadata.Raw_Used_Blu],x[metadata.Raw_Values_Blu_500nm] , x[metadata.Raw_Selected_Blu_500nm] , x[metadata.Raw_Avg_Blu_500nm] , x[metadata.Raw_StdDev_Blu] , x[metadata.Cal_Used_Blu] , x[metadata.Cal_Values_Blu_500nm], x[metadata.Cal_Selected_Blu_500nm], x[metadata.Cal_Avg_Blu_500nm], x[metadata.Cal_StdDev_Blu],  
                                x[metadata.Raw_Used_Grn],x[metadata.Raw_Values_Grn_550nm] , x[metadata.Raw_Selected_Grn_550nm] , x[metadata.Raw_Avg_Grn_550nm] , x[metadata.Raw_StdDev_Grn] , x[metadata.Cal_Used_Grn] , x[metadata.Cal_Values_Grn_550nm], x[metadata.Cal_Selected_Grn_550nm], x[metadata.Cal_Avg_Grn_550nm], x[metadata.Cal_StdDev_Grn],  
                                x[metadata.Raw_Used_Yel],x[metadata.Raw_Values_Yel_570nm] , x[metadata.Raw_Selected_Yel_570nm] , x[metadata.Raw_Avg_Yel_570nm] , x[metadata.Raw_StdDev_Yel] , x[metadata.Cal_Used_Yel] , x[metadata.Cal_Values_Yel_570nm], x[metadata.Cal_Selected_Yel_570nm], x[metadata.Cal_Avg_Yel_570nm], x[metadata.Cal_StdDev_Yel], 
                                x[metadata.Raw_Used_Org],x[metadata.Raw_Values_Org_600nm] , x[metadata.Raw_Selected_Org_600nm] , x[metadata.Raw_Avg_Org_600nm] , x[metadata.Raw_StdDev_Org] , x[metadata.Cal_Used_Org] , x[metadata.Cal_Values_Org_600nm], x[metadata.Cal_Selected_Org_600nm], x[metadata.Cal_Avg_Org_600nm], x[metadata.Cal_StdDev_Org], 
                                x[metadata.Raw_Used_Red],x[metadata.Raw_Values_Red_650nm] , x[metadata.Raw_Selected_Red_650nm] , x[metadata.Raw_Avg_Red_650nm] , x[metadata.Raw_StdDev_Red] , x[metadata.Cal_Used_Red] , x[metadata.Cal_Values_Red_650nm], x[metadata.Cal_Selected_Red_650nm], x[metadata.Cal_Avg_Red_650nm], x[metadata.Cal_StdDev_Red]
                                ]
            data.append(row)
        print(f"[INFO] Sending Data Rows are : {len(data)}")
        return jsonify({"response": False,"result": data})
    pass
@app.route("/api/rack-status")
def rack_status():
    dict = [
            {
                "rackNum": 1,
                "temp": 36,
                "progress": 10,
                "status": "Running",
                "openBay": 2,
                "running": 1,
                "complete": 2,
                "bayError": 1,
                "errorList": ["Cassette insert error (111b) – Bay -1A", "No error - Bay -1B"]
            },
            {
                "rackNum": 2,
                "temp": 56,
                "progress": 40,
                "status": "Error",
                "openBay": 1,
                "running": 0,
                "complete": 1,
                "bayError": 3,
                "errorList": ["Cassette insert error (222b) – Bay -2A", "No error - Bay -2B"]
            },
            {
                "rackNum": 3,
                "temp": 6,
                "progress": 100,
                "status": "Completed",
                "openBay": 0,
                "running": 0,
                "complete": 5,
                "bayError": 0,
                "errorList": ["Cassette insert error (333b) – Bay -3A", "No error - Bay -3B"]
            }
        ]
    return jsonify(dict)
    pass # end of rack_status function
@app.route("/")

def hello_world():
    return jsonify({"response": True,"result": "Please Send Post request to endpoint /api/runJob!"})

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(port=8000, debug=True, use_reloader=False)).start()