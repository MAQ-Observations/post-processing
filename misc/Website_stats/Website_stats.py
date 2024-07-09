#Load modules
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from Website_stats_functions import *

#Set directories
stats_path = 'W:\\ESG\\DOW_MAQ\\MAQ_Archive\\MAQ-Observations.nl\\Admin\\FormsExports\\'
figures_path = 'W:\\ESG\\DOW_MAQ\\MAQ_Archive\\MAQ-Observations.nl\\Admin\\GitHub\\misc\\Website_stats\\Figures\\'

#Switch to save figures
savefig = True
figdate = '2024-06-27'

#Load .csv files in dataframe
#Note that these .csv files are not provided due to privacy reasons. We can not make them available.
user_reg_file = 'user-registration-user-update-2024-06-27.csv'
oper_data_file = 'operational-data-2024-06-27.csv'
data_figs_file = 'data-figures-2024-06-27.csv'
data_down_file = 'data-downloads-2024-06-27.csv'

user_reg = pd.read_csv(stats_path+user_reg_file)
oper_data = pd.read_csv(stats_path+oper_data_file)
data_figs = pd.read_csv(stats_path+data_figs_file)
data_down = pd.read_csv(stats_path+data_down_file)
data_down = data_down[data_down['input_radio'].isin(['Basic','Advanced','Single'])]


#Everything related to data figures and User registrations first
#Entries over time different forms
#entries_over_time(user_reg,False,'API Users',figures_path,figdate+'_user_registration_over_time',savefig)
#entries_over_time(oper_data,True,'Operational Data Views',figures_path,figdate+'_operational_data_over_time',savefig)
#entries_over_time(data_figs,True,'Historical Data Views',figures_path,figdate+'_data_figures_over_time',savefig)

#Historical graphs specific streams
#historical_graphs_streams(data_figs,figures_path,figdate+'_historical_streams',savefig)


#Now everything related to data downloads
#entries_over_time_downloads(data_down,True,'Data Downloads',figures_path,figdate+'_data_downloads',savefig)
specifics_per_input_radio(data_down,'Data Downloads',figures_path,figdate+'_data_downloads',savefig)
#For Single/Advanced/Basic: Pie charts for downloaded streams

#fun_statistics()
#Unique users/email-adresses
#@wur vs @non-wur email
#Total years of data downloaded (unique downloads * date_range)
#Number of data points downloaded (check stream interval?!)
#Favorite browser
#Favorate OS

#ApiKey out of functions to here
