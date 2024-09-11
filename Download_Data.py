#Load modules

import datetime as dt
from fetch_data import *

#User defined input, specify your wishes below

start_date = dt.datetime(2024,1,1)           #Start date (yyyy,mm,dd)
end_date = dt.datetime(2024,1,31)            #End date (yyyy,mm,dd)
site = 2                                     #Site 1=Veenkampen, 2=Loobos, 3=Amsterdam
variables = ['P_1_1_1','LE','SWC_1_1_1']                                 
API_KEY = '<ApiKey>'                              #Put you API key here as a string, see https://maq-observations.nl/api/
save_filename = 'MAQ-Observations_request.csv'    #You can define the name of the file you want to save your data to


#Run the request:

fetch_data(start_date,end_date,site,variables,API_KEY,True,save_filename)
