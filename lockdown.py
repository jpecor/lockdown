""""
MIT License

Copyright (c) 2020 Jason Pecor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
`lockdown.py`
================================================================================
This Python program fetches COVID-19 daily reports from the CDC and does a bit
of data gathering on the numbers. It's really more of an exercise in learning
a bit about Pandas than anything else.

* Author: Jason Pecor

"""


import pandas as pd 
import re

# Month abbreviations, number, date range
months = {"jan":('01', 1,31),
          "feb":('02', 20,28),
          "mar":('03', 1,31),
          "apr":('04', 1,6),
          "may":('05', 1,31),
          "jun":('06', 1,30),
          "jul":('07', 1,31),
          "aug":('08', 1,31),
          "sep":('09', 1,30),
          "oct":('10', 1,31),
          "nov":('11', 1,28),
          "dec":('12', 1,28)
         }

# target_state = 'Wisconsin'
target_state = 'Iowa'
target_months = ['mar','apr']

dfs = {}
wi = {}

for month in target_months:

    first_day = months[month][1]
    last_day = months[month][2]+1  #range() in Python is exlusive, +1 included upper bound

    for day in range(first_day,last_day):

        date = F'{months[month][0]}-{day:02}-2020'

        url = F'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date}.csv'

        dfs[date] = pd.read_csv(url)
        keys = dfs[date].keys().values

        wi = None
        df = dfs[date]

        for key in keys:

            if (key.find('Province_State') >= 0):
                states = df['Province_State']
                for state in states:
                    if (type(state)is str):
                        if (state.find(target_state)>=0):
                            wi = df[df['Province_State']==target_state]

            # Not doing anytyhing with this right now...
            elif (key.find('Province/State') >= 0):
                states = df['Province/State']
                for state in states:
                    if (type(state)is str):
                        if (state.find(target_state)>=0):
                            wi = df[df['Province/State']==target_state]
            
        total_confirmed = 0
        total_deaths = 0

        if (wi is not None):
            for city in range(0,wi['Confirmed'].size):
                confirmed = wi['Confirmed'].values[city]
                deaths = wi['Deaths'].values[city]
                # loc = wi['Admin2'].values[city]

                total_confirmed += confirmed
                total_deaths += deaths

                # print(F'Date: {date} - City: {loc} Confirmed: {confirmed} - Total Confirmed: {total_confirmed}')
                # print(F'Date: - Confirmed: {confirmed} - Total Confirmed: {total_confirmed}')

            print(F'{date}.csv : {target_state} - confirmed: {total_confirmed}  deaths: {total_deaths} ')



    


