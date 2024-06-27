#Load modules
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

def entries_over_time(df,groupby,title,saveloc,savename,savefig):
    # Parse the 'Submission Create Date' as datetime
    df['Submission Create Date'] = pd.to_datetime(df['Submission Create Date'])

    # Set the 'Submission Create Date' as the index
    df.set_index('Submission Create Date', inplace=True)

    # Resample by day and count the number of submissions
    if groupby == True:
        user_counts = df.fillna(0).groupby('Site selection').resample('D').size().unstack(level=0)
        user_counts = user_counts[['1_1', '2_2', '3_3']].rename(columns={'1_1': 'Veenkampen', '2_2': 'Loobos', '3_3': 'Amsterdam'})
    if groupby == False:
        user_counts = df.resample('D').size()
    cumulative_user_counts = user_counts.fillna(0).cumsum(skipna=True)
        
    # Plot the number of submissions over time
    plt.figure(figsize=(10, 6))
    if groupby == True:
        for site_selection in cumulative_user_counts.columns:
            cumulative_user_counts[site_selection].plot(label=site_selection, linestyle=':', linewidth=2)
        cumulative_total = cumulative_user_counts.sum(axis=1)
        cumulative_total.plot(label='Total', linestyle='-', linewidth=3, color='black')
    if groupby == False:
        cumulative_user_counts.plot(label='Total', linestyle='-', linewidth=3, color='black')
    plt.xlim(pd.Timestamp('2023-11-01'), cumulative_user_counts.index[-1])
    plt.title('Number of '+title+' over time')
    plt.xlabel('Date')
    plt.ylabel('Number of entries')
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()
    if savefig == True:
        plt.savefig(saveloc+savename+'.png',dpi=300)
    plt.close()
    
    return

