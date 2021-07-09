# pip install openpyxl, pandas, unicodecsv
import sys

import pandas as pd
import unicodecsv

# reads a CSV file
def read_csv(path):
    with open(path, "rb") as f:
        reader = list(unicodecsv.DictReader(f, delimiter=";"))
        return reader

# converts excel .xlsx file into a pandas.Dataframe
path = input("Path to CSV: ")
data = pd.DataFrame(read_csv(path))
# cleanses every null value in the "Energy consumed (wh)" column
zero = data[data['Energy consumed (wh)'].astype('int64') == 0]
whitespace = data[data['Energy consumed (wh)'].astype('str') == '']
null = data[data['Energy consumed (wh)'].isnull()]

data = zero.append(whitespace).append(null)

# saving to an excel file
data.to_excel('0kWh charges.xlsx', index=False, sheet_name='Without Null Values')
sys.exit(0)
# print the result


