### How to export part of the data

import sqlite3
import csv


# Connect to the SQLite database
conn = sqlite3.connect('chembl_34.db')  # Update with your database path
cursor = conn.cursor()
# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for table in tables:
    print(table[0])
conn.close()


# Connect to the SQLite database
conn = sqlite3.connect('chembl_34.db')
cursor = conn.cursor()
# Get table structure
cursor.execute("PRAGMA table_info(drug_indication);")
columns = cursor.fetchall()
# Print table columns
for col in columns:
    print(f"Column Name: {col[1]} | Data Type: {col[2]}")
conn.close()


# Connect to the SQLite database
conn = sqlite3.connect('chembl_34.db')
cursor = conn.cursor()

# Define the updated query based on the actual columns
query = """
SELECT
    molecule_dictionary.pref_name AS Drug_Name,
    molecule_dictionary.molregno AS Drug_ID,
    drug_indication.mesh_id AS Disease_ID,
    drug_indication.mesh_heading AS Disease_Name,
    drug_indication.efo_id AS EFO_ID,
    drug_indication.efo_term AS EFO_Term,
    drug_indication.max_phase_for_ind AS Max_Phase
FROM
    drug_indication
JOIN
    molecule_dictionary ON drug_indication.molregno = molecule_dictionary.molregno;
"""

# Execute the query
cursor.execute(query)

# Write to a tab-delimited file
with open('chembl_drug_indications.tsv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter='\t')
    # Write header
    writer.writerow([desc[0] for desc in cursor.description])
    # Write data rows
    for row in cursor.fetchall():
        writer.writerow(row)

print("Data exported to chembl_drug_indications.tsv")
conn.close()






### How to export all the data

import sqlite3
import pandas as pd

# Specify the path to the SQLite database file
db_file = "your_database.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_file)

# Query to retrieve all table names in the database
query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql_query(query, conn)  # Execute the query and store the result in a DataFrame

# Iterate through all table names and export each table as a TSV file
for table_name in tables['name']:
    print(f"Exporting table: {table_name}")  # Log the current table being exported
    # Load the table's data into a Pandas DataFrame
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    # Define the output file name (table_name.tsv)
    output_file = f"{table_name}.tsv"
    # Export the table to a TSV file (tab-separated values)
    df.to_csv(output_file, sep="\t", index=False)
    print(f"Table {table_name} exported to {output_file}")  # Log successful export

# Close the database connection after exporting all tables
conn.close()
print("All tables have been exported successfully.")  # Final confirmation