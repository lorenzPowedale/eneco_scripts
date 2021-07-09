# pip install openpyxl, pandas, unicodecsv
import pandas as pd
import unicodecsv
import sys
import math

output = ['CP communication unit', 'End timestamp', 'Start timestamp', 'Csid']


# cleanses all 0s, NaNs and Nulls out of the DataFrame
def cleanZeroSecondCharges(data):
    print("Before 0sec cleaning", len(data))
    data = data[data['Duration (mins)'] != '']
    data = data[data['Duration (mins)'].astype('int64').notnull()]
    data = data[data['Duration (mins)'].astype('int64') != 0]
    print("After 0sec cleaning", len(data))
    return data


# reads a CSV file
def read_csv(path):
    with open(path, "rb") as f:
        reader = list(unicodecsv.DictReader(f, delimiter=";"))
        return reader

# Syntax e.g. 2021-06-01 00:00:00+02:00
time = input('start-day: ')
# converts excel .xlsx file into a pandas.Dataframe
data = cleanZeroSecondCharges(pd.DataFrame(read_csv(input("Path to CSV of Month: "))))
data['Start timestamp'] = pd.to_datetime(data['Start timestamp'])
data['End timestamp'] = pd.to_datetime(data['End timestamp'])
# Grouping every 'CP communication unit' in month
grouped_df = data.groupby(['CP communication unit'], axis=0, as_index=False)

data_copy = pd.DataFrame()
for key, item in grouped_df:
    group = grouped_df.get_group(key) \
        .assign(total=grouped_df.get_group(key)['Start timestamp']) \
        .sort_values(by=['Start timestamp'], axis=0)
    group = group[output]
    group['Start timestamp'] = group['Start timestamp'].shift(-1)
    group = group[group['Start timestamp'].notnull()]
    group = group[group['Start timestamp'] < group['End timestamp']]
    group = group[group['Start timestamp'].astype('str') >= time]
    data_copy = data_copy.append(group)
data_copy = data_copy[data_copy['Start timestamp'].notnull()]
data_copy['Start timestamp'] = data_copy['Start timestamp'].astype('str')
data_copy['End timestamp'] = data_copy['End timestamp'].astype('str')
data_copy.to_excel("overlapes.xlsx", index=False)
print("Finished")
sys.exit(0)
