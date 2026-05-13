import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def ask_to_save(chart_name, dashboard_charts):
    save_choice = input("\nWhat do you want to do with this chart?:"
                        "\n1. Show only"
                        "\n2. Save as PNG"
                        "\n3. Add to dashboard"
                        "\nEnter Choice: ").strip()

    if save_choice == '1':
        plt.show()
    elif save_choice == '2':
        filename = input("Enter a filename (without extension): ").strip()
        if not filename:
            filename = chart_name
        plt.savefig(f"{filename}.png", bbox_inches='tight')
        print(f"Chart saved as {filename}.png")
        plt.show()
    elif save_choice == '3':
        if len(dashboard_charts) >= 8:
            print("Dashboard is full. Maximum 8 charts allowed.")
            plt.show()
        else:
            dashboard_charts.append((chart_name, plt.gcf()))
            print(f"Chart added to dashboard. ({len(dashboard_charts)}/8 slots used)")
            plt.close()
    else:
        print("Invalid Input. Chart not saved.")
        plt.show()

def save_dashboard(dashboard_charts):
    if not dashboard_charts:
        print("No charts in dashboard.")
        return

    no_of_charts = len(dashboard_charts)

    no_of_columns = 2
    no_of_rows = (no_of_charts + 1) // 2

    fig, axes = plt.subplots(no_of_rows, no_of_columns, figsize=(14, no_of_rows * 5))
    axes = axes.flatten()  

    for i, (chart_name, saved_fig) in enumerate(dashboard_charts):
        saved_fig.canvas.draw()
        image = np.frombuffer(saved_fig.canvas.tostring_rgb(), dtype=np.uint8)
        image = image.reshape(saved_fig.canvas.get_width_height()[::-1] + (3,))
        axes[i].imshow(image)
        axes[i].axis('off')
        axes[i].set_title(chart_name)

    for j in range(no_of_charts, len(axes)):
        axes[j].axis('off')

    filename = input("Enter a filename for the dashboard PNG (without extension): ").strip()
    if not filename:
        filename = "dashboard"

    plt.savefig(f"{filename}.png", bbox_inches='tight')
    print(f"Dashboard saved as {filename}.png")
    plt.show()

def show_column_list(df):
    print('------------------------------------------------------------')
    print("Available Columns")
    print('\u203e'*17)
    for index, column in enumerate(df.columns):
        if pd.api.types.is_numeric_dtype(df[column]):
            col_type = 'numeric'
        elif pd.api.types.is_object_dtype(df[column]) or pd.api.types.is_string_dtype(df[column]):
            col_type = 'text'
        else:
            col_type = 'other'
        print(f"{index}.  {column}  ({col_type})")
    print('------------------------------------------------------------')

def show_histogram(df, column, dashboard_charts):
    fig, ax = plt.subplots()

    ax.hist(df[column].dropna(), bins=20, color='steelblue', edgecolor='black')

    mean_value = df[column].mean()
    median_value = df[column].median()
    ax.axvline(mean_value,   color='red',    linestyle='--', linewidth=1.5, label=f'Mean:   {mean_value:.2f}')
    ax.axvline(median_value, color='orange', linestyle='--', linewidth=1.5, label=f'Median: {median_value:.2f}')

    ax.set_title(f'Distribution of {column}')
    ax.set_xlabel(column)
    ax.set_ylabel('Count')
    ax.legend()
    plt.tight_layout()

    ask_to_save(f'histogram_{column}', dashboard_charts)
    plt.show()

def show_line_chart(df, column, dashboard_charts):
    fig, ax = plt.subplots()

    ax.plot(df[column].dropna().reset_index(drop=True), color='steelblue')
    ax.set_title(f'{column} over Index')
    ax.set_xlabel('Row Index')
    ax.set_ylabel(column)
    plt.tight_layout()

    ask_to_save(f'line_{column}', dashboard_charts)
    plt.show()

