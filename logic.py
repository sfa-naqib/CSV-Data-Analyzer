
def adjusting_salary(df):
    avg_salary_by_team_n_management = df.groupby(['Team','Senior Management'])['Salary'].mean()
    avg_salary_by_team = df.groupby('Team')['Salary'].mean()
    avg_salary = df['Salary'].mean()
    missing_salary_rows = df[df['Salary'].isnull()]
    for index, row in missing_salary_rows.iterrows():
        team = row['Team']
        management_status = row['Senior Management']
        group_key = (team,management_status)
        if group_key in avg_salary_by_team_n_management.index:
            df.loc[index,'Salary'] = avg_salary_by_team_n_management[group_key]
        elif team in avg_salary_by_team.index:
            df.loc[index,'Salary'] = avg_salary_by_team[team]
        else:
            df.loc[index,'Salary'] = avg_salary
    return df

def adjusting_team(df):
    missing_team_rows = df[df['Team'].isnull()]
    missing_count = len(df[df['Team'].isnull()])
    if missing_count/len(df) < 0.05:
        df.drop(missing_team_rows.index,inplace=True)
    else:
        df.loc[missing_team_rows.index, 'Team'] = 'missing'
    return df

def adjusting_fname(df):
    male_missing = (df['fname'].isnull()) & (df['Gender'] == 'Male')
    female_missing = (df['fname'].isnull()) & (df['Gender'] == 'Female')
    other_missing = (df['fname'].isnull()) & (~df['Gender'].isin(['Male','Female']))

    df.loc[male_missing, 'First Name'] = 'John'
    df.loc[female_missing, 'First Name'] = 'Jane'
    df.loc[other_missing, 'First Name'] = 'Doe'
    return df

def adjusting_bonus(df):
    avg_bonus_team_n_mgmt = df.groupby(['Team','Senior Management'])['Bonus %'].mean()
    avg_bonus_team = df.groupby['Team']['Bonus %'].mean()
    avg_bonus = df['Bonus %'].mean()
    missing_bonus_rows = df[df['Bonus %'].isnull()]
    for index, row in missing_bonus_rows.iterrows():
        team = row['Team']
        management_status = row['Senior Management']
        group_key = (team, management_status)
        if group_key in avg_bonus_team_n_mgmt.index:
            df.loc[index, 'Bonus %'] = avg_bonus_team_n_mgmt[group_key]
        elif team in avg_bonus_team.index:
            df.loc[index, 'Bonus %'] = avg_bonus_team[team]
        else:
            df.loc[index, 'Bonus %'] = avg_bonus
    return df
    
def adjusting_gender(df):
    missing_gender_rows = df[df['Gender'].isnull()]
    df = df.dropna(subset = ['Gender'])
    return df

def drop_columns(df,column_name):
    return df.drop(column_name, axis = 1)
