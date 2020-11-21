import importlib
import pickle
from math import radians, cos, sin, asin, sqrt
import time
from bson import json_util
import joblib
import os
from flask import Flask,Response,json,jsonify,request
import pymongo
import traceback
import numpy as np
import pandas as pd
from pyroutelib3 import Router
Model = importlib.import_module('Model')
scaler_x = Model.scaler_x

app = Flask(__name__)
port = int(os.getenv('PORT', 8000))

#load model
model = pickle.load(open('model.pkl', 'rb'))

#connect to db
#uri = 'mongodb+srv://khouloudayadi:ayadi1101@network.soh94.azure.mongodb.net/network?retryWrites=true&w=majority'
uri = 'mongodb://khouloudayadi:ayadi1101@ds038547.mlab.com:38547/network?retryWrites=false'
client = pymongo.MongoClient(uri)
db=client.network

def predict_time(Xnew, model, scaler_x):
    Xnew = np.array(Xnew).reshape(1, -1)
    Xnew = scaler_x.transform(Xnew)
    ynew = model.predict(Xnew)
    return ynew[0]

def haversine(lon1, lat1, lon2, lat2):
    radius = 6371 * 1000  # dist in m
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    dist = c * radius
    return dist

def trajetPlot(coor_depart,coor_arrivee):
    router = Router("car")
    depart = router.findNode(coor_depart[0], coor_depart[1])
    arrivee = router.findNode(coor_arrivee[0], coor_arrivee[1])
    routeLatLons = [coor_depart, coor_arrivee]
    status, route = router.doRoute(depart, arrivee)
    if status == 'success':
        routeLatLons = list(map(router.nodeLatLon, route))
    return (routeLatLons)

def search_all_zone(zone, coor_depart,coor_arrivee):
    minDist=70000
    newlist = []
    routeLatLons = trajetPlot(coor_depart,coor_arrivee)

    for doc in list(zone):
        for j in range(0, len(routeLatLons)):
            dist = round(haversine(doc['lat_center'],doc['lon_center'], routeLatLons[j][0], routeLatLons[j][1]),4)
            if(dist <  doc['raduis']):
                dist_min=round(haversine(doc['lat_center'],doc['lon_center'], coor_depart[0], coor_depart[1]),4)
                if(dist_min < minDist):
                    minDist=dist_min
                    newlist=[doc['lat_center'], doc['lon_center'], doc['raduis']]
                break
            else :
                continue

    return newlist

def addData(timeStamp, start_lat, start_lon, end_lat, end_lon, vitesse,network,zone_noir_lat,zone_noir_lon,raduis):
    #collect new data
    newDataSet = db.NewDataSet
    row={
    'timeStamp':timeStamp,
    'start_lat':start_lat,
    'start_lon':start_lon,
    'end_lat':end_lat,
    'end_lon':end_lon,
    'vitesse':vitesse,
    'zone_noir_lat':zone_noir_lat,
    'zone_noir_lon':zone_noir_lon,
    'raduis':raduis,
    'network':network
    }
    newDataSet.insert_one(row)
    print("insert successfully")

@app.route('/addCell', methods=['POST'])
def addCell():
    cid = request.json['cid']
    radio = request.json['radio']
    mcc = request.json['mcc']
    mnc = request.json['mnc']
    area = request.json['area']
    lon = request.json['lon']
    lat = request.json['lat']
    range = request.json['range']
    Cell = db.cellTower.find_one({"cid": cid})
    if not Cell :
        row={
        'radio':radio,
        'mcc':mcc,
        'mnc':mnc,
        'area':area,
        'cid':cid,
        'lon':lon,
        'lat':lat,
        'range':range
        }
        db.cellTower.insert(row)
        return jsonify({"message": "Add success", "success": True})
    else:
        return jsonify({"message": "Cell exist deja", "success": False})

@app.route('/getCell', methods=['GET'])
def getCell():
    listCell=[]
    DataSetCell = db.cellTower.find()
    if DataSetCell:
        for doc in list(DataSetCell):
            listCell.append({'radio':doc['radio'],'mcc': doc['mcc'],'mnc': doc['mnc'],'cid':doc['cid'],'area':doc['area'],'lon': doc['lon'],'lat':doc['lat'],'range':doc['range']})
        print(listCell)
        return jsonify({"result":listCell, "success":True})
    else:
        return jsonify({"message": "Empty List", "success": False})
    #response = json_util.dumps(DataSetCell)
    #return Response(response)

@app.route('/getCellByCid/<cid>', methods=['GET'])
def getCellByCid(cid):
    CellByCid=[]
    Cell = db.cellTower.find({'cid':cid})
    if Cell:
        for doc in list(Cell):
            CellByCid.append({'radio':doc['radio'],'mcc': doc['mcc'],'mnc': doc['mnc'],'cid':doc['cid'],'area':doc['area'],'lon': doc['lon'],'lat':doc['lat'],'range':doc['range']})
        return jsonify({"result":CellByCid, "success":True})
    else:
        return jsonify({"message": "Cell not found", "success": False})

@app.route('/predict', methods=['POST'])
def predict():
    #start = time.process_time()
    start_lat = request.json['start_lat']
    start_lon = request.json['start_lon']
    end_lat = request.json['end_lat']
    end_lon = request.json['end_lon']
    vitesse = request.json['vitesse']
    timeStamp = request.json['timeStamp']
    network = request.json['network']

    coor_depart = [start_lat,start_lon]
    coor_arrivee = [end_lat, end_lon]

    zone_noir_lat=0
    zone_noir_lon=0
    raduis=0

    all_zone = db.zone_noir
    zone = all_zone.find()
    newlist=search_all_zone(zone, coor_depart, coor_arrivee)

    if(not newlist):
        addData(timeStamp, start_lat, start_lon, end_lat, end_lon, vitesse,network,zone_noir_lat,zone_noir_lon,raduis)
        return jsonify({"message":"trajet connecté ! aucune zone non connecte","success":False})
    else:
        zone_noir_lat = newlist[0]
        zone_noir_lon = newlist[1]
        raduis = newlist[2]
        distance_start_noir = round((haversine(start_lon, start_lat, zone_noir_lon, zone_noir_lat) - raduis), 4)
        distance_end_noir = round((haversine(zone_noir_lon, zone_noir_lat, end_lon, end_lat) - raduis), 4)
        if model:
            try:
                Xnew = [start_lat, start_lon, end_lat, end_lon, zone_noir_lat, zone_noir_lon, raduis, vitesse, distance_start_noir, distance_end_noir]
                ynew = predict_time(Xnew, model, scaler_x)
                print("X=%s, Predicted=%s" % (Xnew, ynew))
                addData(timeStamp, start_lat, start_lon, end_lat, end_lon, vitesse,network,zone_noir_lat,zone_noir_lon,raduis)
                return jsonify({"result":str(ynew),"distance":str(distance_start_noir), "success":True})
            except:
                return jsonify({"message":traceback.format_exc(),"success":False})
        else:
            return jsonify({"message":"No model here to use","success":False})


@app.route('/')
def root():
    return "Api My Network"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