def show_boxplot_single(df, column, dashboard_charts):
    fig, ax = plt.subplots()

    ax.boxplot(df[column].dropna(), vert=True, patch_artist=True,
               boxprops=dict(facecolor='steelblue', color='black'))
    ax.set_title(f'Boxplot of {column}')
    ax.set_ylabel(column)
    plt.tight_layout()

    ask_to_save(f'boxplot_{column}', dashboard_charts)
    plt.show()

def show_boxplot_multi(df, column, dashboard_charts):
    numeric_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col]) and col != column]

    if not numeric_columns:
        print("No other numeric columns available for comparison.")
        return

    print("------------------------------------------")
    print("Available numeric columns to compare with:\n")
    for index, col in enumerate(numeric_columns):
        print(f"{index}.  {col}")
    print("------------------------------------------")
    print("You can select multiple columns separated by commas. Example: 0,2,3")

    selection = input("Enter column indexes: ").strip()
    selected_indexes = selection.split(',')

    columns_to_plot = [column]

    for item in selected_indexes:
        item = item.strip()
        if not item.isdigit():
            print(f"Skipping invalid input: {item}")
            continue
        idx = int(item)
        if not (0 <= idx < len(numeric_columns)):
            print(f"Skipping out of range index: {idx}")
            continue
        if numeric_columns[idx] not in columns_to_plot:
            columns_to_plot.append(numeric_columns[idx])

    if len(columns_to_plot) < 2:
        print("Not enough valid columns selected. Showing single boxplot instead.")
        show_boxplot_single(df, column, dashboard_charts)
        return

    data_to_plot = [df[col].dropna() for col in columns_to_plot]

    fig, ax = plt.subplots()
    ax.boxplot(data_to_plot, patch_artist=True,
               boxprops=dict(facecolor='steelblue', color='black'))
    ax.set_xticks(range(1, len(columns_to_plot) + 1))
    ax.set_xticklabels(columns_to_plot, rotation=45, ha='right')
    ax.set_title('Boxplot Comparison')
    ax.set_ylabel('Values')
    plt.tight_layout()

    ask_to_save('boxplot_comparison', dashboard_charts)
    plt.show()

def show_scatter_chart(df, column, dashboard_charts):
    numeric_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col]) and col != column]

    if not numeric_columns:
        print("No other numeric columns available for scatter plot.")
        return

    print("------------------------------------------")
    print("Available numeric columns for the Y axis:\n")
    for index, col in enumerate(numeric_columns):
        print(f"{index}.  {col}")
    print("------------------------------------------")

    y_choice = input("Enter the index of the column for the Y axis: ").strip()

    if not y_choice.isdigit():
        print("Invalid Input. Must be a number.")
        return

    y_index = int(y_choice)

    if not (0 <= y_index < len(numeric_columns)):
        print(f"Invalid Input. Must be between 0 and {len(numeric_columns)-1}.")
        return

    column_y = numeric_columns[y_index]

    fig, ax = plt.subplots()
    ax.scatter(df[column], df[column_y], color='steelblue', edgecolor='black', alpha=0.6)
    ax.set_title(f'{column} vs {column_y}')
    ax.set_xlabel(column)
    ax.set_ylabel(column_y)
    plt.tight_layout()

    ask_to_save(f'scatter_{column}_vs_{column_y}', dashboard_charts)
    plt.show()

