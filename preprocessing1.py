import pandas as pd

# Define the path to the CSV file
file_path = r"C:\New folder (4)\data\INRX.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Replace "null" values with NaN
df.replace("null", pd.NA, inplace=True)

# Drop rows containing NaN values
df.dropna(inplace=True)

# Write the cleaned DataFrame back to a CSV file
cleaned_file_path = r"C:\New folder (4)\data\INRX.csv"
df.to_csv(cleaned_file_path, index=False)

print("Null values deleted and cleaned file saved successfully.")
