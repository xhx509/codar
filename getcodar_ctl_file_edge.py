# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:07:26 2013
this is a control file ,user can import value from here
@author: hxu
"""
from matplotlib.dates import date2num

import datetime as dt

def getcodar_ctl_file_edge_py():
  dtime='2012,8,24,13,0'  #time
  latlon=[41.0,39.0,-71.0,-73.0] #latmax,latmin,lonmax,lonmin
  num_interval=[1,1]  #number, interval hour
  model_option=[5]  #choose one url to get codar
  #1,http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km_fmrc/Macoora_6km_Totals_(FMRC)_best.ncd" 
  #2,http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/sw06" 
  #3,http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km"          
  #4,http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora8km"   
  #5,http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km_clone"
#this one work with getsst_codar,getcodar  

  datetime_wanted=date2num(dt.datetime.strptime(dtime,'%Y,%m,%d,%H,%M')) 
  
  lat_max=float(latlon[0])
  lat_min=float(latlon[1])
  lon_max=float(latlon[2])
  lon_min=float(latlon[3])

  #print num_interval
  num=int(num_interval[0])
  interval=int(num_interval[1])
  interval_dtime=dt.timedelta( 0,interval*60*60 )

  '''
  num_interval=f.readline()
  num_interval=num_interval[0:num_interval.index(']')].strip('[').split(',')
  print num_interval
  num=int(num_interval[0])
  interval=int(num_interval[1])
  interval_dtime=datetime.timedelta( 0,interval*60*60 )
  step_size=int(num_interval[2])
  '''

  model_option=model_option[0]
  
  if model_option=='1':
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km_fmrc/Macoora_6km_Totals_(FMRC)_best.ncd" 
  if model_option=='2':
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/sw06" 
  if model_option=='3':
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km"          
  if model_option=='4':
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora8km"   
  if model_option=='5':
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km_clone"
  if model_option=='6':
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/5Mhz_6km_realtime_fmrc/Maracoos_5MHz_6km_Totals-FMRC_best.ncd"
  return datetime_wanted,url,model_option,lat_max,lon_max,lat_min,lon_min,num,interval_dtime