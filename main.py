import pandas as pd
from logic import adjusting_bonus, adjusting_team, adjusting_salary, adjusting_fname, adjusting_gender, drop_columns

filename = input(f"What is the filename of the CSV file: ")

try:
    if not filename.endswith('.csv'):
        filename = filename + ".csv"
    filepath = "Data/" + filename
    df = pd.read_csv(filepath)
except FileNotFoundError:
    print(f"It should be a Valid csv Filename inside the Data folder")
    raise

df = adjusting_bonus(df)
df = adjusting_salary(df)
df = adjusting_fname(df)
df = adjusting_team(df)
df = adjusting_gender(df)
df = drop_columns(df, 'Last Login')
df = drop_columns(df, 'Start Date')

df.to_csv('employees_cleaned.csv', index = False)
