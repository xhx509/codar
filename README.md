Codar
=====

This program gets ocean codar data from http://tds.marine.rutgers.edu:8080/thredds/catalog.html . 

Some processes combined with drifter data.

User should cheak or modify control file 'getcodar_bydrifter_ctl.txt' or 'getcodar_byrange_ctl.txt' before 
running the process.

A picture would be generated after you running a process.


getcodar_drifter.py  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;      plot raw drifter and codar data in a picture

getcodar.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;      plot codar data

getsst_codar_drifter.py  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     plot raw drifter, codar and observed sst in a picture

getsst_codar.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;      plot observed sst and codar in a picture

gettrack_codar.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;      according codar data , estimate a drifter track