def show_grouped_bar_chart(df, column, dashboard_charts):
    text_columns = [col for col in df.columns
                    if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col])]

    if not text_columns:
        print("No categorical columns available for grouping.")
        return

    print("------------------------------------------")
    print("Available categorical columns to group by:\n")
    for index, col in enumerate(text_columns):
        print(f"{index}.  {col}")
    print("------------------------------------------")

    group_choice = input("Enter the index of the column to group by: ").strip()

    if not group_choice.isdigit():
        print("Invalid Input. Must be a number.")
        return

    group_index = int(group_choice)

    if not (0 <= group_index < len(text_columns)):
        print(f"Invalid Input. Must be between 0 and {len(text_columns)-1}.")
        return

    group_column = text_columns[group_index]

    grouped_mean = df.groupby(group_column)[column].mean().sort_values(ascending=False)
    grouped_min  = df.groupby(group_column)[column].min().reindex(grouped_mean.index)
    grouped_max  = df.groupby(group_column)[column].max().reindex(grouped_mean.index)

    categories = grouped_mean.index.tolist()
    x = np.arange(len(categories))
    bar_width = 0.25

    fig, ax = plt.subplots()

    ax.bar(x - bar_width, grouped_min.values,  width=bar_width, label='Min',  color='steelblue', edgecolor='black')
    ax.bar(x,             grouped_mean.values, width=bar_width, label='Mean', color='coral',     edgecolor='black')
    ax.bar(x + bar_width, grouped_max.values,  width=bar_width, label='Max',  color='seagreen',  edgecolor='black')

    ax.set_title(f'Min / Mean / Max of {column} by {group_column}')
    ax.set_xlabel(group_column)
    ax.set_ylabel(column)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()

    ask_to_save(f'grouped_{column}_by_{group_column}', dashboard_charts)
    plt.show()

def show_count_bar_chart(df, column, dashboard_charts):
    counts = df[column].value_counts()

    fig, ax = plt.subplots()

    ax.barh(counts.index, counts.values, color='coral', edgecolor='black')
    ax.set_title(f'Count of each value in {column}')
    ax.set_xlabel('Count')
    ax.set_ylabel(column)
    plt.tight_layout()

    ask_to_save(f'count_bar_{column}', dashboard_charts)
    plt.show()

def show_pie_chart(df, column, dashboard_charts):
    counts = df[column].value_counts()
    total = counts.sum()

    main_counts = counts[counts / total * 100 >= 3]
    others_total = counts[counts / total * 100 < 3].sum()

    if others_total > 0:
        main_counts['Others'] = others_total

    if len(main_counts) > 10:
        print(f"Warning: {column} still has {len(main_counts)} slices after grouping small values. Pie chart may be hard to read.")
        confirmation = input("Do you still want to continue? (y/n): ").strip().lower()
        if confirmation != 'y':
            print("Pie chart cancelled.")
            return

    fig, ax = plt.subplots()
    ax.pie(main_counts.values, labels=main_counts.index, autopct='%1.1f%%', startangle=90)
    ax.set_title(f'Proportion of each value in {column}')
    plt.tight_layout()

    ask_to_save(f'pie_{column}', dashboard_charts)
    plt.show()

def show_stacked_bar_chart(df, column, dashboard_charts):
    text_columns = [col for col in df.columns
                    if (pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col]))
                    and col != column]

    if not text_columns:
        print("No other categorical columns available for stacking.")
        return

    print("------------------------------------------")
    print("Available categorical columns to stack by:\n")
    for index, col in enumerate(text_columns):
        print(f"{index}.  {col}")
    print("------------------------------------------")

    stack_choice = input("Enter the index of the column to stack by: ").strip()

    if not stack_choice.isdigit():
        print("Invalid Input. Must be a number.")
        return

    stack_index = int(stack_choice)

    if not (0 <= stack_index < len(text_columns)):
        print(f"Invalid Input. Must be between 0 and {len(text_columns)-1}.")
        return

    stack_column = text_columns[stack_index]

    grouped = df.groupby([column, stack_column]).size().unstack(fill_value=0)

    fig, ax = plt.subplots()

    colors = plt.cm.Set2.colors
    bottom_values = np.zeros(len(grouped))

    for i, stack_value in enumerate(grouped.columns):
        bar_values = grouped[stack_value].values
        ax.bar(grouped.index, bar_values, bottom=bottom_values,
               label=stack_value, color=colors[i % len(colors)], edgecolor='black')
        bottom_values = bottom_values + bar_values

    ax.set_title(f'{column} broken down by {stack_column}')
    ax.set_xlabel(column)
    ax.set_ylabel('Count')
    ax.set_xticks(range(len(grouped.index)))
    ax.set_xticklabels(grouped.index, rotation=45, ha='right')
    ax.legend(title=stack_column)
    plt.tight_layout()

    ask_to_save(f'stacked_{column}_by_{stack_column}', dashboard_charts)
    plt.show()

