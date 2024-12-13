#Load modules
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime as dt
import requests
from collections import Counter, defaultdict
import re

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
    df_converted = stream_number_to_variable_name(grouped,'v1')
        
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
    plt.close()


def stream_number_to_variable_name(df,v):    
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
                                    
                df_selected = df_metadata[['id', 'station_id', 'name']]
                
                df_appended = pd.concat([df_appended,df_selected])
    
        df_appended.to_pickle('df_json_metadata_new.pkl')
        
    df.index = df.index.map(str)
    df_appended['id'] = df_appended['id'].astype(str)
    df = df.reset_index()
    
    if v == 'v1':
        df.columns = ['id', 'value']
        merged_df = df.merge(df_appended[['id', 'station_id', 'name']], how='left', left_on='id', right_on='id')
        merged_df['id'] = merged_df['name'].combine_first(merged_df['id'].astype(str))
        df_converted = merged_df.set_index('id')[['station_id','value']]
        df_converted = df_converted.dropna(subset = ['station_id'])
    if v == 'v2':
        df = df['Measurement']
        df = pd.DataFrame({'id': df})
        df['id'] = df['id'].astype(int).astype(str)
        merged_df = pd.merge(df, df_appended, on='id', how='inner')
        merged_df['id'] = merged_df['name'].combine_first(merged_df['id'].astype(str))
        df_converted = merged_df.set_index('id')[['station_id','name']]
        df_converted = df_converted.dropna(subset = ['station_id'])

    return df_converted
    
def stream_number_to_variable_name_single(df):    
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
                                    
                df_selected = df_metadata[['id', 'station_id', 'name']]
                
                df_appended = pd.concat([df_appended,df_selected])
    
        df_appended.to_pickle('df_json_metadata_new.pkl')
        
    df.index = df.index.map(str)
    df_appended['id'] = df_appended['id'].astype(str)    

    df = df.reset_index()
    
    merged_df = pd.merge(df, df_appended, on='id', how='inner')
    merged_df['id'] = merged_df['name'].combine_first(merged_df['id'].astype(str))
    df_converted = merged_df.set_index('id')[['station_id','name']]
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
    pd.set_option('display.max_columns', None)

    basic = df[df['input_radio'].isin(['Basic'])]
    advanced = df[df['input_radio'].isin(['Advanced'])]
    single = df[df['input_radio'].isin(['Single'])]

    
    #PROCESSING FOR BASIC DOWNLOADS
    base_patterns = [
        'Temperature', 'Relative humidity', 'Air pressure', 'Precipitation', 
        'Incoming shortwave radiation', 'Wind speed', 'Wind direction'
    ]
    codes = ['1_1', '2_2', '3_3']

    pattern_counts = defaultdict(int)

    pattern_regex = re.compile(r'(\b(?:Temperature|Relative humidity|Air pressure|Precipitation|Incoming shortwave radiation|Wind speed|Wind direction)\b):\s*((?:\d_\d\|\d+)(?:,\s*\d_\d\|\d+)*)')

    for index, row in basic.iterrows():
        tabular_grid = str(row['tabular_grid'])
                
        matches = pattern_regex.findall(tabular_grid)
              
        for match in matches:
            pattern_name = match[0]
            pattern_code_values = match[1].replace(' ', '').split(',')
            for pattern_code_value in pattern_code_values:
                code_value_parts = pattern_code_value.split('|')
                code = code_value_parts[0].strip()
                value = code_value_parts[1].strip()
                pattern_counts[f'{pattern_name}: {code}'] += 1
                    
    patterns_order = ['1_1', '2_2', '3_3']

    def custom_sort_key(item):
        key, value = item
        pattern = key.split(': ')[1]
        pattern_index = patterns_order.index(pattern) if pattern in patterns_order else len(patterns_order)
        return (pattern_index, -value)
    
    sorted_items = sorted(pattern_counts.items(), key=custom_sort_key)    
        
    labels = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]

    colors = ['#08306b', '#08519c', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef',
                '#7f2704', '#a63603', '#d94801', '#f16913', '#fd8d3c', '#fdae6b', '#fdd0a2',
                '#00441b', '#006d2c', '#238b45', '#41ab5d', '#74c476', '#a1d99b']

    hatches = ['+', 'o', '|', '-', '/', '\\', '*',
                '+', 'x', 'o', '|', '-', '/', '\\',
                '*', 'o', '|', '-', '+', '/']
                
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(counts, labels=labels, colors=colors, autopct='%1.1f%%', 
                                      wedgeprops={'linewidth': 1, 'edgecolor': 'black'},
                                      textprops={'fontsize': 12}, pctdistance=0.85, labeldistance=1.1)
    for wedge, hatch in zip(wedges, hatches):
        wedge.set_hatch(hatch)
    for autotext in autotexts:
        autotext.set_color('white')
    ax.set_aspect('equal')
    ax.set_title('Basic download percentages', fontsize=16)
    plt.tight_layout()
    if savefig == True:
        plt.savefig(saveloc+savename+'_pie_basic.png',dpi=300)
    plt.show()
    plt.close()
            
    #PROCESSING FOR ADVANCED DOWNLOADS
    patterns = ['Meteorology: 1_1', 'Meteorology: 2_2', 'Meteorology: 3_3',
                'Air Quality: 1_1', 'Air Quality: 2_2', 'Air Quality: 3_3',
                'Fluxes: 1_1', 'Fluxes: 2_2', 'Fluxes: 3_3',
                'Soil: 1_1', 'Soil: 2_2', 'Soil: 3_3',
                'Leaf Wetness: 1_1', 'Leaf Wetness: 2_2', 'Leaf Wetness: 3_3']

    pattern_counts = defaultdict(int)
    advanced = advanced[advanced['tabular_grid.1'].notnull()]

    for index, row in advanced.iterrows():
        parts = row['tabular_grid.1'].split('|')
        
        for part in parts:
            matches = [pattern for pattern in patterns if pattern in part]
            
            for match in matches:
                pattern_counts[match] += 1
    
    patterns_order = ['1_1', '2_2', '3_3']

    sorted_items = sorted(pattern_counts.items(), key=custom_sort_key)
    
        
    labels = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]

    colors = [
        '#08306b', '#08519c', '#2171b5', '#4292c6',
        '#7f2704', '#a63603', '#d94801', '#f16913', '#fd8d3c',
        '#00441b', '#006d2c']

    hatches = ['+', 'o', '|', '-', '+', '/', '-',
                '|', 'o', '-', '+']
                
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(counts, labels=labels, colors=colors, autopct='%1.1f%%', 
                                      wedgeprops={'linewidth': 1, 'edgecolor': 'black'},
                                      textprops={'fontsize': 12}, pctdistance=0.85, labeldistance=1.1)
    for wedge, hatch in zip(wedges, hatches):
        wedge.set_hatch(hatch)
    for autotext in autotexts:
        autotext.set_color('white')
    ax.set_aspect('equal')
    ax.set_title('Advanced download percentages', fontsize=16)
    plt.tight_layout()
    if savefig == True:
        plt.savefig(saveloc+savename+'_pie_advanced.png',dpi=300)
    plt.show()
    plt.close()

    #PROCESSING FOR SINGLE DOWNLOADS
    df_converted = stream_number_to_variable_name(single,'v2')
    
    counts = df_converted.value_counts().reset_index(name='count').sort_values(by='count', ascending=True).reset_index()
    
    colors = {1.0: '#1f77b4', 2.0: '#ff7f0e', 3.0: '#2ca02c'}
    bar_colors = counts['station_id'].map(colors)
       
    plt.figure(figsize=(10, 6))
    plt.bar(counts.index, counts['count'], color=bar_colors, zorder=3)
    plt.xlabel('Stream')
    plt.ylabel('Count')
    plt.title('Histogram of Single Download Stream by Count')
    plt.xticks(counts.index, counts['name'], rotation=45, ha='right')
    plt.grid(True, zorder=1)
    patch1 = mpatches.Patch(color='#1f77b4', label='Veenkampen')
    patch2 = mpatches.Patch(color='#ff7f0e', label='Loobos')
    patch3 = mpatches.Patch(color='#2ca02c', label='Amsterdam')
    plt.legend(handles=[patch1, patch2, patch3], loc='best')
    plt.tight_layout()
    if savefig == True:
        plt.savefig(saveloc+savename+'_bar_single.png',dpi=300)
    plt.show()
    plt.close()
    
