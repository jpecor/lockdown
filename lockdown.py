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
from bokeh.plotting import figure, output_file, show
from bokeh.models import Legend
import re
import math

# Month abbreviations, number, date range
months = {"jan":('01', 1,31),
          "feb":('02', 20,28),
          "mar":('03', 22,31), 
          "apr":('04', 1,12),
          "may":('05', 1,31),
          "jun":('06', 1,30),
          "jul":('07', 1,31),
          "aug":('08', 1,31),
          "sep":('09', 1,30),
          "oct":('10', 1,31),
          "nov":('11', 1,28),
          "dec":('12', 1,28)
         }

target_states = ['Wisconsin', 'Idaho', 'Iowa']
# target_states = ['Wisconsin']

state_colors = {'Wisconsin':'blue',
                'Idaho':'red',
                'Iowa':'orange'}

# target_state = 'Wisconsin'
# target_state = 'Idaho'
# target_state = 'Iowa'

target_city = 'Eau Claire'

# target_months = ['mar','apr']
target_months = ['apr']

dfs = {}
statefs = {}

total_confirmed = 0
total_state_deaths = 0

plot_dates = []
plot_confirmed = {}

for month in target_months:

    first_day = months[month][1]
    last_day = months[month][2]+1  #range() in Python is exlusive, +1 included upper bound

    for day in range(first_day,last_day):

        state_confirmed = 0
        state_deaths = 0

        date = F'{months[month][0]}-{day:02}-2020'
        print(f'Fetching data for {date}')

        plot_dates.append(date)

        csv = F'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date}.csv'
        # csv = F'../statvilla/covid19/jhdata/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/{date}.csv'

        dfs[date] = pd.read_csv(csv)
        keys = dfs[date].keys().values

        statef = None   # Create a data frame just for a given state
        df = dfs[date]

        for key in keys:
            # Look for a target state
            
            if (key.find('Province_State') >= 0):

                states = df['Province_State']

                for target_state in target_states:

                    total_confirmed = 0
                    total_deaths = 0

                    for state in states:
                        # print(state)
                        if (type(state)is str):
                            if (state.find(target_state)>=0):
                                statefs[target_state] = df[df['Province_State']==target_state]
                                
                    # If a target state was found, grab data from it.
                    state_confirmed = 0
                    state_deaths = 0
                    confirmed_plot_values = []
                    xs = []
                    ys = []
                    
                    if (statefs[target_state] is not None):

                        for city in range(0,statefs[target_state]['Confirmed'].size):
                            
                            state_confirmed += statefs[target_state]['Confirmed'].values[city]
                            state_deaths += statefs[target_state]['Deaths'].values[city]

                        d_confirmed = state_confirmed - total_confirmed
                        total_confirmed = state_confirmed

                        d_state_deaths = state_deaths - total_deaths
                        total_deaths = state_deaths

                        confirmed_plot_values.append(total_confirmed)
                    
                    print(F'{date}.csv : {target_state:10} - confirmed: {state_confirmed:4} change: {d_confirmed:4} | deaths: {state_deaths:4} change: {d_state_deaths:4} |' )

                    # print(confirmed_plot_values)
                    if (target_state in plot_confirmed.keys()):
                         plot_confirmed[target_state].append(total_confirmed)
                    else:
                        plot_confirmed[target_state] = [total_confirmed]

xs = []
ys = []
colors = []

# Thanks to John S. for the jumpstart on the Bokeh code

# output to static HTML file
output_file("lines.html")

p = figure(plot_width=800, plot_height=400,x_range=plot_dates)
p.xaxis.major_label_orientation = math.pi/2

legend = Legend(location=(0,0))
p.add_layout(legend, 'right')

for state in target_states:
    xs.append(plot_dates)
    ys.append(plot_confirmed[state])
    colors.append(state_colors[state])
    p.line(x=plot_dates, y=plot_confirmed[state], legend_label=state , line_width=2, color=state_colors[state])
    
#p.multi_line(xs, ys, line_width=2, legend = target_states, color=colors)
# p.line(x=plot_dates, y=plot_confirmed_plot_values, legend_label=target_state , line_width=2, color="blue")

# show the results
show(p)

# City-specific.  We'll add this back in later
"""
# Get a specific city
            if (target_city is not None): 
                if (key.find('Admin2') >= 0):
                    cities = df['Admin2']
                    for city in cities:
                        if (type(city)is str):
                            if (city.find(target_city)>=0):
                                tc = df[df['Admin2']==target_city]
                                # stated_confirmed = tc['Confirmed'].values[target_city]
                                # state_deaths = tc['state_Deaths'].values[target_city]
                                # print(F'{date}.csv : {target_city} - stated_confirmed: {stated_confirmed}  state_deaths: {state_deaths} ')
                                # print(tc)
"""
