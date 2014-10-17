# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 13:42:41 2012

@author:huanxin
"""
############################################################################
#This project could plot sst,codar, drifter track data on a picture
#It gets input value from control file "getcodar_bydrifter_ctl.txt" or  
#a python function "getcodar_ctl_file_py()"
#From lat lon of drifter data, it gets a range area first,
# then it gets codar and sst data in this range.
#At last, it plots a picture
#Input values:datetime_wanted,filename,driftnumber,url,model_option,num,interval_dtime,interval,step_size
#output values:gbox,drifter_data,id,lat_vel,lon_vel,u,v
#function uses:getcodar_ctl_file,getdrift_raw_range_latlon,getcodar_ctl_lalo,getcodar_ctl_id,getdrift_raw,getcodar_edge,plot_getsst
############################################################################
import pytz 
from matplotlib.dates import date2num, num2date
import datetime
import pylab
import sys
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
import numpy as np

pydir='../'

sys.path.append(pydir)
from hx import getcodar_ctl_file,getdrift_raw_range_latlon,getcodar_ctl_lalo,getcodar_ctl_id,getdrift_raw,getcodar_edge,plot_getsst
from getcodar_bydrifter_ctl_py import getcodar_ctl_file_py

""""""""""""""""""""""""""""""""""""""""""""""""""""
Notice: make sure to select appropriate data of codar and drifter, especially same time period.
""""""""""""""""""""""""""""""""""""""""""""""""""""
####################################################################
#### input #########################################################
  
utc = pytz.timezone('UTC')
png_num=0 #for save picture
inputfilename='./getcodar_bydrifter_ctl.txt'
#id=str(int(id))
if inputfilename[-2:]=='py':
  (datetime_wanted,filename,driftnumber,url,model_option,num,interval_dtime,interval,step_size)=getcodar_ctl_file_py()
else:
  (datetime_wanted,filename,driftnumber,url,model_option,num,interval_dtime,interval,step_size)=getcodar_ctl_file(inputfilename)
id3=int(driftnumber)  #change format for id
datetime_wanted_1=datetime_wanted
(maxlon,minlon,maxlat,minlat)=getdrift_raw_range_latlon(filename,id3,interval,datetime_wanted_1,num,step_size)
for i in range(5):  #make sure the picture can show lat and lon clearly
    if maxlat-minlat<=0.1:
        maxlat=maxlat+0.01
        minlat=minlat-0.01
    if maxlon-minlon<=0.1:
        maxlon=maxlon+0.01
        minlon=minlon-0.01

(lat_max_i,lon_max_i,lat_min_i,lon_min_i)=getcodar_ctl_lalo(model_option,maxlat,maxlon,minlat,minlon)# get index of max min lat lon
gbox=[minlon-0.03,maxlon+0.03, minlat-0.03, maxlat+0.03] # get edge for get sst
for x in range(num):
     
  id=getcodar_ctl_id(model_option,url,datetime_wanted) #get index of codar
  ask_input=num2date(datetime_wanted) #get time for getsst
  (drifter_data)=getdrift_raw(filename,id3,interval,datetime_wanted) #get drifter data
  lat=drifter_data['lat']
  lon=drifter_data['lon']
  (lat_vel,lon_vel,u,v)=getcodar_edge(url,id,lat_max_i,lon_max_i,lat_min_i,lon_min_i) #get codar data
  id=str(id)
  idg1=list(ml.find(np.array(u)<>-999.0/100.))
  idg2=list(ml.find(np.array(lat_vel)>=minlat))
  idg12=list(set(idg1).intersection(set(idg2)))
  idg3=list(ml.find(np.array(lon_vel)>=minlon))
  idg=list(set(idg12).intersection(set(idg3)))     #get index for codar data based on  edge and id(time)
  
  png_num=png_num+1  #for save movie picture
 
  if len(idg)<>0:
  
    fig = plt.figure()

    ax = fig.add_subplot(111)

    plt.title(str(num2date(datetime_wanted).strftime("%d-%b-%Y %H"))+'h')   #plot title
    pylab.ylim([minlat-0.02,maxlat+0.02])    #limit edge
    pylab.xlim([minlon-0.02,maxlon+0.02])
    plot_getsst(ask_input,utc,gbox)    #plot  sst
    #plot codar
    codar_scale_index=np.average(np.average(np.reshape(u,np.size(u))[idg]),np.average(np.reshape(v,np.size(v))[idg]))
    q=plt.quiver(np.reshape(lon_vel,np.size(lon_vel))[idg],np.reshape(lat_vel,np.size(lat_vel))[idg],np.reshape(u,np.size(u))[idg],np.reshape(v,np.size(v))[idg],angles='xy',scale=1,color='b',label='codar')
    p = plt.quiverkey(q,minlon-0.01,maxlat+0.06,0.2,str(round(0.2,2))+"m/s",coordinates='data',color='b')  #plot key
    #codar_scale_index/10 get the suit size of arrow      
    lat_wanted=lat[-1]
    lon_wanted=lon[-1]
  
    plt.plot(lon_wanted,lat_wanted,'.',markersize=30,color='r',label='end')#end time
    plt.plot(np.reshape(lon,np.size(lon)),np.reshape(lat,np.size(lat)),color='black')
    plt.plot(lon[0],lat[0],'.',markersize=20,color='g',label='start')  # start time
    plt.legend( numpoints=1)

    plt.title(str(num2date(datetime_wanted).strftime("%d-%b-%Y %H"))+'h')
   
  else:
    print "Sorry. No good  codar data at this time"
     
    plt.title(str(num2date(datetime_wanted).strftime("%d-%b-%Y %H"))+'h')
    plot_getsst(ask_input,utc,gbox)
    lat_wanted=lat[-1]
    lon_wanted=lon[-1]
    #find wanted point lat,lon

    plt.plot(lon_wanted,lat_wanted,'.',markersize=30,color='r',label='end')
    plt.plot(np.reshape(lon,np.size(lon)),np.reshape(lat,np.size(lat)),color='black')
    pylab.ylim([minlat-0.02,maxlat+0.02])
    pylab.xlim([minlon-0.02,maxlon+0.02])
    plt.plot(lon[0],lat[0],'.',markersize=20,color='g',label='start')  # start time
    plt.legend()
  #for another forloop 
  id=int(id)+interval 
  plt.savefig('./'+str('%03d' % png_num) + '.png')
  datetime_wanted=date2num(num2date(datetime_wanted)+datetime.timedelta( 0,step_size*60*60 ))  

plt.show()
#plt.close()