# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 13:56:55 2012

@author: huanxin
"""
############################################################
#It gets input value from control file './getcodar_byrange_ctl.txt' 
#or a python function 
#it gets index of lat,lon by function 'getcodar_ctl_lalo'
#then gets id of codar data by function 'getcodar_ctl_id'
#gets data 'lat_vel,lon_vel,u,v' by function 'getcodar_edge'
#delete bad data
#plot with basemap(region)
#Input values:datetime_wanted,filename,driftnumber,url,model_option,num,interval_dtime,interval,step_size
#output values:gbox,id,lat_vel,lon_vel,u,v
#function uses:getcodar_ctl_file_edge,getcodar_ctl_lalo,getcodar_ctl_id,getcodar_edge
############################################################
from matplotlib.dates import date2num, num2date
import pylab
import sys
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
import numpy as np
sys.path.append('/net/home3/ocn/jmanning/py/mygit/modules/')
from basemap import basemap_region
pydir='../'
sys.path.append(pydir)
from hx import getcodar_ctl_file_edge,getcodar_ctl_lalo,getcodar_ctl_id,getcodar_edge
from getcodar_ctl_file_edge import getcodar_ctl_file_edge_py
###############################################
inputfilename='./getcodar_byrange_ctl.txt'
png_num=0 # for saving picture 
if inputfilename[-2:]=='py':
    datetime_wanted,url,model_option,lat_max,lon_max,lat_min,lon_min,num,interval_dtime=getcodar_ctl_file_edge_py() # reads control file
else:
    datetime_wanted,url,model_option,lat_max,lon_max,lat_min,lon_min,num,interval_dtime,arrow_percent=getcodar_ctl_file_edge(inputfilename) # reads control file
for i in range(num): # loop through number of figures
  png_num=png_num+1 
  lat_max_i,lon_max_i,lat_min_i,lon_min_i=getcodar_ctl_lalo(model_option,lat_max,lon_max,lat_min,lon_min) # gets spatial index of box
  id=getcodar_ctl_id(model_option,url,datetime_wanted) # gets time index
  lat_vel,lon_vel,u,v=getcodar_edge(url,id,lat_max_i,lon_max_i,lat_min_i,lon_min_i) # gets actual values of lat, lon, U & V
  id=str(id)
  idg1=list(ml.find(np.array(u)<>-999.0/100.))   # index u values that are good
  idg2=list(ml.find(np.array(lat_vel)>=lat_min)) # index lats > lat_min
  idg12=list(set(idg1).intersection(set(idg2)))  # intersection of idg1 and idg2
  idg3=list(ml.find(np.array(lon_vel)>=lon_min)) # index lon > lon_min
  idg=list(set(idg12).intersection(set(idg3)))   # final intersection
  arrow_percent=100.0/arrow_percent
  for i in idg:    # because of too more arrows, we cut some of them
      if i%arrow_percent<>0:
          idg.remove(i)
          
  if len(idg)<>0:
    plt.title('') 
    plt.title(str(num2date(datetime_wanted).strftime("%d-%b-%Y %H"))+'h')
    pylab.ylim([lat_min-0.02,lat_max+0.02])
    pylab.xlim([lon_min-0.02,lon_max+0.02]) #enge
    q=plt.quiver(np.reshape(lon_vel,np.size(lon_vel))[idg],np.reshape(lat_vel,np.size(lat_vel))[idg],np.reshape(u,np.size(u))[idg],np.reshape(v,np.size(v))[idg],angles='xy',scale=3,color='b')
    p=plt.quiverkey(q,min(lon_vel[0])+.1,max(lat_vel[0])-.1,1.2,str(round(1.2,2))+"m/s",coordinates='data',color='r')     
    bathy=True
    region='wv'
    basemap_region(region)
    #rbasemap_usgs([lat_min-0.08,lat_max+0.08],[lon_max+0.09,lon_min-0.09],bathy,False,2,[-200,-60],10)
    #plt.savefig('/net/home3/ocn/jmanning/py/huanxin/work/hx/'+str(datetime_wanted)+ '.png')
    plt.show()
    plt.savefig('./'+str('%03d' % png_num) + '.png')
    datetime_wanted=date2num(num2date(datetime_wanted)+interval_dtime)  #for forloop
    #plt.close()
  else:
    print 'no data'