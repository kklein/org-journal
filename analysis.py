from math import ceil
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from orgparse import load

WEEK_ROOT = Path("/Users/kevin/org/weeks")
PROPERTIES = [
    "Sleep",
    "Exercise",
    "Happiness",
    "Wellbeing",
    "Eating",
    "Stress",
    "Fasting",
]
MAX_WEEK = 8
FIRST_WEEKDAY_INDEX = 3


def load_data(
    max_week: int = MAX_WEEK,
    week_root: Path = WEEK_ROOT,
    first_weekday_index: int = FIRST_WEEKDAY_INDEX,
) -> pd.DataFrame:
    values = {}
    for week in range(1, max_week + 1):
        root = load(week_root / f"{week}.org")
        for child_index in range(first_weekday_index, first_weekday_index + 7):
            day_values = root.children[child_index].properties
            day_values.update({"week": week})
            day = (week - 1) * 7 + (child_index - first_weekday_index)
            values[day] = day_values

    df = pd.DataFrame(values)
    return df.transpose()


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.replace("x", np.nan)
    df = df.astype(np.float16)
    for property in PROPERTIES:
        averages = df.groupby("week")[property].mean().reset_index()
        df = df.merge(averages, on="week", suffixes=["", "_weekly"])
    return df


def plot_histograms(df: pd.DataFrame, columns: list[str] = PROPERTIES) -> None:
    fig, ax = plt.subplots()
    df[columns].hist(ax=ax)
    fig.show()


def plot_trends(
    df: pd.DataFrame, columns: list[str] = PROPERTIES, n_plot_cols: int = 4
) -> None:
    fig, axs = plt.subplots(ceil(len(columns) / n_plot_cols), n_plot_cols)
    axis_counter = 0
    df2 = df.reset_index()
    for property in PROPERTIES:
        ax = axs[axis_counter // n_plot_cols][axis_counter % n_plot_cols]
        df2.plot(x="index", y=property, ax=ax)
        df2.plot(x="index", y=f"{property}_weekly", ax=ax)
        axis_counter += 1
        if property != "Fasting":
            ax.set_ylim([0.0, 5.0])
    fig.show()


df_raw = load_data()
df = process_data(df_raw)
plot_histograms(df)
plot_trends(df)
