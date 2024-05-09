import PySimpleGUI as sg
import data_cleaning
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np


def gradient_boosting_regression():
    df = data_cleaning.cleandata()

    franchIDs = df['franchID'].unique().tolist()
    stats = ['W', 'L', 'R', 'AB', 'H', '2B', '3B', 'HR', 'BB', 'SO', 'SB', 'CS', 'RA', 'ER', 'ERA', 'CG', 'SHO', 'SV',
             'HA', 'HRA', 'BBA', 'SOA', 'E', 'DP', 'attendance', 'BPF', 'PPF']

    layout = [
        [sg.Text('Select Franchise ID:', size=(20, 1)),
         sg.Combo(franchIDs, key='FRANCHID', size=(20, 1), expand_x=True)],
        [sg.Text('Select Statistic:', size=(20, 1)), sg.Combo(stats, key='STAT', size=(20, 1), expand_x=True)],
        [sg.Button('Predict', size=(10, 1)), sg.Stretch(), sg.Exit(size=(10, 1))],
        [sg.Text('Prediction:', key='PREDICTION', size=(40, 2), expand_x=True)]
    ]

    window_size = (500, 150)

    window = sg.Window('Gradient Boosting Regression Prediction', layout, size=window_size, resizable=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Predict':
            team = values['FRANCHID']
            stat = values['STAT']
            df_team = df[df['franchID'] == team]
            X = df_team['yearID'].values.reshape(-1, 1)
            y = df_team[stat].values

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
            model.fit(X_train, y_train)

            future_years = np.array([[2024]])
            predicted_stat = model.predict(future_years)
            predicted_stat_rounded_up = np.ceil(predicted_stat).astype(int)

            prediction_text = f"Predicted {stat}s for {team} in 2024: {predicted_stat_rounded_up[0]}"
            window['PREDICTION'].update(prediction_text)

    window.close()
