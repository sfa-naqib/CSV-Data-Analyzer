import pandas as pd
import time
from cleaner import standardize_column_names, column_type_correction, clean_text_columns, clean_duplicates, make_categorical_consistent
from missing_values_handling import handling_missing_values


filename = input(f"What is the filename of the CSV file: ")

try:
    if not filename.endswith('.csv'):
        filename = filename + ".csv"
    filepath = "Data/" + filename
    df = pd.read_csv(filepath)
except FileNotFoundError:
    print(f"It should be a Valid csv Filename inside the Data folder")
    raise

df = standardize_column_names(df)
print("Cleaning process of the csv file is starting.", end = '')
time.sleep(1)
print(".", end = '')
time.sleep(1)
print(".")
time.sleep(1)
print("Standardizing Column Names.", end = '')
time.sleep(1)
print(".", end = '')
time.sleep(1)
print(".")
time.sleep(1)
print("Column names have been standardized.")

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


print("Now cleaning text columns.", end = '')
time.sleep(1)
print(".")
time.sleep(1)
df = clean_text_columns(df)
print("Text columns have been cleaned.\n")

print("\nNow Checking for Duplicate Rows...")
df = clean_duplicates(df)

print("\n\nChecking Categorical (Text) Columns for Consistency...")
df = make_categorical_consistent(df)

print("\n\nChecking for Missing Values...")
df = handling_missing_values(df)
print("Missing Values in all the columns are handled")


print('------------------------------------------------------------')
print("Summary of Numerical Columns")
print('\u203e'*28)

numerical_columns = [column for column in df.columns if pd.api.types.is_numeric_dtype(df[column])]

if not numerical_columns:
    print("No numerical columns found.")
else:
    numerical_summary = {
        'Column Name': [],
        'Min': [],
        'Max': [],
        'Mean': [],
        'Median': [],
        'Std Dev': [],
        'Missing Count': []
    }

    for column in numerical_columns:
        numerical_summary['Column Name'].append(column)
        numerical_summary['Min'].append(round(df[column].min(), 2))
        numerical_summary['Max'].append(round(df[column].max(), 2))
        numerical_summary['Mean'].append(round(df[column].mean(), 2))
        numerical_summary['Median'].append(round(df[column].median(), 2))
        numerical_summary['Std Dev'].append(round(df[column].std(), 2))
        numerical_summary['Missing Count'].append(df[column].isnull().sum())

    numerical_summary_df = pd.DataFrame(numerical_summary)
    print(numerical_summary_df.to_string(index=False))

print('------------------------------------------------------------')


output_filename = filename.replace('.csv', '_cleaned.csv')
df.to_csv(output_filename, index=False)
print(f"\n\nCleaned file saved as: {output_filename}")


dashboard_choice = input("\nDo you want to create charts for the cleaned data? (y/n): ").strip().lower()

if dashboard_choice == 'y':
    import dashboard
    dashboard.run(df)
elif dashboard_choice == 'n':
    print("Okay. Exiting.")
else:
    print("Invalid Input. Exiting.")