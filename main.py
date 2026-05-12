import pandas as pd
from logic import adjusting_bonus, adjusting_team, adjusting_salary, adjusting_fname, adjusting_gender, drop_columns
from cleaner import column_type_correction

filename = input(f"What is the filename of the CSV file: ")

try:
    if not filename.endswith('.csv'):
        filename = filename + ".csv"
    filepath = "Data/" + filename
    df = pd.read_csv(filepath)
except FileNotFoundError:
    print(f"It should be a Valid csv Filename inside the Data folder")
    raise

columns = df.columns

no_of_rows = df.shape[0]
no_of_columns = df.shape[1]

summary = {
    'Column Name': [],
    'Type': [],
    'Missing Count': [],
    'Missing %': [] 
    }

def map_dtype(dtype):
    if 'int' in dtype or 'float' in dtype:
        return 'numeric'
    elif 'object' in dtype or 'str' in dtype:
        return 'text'
    elif 'bool' in dtype:
        return 'boolean'
    elif 'datetime' in dtype:
        return 'date'
    else:
        return 'other'

for column in columns:
    no_of_missing_values = df[column].isnull().sum()
    summary['Column Name'].append(column)
    data_type = str(df[column].dtype)
    summary['Type'].append(map_dtype(data_type))
    summary['Missing Count'].append(no_of_missing_values)
    missing_percent = (no_of_missing_values/no_of_rows)*100
    summary['Missing %'].append(missing_percent)

summary_df = pd.DataFrame(summary)
summary_df['Missing %'] = summary_df['Missing %'].round(2)
summary_df.insert(0,'Column Index', summary_df.index)

print('------------------------------------------------------------')
print(f"Summary of the Dataframe")
print('\u203e'*24)
print(f"Total Number of Rows: {no_of_rows}")
print(f"Total Number of Columns: {no_of_columns}\n")
print(summary_df.to_string(index=False))
print('------------------------------------------------------------')

while True:
    type_ok = input(f"Does all the columns' types seem correct now? (y/n)")

    if type_ok.lower() == 'y':
        print('OK. Proceeding to the next step')
        break

    elif type_ok.lower() == 'n':
        dx = input(f"Please enter the index of a column that you think the type is incorrect: ").strip()

        if not dx.isdigit():
            print(f"Invalid Input. The Column Index must be a number")
            continue

        dx = int(dx)
        column_length = len(df.columns)

        if dx < 0 or dx >= column_length:
            print(f"Invalid Input. The Column Index must be number between 0 and {column_length-1}.")
            continue

        selected_column_name = df.columns[dx]
        print(f"Selected Column's name is: {selected_column_name}")
        print(f"Current Type for this column is: {df[selected_column_name].dtype}")
        df = column_type_correction(df,selected_column_name)
        print(f"{selected_column_name} column updated to as type: {df[selected_column_name].dtype}\n")
    else:
        print('Invalid Response. Please enter y or n')

