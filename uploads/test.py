# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load the training data
# train_df = pd.read_csv('C:/Users/armaa/OneDrive/Desktop/ADAAS/AgenticDataAnalysis/uploads/train.csv')

# # Create the count plot
# plt.figure(figsize=(8, 6))
# sns.countplot(data=train_df, x='Sex', hue='Survived', palette='viridis')

# # Customize the plot
# plt.title('Survival Count by Sex', fontsize=16)
# plt.xlabel('Sex', fontsize=12)
# plt.ylabel('Number of Passengers', fontsize=12)
# plt.xticks(ticks=[0, 1], labels=['Female', 'Male'])
# plt.legend(title='Survived', labels=['No', 'Yes'])
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.tight_layout()
# plt.show() # This command displays the plot

# import pandas as pd

# # Load the training data
# train_df = pd.read_csv('C:/Users/armaa/OneDrive/Desktop/ADAAS/AgenticDataAnalysis/uploads/train.csv')

# # Count the number of male and female passengers
# sex_counts = train_df['Sex'].value_counts()

# print("Number of passengers by Sex:")
# print(sex_counts)

# # For clarity, extract specific counts if available
# if 'male' in sex_counts:
#     print(f"\nTotal Male Passengers: {sex_counts['male']}")
# if 'female' in sex_counts:
#     print(f"Total Female Passengers: {sex_counts['female']}")

import pandas as pd

# Define the path to the cards data file
cards_data_path = 'C:\\Users\\armaa\\OneDrive\\Desktop\\ADAAS\\AgenticDataAnalysis\\uploads\\cards_data.csv'

try:
    # Load the cards_data.csv file
    cards_df = pd.read_csv(cards_data_path)

    # Define the client ID we are looking for
    client_id_to_find = 825

    # Filter the DataFrame to get cards belonging to this client ID
    # This assumes 'client_id' is the correct column name in cards_data.csv
    client_cards = cards_df[cards_df['client_id'] == client_id_to_find]

    print(f"--- Cards for Client ID: {client_id_to_find} ---")

    if not client_cards.empty:
        # Display all columns for the found cards
        # Using .to_string() to ensure all rows/columns are printed without truncation
        print(client_cards.to_string())
    else:
        print(f"No cards found for client with ID {client_id_to_find}.")

except FileNotFoundError:
    print(f"Error: The file was not found at the specified path: {cards_data_path}")
    print("Please double-check the path and ensure the file exists.")
except KeyError:
    print("Error: 'client_id' column not found in cards_data.csv.")
    print("Please verify the exact column name in your cards_data.csv file if it's not 'client_id'.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")