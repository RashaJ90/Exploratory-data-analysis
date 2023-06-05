from scipy.stats import kurtosis
from scipy.stats import skew
import numpy as np
import pandas as pd
from geopandas import GeoDataFrame
from tabulate import tabulate
from IPython.display import display, Math
from create_dataset import create_dataset
from visualize import *

def main():
    # CLean Data:
    fifa_df = create_dataset()
    print(fifa_df.info())# change if column type is wrong!!
    # Count NaN values per columns:
    fifa_nan_cols = fifa_df.isna().sum()
    """
        Since only Club and Continent columns has Nan values, we will not delete the Nan rows,
        it will not affect our performance analysis of these players.
        One approach for visualization of these columns is to do padding to clubs and Continent, only if needed!
    """
    # Divide the DF to three specified DF's:
    fifa_players_info = fifa_df.iloc[:, 1:11]
    # cols:['Name', 'Age', 'Nationality', 'Continent', 'Overall', 'Potential', 'Club', 'League', 'Value', 'Wage']
    fifa_players_attribures = fifa_df.iloc[:, [1, 6] + list(range(11, 45))]
    # cols:['Name', 'Potential', 'Acceleration', 'Aggression', 'Agility', 'Balance',
    #        'Ball.control', 'Composure', 'Crossing', 'Curve', 'Dribbling',
    #        'Finishing', 'Free.kick.accuracy', 'GK.diving', 'GK.handling',
    #        'GK.kicking', 'GK.positioning', 'GK.reflexes', 'Heading.accuracy',
    #        'Interceptions', 'Jumping', 'Long.passing', 'Long.shots', 'Marking',
    #        'Penalties', 'Positioning', 'Reactions', 'Short.passing', 'Shot.power',
    #        'Sliding.tackle', 'Sprint.speed', 'Stamina', 'Standing.tackle',
    #        'Strength', 'Vision', 'Volleys']
    fifa_players_positions = fifa_df.iloc[:, [1, 6] + list(range(45, 72))]
    # cols:['Name', 'Potential', 'CAM', 'CB', 'CDM', 'CF', 'CM', 'LAM', 'LB', 'LCB',
    #        'LCM', 'LDM', 'LF', 'LM', 'LS', 'LW', 'LWB', 'RAM', 'RB', 'RCB', 'RCM',
    #        'RDM', 'RF', 'RM', 'RS', 'RW', 'RWB', 'ST', 'Preferred.Positions']

    # Players Age distibution:
    ggplot_geombar(data=fifa_df, params={"x": "Age", "xlab": "Players Age", "ylab": "Count", "title": ""})
    # Players Overall ability by Leagues: Spain LIga has the highest median of overall ability players
    ggplot_boxplot(data=fifa_df,
                   params={"x": "League", "y": "Overall", "xlab": "League", "ylab": "Overall", "title": ""})
    # Players Wage Density[log-scale]: Most players get paid between 1k-10k
    ggplot_density_log(data=fifa_df, params={"x": "Wage", "title": ""})

    # Skewness + Kurtosis to measure the Wage dist.:
    players_Wage = np.array(fifa_df[fifa_df["Wage"] > 0]["Wage"])
    wage_skew, wage_skew_log = skew(players_Wage), skew(np.log(players_Wage)) #  more weight in the left tail of the distribution.
    wage_kurt, wage_kurt_log = kurtosis(players_Wage, fisher=True),  kurtosis(np.log(players_Wage), fisher=True)

    # Better see the tails:
    qq_plots(data=players_Wage)
    qq_plots(data=np.log(players_Wage))

    # 10-best players by Value and Overall
    best_10_by_value = fifa_players_info.sort_values(by=['Value'], ascending=False).iloc[:10, :]
    best_10_by_overall = fifa_players_info.sort_values(by=['Overall'], ascending=False).iloc[:10, :]
    # 7 out of the top-10 players with the highest value also the best players in terms of overall ability
    best_common = best_10_by_value.reset_index().merge(best_10_by_overall).set_index('index')
    best_players = best_common.Name
    display(best_players)

    # 10-best Clubs and Worst in Overall:
    club_grouped_df = fifa_players_info.groupby('Club', as_index=False)['Overall'].mean().sort_values(by=['Overall'], ascending=False)
    best_clubs = club_grouped_df.iloc[:10,:]
    print(tabulate(best_clubs, headers='keys', tablefmt='psql'))
    worst_clubs = club_grouped_df.iloc[-10:,:].sort_values(by=['Overall'])
    print(tabulate(worst_clubs, headers='keys', tablefmt='psql'))

    # world map by players number and Overall mean:
    world = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres')
    )
    nationality_grouped_df = fifa_players_info.groupby(['Nationality']).size().reset_index(name='counts')
    nationality_world = GeoDataFrame(nationality_grouped_df.merge(world, right_on='name', left_on='Nationality'))
    world_map(data=nationality_world, params={"col": "counts", "title": "# of Players by Country"})

    nationality_overall_grouped_df = fifa_players_info.groupby(['Nationality'])['Overall'].mean().reset_index(name='mean')
    nationality_overall_world = GeoDataFrame(nationality_overall_grouped_df.merge(world, right_on='name', left_on='Nationality'))
    world_map(data=nationality_overall_world, params={"col": "mean", "title": "Players Overall mean by Country"})

    joined_by_country = pd.merge(nationality_grouped_df, nationality_overall_grouped_df).rename(columns={'mean': "Overall_ability_mean"})
    print(tabulate(joined_by_country[(joined_by_country.counts < 20) & (joined_by_country.Overall_ability_mean > 70)].sort_values(by=['Overall_ability_mean'], ascending=False), headers='keys', tablefmt='psql'))



if __name__ == "__main__":
    main()