def fun_statistics(df,title,saveloc,savename,savefig):
    unique_emails = df['Email'].unique()
    string_list = [str(element) for element in unique_emails]
    
    total_count = len(string_list)
    wurnl_count = sum(s.count('@wur.nl') for s in string_list)
    non_wur_nl_count = total_count - wurnl_count
    
    unique_browser = df['Submitter Browser'].unique()
    unique_os = df['Submitter Device'].unique()
    
    counter_browser = Counter(df['Submitter Browser'])
    counter_os = Counter(df['Submitter Device'])
    
    counts_browser = []
    counts_os = []
    
    for target in unique_browser:
        counts_browser.append(counter_browser[target])
        
    for target in unique_os:
        counts_os.append(counter_os[target])
    
    df_date = pd.DataFrame()
    df_date['Date Range'] = df['Date range'].combine_first(df['Date range.1'])
    
    def count_days(date_range):
        dates = date_range.split(' to ')
        start_date = dt.datetime.strptime(dates[0], '%Y-%m-%d')
        end_date = dt.datetime.strptime(dates[-1], '%Y-%m-%d')
        days_diff = (end_date - start_date).days + 1
        if days_diff > 5000:
            days_diff = 5000
        return days_diff

    total_years = round(df_date['Date Range'].apply(count_days).sum()/365,1)  
        
    plt.rcParams["font.family"] = "Palatino Linotype"

    fig, ax = plt.subplots()
    ax.set_title('Extra statistics Data Downloads', fontsize=16, pad=20, weight='bold')
    lines_of_text = [
        "Total downloads (non-API):",
        "          "+str(len(df)),
        "Unique user (email) downloads:",
        "          "+str(total_count),
        "@wur.nl / non-@wur.nl unique user downloads:",
        "          "+str(wurnl_count)+" / "+str(non_wur_nl_count),
        "Total years of data downloaded: ",
        "          "+str(total_years),
        "Favorite browsers:",
        "          "+str(unique_browser[0])+" "+str(counts_browser[0])+" | "+str(unique_browser[1])+" "+str(counts_browser[1])+" | "+str(unique_browser[2])+" "+str(counts_browser[2])+" | "+str(unique_browser[3])+" "+str(counts_browser[3])+" | "+str(unique_browser[4])+" "+str(counts_browser[4]),
        "Favorite OS:",
        "          "+str(unique_os[0])+" "+str(counts_os[0])+" | "+str(unique_os[1])+" "+str(counts_os[1])+" | "+str(unique_os[2])+" "+str(counts_os[2])+" | "+str(unique_os[3])+" "+str(counts_os[3])+" | "+str(unique_os[4])+" "+str(counts_os[4]),
    ]
    y_position = 0.95
    for line in lines_of_text:
        ax.text(0.1, y_position, line, fontsize=12, verticalalignment='top')
        y_position -= 0.1 
    ax.axis('off')
    plt.tight_layout()
    if savefig == True:
        plt.savefig(saveloc+savename+'_extra_text.png',dpi=300)
    plt.show()
    plt.close()
