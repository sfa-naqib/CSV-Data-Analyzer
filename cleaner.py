import pandas as pd
import re

def standardize_column_names(df):
    for column in df.columns:
        pattern = r'[^a-zA-Z 0-9]'
        new_name = re.sub(pattern, '', column)
        new_name = new_name.strip()
        new_name = new_name.lower()
        new_name = new_name.replace(' ','_')
        df.rename(columns = {column:new_name}, inplace = True)
    
    return df

def column_type_correction(df, selected_column_name):
    correct_type = input("Which is the correct data type for the column?: "
                            "\n1.Text"
                            "\n2.Numerical"
                            "\n3.Date"
                            "\n4.Time"
                            "\n5.Boolean"
                            "\n6.Binary"
                            "\n7.Others / leave unchanged"
                            "\nEnter Choice:").strip()
    
    if correct_type in ['1','6']:
        df[selected_column_name] = df[selected_column_name].astype("string")
    elif correct_type == '2':
        original = df[selected_column_name]

        cleaned = (
                    original
                            .astype("string")
                            .str.strip()
                            .str.replace(',', '', regex=False)
                            .str.replace('$', '', regex=False)
                            .str.replace('BDT', '', regex=False)
                            .str.replace('TK', '', regex=False)
                            .str.replace('৳', '', regex=False)
                            .str.replace('%', '', regex=False)
                    )
        
        converted = pd.to_numeric(cleaned, errors = 'coerce')

        no_of_original_data = original.notnull().sum()
        no_of_converted_data = converted.notnull().sum()

        if no_of_original_data == 0:
            print(f"This column has no data to convert")
            return df
        
        conversion_ratio = (no_of_converted_data/no_of_original_data)*100

        if conversion_ratio >= 75:
            df[selected_column_name] = converted
            print("Column converted to numeric.")
        else:
            confirmation = input(f"Only {conversion_ratio:.2f}% values can be converted to numeric. Convert {selected_column_name} column to Numeric anyway? (y/n): ").strip().lower()
            if confirmation == 'y':
                df[selected_column_name] = converted
                print("Column converted to numeric.")
            elif confirmation == 'n':
                print(f"Column type is left unchanged")
            else:
                print("Invalid Input. Try again.")

        return df

        
    elif correct_type in ['3','4']:
        df[selected_column_name] = pd.to_datetime(df[selected_column_name], errors = 'coerce')
    elif correct_type == '5':
        boolean_values = {'true':True,'false':False,'y':True,'n':False,'1':True,'0':False,'yes':True,'no':False}
        df[selected_column_name] = df[selected_column_name].astype("string").str.strip().str.lower().map(boolean_values)
    elif correct_type == '7':
        print(f"Column left unchanged")
    else:
        print(f"Invalid Input. It should be between 1 to 7.")
    
    return df

def clean_text_columns(df):
    for column in df.columns:
        if pd.api.types.is_string_dtype(df[column]) or pd.api.types.is_object_dtype(df[column]):
            df[column] =  df[column].str.strip()
            df[column] =  df[column].replace('', pd.NA)

    return df

def clean_duplicates(df):
    duplicate_count = df.duplicated().sum()

    if duplicate_count == 0:
        print("No duplicates found")
        return df

    df = df.drop_duplicates(keep='first')
    print("Duplicate entries deleted")
    return df

def make_categorical_consistent(df):
    for column in df.columns:
        if not (pd.api.types.is_string_dtype(df[column]) or pd.api.types.is_object_dtype(df[column])):
            continue

        unique_values = df[column].dropna().unique()
        no_of_unique_values = len(unique_values)

        if no_of_unique_values == 0:
            continue

        print(f"------------------------------------------------------------")
        print(f"Process for making Categorical Column values consistent starting... ")
        print(f"Column Name: {column}")
        print(f"Number of Unique Values: {no_of_unique_values}")
        if no_of_unique_values <= 50:
            print(f"Unique Values: {list(unique_values)}")

        handling_choice = input("\nWhat do you want to do with this column?:"
                                "\n1. Make all values lowercase"
                                "\n2. Make all values uppercase"
                                "\n3. Make all values title case (First Letter Capital)"
                                "\n4. Ignore"
                                "\nEnter Choice: ").strip()

        if handling_choice == '1':
            df[column] = df[column].str.lower()
            print(f"{column} converted to lowercase.")

        elif handling_choice == '2':
            df[column] = df[column].str.upper()
            print(f"{column} converted to uppercase.")

        elif handling_choice == '3':
            df[column] = df[column].str.title()
            print(f"{column} converted to title case.")

        elif handling_choice == '4':
            print(f"Ignoring {column}. Moving on to the next.")
            continue

        else:
            print("Invalid Input. Valid Inputs are 1, 2, 3, 4 only.")

    return df
