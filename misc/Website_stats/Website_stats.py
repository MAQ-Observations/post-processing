#Load modules
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from Website_stats_functions import *

#Set directories
#Path where stats files (.csv) are located
stats_path = 'W:\\ESG\\DOW_MAQ\\MAQ_Archive\\MAQ-Observations.nl\\Admin\\FormsExports\\'
#Path where figures (.png) are saved
figures_path = 'W:\\ESG\\DOW_MAQ\\MAQ_Archive\\MAQ-Observations.nl\\Admin\\GitHub\\misc\\Website_stats\\Figures\\'

#Switch to save figures, and date to include in the figure title
savefig = True
figdate = '2024-07-12'

#Load .csv files in dataframe
#Note that these .csv files are not provided due to privacy reasons. We can not make them available.
user_reg_file = 'user-registration-user-update-2024-07-12.csv'
oper_data_file = 'operational-data-2024-07-12.csv'
data_figs_file = 'data-figures-2024-07-12.csv'
data_down_file = 'data-downloads-2024-07-12.csv'

user_reg = pd.read_csv(stats_path+user_reg_file)
oper_data = pd.read_csv(stats_path+oper_data_file)
data_figs = pd.read_csv(stats_path+data_figs_file)
data_down = pd.read_csv(stats_path+data_down_file)
data_down = data_down[data_down['input_radio'].isin(['Basic','Advanced','Single'])] #Only select data downloaded throuh Basic, Advanced and Single
data_down_copy = data_down.copy()
data_down_copy2 = data_down.copy()

#Everything related to Data Figures and User registrations first
#Entries over time different forms
entries_over_time(user_reg,False,'API Users',figures_path,figdate+'_user_registration_over_time',savefig)
entries_over_time(oper_data,True,'Operational Data Views',figures_path,figdate+'_operational_data_over_time',savefig)
entries_over_time(data_figs,True,'Historical Data Views',figures_path,figdate+'_data_figures_over_time',savefig)
#Historical graphs counts for specific streams
historical_graphs_streams(data_figs,figures_path,figdate+'_historical_streams',savefig)


#Now everything related to data downloads
entries_over_time_downloads(data_down,True,'Data Downloads',figures_path,figdate+'_data_downloads',savefig)
specifics_per_input_radio(data_down_copy,'Data Downloads',figures_path,figdate+'_data_downloads',savefig)
fun_statistics(data_down_copy2,'Data Downloads',figures_path,figdate+'_data_downloads',savefig)
