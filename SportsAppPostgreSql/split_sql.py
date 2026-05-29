import os
import re

def extract_table_name(sql):
    """
    Extracts the table name from a SQL statement.

    Args:
        sql (str): The SQL statement.

    Returns:
        str: The table name, or None if not found.
    """
    pattern = r'(\w+)\s*?\((.*?)\)\s*?;'
    match = re.search(pattern, sql)
    if match:
        return match.group(1)
    return None

def split_sql():
    """
    Splits the SQL statements in `sportsapp.sql` into separate files in the `ddl_scripts` directory.
    """
    with open('sportsapp.sql', 'r') as f:
        content = f.read()

    table_definitions = re.findall(r'CREATE TABLE\s+(.*?)\s*;\s*?(?=\nCREATE TABLE|\Z)', content, re.DOTALL)

    if not os.path.exists('ddl_scripts'):
        os.makedirs('ddl_scripts')

    for i, table_definition in enumerate(table_definitions):
        table_name = extract_table_name(table_definition)
        if table_name:
            with open(f'ddl_scripts/{table_name}.sql', 'w') as f:
                f.write(table_definition)
        else:
            print(f"Failed to extract table name from: {table_definition}")

split_sql()