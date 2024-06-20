# ADMIN DEFINED INPUT AND CODE
# We recommend to not change the code below. However, you can tailor the code below to change the output structure if you want.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import requests

def generate_graphs(save_files,df):
    datetime_array = pd.to_datetime(df['Timestamp'][1:].values)
    datetime_array_np = datetime_array.to_numpy()
    
    # Loop over columns and plot each one
    for column in df.columns[1:]:
        plt.figure(figsize=(15,7))
        plt.plot(datetime_array_np, df[column][1:].values, label=column)
        plt.xlim([datetime_array_np[0],datetime_array_np[-1]])
        plt.xlabel('Timestamp')
        plt.ylabel(column+' ['+df[column][0]+']')
        plt.legend(loc='best')
        plt.xticks(rotation=45, ha='right')
        plt.savefig('Figures/'+column+'.png',dpi=300)
        plt.close()
