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