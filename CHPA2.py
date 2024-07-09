from os import path
import sys
from plottable import ColumnDefinition, Table
from plottable.cmap import normed_cmap, centered_cmap
import pandas as pd
import numpy as np

sys.path.append(path.abspath("../chart_class"))
from dataframe import DfAnalyzer
from figure import GridFigure
from color import COLOR_DICT
import matplotlib as mpl
import matplotlib.pyplot as plt
from typing import Optional, Tuple, List, Dict
import re

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

D_TEXT = {
    "Value": "销售额",
    "Volume (Std Counting Unit)": "PTD",
    "MOLECULE": "通用名",
    "PRODUCT": "产品",
    "PACKAGE": "产品包装",
    "CORPORATION": "生产企业",
    ("MOLECULE", "CORPORATION"): ("通用名", "生产企业"),
    "TC III": "治疗大类",
    "TC IV": "治疗大类",
    "FDC CLASS": "治疗大类",
    "MAT": "滚动年",
    "MQT": "滚动季",
    "QTR": "季度",
    "VBP": "VBP状态",
    "CLASS": "品类",
    "FORM": "剂型",
}


def extract_strength(text: str) -> Optional[str]:
    matches = re.findall(r"\d+(?:\.\d+)?\s*(?:MG|G|IU|Y)", text)
    if len(matches) > 0:
        return matches[0]
    else:
        return None


def convert_std_volume(df, dimension, target, strength, ratio):
    column_unit = "UNIT"
    column_strength = "STRENGTH"
    unit_std_volume = "PTD"
    column_value = "AMOUNT"
    mask = (
        (df[dimension] == target)
        & (df[column_strength] == strength)
        & (df[column_unit] == unit_std_volume)
    )
    df.loc[mask, column_value] = (df.loc[mask, column_value]) * ratio


