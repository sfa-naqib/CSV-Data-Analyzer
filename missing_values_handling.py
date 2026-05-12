import pandas as pd

def fill_numeric_by_dependencies(df,column,dependency_list):
    avg_column = df[column].mean()
    missing_column_rows = df[df[column].isnull()]
    
    if not dependency_list:
        print("No valid dependency columns selected.")
        return df
    
    elif len(dependency_list) == 3:
        dependency_columns = [df.columns[i] for i in dependency_list]
        avg_dependency_group_123 = df.groupby(dependency_columns, dropna=False)[column].mean()
        avg_dependency_group_12  = df.groupby(dependency_columns[0:2], dropna=False)[column].mean()
        avg_dependency_group_1   = df.groupby(dependency_columns[0], dropna=False)[column].mean()

        for index,row in missing_column_rows.iterrows():
            dep_val_1 = row[dependency_columns[0]]
            dep_val_2 = row[dependency_columns[1]]
            dep_val_3 = row[dependency_columns[2]]

            group_key_123 = (dep_val_1,dep_val_2,dep_val_3)
            group_key_12 = (dep_val_1,dep_val_2)


            if group_key_123 in avg_dependency_group_123.index:
                df.loc[index,column] = avg_dependency_group_123[group_key_123]
            elif group_key_12 in avg_dependency_group_12.index:
                df.loc[index,column] = avg_dependency_group_12[group_key_12]
            elif dep_val_1 in avg_dependency_group_1.index:
                df.loc[index,column] = avg_dependency_group_1[dep_val_1]                                                               
            else:
                df.loc[index,column] = avg_column  
        
    elif len(dependency_list) == 2:
        dependency_columns = [df.columns[i] for i in dependency_list]
        avg_dependency_group_12 = df.groupby(dependency_columns, dropna=False)[column].mean()
        avg_dependency_group_1   = df.groupby(dependency_columns[0], dropna=False)[column].mean()

        for index,row in missing_column_rows.iterrows():
            dep_val_1 = row[dependency_columns[0]]
            dep_val_2 = row[dependency_columns[1]]

            group_key_12 = (dep_val_1,dep_val_2)

            if group_key_12 in avg_dependency_group_12.index:
                df.loc[index,column] = avg_dependency_group_12[group_key_12]
            elif dep_val_1 in avg_dependency_group_1.index:
                df.loc[index,column] = avg_dependency_group_1[dep_val_1]                                                               
            else:
                df.loc[index,column] = avg_column 
    
    else:
        dependency_columns = [df.columns[i] for i in dependency_list]
        avg_dependency_group_1   = df.groupby(dependency_columns[0], dropna=False)[column].mean()

        for index,row in missing_column_rows.iterrows():
            dep_val_1 = row[dependency_columns[0]]

            if dep_val_1 in avg_dependency_group_1.index:
                df.loc[index,column] = avg_dependency_group_1[dep_val_1]
            else:
                df.loc[index,column] = avg_column
    
    return df

def fill_text_by_dependency(df, column, dependency_column):
    overall_mode = df[column].mode()

    if overall_mode.empty:
        print(f"No mode available for {column}.")
        return df

    overall_mode = overall_mode[0]

    missing_rows = df[df[column].isnull()]

    grouped_mode = df.groupby(dependency_column)[column].agg(
        lambda x: x.mode()[0] if not x.mode().empty else overall_mode
    )

    for index, row in missing_rows.iterrows():
        dep_value = row[dependency_column]

        if dep_value in grouped_mode.index:
            df.loc[index, column] = grouped_mode[dep_value]
        else:
            df.loc[index, column] = overall_mode

    return df

