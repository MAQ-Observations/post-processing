#Load modules

import datetime as dt
from fetch_data import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
import matplotlib.dates as dates
pd.plotting.register_matplotlib_converters()
import os
import matplotlib.image as image

#User defined input, specify your wishes below

#Default yesterday figure
start_date = dt.datetime.now() - dt.timedelta(1)
end_date = dt.datetime.now()
#Otherwise, define your start date and end date here
#start_date = dt.datetime(2025,3,1)           #Start date (yyyy,mm,dd)
#end_date = dt.datetime(2025,3,2)            #End date (yyyy,mm,dd)
site = 1                                     #Site 1=Veenkampen, 2=Loobos, 3=Amsterdam
variables = ['TA_1_1_2','RH_1_1_1','TA_1_2_1']                                 
API_KEY = '<ApiKey>'                              #Put you API key here as a string, see https://maq-observations.nl/api/
save_filename = 'temp_file.csv'    #You can define the name of the file you want to save your data to

#Run the request:
fetch_data(start_date,end_date,site,variables,API_KEY,True,save_filename)

df = pd.read_csv('temp_file.csv',index_col=0,skiprows=[1])
df.index = pd.to_datetime(df.index)
print(df)
os.remove('temp_file.csv')

#Do the calculations
wetbulb = df['TA_1_1_2'].values * np.arctan(0.151977 * (df['RH_1_1_1'].values + 8.3133659) ** 0.5) \
            + np.arctan(df['TA_1_1_2'].values + df['RH_1_1_1'].values) - np.arctan(df['RH_1_1_1'].values - 1.676331) \
            + 0.0039838 * df['RH_1_1_1'].values ** 1.5 * np.arctan(0.023101 * df['RH_1_1_1'].values) - 4.686035
dewpoint = (df['RH_1_1_1'] / 100.) ** (1./8.) * (112. + 0.9 * df['TA_1_1_2']) + 0.1 * df['TA_1_1_2'] - 112.

#Figure settings
fs_title = 22
fs_labels = 19
fs_ticks = 15
fs_text = 12
fs_legend = 12
fig_dpi = 80
xlim = df.index[0] - pd.Timedelta(minutes=1)
logo = image.imread('WUR_logo.png')
xaxis_ticks = ['{:02d}'.format(jj) for jj in df.index.hour[::60]]
date_text = df.index[-1].day_name() + '    ' + df.index[-1].strftime('%d-%m-%Y')
tmin = df['TA_1_1_2'].min()
tmax = df['TA_1_1_2'].max()
tmean_last10min = df['TA_1_1_2'][-11:].mean()
if np.isnan(tmin) or np.isnan(tmax):
    textminmax = '$T_{min}$ and $T_{max}$ over last 24 hours: -'
else:
    textminmax = '$T_{min}$ and $T_{max}$ over last 24 hours: %.1f °C and %.1f °C' % (tmin, tmax)
if np.isnan(tmean_last10min):
    textmean = '$T_{mean}$ over last 10 minutes: -'
else:
    textmean = '$T_{mean}$ over last 10 minutes: %.1f °C' % tmean_last10min


#Plot the figure
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(df.index.values, df['TA_1_1_2'].values, color='goldenrod', label='Dry bulb(+150 cm)', linewidth=2)
ax.plot(df.index.values, wetbulb, color='darkturquoise', label='Wet bulb(+150 cm, computed)', linewidth=2)
ax.plot(df.index.values, df['TA_1_2_1'].values, color='deeppink', label='Shielded(+10 cm)', linewidth=2)
ax.plot(df.index.values, dewpoint.values, color='darkblue', label='Dew point(+150 cm, computed)', linewidth=2)
plt.legend(loc='upper right', bbox_to_anchor=(1.39, 1), fontsize=fs_legend)
plt.ylabel('Temperature [°C]', fontsize=fs_labels)
plt.xlabel('Time [UTC]', fontsize=fs_labels)
plt.title('Temperature', fontsize=fs_title, pad=45)
plt.grid(color='gainsboro', linestyle='--', which='both')
ax.xaxis.set_minor_locator(dates.HourLocator(interval=1))
ax.xaxis.set_minor_formatter(dates.DateFormatter('%H'))
ax.xaxis.set_major_locator(dates.DayLocator(interval=1))
ax.xaxis.set_major_formatter(dates.DateFormatter('\n %d %b %Y'))
ax.set_xlim([xlim, df.index[-1]])
for item in (ax.get_xticklabels(which='both') + ax.get_yticklabels()):
    item.set_fontsize(fs_ticks)
plt.text(0.8, 1.05, date_text, transform=ax.transAxes, fontsize=fs_text)
plt.text(0.26, 1.065, textminmax, transform=ax.transAxes, fontsize=fs_text)
plt.text(0.35, 1.02, textmean, transform=ax.transAxes, fontsize=fs_text)
imagebox = OffsetImage(logo, zoom=0.5)
ab = AnnotationBbox(imagebox, (0.06, 1.12), frameon=False, xycoords=ax.transAxes)
ax.add_artist(ab)
plt.tight_layout(rect=[0, 0.0, 1.05, 1.])    # [left, bottom, right, top]
plt.savefig('Figures/Temp_'+str(start_date.strftime('%Y-%m-%d'))+'.png', dpi=fig_dpi)
plt.close()


