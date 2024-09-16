import numpy as np
import pandas as pd


def linear_regression(x, y):
    # number of observations/points
    n = np.size(x)

    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)

    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y * x) - n * m_y * m_x
    SS_xx = np.sum(x * x) - n * m_x * m_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1 * m_x

    return b_0, b_1


def add_rate(kind):
    data1 = pd.read_excel("data/produktivitas/plantation_fix.xlsx",
                          engine="openpyxl")

    data2 = pd.read_excel("data/produktivitas/rice_fix.xlsx",
                          engine="openpyxl")

    data3 = pd.read_excel("data/produktivitas/vegetables_fix.xlsx",
                          engine="openpyxl")

    data_target = pd.DataFrame(columns=["commodity",
                                        "rate_change"])

    if kind == "All":
        dataset = [data1, data2, data3]
    elif kind == "Plantations":
        dataset = [data1]
    elif kind == "Agriculture":
        dataset = [data2]
    elif kind == "Vegetables":
        dataset = [data3]

    col_1 = []
    rate_change = []

    for data in dataset:
        data_true = data.groupby(["commodity", "year"],
                                 as_index=False).aggregate({'total_productivity': np.sum})
        cols = data_true['commodity'].unique()

        for col in cols:
            data_rate = data_true[data_true["commodity"] == col]
            x = data_rate["year"].values
            y = data_rate["total_productivity"].values
            b, a = linear_regression(x, y)

            col_1.append(col)
            rate_change.append(a)

    data_target["commodity"] = col_1
    data_target["rate_change"] = rate_change

    return data_target
