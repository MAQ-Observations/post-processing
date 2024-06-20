# ADMIN DEFINED INPUT AND CODE
# We recommend to not change the code below. However, you can tailor the code below to change the output structure if you want.

import pandas as pd
import requests

def fetch_data(start_date,end_date,site,variables,API_KEY,save_file,save_filename):
    HOST_KL = 'https://maq-observations.nl'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'ApiKey {}'.format(API_KEY),
        'Content-Type': 'application/json'
    }
    
    # Format the dates as strings
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    # Define the endpoint to fetch metadata (streams)
    END_POINT_METADATA = f'/wp-json/maq/v1/sites/{site}/stations/1/streams'
    
    # Make the GET request to fetch metadata (streams)
    response_metadata = requests.get(HOST_KL + END_POINT_METADATA, headers=headers)
    
    # Check if the request was successful
    if response_metadata.status_code == 200:
        data_metadata = response_metadata.json()
        
        # Convert the metadata to a DataFrame
        df_metadata = pd.DataFrame(data_metadata['streams'])
        
        # Filter the DataFrame for the specified variables
        df_filtered = df_metadata[df_metadata['name'].isin(variables)]
    
        # Prepare to collect units information
        units_info = {}

        # Loop through each variable and fetch its units information
        for _, row in df_filtered.iterrows():
            variable_name = row['name']
            unit_name = row['unit']['name'] if 'unit' in row and 'name' in row['unit'] else ''
            unit_description = row['unit']['description'] if 'unit' in row and 'description' in row['unit'] else ''
            
            # Store units information in a dictionary for later use
            units_info[variable_name] = unit_name if unit_name else unit_description
    
        # Proceed to fetch time-series data only if there are variables to fetch
        if units_info:
            # Prepare to collect time-series data
            all_data = []
    
            # Loop through each variable and fetch its time-series data
            for variable_name in variables:
                stream_id = df_filtered.loc[df_filtered['name'] == variable_name, 'id'].iloc[0]
            
                # Construct the URL for time-series data for this stream
                data_url = f"{HOST_KL}/wp-json/maq/v1/streams/{stream_id}/measures?from={start_date_str}&to={end_date_str}"
                
                print('Processing variable ' + variable_name + " at " + data_url)
            
                # Fetch the time-series data
                data_response = requests.get(data_url, headers=headers)

                if data_response.status_code == 200:
                    data_content = data_response.json()

                    # Convert the time-series data to a DataFrame
                    if 'measures' in data_content and data_content['measures']:
                        time_series_df = pd.DataFrame(data_content['measures'])
                        time_series_df['variable'] = variable_name
                        all_data.append(time_series_df)
                else:
                    print(f"Failed to retrieve data for variable {variable_name}. HTTP Status code: {data_response.status_code}")

            if all_data:
                # Concatenate all data into a single DataFrame
                final_df = pd.concat(all_data, ignore_index=True)

                # Pivot the DataFrame to the desired format
                final_df_pivoted = final_df.pivot(index='timestamp', columns='variable', values='value')

                # Reset index to make timestamp a column instead of index
                final_df_pivoted = final_df_pivoted.reset_index()

                # Rename the 'timestamp' column to 'Timestamp'
                final_df_pivoted = final_df_pivoted.rename(columns={'timestamp': 'Timestamp'})

                # Convert 'Timestamp' column to datetime format and format the timestamp
                final_df_pivoted['Timestamp'] = pd.to_datetime(final_df_pivoted['Timestamp'], utc=True)
                final_df_pivoted['Timestamp'] = final_df_pivoted['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

                # Insert units as the second row
                units_row = ['YYYY-MM-DD HH:MM:SS UTC'] + [units_info[var] for var in final_df_pivoted.columns[1:]]
                final_df_pivoted.loc[0] = units_row
                
                # Print a sample of the data
                print("Sample of the data:")
                print(final_df_pivoted.head())

                if save_file == True:   
                    # Save the final DataFrame to a CSV file
                    final_df_pivoted.to_csv(save_filename, index=False)
                    print("Data successfully saved to "+str(save_filename))
                    
                if save_file == False:
                    return final_df_pivoted
                   
            else:
                print("No data was retrieved for the specified variables and date range.")
        else:
            print("No units information available for the specified variables.")
    else:
        print(f"Failed to retrieve metadata. HTTP Status code: {response_metadata.status_code}")
