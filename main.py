import data_cleaning
import RandomForrest
import GradientBoost


def main():
    # data = data_cleaning.cleandata()
    # sep_teams = data_cleaning.separate_by_franchid(data)
    # graph_wins = data_cleaning.graph_individual_wins_by_year(sep_teams)
    # graph_losses = data_cleaning.graph_individual_losses_by_year(sep_teams)
    prediction1 = RandomForrest.random_forest_regression()
    # prediction = GradientBoost.gradient_boosting_regression()
    print(prediction1)


if __name__ == "__main__":
    main()
