# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 15:34:19 2012


@author: huanxin
"""
#########################################################
#from control file to get latmax,latmin,lonmax,lonmin,time,number, interval,and one url to get codar
#control file "./getcodar_byrange_ctl.txt"
#this program use for plotting codar and sst
#The saving file will be in same floder as this program
#the picture will be showed with basemap
#Input values:datetime_wanted,filename,model_option,num,interval_dtime,interval,step_size
#output values:gbox,drifter_data,id,lat_vel,lon_vel,u,v
#function uses:getcodar_ctl_file_edge,getcodar_ctl_lalo,getcodar_ctl_id,getcodar_edge, plot_getsst
####################################################
from matplotlib.dates import date2num, num2date
import pylab
import sys

import matplotlib.pyplot as plt
import matplotlib.mlab as ml
import numpy as np
sys.path.append("/usr/local/lib/python2.7/dist-packages/Pydap-3.0.1-py2.7.egg")
sys.path.append('/net/home3/ocn/jmanning/py/mygit/modules/')
from basemap import basemap_region
import pytz
#sys.path.append("/home3/ocn/jmanning/py/geoport/jmanning/oceanography/")
#import basemap as bm
from hx import getcodar_ctl_file_edge,getcodar_ctl_lalo,getcodar_ctl_id,getcodar_edge, plot_getsst

utc = pytz.timezone('UTC')
png_num=0 # for saving picture  
inputfilename='./getcodar_byrange_ctl.txt'
datetime_wanted,url,model_option,lat_max,lon_max,lat_min,lon_min,num,interval_dtime,arrow_percent=getcodar_ctl_file_edge(inputfilename)  #get data from ctl file
gbox=[lon_min, lon_max, lat_min, lat_max]# 2012 ring , get edge box for sst
lat_max_i,lon_max_i,lat_min_i,lon_min_i=getcodar_ctl_lalo(model_option,lat_max,lon_max,lat_min,lon_min)
for i in range(num):
    #
  
  id=getcodar_ctl_id(model_option,url,datetime_wanted)
  lat_vel,lon_vel,u,v=getcodar_edge(url,id,lat_max_i,lon_max_i,lat_min_i,lon_min_i) #get edge of codar

  id=str(id) # change id format
  idg1=list(ml.find(np.array(u)<>-999.0/100.))
  idg2=list(ml.find(np.array(lat_vel)>=lat_min))
  idg12=list(set(idg1).intersection(set(idg2)))
  idg3=list(ml.find(np.array(lon_vel)>=lon_min))
  idg=list(set(idg12).intersection(set(idg3)))   # get index of codar data

  for i in idg:    # because of too more arrows, we cut some of them
      if i%arrow_percent<>0:
          idg.remove(i)
          
  if len(idg)<>0:

    ask_input=num2date(datetime_wanted)
    plot_getsst(ask_input,utc,gbox)
    #basemap_standard(lon_vel[idg[0]],lat_vel[idg[0]],0.5)
    #bm.basemap_usgs([min(np.reshape(lon_vel,np.size(lon_vel))[idg],max(np.reshape(lon_vel,np.size(lon_vel))[idg]))],[min(np.reshape(lat_vel,np.size(lat_vel))[idg],max(np.reshape(lat_vel,np.size(lat_vel))[idg]))],True)
    q=plt.quiver(np.reshape(lon_vel,np.size(lon_vel))[idg],np.reshape(lat_vel,np.size(lat_vel))[idg],np.reshape(u,np.size(u))[idg],np.reshape(v,np.size(v))[idg],angles='xy',scale=1,color='black')
    plt.title(str(num2date(datetime_wanted).strftime("%d-%b-%Y %H"))+'h')
    pylab.ylim([lat_min+0.01,lat_max-0.01])
    pylab.xlim([lon_min+0.01,lon_max-0.01])
    p=plt.quiverkey(q,min(lon_vel[0])+.1,max(lat_vel[0])-.1,1.2,str(round(1.2,2))+"m/s",coordinates='data',color='r')     
    bathy=True
    region='wv'
    basemap_region(region)
    #plt.savefig('/net/home3/ocn/jmanning/py/huanxin/work/hx/'+str(datetime_wanted)+ '.png')
    plt.savefig(str('%03d' % png_num) + '.png')
    png_num=png_num+1 # for next loop 
    datetime_wanted=date2num(num2date(datetime_wanted)+interval_dtime) # add interval_dtime for another forloop
    plt.show()
    #plt.close()


