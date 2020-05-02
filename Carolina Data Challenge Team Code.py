# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 10:29:25 2019

@author: Ishaan
"""

#imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
#import dataset
driver_passenger = pd.read_csv('https://query.data.world/s/6e4vmnnkn3tbd3yczg5l6cf7ll45uj', sep = ";")
purpose_of_traffic_stop = pd.read_csv('https://query.data.world/s/huflzupya4lvj3pu7uvvjefeggftyw', sep = ';')
arrest_reports = pd.read_csv('https://query.data.world/s/psvcfjwpetg5copuvevxax5t7sckqr',sep=';')
police_demographics = pd.read_csv('https://query.data.world/s/nfxih6m5zbrgvwerxbi367w5txvynb', sep = ';')
incident_reports = pd.read_csv('https://query.data.world/s/r3ywmykzlqdwgxdxbins3rmwldcznp',sep=';')
public_safety = pd.read_csv('https://query.data.world/s/jbowoiscsvuagaiy7rymsqj5k2gp27', sep = ';')



incident_reports = incident_reports.dropna(how = 'all',inplace=False)


#FIX ADDRESS DATA TO MATCH INCIDENT_REPORTS

pd.options.mode.chained_assignment = None
count = 0
for item in arrest_reports['Address']:
    arrest_reports['Address'][count] = item.split(' CHAPEL HILL NC')[0]
    
    count += 1


#print(arrest_reports['Address'])

incident_reports.columns = ['Agency', 'Offense', 'Address', 'City', 'State', 'Forcible',
       'Incident ID', 'Zipcode', 'Date of Report', 'Date of Occurrence',
       'Date Found', 'Reported As', 'Premise Description',
       'Weapon Description', 'Victim Age', 'Victim Race', 'Victim Gender',
       'latitude_longitude']

time = ['Part Time','Full Time']

count = 0

for status in police_demographics['Status']:
    
    level = [i for i in range(len(time)) if status == time[i]]
            
    try:
            police_demographics['Status'][count] = int(level[0])
    except:
            police_demographics['Status'][count] = np.NaN
            
    
    
    
    count += 1


#plt.scatter(police_demographics['Service Years'],police_demographics['Status'])
lat = []
lon = []
for row in  incident_reports['latitude_longitude']:
    
    try:
        
        line = row.split(',')
        print("Line 0",line[0])
        print("Line 1",line[1])
        lat.append(line[0])
        lon.append(line[1])
        
        
    except Exception as e:
        print(str(e))
        lat.append(np.NaN)
        lon.append(np.NaN)
    
incident_reports['Latitude'] = lat
incident_reports['Longitude'] = lon


incident_reports.to_csv('incident_latlong.csv')




driver_passenger.groupby(['Gender','year','Type']).mean()[['White', 'Black', 'Native American', 'Asian', 'Other']]

test = arrest_reports.groupby("Arrestee's Race")["Arrestee's Race"].count()

test = test.sort_values(ascending = False)
plt.figure()
test.plot(kind = 'bar', title = 'Count of Arrests by race')

incident_reports.dropna(how = 'all', inplace = False)

incident_and_arrest = pd.merge(arrest_reports, incident_reports, how='outer')

incident_and_arrest.sort_values('Address', inplace = True)

incident_reports.rename(columns = {'Street':'Address'}, inplace = True)


police_demographics.shape


police_demographics.columns = ['Ed Number','Job Description','Status','Age','Years of Service',
                               'Gender','Race']

white_men_police = police_demographics[(police_demographics["Status"]=='Full Time') & (police_demographics["Race"]=='W') & (police_demographics["Gender"]=='M') & (police_demographics["Age"] < 40)].shape[0]

old_white_men_police = police_demographics[(police_demographics["Status"]=='Full Time') & (police_demographics["Race"]=='W') & (police_demographics["Gender"]=='M') & (police_demographics["Age"] >= 40)].shape[0]

police_f_and_other = police_demographics[(police_demographics["Status"]=='Full Time') & ((police_demographics["Race"]!='W') | (police_demographics["Gender"]!='M'))].shape[0]

print(police_f_and_other,white_men_police,old_white_men_police)

objects = ('Female and non-White', 'White Male < 40 yo', 'White Male Officers 40+ yo')
y_pos = np.arange(len(objects))
performance = [police_f_and_other,white_men_police,old_white_men_police]

plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Number of Officers')
plt.title('Chapel HIll Police Officers Race/Gender')

plt.show()


print(driver_passenger.head(14))


driver_passenger.groupby(['Gender','year','Type']).mean()[['White', 'Black', 'Native American', 'Asian', 'Other']]

print(purpose_of_traffic_stop.head())

on_view_enforce = enforcement_taken[enforcement_taken['Action'] == 'On-View Arrest']
on_view_enforce = on_view_enforce.groupby('Gender').sum()
del on_view_enforce['Year']

on_view_enforce['Other Races'] = on_view_enforce[['Asian', 'Other', 'Native American']].sum(axis=1)
on_view_enforce

arrest_c_1 = enforcement_taken['Action'] == 'On-View Arrest'
arrest_c_2 = enforcement_taken['Action'] == 'Citation Issued'
arrest_c = arrest_c_1 | arrest_c_2

all_arrest_enforce = enforcement_taken[arrest_c]
all_arrest_enforce = all_arrest_enforce.groupby('Gender').sum()
del all_arrest_enforce['Year']

all_arrest_enforce['Other Races'] = all_arrest_enforce[['Asian', 'Other', 'Native American']].sum(axis=1)

critera1 = enforcement_taken['Action'] == 'Male Total'
criteria2 = enforcement_taken['Action'] == 'Female Total'
criteria_all = critera1 | criteria2

total_enforcement = enforcement_taken[criteria_all]
total_enforcement = total_enforcement.groupby('Gender').sum()
del total_enforcement['Year']

total_enforcement['Other Races'] = total_enforcement[['Asian', 'Other', 'Native American']].sum(axis=1)

on_view_enforce.plot(y = ['White', 'Black', 'Other Races'], kind = 'bar', title = "On View Arrests")
all_arrest_enforce.plot(y = ['White', 'Black', 'Other Races'], kind = 'bar', title = "Arrests/Citations")
total_enforcement.plot(y = ['White', 'Black', 'Other Races'], kind = 'bar', title = 'Cars Pulled Over')
