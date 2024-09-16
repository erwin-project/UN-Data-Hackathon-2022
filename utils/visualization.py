import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils import machine_learning as ml


def visualization_data(dataset, x_label, y_label, x_title, y_title, title):
    x = dataset[x_label].values
    y = dataset[y_label].values
    b, a = ml.linear_regression(x, y)
    y_pred = b + a * x

    fig, ax = plt.subplots(1, figsize=(12, 10))
    sns.set(rc={'axes.facecolor': '#33FFA2'})
    sns.lineplot(dataset.set_index(x_label)[y_label],
                 ax=ax)
    ax.plot(x, y_pred, color="r")
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.set_title(title)

    return fig, ax


def chart_pie(recipe, data, kind):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:

    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    wedges, texts = ax.pie(data,
                           explode=(0, 0.1, 0),
                           wedgeprops=dict(width=0.5),
                           startangle=-40)

    bbox_props = dict(boxstyle="square,pad=0.3",
                      fc="w",
                      ec="k",
                      lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-",
                              color="black"),
              bbox=bbox_props,
              zorder=0,
              c="black",
              va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontal_alignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connection_style = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connection_style})
        ax.annotate(str(data[i]) + " commodity \n have " + recipe[i],
                    xy=(x, y),
                    fontsize=5,
                    xytext=(1.3 * np.sign(x), 1.4 * y),
                    horizontalalignment=horizontal_alignment, **kw)

    ax.set_title(str("The Graph of " + kind + " Rate Production"))

    return fig, ax
