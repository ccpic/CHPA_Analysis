from CHPA2 import CHPA, convert_std_volume
from sqlalchemy import create_engine
import pandas as pd
from plottable import ColumnDefinition, Table
from plottable.cmap import normed_cmap, centered_cmap
import matplotlib as mpl
import matplotlib.pyplot as plt

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"
# condition = "MOLECULE in ('氢氯吡格雷|CLOPIDOGREL', '氯吡格雷|CLOPIDOGREL')"

condition = "MOLECULE in ('CLOPIDOGREL|氯吡格雷', 'TICAGRELOR|替格瑞洛', 'INDOBUFEN|吲哚布芬') OR PRODUCT='BAYASPIRIN               BAY'"
# condition = "MOLECULE in ('CLOPIDOGREL|氯吡格雷')"
sql = "SELECT * FROM " + table_name + " WHERE " + condition
df = pd.read_sql(sql=sql, con=engine)

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
# df["PRODUCT"] = df["PRODUCT"].str.split("|").str[0]
# df["PRODUCT_CORP"] = (
#     df["PRODUCT_CORP"].str.split("（").str[0].str.split("|").str[0]
#     + "\n"
#     + df["PRODUCT_CORP"].str.split("（").str[1].str.split("|").str[0]
# )
df["STRENGTH"] = df["PACKAGE"].apply(lambda x: x.split()[-2])

mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])

mask = df["PRODUCT"] == "硫酸氢氯吡格雷片"
df.loc[mask, "PRODUCT"] = "帅信/帅泰"
mask = df["PRODUCT"] == "替格瑞洛"
df.loc[mask, "PRODUCT"] = "泰仪"
mask = df["MOLECULE"] == "氢氯吡格雷"
df.loc[mask, "MOLECULE"] = "氯吡格雷"

convert_std_volume(df, "MOLECULE", "氯吡格雷", "25MG", 0.333333)
convert_std_volume(df, "MOLECULE", "替格瑞洛", "90MG", 0.5)
convert_std_volume(df, "MOLECULE", "替格瑞洛", "60MG", 0.5)
convert_std_volume(df, "MOLECULE", "吲哚布芬", "100MG", 0.5)


r = CHPA(df, name="抗血小板市场", date_column="DATE", period_interval=3)

# r.plot_overall_performance(
#     index="MOLECULE",
#     sorter=["替格瑞洛", "氯吡格雷", "阿司匹林", "吲哚布芬"],
#     unit_change="百万",
#     label_threshold=0.01,
# )
# r.plot_overall_performance(
#     index="MOLECULE",
#     sorter=["替格瑞洛", "氯吡格雷", "阿司匹林", "吲哚布芬"],
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
#     label_threshold=0.01,
# )

# r.plot_overall_performance(
#     index="MOLECULE",
#     sorter=["替格瑞洛", "氯吡格雷", "阿司匹林", "吲哚布芬"],
#     unit_change="百万",
#     period="QTR",
#     label_threshold=0.01,
# )
# r.plot_overall_performance(
#     index="MOLECULE",
#     sorter=["替格瑞洛", "氯吡格雷", "阿司匹林", "吲哚布芬"],
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
#     period="QTR",
#     label_threshold=0.01,
# )


# r.plot_size_diff(
#     index="PRODUCT",
#     unit="Value",
#     unit_change="百万",
#     label_limit=10,
# )

# r.plot_size_diff(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
#     label_limit=10,
# )

# r.plot_share_gr(
#     index="PRODUCT",
#     unit="Value",
#     ylim=(-0.5, 1),
#     label_limit=10,
# )
# r.plot_share_gr(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     ylim=(-0.5, 1),
#     label_limit=10,
#     label_topy=4,
# )


# r.plottable_latest(
#     index="PRODUCT", unit="Value", focus="TALCOM (SI6)", hue="CORPORATION"
# )
# r.plottable_latest(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     focus="TALCOM (SI6)",
#     hue="CORPORATION",
# )

# r.plot_share_trend(
#     index="PRODUCT",
#     focus="TALCOM (SI6)"
# )
# r.plot_share_trend(
#     index="PRODUCT",
#     focus="TALCOM (SI6)",
#     unit="Volume (Std Counting Unit)",
# )

# r.plottable_annual(index="PRODUCT", unit="Value")
# r.plottable_annual(index="PRODUCT", unit="Volume (Std Counting Unit)")


D_MAP = {
    "PLAVIX (SG9)": "PLAVIX (SG9)",
    "EN CUN (S1H)": "EN CUN (S1H)",
    "TALCOM (SI6)": "TALCOM (SI6)",
    "SHUAI XIN (LUU)": "SHUAI XIN/SHUAI TAI (LUU)",
    "SHUAI TAI (LUU)": "SHUAI XIN/SHUAI TAI (LUU)",
}
df2 = df[df["MOLECULE"] == "氯吡格雷"]
df2["PRODUCT"] = df2["PRODUCT"].map(D_MAP).fillna("Others") # 注意，这里会影响后续出销售明细

