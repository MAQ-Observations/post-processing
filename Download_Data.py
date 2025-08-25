#Load modules
import datetime as dt
from fetch_data import *

#User defined input, specify your wishes below
start_date = dt.datetime(2025,06,01)           			#Start date (yyyy,mm,dd)
end_date = dt.datetime(2025,06,08)            			#End date (yyyy,mm,dd)
site = 1                                     			#Site 1=Veenkampen, 2=Loobos, 3=Amsterdam
variables = ['TA_1_1_1','RH_1_1_1','WS_1_1_1']                                 
API_KEY = '<ApiKey>'        							#Put you API key here as a string, see https://maq-observations.nl/api/
save_filename = 'MAQ-Observations_request.csv'    		#You can define the name of the file you want to save your data to

#Run the request:
fetch_data(start_date,end_date,site,variables,API_KEY,True,save_filename)
