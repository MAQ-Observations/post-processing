#Load modules

import datetime as dt
from generate_graphs import *

#User defined input, specify your wishes below

start_date = dt.datetime(2024,1,1)           #Start date (yyyy,mm,dd)
end_date = dt.datetime(2024,1,31)            #End date (yyyy,mm,dd)
site = 1                                     #Site 1=Veenkampen, 2=Loobos, 3=Amsterdam
variables = ['TA_2_1_1',                     #Array of variables to download, see https://maq-observations.nl/instruments/ for a full list, use the 'Steam names', column 1
             'TA_1_1_1',
             'RH_1_1_1',
             'SW_IN_1_1_1',
             'SW_OUT_1_1_1',
             'LW_IN_1_1_1',
             'LW_OUT_1_1_1',
             'VIS_1_1_1',
             'WS_1_1_1',
             'WD_1_1_1',
             'P_1_1_1']                                 
API_KEY = '<ApiKey>'  #Put you API key here as a string, see https://maq-observations.nl/api/
save_filename = 
save_files = True                                 #True/False switch to save the generated figures


#Run the request

fetch_data(start_date,end_date,site,variables,API_KEY,save_filename)
generate_graphs(start_date,end_date,site,variables,API_KEY,save_files)