def handling_missing_in_numeric_column(df,column, missing_rows, missing_percentage):
    handling_choice = input(f"\nWhat do you want to do for the missing values?:"
                            "\n1. Fill with average value"
                            "\n2. Fill with median value"
                            "\n3. Fill depending on other column values"
                            "\n4. Ignore"
                            "\n5. Delete the missing rows"
                            "\n6. Delete the column").strip()
    
    if handling_choice == '1':
        average = df[column].mean()
        df.loc[missing_rows, column] = average

    elif handling_choice == '2':
        median_value = df[column].median()
        df.loc[missing_rows, column] = median_value
    
    elif handling_choice == '3':
        columns = df.columns
        print("------------------------------------------")
        print(f"Here are the indexes and column names:\n")
        for index, col_name in enumerate(columns):
            print(f"{index}.  {col_name}")
        print("------------------------------------------")
        print(f"If the Values of {column} column depend on other columns: \n"
                f"For handling the missing values of {column} column,\n"
                "You can choose one by one upto 3 dependency columns")

        dependency_list = []
        choice_count = 1
        dependency_len = input(f"How many dependency column do you want?(1-3): ").strip()
        if (not dependency_len.isdigit()) or int(dependency_len) < 1 or int(dependency_len)>3:
            print(f"Invalid Input. You can have maximum 3 dependency column. So, valid inputs are 1,2,3 only")
        else:
            while choice_count <= int(dependency_len):       
                dependency_choice = input(f"Dependent Column No.{choice_count}. Please enter the index of the dependency column: ").strip()
                if not dependency_choice.isdigit():
                    print(f"Invalid Input. Must be an integer between 0 and {len(df.columns)-1}")
                    continue
                dep_index = int(dependency_choice)
                if not (0 <= dep_index < len(df.columns)):
                    print(f"Invalid Input. Must be an integer between 0 and {len(df.columns)-1}")
                elif df.columns[dep_index] == column:
                    print(f"Target column cannot be its own dependency.")
                elif dep_index in dependency_list:
                    print("Duplicate Input. This column is already listed as dependency")
                else:
                    dependency_list.append(dep_index)
                    choice_count += 1
            df = fill_numeric_by_dependencies(df,column,dependency_list)

    elif handling_choice == '4':
        print(f"Ignoring the missing values of {column}. Moving on to the next.")
        return df

    elif handling_choice == '5':
        confirmation = input(f"Are you sure, you want to delete the missing rows, which represents {missing_percentage}% of the data? (y/n)").strip().lower()
        if confirmation == 'y':
            df = df.dropna(subset = [column])
        elif confirmation == 'n':
            print("Delete Aborted.")
        else:
            print("Invalid Input")
    
    elif handling_choice == '6':
        confirmation = input(f"Are you sure, you want to delete the entire column named {column}? (y/n)").strip().lower()
        if confirmation == 'y':
            df = df.drop(column, axis = 1)
        elif confirmation == 'n':
            print("Delete Aborted.")
        else:
            print("Invalid Input")
    
    else:
        print(f"Invalid Input. Valid Inputs are 1,2,3,4,5,6 only.")

    return df

def handling_missing_in_text_columns(df, column, missing_rows, missing_percentage):
    handling_choice = input(
            "\nWhat do you want to do for the missing values?"
            "\n1. Fill with default value"
            "\n2. Fill with most frequent value"
            "\n3. Fill depending on another column"
            "\n4. Ignore"
            "\n5. Delete the missing rows"
            "\n6. Delete the column"
            "\nEnter choice: "
        ).strip()

    if handling_choice == '1':
        default_value = input("Enter default value: ").strip()
        if not default_value:
            print("No value entered. Skipping.")
            return df

        df.loc[missing_rows, column] = default_value

    elif handling_choice == '2':
        mode_values = df[column].mode()

        if mode_values.empty:
            print("No most frequent value available.")
        else:
            df.loc[missing_rows, column] = mode_values[0]

    elif handling_choice == '3':
        print("------------------------------------------")
        print("Here are the indexes and column names:\n")
        for index, col_name in enumerate(df.columns):
            print(f"{index}. {col_name}")
        print("------------------------------------------")

        dependency_choice = input(
            f"Enter the index of the dependency column for filling missing values in {column}: "
        ).strip()

        if not dependency_choice.isdigit():
            print("Invalid input. Must be an integer.")

        else:
            dep_index = int(dependency_choice)

            if not (0 <= dep_index < len(df.columns)):
                print(f"Invalid input. Must be between 0 and {len(df.columns)-1}.")

            elif df.columns[dep_index] == column:
                print("Target column cannot be its own dependency.")

            else:
                dependency_column = df.columns[dep_index]
                df = fill_text_by_dependency(df, column, dependency_column)

    elif handling_choice == '4':
        print(f"Ignoring missing values of {column}.")
        return df

    elif handling_choice == '5':
        confirmation = input(
            f"Are you sure you want to delete rows with missing {column}? "
            f"This affects {missing_percentage:.2f}% of data. (y/n): "
        ).strip().lower()

        if confirmation == 'y':
            df = df.dropna(subset=[column])
        else:
            print("Delete aborted.")

    elif handling_choice == '6':
        confirmation = input(
            f"Are you sure you want to delete the column {column}? (y/n): "
        ).strip().lower()

        if confirmation == 'y':
            df = df.drop(columns=[column])
        else:
            print("Delete aborted.")

    else:
        print("Invalid input. Valid choices are 1-6.")

    return df

def handling_missing_values(df):
    threshold = input("What missing percentage should be considered ignorable?: ").strip().replace('%','')
    try:
        threshold = float(threshold)
        if not (0 < threshold < 100):
            raise ValueError
    except ValueError:
        print("Invalid Input. Valid inputs are integers between 0 and 100")
        return df
    
    for column in list(df.columns):
        missing_rows = df[column].isnull()
        missing_count = missing_rows.sum()
        missing_percentage = (missing_count/(len(df[column])))*100
        
        if missing_count == 0:
            continue
        if  missing_percentage <= threshold:
            continue

        print(f"Column Name: {column}")
        print(f"Column Type: {df[column].dtype}")
        print(f"Number of Missing Values: {missing_count}")
        print(f"Missing Percentage: {missing_percentage}")
        
        if pd.api.types.is_numeric_dtype(df[column]): 
            df = handling_missing_in_numeric_column(df,column,missing_rows, missing_percentage)
        
        elif pd.api.types.is_object_dtype(df[column]) or pd.api.types.is_string_dtype(df[column]):
            df = handling_missing_in_text_columns(df, column, missing_rows, missing_percentage)
        else:
            continue
    return df
        