def show_chart_menu_for_numeric(df, column, dashboard_charts):
    chart_choice = input(f"\n{column} is a numeric column. What chart do you want?:"
                         "\n1. Histogram with Mean & Median lines"
                         "\n2. Line Chart (shows values across rows)"
                         "\n3. Box Plot - Single column"
                         "\n4. Box Plot - Compare with other numeric columns"
                         "\n5. Scatter Plot (compare with another numeric column)"
                         "\n6. Grouped Bar Chart (Min / Mean / Max by a category)"
                         "\nEnter Choice: ").strip()

    if chart_choice == '1':
        show_histogram(df, column, dashboard_charts)
    elif chart_choice == '2':
        show_line_chart(df, column, dashboard_charts)
    elif chart_choice == '3':
        show_boxplot_single(df, column, dashboard_charts)
    elif chart_choice == '4':
        show_boxplot_multi(df, column, dashboard_charts)
    elif chart_choice == '5':
        show_scatter_chart(df, column, dashboard_charts)
    elif chart_choice == '6':
        show_grouped_bar_chart(df, column, dashboard_charts)
    else:
        print("Invalid Input. Valid Inputs are 1, 2, 3, 4, 5, 6 only.")

def show_chart_menu_for_text(df, column, dashboard_charts):
    chart_choice = input(f"\n{column} is a text column. What chart do you want?:"
                         "\n1. Bar Chart - Horizontal (count of each unique value)"
                         "\n2. Pie Chart (proportion of each unique value)"
                         "\n3. Stacked Bar Chart (break down by another category)"
                         "\nEnter Choice: ").strip()

    if chart_choice == '1':
        show_count_bar_chart(df, column, dashboard_charts)
    elif chart_choice == '2':
        show_pie_chart(df, column, dashboard_charts)
    elif chart_choice == '3':
        show_stacked_bar_chart(df, column, dashboard_charts)
    else:
        print("Invalid Input. Valid Inputs are 1, 2, 3 only.")

def run(df):
    dashboard_charts = []
    print('------------------------------------------------------------')
    print("Welcome to the Dashboard")
    print('\u203e'*24)

    while True:
        show_column_list(df)

        column_choice = input("Enter the index of the column you want to visualize (or 'q' to quit): ").strip()

        if column_choice.lower() == 'q':
            print("Exiting dashboard.")
            break

        if not column_choice.isdigit():
            print("Invalid Input. The Column Index must be a number.")
            continue

        column_index = int(column_choice)

        if not (0 <= column_index < len(df.columns)):
            print(f"Invalid Input. Must be between 0 and {len(df.columns)-1}.")
            continue

        selected_column = df.columns[column_index]
        print(f"\nSelected Column: {selected_column}")

        if pd.api.types.is_numeric_dtype(df[selected_column]):
            show_chart_menu_for_numeric(df, selected_column, dashboard_charts)

        elif pd.api.types.is_object_dtype(df[selected_column]) or pd.api.types.is_string_dtype(df[selected_column]):
            show_chart_menu_for_text(df, selected_column, dashboard_charts)

        else:
            print(f"Sorry, {selected_column} is of type '{df[selected_column].dtype}' which is not supported for charting yet.")

        print()

    if dashboard_charts:
        save_choice = input(f"\nYou have {len(dashboard_charts)} charts in your dashboard. Save it? (y/n): ").strip().lower()
        if save_choice == 'y':
            save_dashboard(dashboard_charts)