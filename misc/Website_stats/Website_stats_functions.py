#Load modules
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime as dt
import requests

def entries_over_time(df,groupby,title,saveloc,savename,savefig):
    df['Submission Create Date'] = pd.to_datetime(df['Submission Create Date'])
    df.set_index('Submission Create Date', inplace=True)

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
        
    monthly_df = user_counts.resample('M').sum()
#    plt.figure(figsize=(12, 6))
    monthly_df.plot(kind='bar', width=0.8)
    plt.title('Number of '+title+' per month')
    plt.xlabel('Month')
    plt.ylabel('Number of entries')
    plt.xticks(rotation=45,ha='right')
    plt.gca().set_xticklabels([date.strftime('%b %Y') for date in monthly_df.index])
    plt.legend(loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    if savefig == True:
        plt.savefig(saveloc+savename+'_bar.png',dpi=300)
    plt.close()
    
    return

def historical_graphs_streams(df,saveloc,savename,savefig):
    grouped = df.groupby('Measurement').size().sort_values().tail(60)
    df_converted = stream_number_to_variable_name(grouped)
        
    colors = {1.0: '#1f77b4', 2.0: '#ff7f0e', 3.0: '#2ca02c'}
    bar_colors = df_converted['station_id'].map(colors)
   
    plt.figure(figsize=(10, 6))
    df_converted['value'].plot(kind='bar', color=bar_colors, zorder=3)
    plt.xlabel('Stream')
    plt.ylabel('Count')
    plt.title('Histogram of Historical Data Stream Charts by Count')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True,zorder=1)
    handles, labels = plt.gca().get_legend_handles_labels()
    patch1 = mpatches.Patch(color='#1f77b4', label='Veenkampen')   
    patch2 = mpatches.Patch(color='#ff7f0e', label='Loobos')   
    patch3 = mpatches.Patch(color='#2ca02c', label='Amsterdam')   
    plt.legend(loc='best',handles=[patch1,patch2,patch3])
    plt.tight_layout()
    if savefig == True:
        plt.savefig(saveloc+savename+'_bar.png',dpi=300)
    plt.show()


def stream_number_to_variable_name(df):    
    df_appended = pd.DataFrame()
    
    load_from_pkl = True
    
    if load_from_pkl == True:
        df_appended = pd.read_pickle('df_json_metadata.pkl')
    
    if load_from_pkl == False:
        API_KEY = '<ApiKey>'        #Put ApiKey here

        HOST_KL = 'https://maq-observations.nl'
        headers = {
            'Accept': 'application/json',
            'Authorization': 'ApiKey {}'.format(API_KEY),
            'Content-Type': 'application/json'
        }

        for site in [1,2,3]:
            # Define the endpoint to fetch metadata (streams)
            END_POINT_METADATA = f'/wp-json/maq/v1/sites/{site}/stations/{site}/streams'
            
            # Make the GET request to fetch metadata (streams)
            response_metadata = requests.get(HOST_KL + END_POINT_METADATA, headers=headers)
            print(response_metadata)
            
            # Check if the request was successful
            if response_metadata.status_code == 200:
                data_metadata = response_metadata.json()
                
                # Convert the metadata to a DataFrame
                df_metadata = pd.DataFrame(data_metadata['streams'])
                    
                #print(df_metadata)
                #print(df_metadata.columns)
                
                df_selected = df_metadata[['id', 'station_id', 'name']]
                
                df_appended = pd.concat([df_appended,df_selected])
    
    df_appended.to_pickle('df_json_metadata.pkl')
        
    df.index = df.index.map(str)
    df_appended['id'] = df_appended['id'].astype(str)

    df = df.reset_index()
    df.columns = ['id', 'value']
    merged_df = df.merge(df_appended[['id', 'station_id', 'name']], how='left', left_on='id', right_on='id')
    merged_df['id'] = merged_df['name'].combine_first(merged_df['id'].astype(str))
    df_converted = merged_df.set_index('id')[['station_id','value']]
    df_converted = df_converted.dropna(subset = ['station_id'])
    
    return df_converted
    
    
    
    
def entries_over_time_downloads(df,groupby,title,saveloc,savename,savefig):
    df['Submission Create Date'] = pd.to_datetime(df['Submission Create Date'])
    df.set_index('Submission Create Date', inplace=True)
    
    colors = ['tab:red', 'tab:purple', 'tab:brown']

    if groupby == True:
        user_counts = df.fillna(0).groupby('input_radio').resample('D').size().unstack(level=0)
    if groupby == False:
        user_counts = df.resample('D').size()
    cumulative_user_counts = user_counts.fillna(0).cumsum(skipna=True)
        
    # Plot the number of submissions over time
    plt.figure(figsize=(10, 6))
    if groupby == True:
        i=0
        for site_selection in cumulative_user_counts.columns:
            cumulative_user_counts[site_selection].plot(label=site_selection, linestyle=':', linewidth=2, color=colors[i])
            i=i+1
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
        
    monthly_df = user_counts.resample('M').sum()
#    plt.figure(figsize=(12, 6))
    monthly_df.plot(kind='bar', width=0.8, color=colors)
    plt.title('Number of '+title+' per month')
    plt.xlabel('Month')
    plt.ylabel('Number of entries')
    plt.xticks(rotation=45,ha='right')
    plt.gca().set_xticklabels([date.strftime('%b %Y') for date in monthly_df.index])
    plt.legend(loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    if savefig == True:
        plt.savefig(saveloc+savename+'_bar.png',dpi=300)
    plt.close()
    
    return



def specifics_per_input_radio(df,title,saveloc,savename,savefig):
    basic = df[df['input_radio'].isin(['Basic'])]
    advanced = df[df['input_radio'].isin(['Advanced'])]
    single = df[df['input_radio'].isin(['Single'])]

    print(basic)