class CHPA(DfAnalyzer):
    def plot_overall_performance(
        self,
        index: str,
        unit: Literal["Value", "Volume (Std Counting Unit)", "PTD"] = "Value",
        unit_change: Optional[Literal["十亿", "亿", "百万", "万", "千"]] = None,
        period: Literal["MAT", "QTR"] = "MAT",
        sorter: List[str] = None,
        label_threshold: float = 0.02,
        color_dict: Dict[str, str] = COLOR_DICT,
        width: Optional[float] = 12,
        height: Optional[float] = 5.5,
    ):
        df = (
            self.get_pivot(
                index=index,
                columns=self.date_column,
                values="AMOUNT",
                query_str=f"UNIT=='{unit}' and PERIOD=='{period}'",
            )
            .div(self.unit_change(unit_change))
            .reindex(sorter)
            .dropna()
        )

        if period == "MAT":
            df = df.iloc[:, [-13, -9, -5, -1]]

        # df.to_excel("test.xlsx")
        print(df)

        text_index = D_TEXT.get(index, index)
        text_unit = D_TEXT.get(unit, unit)
        text_period = D_TEXT.get(period)
        text_unit_change = "" if unit_change is None else f" ({unit_change})"

        f = plt.figure(
            FigureClass=GridFigure,
            width=width,
            height=height,
            fontsize=11,
            style={
                "title": (
                    f"{self.name}分{text_index}{text_unit}{text_period}趋势"
                    if df.shape[0] > 1
                    else f"{self.name}{text_unit}{text_period}趋势"
                ),
            },
            color_dict=color_dict,
        )

        if period == "MAT":
            if df.shape[0] > 1:
                label_formatter = "{abs} ({share})"
            else:
                label_formatter = "{abs}"
        else:
            if df.shape[0] > 1:
                label_formatter = "{share}"
            else:
                label_formatter = "{abs}"

        f.plot(
            kind="bar",
            data=df.transpose(),
            ax_index=0,
            style={
                "ylabel": f"{text_period}{text_unit}{text_unit_change}",
                "xticklabel_rotation": 0 if period == "MAT" else 90,
            },
            label_formatter=label_formatter,
            show_gr_text=True if period == "MAT" else False,
            show_total_bar=True if (period == "MAT" and df.shape[0] > 1) else False,
            show_total_label=True if df.shape[0] > 1 else False,
            bar_width=0.5 if period == "MAT" else 0.8,
            label_fontsize=11 if period == "MAT" else 9,
            label_threshold=label_threshold,
        )

        f.save()

        return df

    def plot_overall_performance_dual(
        self,
        index: str,
        unit_change: Optional[
            Tuple[
                Literal["十亿", "亿", "百万", "万", "千"],
                Literal["十亿", "亿", "百万", "万", "千"],
            ]
        ] = None,
        period: Literal["MAT", "QTR"] = "MAT",
        sorter: List[str] = None,
        label_threshold: float = 0.02,
        color_dict: Dict[str, str] = COLOR_DICT,
        width: Optional[float] = 12,
        height: Optional[float] = 5.5,
    ):
        unit1 = "Value"
        unit2 = "PTD"

        df1 = (
            self.get_pivot(
                index=index,
                columns=self.date_column,
                values="AMOUNT",
                query_str=f"UNIT=='{unit1}' and PERIOD=='{period}'",
            )
            .div(self.unit_change(unit_change))
            .reindex(sorter)
        )
        df2 = (
            self.get_pivot(
                index=index,
                columns=self.date_column,
                values="AMOUNT",
                query_str=f"UNIT=='{unit2}' and PERIOD=='{period}'",
            )
            .div(self.unit_change(unit_change))
            .reindex(sorter)
        )
        if period == "MAT":
            df1 = df1.iloc[:, [-13, -9, -5, -1]]
            df2 = df2.iloc[:, [-13, -9, -5, -1]]

        text_index = D_TEXT.get(index, index)
        # text_unit = D_TEXT.get(unit, unit)
        text_period = D_TEXT.get(period)
        text_unit_change = "" if unit_change is None else f" ({unit_change})"

        f = plt.figure(
            FigureClass=GridFigure,
            nrows=1,
            ncols=2,
            wspace=0.1,
            width=width,
            height=height,
            fontsize=11,
            style={
                "title": (
                    f"{self.name}分{text_index}{text_period}趋势"
                    if df1.shape[0] > 1
                    else f"{self.name}{text_period}趋势"
                ),
                "label_outer": True,
                # "show_legend": True,
            },
            color_dict=color_dict,
        )

        if period == "MAT":
            if df1.shape[0] > 1:
                label_formatter = "{abs}\n({share})"
            else:
                label_formatter = "{abs}"
        else:
            df1.to_excel("test1.xlsx")
            df2.to_excel("test2.xlsx")
            df1 = df1.div(df1.sum()).iloc[:,-9:]
            df2 = df2.div(df2.sum()).iloc[:, -9:]
            if df1.shape[0] > 1:
                label_formatter = "{share}"
            else:
                label_formatter = "{abs}"

        for i, df in enumerate([df1, df2]):
            f.plot(
                kind="bar" if period == "MAT" else "line",
                fmt="{:,.0%}" if period == "QTR" else "{:,.0f}",
                data=df.transpose(),
                ax_index=i,
                style={
                    "title": "金额" if i == 0 else "PTD",
                    "ylabel": f"{text_period}{text_unit_change}" if period == "MAT" else "份额",
                    "show_legend": True if i != 0 else False,
                    "xticklabel_rotation": 0 if period == "MAT" else 90,
                },
                label_formatter=label_formatter,
                show_gr_text=True if period == "MAT" else False,
                show_total_bar=True if (period == "MAT" and df.shape[0] > 1) else False,
                show_total_label=True if df.shape[0] > 1 else False,
                bar_width=0.5 if period == "MAT" else 0.8,
                label_fontsize=10,
                label_threshold=label_threshold,
                # show_label=df.index,
            )

        f.save(tight_layout=False)

        return df

    def plot_trend_with_gr(
        self,
        index: str,
        unit: Literal["Value", "Volume (Std Counting Unit)"] = "Value",
        unit_change: Optional[Literal["十亿", "亿", "百万", "万", "千"]] = None,
        period: Literal["MAT", "QTR"] = "MAT",
        sorter: List[str] = None,
        label_threshold: float = 0.02,
        color_dict: Dict[str, str] = None,
        width: float = 15,
        height: float = 6,
    ):
        df = (
            self.get_pivot(
                index=index,
                columns=self.date_column,
                values="AMOUNT",
                query_str=f"UNIT=='{unit}' and PERIOD=='{period}'",
            )
            .div(self.unit_change(unit_change))
            .reindex(sorter)
        )

        if period == "MAT":
            df = df.iloc[:, [-13, -9, -5, -1]]

        print(df)

        text_index = D_TEXT.get(index, index)
        text_unit = D_TEXT.get(unit, unit)
        text_period = D_TEXT.get(period)
        text_unit_change = "" if unit_change is None else f" ({unit_change})"

        f = plt.figure(
            FigureClass=GridFigure,
            width=width,
            height=height,
            fontsize=11,
            style={
                "title": (
                    f"{self.name}分{text_index}{text_unit}{text_period}趋势"
                    if index is not None
                    else f"{self.name}{text_unit}{text_period}趋势"
                ),
            },
            color_dict=color_dict,
        )

        f.plot(
            kind="bar",
            data=df.transpose(),
            ax_index=0,
            style={
                "ylabel": f"{text_period}{text_unit}{text_unit_change}",
                "xticklabel_rotation": 90 if period == "QTR" else 0,
            },
            label_threshold=label_threshold,
            show_gr_line=True,
            period_change=4 if period == "QTR" else 1,
        )

        f.save()

        return df

    def plot_size_diff(
        self,
        index: str,
        hue: Optional[str] = None,
        focus: Optional[List[str]] = None,
        date: Optional[str] = None,
        unit: Literal["Value", "Volume (Std Counting Unit)"] = "Value",
        unit_change: Optional[Literal["十亿", "亿", "百万", "万", "千"]] = None,
        period: Literal["MAT", "QTR"] = "MAT",
        xlim: Optional[Tuple[float, float]] = None,
        ylim: Optional[Tuple[float, float]] = None,
        label_limit: int = 15,
        label_topy: int = 3,
    ):
        df = self.ptable(
            index=[index, hue] if hue is not None else index,
            date=date,
            values="AMOUNT",
            query_str=f"UNIT=='{unit}' and PERIOD=='{period}'",
        ).div(self.unit_change(unit_change))

        if hue is not None:
            df = df.reset_index().set_index(index)

        df = df.loc[
            :,
            [hue, "表现", "同比净增长"] if hue is not None else ["表现", "同比净增长"],
        ]

        print(df)

        text_index = D_TEXT.get(index, index)
        text_date = self.date.strftime(self._strftime) if date is None else date
        text_unit = D_TEXT.get(unit, unit)
        text_period = D_TEXT.get(period)
        text_unit_change = "" if unit_change is None else f" ({unit_change})"

        f = plt.figure(
            FigureClass=GridFigure,
            width=15,
            height=6,
            fontsize=11,
            style={
                "title": f"{self.name}{text_index}{text_period}{text_unit}绝对值 vs. 净增长",
            },
        )

        f.plot(
            kind="bubble",
            data=df,
            ax_index=0,
            style={
                "xlabel": f"{self.name}{text_period}{text_unit}{text_unit_change}",
                "ylabel": f"{text_period}{text_unit}同比净增长{text_unit_change}",
            },
            x="表现",
            y="同比净增长",
            z="表现",
            hue=hue,
            focus=focus,
            y_avg=0,
            label_limit=label_limit,
            label_topy=label_topy,
            x_fmt="{:,.0f}",
            y_fmt="{:+,.0f}",
            xlim=xlim,
            ylim=ylim,
        )

        f.save()

        return df

    def plot_share_gr(
        self,
        index: str,
        hue: Optional[str] = None,
        focus: Optional[List[str]] = None,
        date: Optional[str] = None,
        unit: Literal["Value", "Volume (Std Counting Unit)"] = "Value",
        period: Literal["MAT", "QTR"] = "MAT",
        xlim: Optional[Tuple[float, float]] = None,
        ylim: Optional[Tuple[float, float]] = None,
        label_limit: int = 15,
        label_topy: int = 3,
    ):
        df = self.ptable(
            index=[index, hue] if hue is not None else index,
            date=date,
            values="AMOUNT",
            query_str=f"UNIT=='{unit}' and PERIOD=='{period}'",
        )

        if hue is not None:
            df = df.reset_index().set_index(index)

        avg_gr = df["表现"].sum() / (df["表现"].subtract(df["同比净增长"]).sum()) - 1

        df = df.loc[
            :,
            [hue, "份额", "同比增长率"] if hue is not None else ["份额", "同比增长率"],
        ]

        text_index = D_TEXT.get(index, index)
        text_date = self.date.strftime(self._strftime) if date is None else date
        text_unit = D_TEXT.get(unit, unit)
        text_period = D_TEXT.get(period)

        df.replace({np.inf: 0, -np.inf: 0, np.nan:0}, inplace=True)
        f = plt.figure(
            FigureClass=GridFigure,
            width=15,
            height=6,
            fontsize=11,
            style={
                "title": f"{self.name}{text_index}{text_period}{text_unit}份额 vs. 同比增长率",
            },
        )

        f.plot(
            kind="bubble",
            data=df,
            ax_index=0,
            style={
                "xlabel": f"{self.name}{text_period}{text_unit}份额",
                "ylabel": f"{text_period}{text_unit}同比增长率",
            },
            x="份额",
            y="同比增长率",
            z="份额",
            hue=hue,
            focus=focus,
            y_avg=avg_gr,
            label_limit=label_limit,
            label_topy=label_topy,
            x_fmt="{:.1%}",
            y_fmt="{:+,.1%}",
            xlim=xlim,
            ylim=ylim,
        )

        f.save()

        return df

    def plot_share_trend(
        self,
        index: str,
        unit: Literal["Value", "Volume (Std Counting Unit)"] = "Value",
        period: Literal["MAT", "QTR"] = "MAT",
        focus: Optional[str] = None,
        topn: int = 10,
        width: float = 16,
        height: float = 7,
    ):
        df = self.get_pivot(
            index=index,
            columns=self.date_column,
            values="AMOUNT",
            query_str=f"UNIT=='{unit}' and PERIOD=='{period}'",
            perc="columns",
        )

        df_topn = df.head(topn)
        if focus not in df_topn.index and focus is not None:
            df_topn = df_topn.append(df.loc[focus, :])

        text_index = D_TEXT.get(index, index)
        text_unit = D_TEXT.get(unit, unit)
        text_period = D_TEXT.get(period)
        text_topn = f"TOP{topn}" if df.shape[0] > topn else ""

        f = plt.figure(
            FigureClass=GridFigure,
            width=width,
            height=height,
            fontsize=11,
            style={
                "title": f"{self.name}{text_topn}{text_index}{text_period}{text_unit}趋势",
            },
        )

        print(df_topn.transpose())
        f.plot(
            kind="line",
            data=df_topn.transpose(),
            ax_index=0,
            fmt="{:,.1%}",
            show_label=df_topn.transpose().columns,
            endpoint_label_only=True,
            style={"major_grid": {}, "xticklabel_rotation": 90, "remove_yticks": True},
        )

        f.save()

        return df

    def plottable_annual(
        self,
        index: str,
        unit: Literal["Value", "Volume (Std Counting Unit)"] = "Value",
        period: Literal["MAT", "QTR"] = "MAT",
        focus: Optional[str] = None,
        topn: int = 20,
        width: int = 28,
        height: int = 10,
        fontsize: Optional[float] = None,
    ):
        df_combined = pd.DataFrame()
        l_date = []
        cmap = {}
        for i in range(4):
            result = self.get_pivot(
                index=index,
                columns=self.date_column,
                values="AMOUNT",
                query_str=f"UNIT=='{unit}' and PERIOD=='{period}'",
            ).iloc[:, i * 4 - 13]
            result.index.name = D_TEXT.get(index, index)

            text_index = D_TEXT.get(index, index)
            text_date = result.name
            text_unit = D_TEXT.get(unit, unit)
            text_period = D_TEXT.get(period)

            rank = result.rank(ascending=False, method="first")
            share = result.div(result.sum())
            df = pd.concat([rank, result, share], axis=1)
            df.reset_index(inplace=True)
            df.columns = [
                f"{text_index}_{text_date}",
                "排名",
                f"{text_unit}_{text_date}",
                f"份额_{text_date}",
            ]
            df.set_index("排名", inplace=True)
            df.sort_index(inplace=True)
            df.index = df.index.map("{:.0f}".format)
            df_combined = pd.concat([df_combined, df], axis=1)
            cmap[text_date] = normed_cmap(
                df[f"份额_{text_date}"], cmap=mpl.cm.PiYG, num_stds=2.5
            )

            l_date.append(text_date)

        col_defs = (
            [
                ColumnDefinition(
                    name=f"{text_index}_{date}",
                    title=text_index,
                    textprops={"ha": "center"},
                    group=f"{text_period}{date}{text_unit}",
                    width=1.5,
                    border="left",
                )
                for date in l_date
            ]
            + [
                ColumnDefinition(
                    name=f"{text_unit}_{date}",
                    title=text_unit,
                    textprops={"ha": "right"},
                    formatter="{:,.0f}",
                    group=f"{text_period}{date}{text_unit}",
                )
                for date in l_date
            ]
            + [
                ColumnDefinition(
                    name=f"份额_{date}",
                    title="份额",
                    textprops={
                        "ha": "right",
                        "bbox": {"boxstyle": "round", "pad": 0.3},
                    },
                    formatter="{:.1%}",
                    width=0.5,
                    group=f"{text_period}{date}{text_unit}",
                    cmap=cmap[date],
                )
                for date in l_date
            ]
        )

        plt.rcParams["font.family"] = ["Microsoft YaHei"]
        plt.rcParams["savefig.bbox"] = "tight"

        fig, ax = plt.subplots(figsize=(width, height))

        title = f"{self.name}历年{text_index}{text_unit}排名"
        fig.suptitle(title, fontsize=22)

        table = Table(
            df_combined.head(topn),
            column_definitions=col_defs,
            row_dividers=True,
            footer_divider=True,
            ax=ax,
            textprops={
                "fontsize": (
                    42 / np.log(df.head(topn).shape[0])
                    if fontsize is None
                    else fontsize
                ),
            },
            even_row_color="#eeeeee",
            row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))},
            col_label_divider_kw={"linewidth": 1, "linestyle": "-"},
            col_label_cell_kw={"height": 2},
            column_border_kw={"linewidth": 1, "linestyle": "-"},
        ).autoset_fontcolors(colnames=None)

        # if focus is not None:
        #     focus_rindex = df.index.get_loc(focus)
        #     if focus_rindex <= 20:
        #         table.rows[focus_rindex].set_facecolor("lightcyan")

        fig.savefig(
            f"plots/{title}.png",
            facecolor=ax.get_facecolor(),
            dpi=400,
        )

        return df_combined

    def plottable_latest(
        self,
        index: str,
        hue: Optional[str] = None,
        unit: Literal["Value", "Volume (Std Counting Unit)"] = "Value",
        period: Literal["MAT", "QTR"] = "MAT",
        date: Optional[str] = None,
        focus: Optional[str] = None,
        topn: int = 20,
        width: int = 28,
        height: int = 10,
        fontsize: Optional[float] = None,
        show_total: bool = False,
    ):
        df = self.ptable(
            index=index,
            hue=hue,
            date=date,
            values="AMOUNT",
            query_str=f"UNIT=='{unit}' and PERIOD=='{period}'",
            fillna=False,
            show_total=show_total,
        )

        df.replace({np.inf: 0, -np.inf: np.nan}, inplace=True)
        print(df)

        df.index.name = D_TEXT.get(index, index)

        text_index = D_TEXT.get(index, index)
        text_date = self.date.strftime(self._strftime) if date is None else date
        text_unit = D_TEXT.get(unit, unit)
        text_period = D_TEXT.get(period)
        text_topn = f"TOP{topn}" if df.shape[0] > topn else ""

        cmap_share = normed_cmap(df["份额"].fillna(0), cmap=mpl.cm.PiYG)
        cmap_share_diff = centered_cmap(
            df["份额变化"].fillna(0), cmap=mpl.cm.PiYG, center=0
        )
        cmap_ei = centered_cmap(
            df["同比增长率"].fillna(0), cmap=mpl.cm.PiYG, center=100
        )

        col_defs = (
            [
                ColumnDefinition(
                    name="排名",
                    title="排名",
                    textprops={"ha": "center"},
                    width=0.5,
                    border="left",
                    formatter="{:,.0f}",
                )
            ]
            + [
                ColumnDefinition(
                    name="TC III",
                    title="类别",
                    textprops={"ha": "center"},
                    width=1,
                )
            ]
            + [
                ColumnDefinition(
                    name="VBP",
                    title="VBP状态",
                    textprops={"ha": "center"},
                    width=1,
                )
            ]
            + [
                ColumnDefinition(
                    name="MOLECULE",
                    title="通用名",
                    textprops={"ha": "center"},
                    width=1,
                )
            ]
            + [
                ColumnDefinition(
                    name="CORPORATION",
                    title="生产企业",
                    textprops={"ha": "center"},
                    width=1,
                )
            ]
            + [
                ColumnDefinition(
                    name="表现",
                    title=f"{text_period}{text_unit}",
                    textprops={"ha": "right"},
                    formatter="{:,.0f}",
                )
            ]
            + [
                ColumnDefinition(
                    name="同比净增长",
                    title="同比净增长",
                    textprops={"ha": "right"},
                    formatter="{:,.0f}",
                    text_cmap=lambda x: "red" if x < 0 else "black",
                )
            ]
            + [
                ColumnDefinition(
                    name="份额",
                    title="份额",
                    textprops={
                        "ha": "right",
                        "bbox": {"boxstyle": "round", "pad": 0.3},
                    },
                    formatter="{:.1%}",
                    width=1,
                    cmap=cmap_share,
                )
            ]
            + [
                ColumnDefinition(
                    name="份额变化",
                    title="份额变化",
                    textprops={
                        "ha": "right",
                        # "bbox": {"boxstyle": "round", "pad": 0.3},
                    },
                    formatter="{:+.1%}",
                    width=1,
                    text_cmap=lambda x: "red" if x < 0 else "black",
                    # cmap=cmap_share_diff,
                )
            ]
            + [
                ColumnDefinition(
                    name="同比增长率",
                    title="同比增长率",
                    textprops={
                        "ha": "right",
                    },
                    formatter="{:+.1%}",
                    width=1,
                    text_cmap=lambda x: "red" if x < 0 else "black",
                )
            ]
            + [
                ColumnDefinition(
                    name="EI",
                    title="EI",
                    textprops={
                        "ha": "center",
                        "bbox": {"boxstyle": "round", "pad": 0.3},
                    },
                    formatter="{:,.0f}",
                    width=1,
                    cmap=cmap_ei,
                )
            ]
        )

        if hue is not None:
            col_defs = col_defs + [
                ColumnDefinition(
                    name=hue,
                    title=D_TEXT.get(hue, hue),
                    textprops={
                        "ha": "center",
                    },
                    width=1,
                )
            ]

        plt.rcParams["font.family"] = ["Microsoft YaHei"]
        plt.rcParams["savefig.bbox"] = "tight"

        fig, ax = plt.subplots(figsize=(width, height))

        title = (
            f"{self.name}{text_date}{text_period}{text_topn}{text_index}{text_unit}明细"
        )
        fig.suptitle(title, fontsize=22)

        # df.head(topn).to_excel(f"plots/{title}.xlsx")
        print(df.head(topn))
        table = Table(
            df.head(topn),
            column_definitions=col_defs,
            row_dividers=True,
            footer_divider=True,
            ax=ax,
            textprops={
                "fontsize": (
                    42 / np.log(df.head(topn).shape[0])
                    if fontsize is None
                    else fontsize
                ),
            },
            even_row_color="#eeeeee",
            row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))},
            col_label_divider_kw={"linewidth": 1, "linestyle": "-"},
            col_label_cell_kw={"height": 2},
            column_border_kw={"linewidth": 1, "linestyle": "-"},
        ).autoset_fontcolors(colnames=["份额", "EI"])

        if focus is not None:
            if isinstance(focus, str):
                focus = [focus]
            for item in focus:
                focus_rindex = df.index.get_loc(item)
                if focus_rindex <= topn -1:
                    table.rows[focus_rindex].set_facecolor("lightcyan")

        if show_total:
            table.rows[df.head(topn).shape[0] - 1].set_facecolor("azure")

        fig.savefig(
            f"plots/{title}.png",
            facecolor=ax.get_facecolor(),
            dpi=400,
        )
        print(f"plots/{title}.png saved.")

        return df
