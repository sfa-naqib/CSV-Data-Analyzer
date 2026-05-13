# Backstory:
When I worked in Sales, I hated the time it took for data analysis, reporting and presentations. So if there were a tool, that'd clean and prepare the data for analysis, make reporting and presentation easy; that'd be awesome. This CSV data analyzer is the first step to that ultimate tool.

# CSV Data Analyzer

A terminal-based, interactive data cleaning tool built with Python. You load a CSV file, and the tool guides you step by step — fixing column types, handling missing values, removing duplicates, and more. After cleaning, you can also visualize the data with charts.

---

## Features

**Cleaning**
- Standardizes column names (removes special characters, makes lowercase, replaces spaces with underscores)
- Lets you correct wrong column types — text, numeric, date, boolean, and more
- Cleans text columns (strips whitespace, removes empty strings)
- Detects and removes duplicate rows
- Makes categorical columns consistent (lowercase, uppercase, or title case)
- Handles missing values — separately for numeric and text columns, with multiple options for each

**Analysis**
- Shows a summary of the dataframe before cleaning (column names, types, missing counts)
- Shows a numerical summary after cleaning (min, max, mean, median, standard deviation)

**Dashboard**
- Interactive chart builder — you pick a column, it shows the relevant chart options
- For numeric columns: Histogram with mean/median lines, Line Chart, Box Plot (single or multi-column comparison), Scatter Plot, Grouped Bar Chart (min/mean/max by category)
- For text columns: Horizontal Bar Chart, Pie Chart (with automatic "Others" grouping), Stacked Bar Chart
- Each chart can be shown only, saved as a PNG, or added to a dashboard
- Up to 8 charts can be collected and saved together as a single dashboard PNG

---

## Project Structure

```
project/
│
├── Data/                         # Put your CSV files here
│
├── main.py                       # Run this to start the tool
├── cleaner.py                    # All cleaning functions
├── missing_values_handling.py    # All missing value handling functions
└── dashboard.py                  # All chart and dashboard functions
```

---

## Requirements

- Python 3
- pandas
- matplotlib
- numpy

Install them with:
```
pip install pandas matplotlib numpy
```

---

## How to Use

**1. Put your CSV file inside the `Data/` folder.**

**2. Run `main.py`:**
```
python main.py
```

**3. The tool will guide you through each step:**

```
Step 1  — Enter the filename of your CSV
Step 2  — Column names are standardized automatically
Step 3  — A summary of the dataframe is shown
Step 4  — You review column types and correct any that look wrong
Step 5  — Text columns are cleaned automatically
Step 6  — Duplicate rows are detected and handled
Step 7  — Categorical columns are made consistent
Step 8  — Missing values are handled column by column
Step 9  — A numerical summary is shown
Step 10 — Cleaned file is saved as filename_cleaned.csv
Step 11 — You can open the dashboard to create charts
```

---

## Missing Value Options

For each column that has missing values above your chosen threshold, the tool asks what to do.

**Numeric columns:**
- Fill with average
- Fill with median
- Fill based on another column's values (up to 3 dependency columns)
- Ignore
- Delete the missing rows
- Delete the column

**Text columns:**
- Fill with a default value
- Fill with the most frequent value
- Fill based on another column's values
- Ignore
- Delete the missing rows
- Delete the column

---

## Dashboard — Chart Options

| Column Type | Available Charts |
|---|---|
| Numeric | Histogram, Line Chart, Box Plot (single), Box Plot (multi), Scatter Plot, Grouped Bar Chart |
| Text | Horizontal Bar Chart, Pie Chart, Stacked Bar Chart |

After each chart, you will be asked:
```
1. Show only
2. Save as PNG
3. Add to dashboard
```

If you add charts to the dashboard, you will be asked at the end if you want to save them all as one PNG file. Maximum 8 charts per dashboard.

---

## Notes

- The cleaned CSV is saved in the same folder as `main.py`, not inside `Data/`
- Column names are automatically cleaned — for example, `First Name!` becomes `first_name`
- The pie chart automatically groups any category below 3% into an "Others" slice
- The grouped bar chart always sorts categories by their mean value, from highest to lowest

---

## Example

```
What is the filename of the CSV file: employees
Cleaning process of the csv file is starting...
Column names have been standardized.

------------------------------------------------------------
Summary of the Dataframe
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Total Number of Rows: 500
Total Number of Columns: 8

 Column Index    Column Name     Type  Missing Count  Missing %
            0           name     text              5       1.00
            1     department     text              0       0.00
            2         salary  numeric             12       2.40
            ...
------------------------------------------------------------
```