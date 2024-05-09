from bs4 import BeautifulSoup as bs  # Import BeautifulSoup for web scraping
from unidecode import unidecode  # Import unidecode for unicode handling
import requests  # Import requests for HTTP requests
import pandas as pd  # Import pandas for data manipulation

# Read player IDs from CSV file and preprocess
df_players_with_ids = pd.read_csv('MLB_Player_Ids.csv', usecols=['FANGRAPHSNAME', 'ESPNID'])
df_players_with_ids['ESPNID'] = pd.to_numeric(df_players_with_ids['ESPNID'], errors='coerce').fillna(-1).astype(int)
df_players_with_ids['FANGRAPHSNAME'] = df_players_with_ids['FANGRAPHSNAME'].str.replace('.', '', regex=False)
df_ids = pd.Series(df_players_with_ids['FANGRAPHSNAME'])

# Read player names from CSV file and preprocess
df = pd.read_csv('PlayerNames.csv')
df['PlayerName'] = df['PlayerName'].apply(unidecode)

# Merge DataFrames on player names
df_merged = pd.merge(df, df_players_with_ids, left_on='PlayerName', right_on='FANGRAPHSNAME', how='left')
df_merged.drop(columns='FANGRAPHSNAME', inplace=True)
df_merged['ESPNID'] = pd.to_numeric(df_merged['ESPNID'], errors='coerce').fillna(-1).astype(int)
df_merged = df_merged.loc[df_merged['ESPNID'] != -1]
df_merged['PlayerName'] = df_merged['PlayerName'].str.lower()
df_merged['PlayerName'] = df_merged['PlayerName'].str.replace(' ', '-', regex=False)

# Extract player names and IDs from merged DataFrame
names_series = pd.Series(df_merged['PlayerName'])
id_series = pd.Series(df_merged['ESPNID'])
player_names = names_series.tolist()
player_ids = id_series.tolist()

# Save the merged DataFrame to a new CSV file
df_merged.to_csv('merged_players.csv', index=False)

# Function to fetch player stats from ESPN website
def fetch_player_stats(player_id, player_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = f'https://www.espn.com/mlb/player/stats/_/id/{player_id}/{player_name}'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return bs(response.text, 'html.parser')  # Parse HTML response
    except requests.RequestException as e:
        print(f"Failed to retrieve page for {player_name}: {e}")
        return None

# Function to extract player stats from HTML soup and save to CSV
def extract_and_save_stats(soup, player_name, player_id):
    career_batting_div = soup.find('div', string='Career Batting')

    if career_batting_div:
        career_batting_table = career_batting_div.find_next('table', class_='Table')

        if career_batting_table:
            # Extract data from HTML table
            header_row = career_batting_table.find('thead').find_all('th')
            headers = [th.get_text(strip=True) for th in header_row]
            body_rows = career_batting_table.find('tbody').find_all('tr')
            data = [[td.get_text(strip=True) for td in tr.find_all('td')] for tr in body_rows]
            df_stats = pd.DataFrame(data, columns=headers)

            # Save data to CSV file
            filename = f"{player_name}_{player_id}_career_batting.csv"
            df_stats.to_csv(filename, index=False)
            print(f"Saved data to {filename}")
        else:
            print(f"Career Batting table not found for {player_name} with ID {player_id}")
    else:
        print(f"'Career Batting' section not found for {player_name} with ID {player_id}")

# Loop through player names and IDs, fetch stats, and save to CSV
for player_id, player_name in zip(player_ids, player_names):
    soup = fetch_player_stats(player_id, player_name)
    if soup:
        extract_and_save_stats(soup, player_name, player_id)
