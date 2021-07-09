# pip install openpyxl, pandas, unicodecsv
import pandas as pd
import unicodecsv
import sys


# cleanses all 0s, NaNs and Nulls out of the DataFrame
def cleanNull(data):
    print("Before 0kWh cleaning", len(data))
    data = data[data['Energy consumed (wh)'] != '']
    data = data[data['Energy consumed (wh)'].astype('int64').notnull()]
    data = data[data['Energy consumed (wh)'].astype('int64') != 0]
    print("After 0kWh cleaning", len(data))
    return data


# reads a CSV file
def read_csv(path):
    with open(path, "rb") as f:
        reader = list(unicodecsv.DictReader(f, delimiter=";"))
        return reader


time = input('start-day month1: ')
# converts excel .xlsx file into a pandas.Dataframe
path = input("Path to CSV of the FIRST Month: ")
data = pd.DataFrame(read_csv(path))
data['Energy stop (wh)'] = data['Energy stop (wh)'].astype('int64')
data = data[data['Start timestamp'].astype('str') > time]
# Selecting the last row of every 'CP communication unit' in month 1
month1 = data.groupby(['CP communication unit'], axis=0, as_index=False)["Energy stop (wh)"].max()

# converts excel .xlsx file into a pandas.Dataframe
time = input('start-day month2: ')
path = input("Path to CSV of the SECOND Month: ")
data = pd.DataFrame(read_csv(path))
data['Energy initial (wh)'] = data['Energy initial (wh)'].astype('int64')
data = data[data['Start timestamp'].astype('str') > time]
# Selecting the last row of every 'CP communication unit' in month 2
month2 = data.groupby(['CP communication unit'], axis=0, as_index=False)["Energy initial (wh)"].min()

# Merging the Months together
result = pd.merge(month1, month2, on='CP communication unit')

# Only keep the rows where the index isn't as it should be
result = result[result['Energy initial (wh)'] != result['Energy stop (wh)']]

# computes the differnce and creates a new Dataframe
diff = result['Energy stop (wh)'] - result['Energy initial (wh)']
diff = pd.concat([result['CP communication unit'], result['Energy stop (wh)'], result['Energy initial (wh)'], diff],
                 axis=1)
diff.columns = ['CP communication unit', 'Energy stop (wh) in Month1', 'Energy initial (wh) in Month2', 'Difference']

# saving the the rows where the index isn't as it should be to an Excel .xlsx file
diff.to_excel("diff_Month1_Month2.xlsx", sheet_name='Irregularities', index=False)

print("Finished")
sys.exit(0)
