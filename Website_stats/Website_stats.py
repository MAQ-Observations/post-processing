#Load modules
import json
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
#data_down = pd.read_csv(stats_path+data_down_file)


#Plot the relevant data
entries_over_time(user_reg,False,'API Users',figures_path,figdate+'_user_registration_over_time',savefig)
entries_over_time(oper_data,True,'Operational Data Views',figures_path,figdate+'_operational_data_over_time',savefig)
entries_over_time(data_figs,True,'Historical Data Views',figures_path,figdate+'_data_figures_over_time',savefig)
  
