import matplotlib.pyplot as plt
import pandas as pd
import datetime

url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
liveurl = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv'

df = pd.read_csv(url, parse_dates=['date'])  # parse CSVs from NYT Github
live_df = pd.read_csv(liveurl, parse_dates=['date'])  # live_df contains today's data, df contains data from before

df = df[df['county'] == 'Hennepin']  # filter for Hennepin data
live_df = live_df[live_df['county'] == 'Hennepin']

df = df[['date', 'cases']]  # get only case + date for each day
live_df = live_df[['date', 'cases']]

df = pd.concat([df, live_df])  # combine dataframes only if new cases have happened today

df_diff = df.set_index('date').diff()  # get number of new cases per day

df_diff['Date'] = df_diff.index.date  # return date to its own column rather than as the index
cutoff = datetime.date(2020, 8, 30)  # set cutoff date
df_diff['cases'][-1] = 306.0 # manually enter today's data if needed (comment out otherwise)
df_diff['School Metric'] = df_diff.rolling(14).sum()  # take 14-day rolling sum
df_diff['School Metric'] *= 10000 / 1265843  # find cases per 10k people
df_diff = df_diff[df_diff['Date'] > cutoff]  # filter only dates after cutoff date

df_diff.plot(y="School Metric", color="k", kind="line", lw="3", label="_nolegend_")  # plot the line

print(df_diff)

plt.annotate(' Today: ' + str(round(df_diff['School Metric'][-1],2)),
             xy=(df_diff['Date'][-1], df_diff['School Metric'].iloc[-1]))  # annotate today's number


plt.axhline(y=10, color='g', linestyle='-', label='Elementary in-person, Middle/high school hybrid')
plt.axhline(y=20, color='y', linestyle='-', label='Both hybrid')  # plot threshold lines
plt.axhline(y=30, color='orange', linestyle='-', label='Elementary hybrid, Middle/high school distance')
plt.axhline(y=50, color='r', linestyle='-', label='Both distance')

plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.07), fancybox=True, shadow=True)  # add legend
plt.ylabel('Number of cases per 10,000 people over 14 days')  # add y-axis label
plt.xlabel('Date')  # add x-axis label
plt.figtext('Data from NYTimes') # add text


plt.tight_layout()  # make sure full legend is shown

plt.show()  # show graph
