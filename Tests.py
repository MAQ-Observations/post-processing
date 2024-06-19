#Load modules

import requests

#Define end point

API_KEY = '<ApiKey>'
HOST_KL = 'https://maq-observations.nl'
headers = {'Accept': 'application/json',
           'Authorization': 'ApiKey {}'.format(API_KEY),
           'Content-Type':'text/csv'}
END_POINT = '/wp-json/maq/v1/sites'
print("url ---->", HOST_KL + END_POINT)

# GET SITES

get = requests.get(HOST_KL + END_POINT, headers=headers)
print(get)
print(get.text)

#GET STATIONS VEENKAMPEN

END_POINT = '/wp-json/maq/v1/sites/1/stations'
get = requests.get(HOST_KL + END_POINT, headers=headers)
print(get)
print(get.text)

#GET STREAMS VEENKAMPEN

END_POINT = '/wp-json/maq/v1/sites/1/stations/1/streams'
get = requests.get(HOST_KL + END_POINT, headers=headers)
print(get)
print(get.text)

#GET DATA TA_2_1_1 VEENKAMPEN 2023-01-01 to 2023-01-02

END_POINT = '/wp-json/maq/v1/streams/48649/measures?from=2023-01-01&to=2023-01-02'
get = requests.get(HOST_KL + END_POINT, headers=headers)
print(get)
print(get.text)
#Alternatively: Use it as a dictionary
a = get.json()
print(a)