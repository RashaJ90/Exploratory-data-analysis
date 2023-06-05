from plotnine import *
import statsmodels.api as sm
from matplotlib import pyplot as plt
import geopandas
import mapclassify


def ggplot_geombar(data, params: dict):
    p = ggplot(data=data) + aes(x=params['x']) + geom_bar() + xlab(params['xlab']) + ylab(params['ylab']) + labs(
        title=params['title']) + theme_seaborn()
    return p


def ggplot_boxplot(data, params: dict):
    p = ggplot(data=data) + aes(x=params['x'], y=params['y'], color=params['y']) + geom_boxplot() + xlab(
        params['xlab']) + ylab(
        params['ylab']) + labs(title=params['title']) + theme_seaborn()
    # theme(axis.text.x = element_text(face = "bold", size = 10, angle = -50, hjust = 0))
    return p


def ggplot_density_log(data, params: dict):
    p = ggplot(data=data) + aes(x=params["x"]) + scale_x_continuous(trans='log10') + geom_density(alpha=.2,
                                                                                                  fill="#00BFC4") + labs(
        title=params["title"]) + theme_seaborn()
    return p


def qq_plots(data):
    p = sm.qqplot(data, line='s')
    plt.show()
    return p


def world_map(data, params: dict):
    fig, ax = plt.subplots(figsize=(10, 4), facecolor=plt.cm.Blues(.2))
    fig.suptitle(params['title'],
                 fontsize='xx-large',
                 fontweight='bold')
    ax.set_facecolor(plt.cm.Blues(.2))
    data.plot(column=params['col'],
              cmap='YlOrRd',
              ax=ax,
              legend=True)

    plt.show()
