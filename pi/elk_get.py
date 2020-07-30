from elasticsearch import Elasticsearch
from datetime import datetime
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
from scipy import interpolate
from scipy.interpolate import RegularGridInterpolator
def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host':'172.16.174.29','port':9200}])
    if _es.ping():
        print("Connected to the server")
    else:
        print("Unable to connect to the server")
    return _es

def search(es_object, index_name, search):
    count = es_object.count(index = index_name, body = search)
    #print(count)
    total_count = count['count']
    # print(total_count)
    res = es_object.search(index = index_name, body = search, size = total_count)
    return res["hits"]["hits"]

def average(arr):
    temp=0
    count=0
    for x in arr:
        if(type(x[1])==float):
            temp=temp+x[1]
            count=count+1
    return temp/count
def gen_search_obj(zone,b_date,e_date):
    return {
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "Room #": zone
          }
        }
      ],
      "filter": [
        {
          "range" : {
            "@timestamp" : {
                "gte": b_date, 
                "lte": e_date
                }
            }
        }
      ]
    }
  }
} 
def convert_to_box_array(l,b,array):
  temp=[]
  i=0
  if(len(array)<4):
    return
  for x in range(0,l):
    temp1=[]
    for y in range(0,b):
      temp1.append(array[i])
      i+=1
    temp.append(temp1)  
  return temp
def gen_interpolate_heatmap(l,b,array):
  mymin1,mymax1=0,l-1
  mymin2,mymax2=0,b-1
  X = np.linspace(mymin1,mymax1,l)
  Y = np.linspace(mymin2,mymax2,b)
  x,y = np.meshgrid(X,Y)
  test = np.array(array)
  f = interpolate.interp2d(x,y,test,kind='linear')
  Xnew = np.linspace(mymin1,mymax1,l*1000)
  Ynew = np.linspace(mymin2,mymax2,b*1000)
  test8x8 = f(Xnew,Ynew)
  cmap= sns.cm.rocket_r  
  ax = sns.heatmap(test8x8,linewidth=0,cmap="Blues_r")
  plt.show()
es = connect_elasticsearch()
def avg_all_room(ardi):
  temps=[]
  for x in ardi:
    if es is not None:
        data=search(es,'copas-2019.08.07',gen_search_obj("zone "+x,"2019-08-07","2019-08-07"))
        # print(data)
        zoneTemp = []
        for row in data:
            z = row["_source"]["Room #"]
            t = row["_source"]["Temp in deg C"]
            T = row["_source"]["@timestamp"]
            if (z=="zone "+x):
                zoneTemp.append([z,t,T]) 
        #print(zoneTemp)
        temps.append(average(zoneTemp))
  return temps
side1=["0011","0006","0002"]
side2=["0005","0007","0004"]
avg1=avg_all_room(side1)
avg2=avg_all_room(side2)
avg_g=[avg1,avg2]
gen_interpolate_heatmap(3,2,avg_g)
side1_u=["1011","1006","1002"]
side2_u=["1005","1007","1004"]
avg1_u=avg_all_room(side1_u)
avg2_u=avg_all_room(side2_u)
avg_u=[avg1_u,avg2_u]
gen_interpolate_heatmap(3,2,avg_u)