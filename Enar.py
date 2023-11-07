import pandas as pd
from os import path
import sys
from plottable import ColumnDefinition, Table
from plottable.cmap import normed_cmap, centered_cmap
import pandas as pd
import numpy as np


sys.path.append(path.abspath("../chart_class"))
from figure import GridFigure
import matplotlib as mpl
import matplotlib.pyplot as plt
from typing import Optional, Tuple, List

if __name__ == "__main__":
    df = pd.read_excel("data.xlsx")
    print(df)
    df["信立坦销售"] = df["信立坦销售"].apply(lambda x: np.log(x) if x != 0 else 0)
    df["肾性贫血市场潜力"] = df["肾性贫血市场潜力"].apply(lambda x: np.log(x) if x != 0 else 0)
    df["系数"] = df["肾性贫血市场潜力"].div(df["信立坦销售贡献"]).apply(lambda x: np.log(x) if x != 0 else 0)
    df["bubble_size"] = 1
    df.set_index("城市", inplace=True)
    print(df)
    f = plt.figure(
        FigureClass=GridFigure,
        width=15,
        height=6,
        fontsize=9,
        style={
            "title": "各城市信立坦销售 vs. 肾性贫血市场潜力",
        },
    )

    f.plot(
        kind="bubble",
        data=df,
        ax_index=0,
        style={
            "xlabel": "肾性贫血市场潜力（取对数）",
            "ylabel": "系数（取对数）",
        },
        x="肾性贫血市场潜力",
        y="系数",
        z="bubble_size",
        hue="事业部",
        bubble_scale=0.01,
        # y_avg=0,
        label_limit=50,
        label_topy=50,
        x_fmt="{:.0f}",
        y_fmt="{:.0f}",
    )

    f.save()
