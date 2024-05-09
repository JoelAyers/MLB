import PySimpleGUI as sg  # Importing PySimpleGUI for GUI
import data_cleaning  # Importing custom module for data cleaning
from sklearn.model_selection import train_test_split  # Importing train_test_split function
from sklearn.ensemble import RandomForestRegressor  # Importing RandomForestRegressor
import numpy as np  # Importing numpy for numerical operations


# Function for performing random forest regression
def random_forest_regression():
    # Clean data using custom function
    df = data_cleaning.cleandata()

    # List of unique franchise IDs
    franchIDs = df['franchID'].unique().tolist()

    # List of baseball statistics
    stats = ['W', 'L', 'R', 'AB', 'H', '2B', '3B', 'HR', 'BB', 'SO', 'SB', 'CS', 'RA', 'ER', 'ERA', 'CG', 'SHO', 'SV',
             'HA', 'HRA', 'BBA', 'SOA', 'E', 'DP', 'attendance', 'BPF', 'PPF']

    # Mapping of franchise IDs to image file names
    image_map = {
        'ANA': 'Angels.gif',
        'ARI': 'DiamondBacks.gif',
        'ATL': 'Braves.gif',
        'BAL': 'Orioles.gif',
        'BOS': 'RedSox.gif',
        'CHC': 'Cubs.gif',
        'CHW': 'WhiteSox.gif',
        'CIN': 'Reds.gif',
        'CLE': 'Guardians.gif',
        'COL': 'Rockies.gif',
        'DET': 'Tigers.gif',
        'FLA': 'Marlins.gif',
        'HOU': 'Astros.gif',
        'KCR': 'Royals.gif',
        'LAD': 'Dodgers.gif',
        'MIL': 'Brewers.gif',
        'MIN': 'Twins.gif',
        'NYM': 'Mets.gif',
        'NYY': 'Yankees.gif',
        'OAK': 'Athletics.gif',
        'PHI': 'Phillies.gif',
        'PIT': 'Pirates.gif',
        'SDP': 'Padres.gif',
        'SEA': 'Mariners.gif',
        'SFG': 'Giants.gif',
        'STL': 'Cardinals.gif',
        'TBR': 'Rays.gif',
        'TEX': 'Rangers.gif',
        'TOR': 'BlueJays.gif',
        'WSN': 'Nationals.gif'
    }

    # Default image path
    default_image_path = 'MLB.gif'

    # GUI layout
    layout = [
        [sg.Text('Type Franchise ID:', size=(20, 1)),
         sg.InputText(size=(20, 1), enable_events=True, key='FRANCHID_INPUT'),
         sg.Listbox(values=franchIDs, size=(20, 4), enable_events=True, key='FRANCHID_LIST'),
         sg.Image(filename=default_image_path, key='IMAGE')],
        [sg.Text('Select Statistic:', size=(20, 1)), sg.Combo(stats, key='STAT', size=(20, 1), expand_x=True)],
        [sg.Button('Predict', size=(10, 1)), sg.Stretch(), sg.Exit(size=(10, 1))],
        [sg.Text('Prediction:', key='PREDICTION', size=(40, 2), expand_x=True)]
    ]

    # Create GUI window
    window = sg.Window('Random Forest Regression Prediction', layout, resizable=True)

    # Event loop
    while True:
        event, values = window.read()

        # Handle window closed or Exit button clicked
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        # Handle input in FRANCHID_INPUT field
        elif event == 'FRANCHID_INPUT':
            input_text = values['FRANCHID_INPUT'].upper()
            filtered_franchises = [fid for fid in franchIDs if input_text in fid]
            window['FRANCHID_LIST'].update(filtered_franchises)
        # Handle selection in FRANCHID_LIST
        elif event == 'FRANCHID_LIST':
            if values['FRANCHID_LIST']:
                selected_id = values['FRANCHID_LIST'][0]
                window['FRANCHID_INPUT'].update(selected_id)
                image_path = image_map.get(selected_id, default_image_path)
                window['IMAGE'].update(filename=image_path)
        # Handle Predict button click
        elif event == 'Predict':
            team = values['FRANCHID_INPUT']
            stat = values['STAT']
            df_team = df[df['franchID'] == team]
            X = df_team['yearID'].values.reshape(-1, 1)
            y = df_team[stat].values

            # Split data into train and test sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Create and train random forest regression model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            # Predict statistic for future year (2024)
            future_years = np.array([[2024]])
            predicted_stat = model.predict(future_years)
            predicted_stat_rounded_up = np.ceil(predicted_stat).astype(int)

            # Update prediction text in GUI
            prediction_text = f"Predicted {stat}s for {team} in 2024: {predicted_stat_rounded_up[0]}"
            window['PREDICTION'].update(prediction_text)

    # Close GUI window
    window.close()
