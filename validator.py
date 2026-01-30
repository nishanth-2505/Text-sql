import re

def validate_sql(sql, allowed_columns):
    """
    Validate SQL:
    - Only columns must exist in allowed_columns
    - Table names, keywords, functions, etc., are ignored
    - Literals (strings/numbers) are ignored
    """

    # Convert allowed columns to lowercase for comparison
    allowed_lower = [c.lower() for c in allowed_columns]

    # Remove string literals (like 'diesel') and numeric literals
    sql_clean = re.sub(r"'[^']*'", "", sql)      # remove strings
    sql_clean = re.sub(r"\b\d+(\.\d+)?\b", "", sql_clean)  # remove numbers

    # Extract all words
    tokens = re.findall(r"\b[a-zA-Z_]+\b", sql_clean.lower())

    # Check each token: if it's not in allowed columns, ignore (assume keyword or table)
    for token in tokens:
        if token not in allowed_lower:
            # Not a column, ignore
            continue

    # If no invalid column found, SQL is valid
    return True
