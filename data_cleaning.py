import pandas as pd
import matplotlib.pyplot as plt


# Function to clean data
def cleandata():
    # Read data from CSV file
    teams_data = pd.read_csv("Teams00_23.csv")

    # Filter out data for the year 2020
    teams_data = teams_data[(teams_data['yearID'] != 2020)]
    # teams_data = teams_data[(teams_data['yearID'] != 2023)]

    return teams_data


# Function to separate data by franchID
def separate_by_franchid(teams_data):
    # Group data by franchID
    grouped = teams_data.groupby('franchID')
    df_dict = {}

    # Iterate over each group
    for franchID, group_df in grouped:
        # Store each group in a dictionary with franchID as key
        df_dict[franchID] = group_df
        # Export each group to a CSV file with the franchID as the file name
        group_df.to_csv(f"{franchID}.csv", index=False)

    return df_dict


# Function to graph wins by year for each franchID
def graph_individual_wins_by_year(df_dict):
    for franchID, df in df_dict.items():
        # Sort dataframe by yearID
        df_sorted = df.sort_values(by='yearID')

        # Plot wins over years
        plt.figure(figsize=(10, 6))
        plt.plot(df_sorted['yearID'], df_sorted['W'], marker='o', linestyle='--')
        plt.title(f'Wins Over Years for {franchID}')
        plt.xlabel('Year')
        plt.ylabel('Wins')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{franchID} Wins')


# Function to graph losses by year for each franchID
def graph_individual_losses_by_year(df_dict):
    for franchID, df in df_dict.items():
        # Sort dataframe by yearID
        df_sorted = df.sort_values(by='yearID')

        # Plot losses over years
        plt.figure(figsize=(10, 6))
        plt.plot(df_sorted['yearID'], df_sorted['L'], marker='o', linestyle='--')
        plt.title(f'Losses Over Years for {franchID}')
        plt.xlabel('Year')
        plt.ylabel('Losses')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{franchID} Losses')
