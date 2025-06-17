import pandas as pd

# Load the dataset
try:
    users_df = pd.read_csv('users_data.csv')

    # Check if 'current_age' column exists
    if 'current_age' in users_df.columns:
        # Calculate the mean of the 'current_age' column
        mean_current_age = users_df['current_age'].mean()
        print(f"The mean age of the users (using 'current_age' column) is: {mean_current_age:.2f} years")
    else:
        print("Error: 'current_age' column not found in the dataset. Available columns are:")
        print(users_df.columns.tolist())

except FileNotFoundError:
    print("Error: The file 'users_data.csv' was not found. Please ensure the path is correct.")
except Exception as e:
    print(f"An error occurred: {e}")
    