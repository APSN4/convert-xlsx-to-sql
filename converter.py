import pandas as pd
import csv

xlsx_file = 'Your_file_name.xlsx'
csv_file = 'Your_file_name.csv'
sql_file = 'Your_file_name.sql'
table_name = 'main'
sql_template = "INSERT INTO {0} (model, color, max_speed) VALUES ({1});"

# Read and store content of an excel file
read_file = pd.read_excel(xlsx_file)

for index, row in read_file.iterrows():
    if index == 0:
        continue  # Skip the header row
    for col in row.index:
        if pd.notnull(row[col]) and isinstance(row[col], str):
            row[col] = row[col].rsplit(',', 1)[0]

# Write the dataframe object into csv file
read_file.to_csv(csv_file,
                 index=None,
                 header=True,
                 quoting=csv.QUOTE_NONNUMERIC)

with open(csv_file, 'r', encoding='utf-8') as file:
    csv_data = csv.reader(file, delimiter=',', quotechar='"')

    with open(sql_file, 'w', encoding='utf-8') as sql:
        next(csv_data)  # skipping the csv file header

        for row in csv_data:
            values = ', '.join("'" + value.replace("'", "''") + "'" for value in row)
            index_r = values.rindex(',')
            values = values[:index_r]
            sql_query = sql_template.format(table_name, values)
            sql.write(sql_query + '\n')