r = CHPA(df2, name="氯吡格雷市场", date_column="DATE", period_interval=3)

# r.plot_overall_performance(
#     index="PRODUCT",
#     unit_change="百万",
#     label_threshold=0.01,
# )
# r.plot_overall_performance(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
#     label_threshold=0.01,
# )

df3 = df[df["MOLECULE"]=="氯吡格雷"]
r = CHPA(df3, name="氯吡格雷市场", date_column="DATE", period_interval=3)

# r.plottable_latest(
#     index="PRODUCT", unit="Value", focus="TALCOM (SI6)", hue="CORPORATION"
# )
# r.plottable_latest(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     focus="TALCOM (SI6)",
#     hue="CORPORATION",
# )

# r.plottable_annual(index="PRODUCT", unit="Value")
# r.plottable_annual(index="PRODUCT", unit="Volume (Std Counting Unit)")

df_combined = pd.DataFrame()
l_date = []
cmap = {}

pivoted = r.get_pivot(index="PRODUCT", columns=r.date_column,values="AMOUNT", query_str=f"UNIT=='Value' and PERIOD=='QTR'" )
result_2021 =  pivoted[['2021-03', '2021-06', '2021-09', "2021-12"]].sum(axis=1)
result_2022 =  pivoted[['2022-03', '2022-06', '2022-09', "2022-12"]].sum(axis=1)
result_2023 =  pivoted[['2023-03', '2023-06']].sum(axis=1)


# for i in range(4):
#     result = self.get_pivot(
#         index=index,
#         columns=self.date_column,
#         values="AMOUNT",
#         query_str=f"UNIT=='{unit}' and PERIOD=='{period}'",
#     ).iloc[:, i * 4 - 13]
#     result.index.name = D_TEXT.get(index, index)

#     text_index = D_TEXT.get(index, index)
#     text_date = result.name
#     text_unit = D_TEXT.get(unit, unit)
#     text_period = D_TEXT.get(period)

#     rank = result.rank(ascending=False, method="first")
#     share = result.div(result.sum())
#     df = pd.concat([rank, result, share], axis=1)
#     df.reset_index(inplace=True)
#     df.columns = [
#         f"{text_index}_{text_date}",
#         "排名",
#         f"{text_unit}_{text_date}",
#         f"份额_{text_date}",
#     ]
#     df.set_index("排名", inplace=True)
#     df.sort_index(inplace=True)
#     df.index = df.index.map("{:.0f}".format)
#     df_combined = pd.concat([df_combined, df], axis=1)
#     cmap[text_date] = normed_cmap(
#         df[f"份额_{text_date}"], cmap=mpl.cm.PiYG, num_stds=2.5
#     )

#     l_date.append(text_date)

# col_defs = (
#     [
#         ColumnDefinition(
#             name=f"{text_index}_{date}",
#             title=text_index,
#             textprops={"ha": "center"},
#             group=f"{text_period}{date}{text_unit}",
#             width=1.5,
#             border="left",
#         )
#         for date in l_date
#     ]
#     + [
#         ColumnDefinition(
#             name=f"{text_unit}_{date}",
#             title=text_unit,
#             textprops={"ha": "right"},
#             formatter="{:,.0f}",
#             group=f"{text_period}{date}{text_unit}",
#         )
#         for date in l_date
#     ]
#     + [
#         ColumnDefinition(
#             name=f"份额_{date}",
#             title="份额",
#             textprops={
#                 "ha": "right",
#                 "bbox": {"boxstyle": "round", "pad": 0.3},
#             },
#             formatter="{:.1%}",
#             width=0.5,
#             group=f"{text_period}{date}{text_unit}",
#             cmap=cmap[date],
#         )
#         for date in l_date
#     ]
# )

# plt.rcParams["font.family"] = ["Microsoft YaHei"]
# plt.rcParams["savefig.bbox"] = "tight"

# fig, ax = plt.subplots(figsize=(width, height))

# title = f"{self.name}历年{text_index}{text_unit}排名"
# fig.suptitle(title, fontsize=22)

# table = Table(
#     df_combined.head(topn),
#     column_definitions=col_defs,
#     row_dividers=True,
#     footer_divider=True,
#     ax=ax,
#     textprops={
#         "fontsize": 42 / np.log(df.head(topn).shape[0]),
#     },
#     even_row_color="#eeeeee",
#     row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))},
#     col_label_divider_kw={"linewidth": 1, "linestyle": "-"},
#     col_label_cell_kw={"height": 2},
#     column_border_kw={"linewidth": 1, "linestyle": "-"},
# ).autoset_fontcolors(colnames=None)

# # if focus is not None:
# #     focus_rindex = df.index.get_loc(focus)
# #     if focus_rindex <= 20:
# #         table.rows[focus_rindex].set_facecolor("lightcyan")

# fig.savefig(
#     f"plots/{title}.png",
#     facecolor=ax.get_facecolor(),
#     dpi=400,
# )