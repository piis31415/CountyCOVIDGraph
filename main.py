import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
 
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
liveurl = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv'
 
df = pd.read_csv(url, parse_dates=['date'])  # parse CSVs from NYT Github
live_df = pd.read_csv(liveurl, parse_dates=['date'])  # live_df contains today's data, df contains data from before
population_df = pd.read_csv('https://raw.githubusercontent.com/piis31415/CountyCOVIDGraph/main/2019_county_population_estimates.csv', sep=';', encoding='latin-1')
 
 
state = 'Minnesota'
county = 'Hennepin'
newcases, probcases = 493, 0 # manually-entered number of new cases today, as of 10/29/20
 
 
manual = True
 
 
population_df = population_df[population_df['STNAME'] == state]  #find population of county
population_df = population_df[population_df['CTYNAME'] == county + ' County']
try:
    population = population_df.iloc[0]['POPESTIMATE2019']
    print(population)
except:
    print("An error occured. Make sure you have spelled the name and the state correctly, and that the state isn't Alaska because alaska names their counties weirdly")
 
df = df[df['state'] == state]
df = df[df['county'] == county]  # filter for county data
live_df = live_df[live_df['state'] == state]
live_df = live_df[live_df['county'] == county]
 
df = df[['date', 'cases']]  # get only case + date for each day
live_df = live_df[['date', 'cases']]
 
df = pd.concat([df, live_df])  # combine dataframes only if new cases have happened today
 
df_diff = df.set_index('date').diff()  # get number of new cases per day
 
df_diff['Date'] = df_diff.index.date  # return date to its own column rather than as the index
cutoff = datetime.date(2020, 8, 31)  # set cutoff date
if manual:
  df_diff.iloc[-1, 0] = newcases # manually enter today's data if needed (comment out otherwise)
 
df_diff['School Metric'] = df_diff.rolling(14).sum()  # take 14-day rolling sum
df_diff['School Metric'] *= 10000 / population  # find cases per 10k people
df_diff = df_diff[df_diff['Date'] > cutoff]  # filter only dates after cutoff date
if not manual:
  df_diff = df_diff[:-1]
 
print(df_diff)
 
fig = plt.figure(dpi=100)
ax = df_diff.plot(y="School Metric", color="k", kind="line", lw="3", label="_", figsize=(7.2,6.4), ax = plt.gca())  # plot the line
ax.set_xlabel("")
fig.patch.set_facecolor('white')
 
plt.annotate(' Today: ' + str(round(df_diff.iloc[-1,2],2)),
             xy=(df_diff.iloc[-1,1], df_diff.iloc[-1,2]))  # annotate today's number
 
ax.tick_params(axis='x', which='major', pad=-10) #move label up a bit
 
plt.axhline(y=10, color='g', linestyle='-', label='Elementary in-person, Middle/high school hybrid')
plt.axhline(y=20, color='y', linestyle='-', label='Both hybrid')  # plot threshold lines
plt.axhline(y=30, color='orange', linestyle='-', label='Elementary hybrid, Middle/high school distance')
plt.axhline(y=50, color='r', linestyle='-', label='Both distance')
 
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True)  # add legend
plt.ylabel('Number of cases per 10,000 people over 14 days')  # add y-axis label
ax.set_xlabel('Date', labelpad=-7)  # add x-axis label
 
 
# add text box saying number of new cases today
if manual:
  caseinfostr ='\n'.join((
      r'New Confirmed Cases: %.0f' % (newcases, ),
      r'New Probable Cases: %.0f' % (probcases, )))
  ax.text(0.6, 0.90, caseinfostr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=dict(facecolor='none', boxstyle='square'))
 
 
 
 
#if state == 'Minnesota':
  #titlestr = 'MN School Metric for ' + county + ' County, as of ' + str(df_diff.iloc[-1,1])
#else:
#  titlestr = 'MN School Metric for ' + county + ' County, ' + state + ', as of ' + str(df_diff.iloc[-1,1])
#plt.title(titlestr, fontsize=16) # add title
 
plt.tight_layout()  # make sure full legend is shown
 
 
 
plt.show()  # show graph
