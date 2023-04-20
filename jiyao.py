from os import path
import sys
from plottable import ColumnDefinition, Table
from plottable.cmap import normed_cmap
from plottable.plots import bar

sys.path.append(path.abspath("../chart_class"))
from dataframe import DfAnalyzer

from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

# ARB单方
condition_arb = "[TC III] in ('C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药')"


condition = condition_arb
sql = "SELECT * FROM " + table_name + " WHERE " + condition
df = pd.read_sql(sql=sql, con=engine)
# print(df['MOLECULE'].unique())

# for col in ['TC III', 'MOLECULE']:
#     df[col] = df[col].map(d_rename).fillna('其他')

# df['TC III'] = df['TC III'].str.split('|').str[1]
df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
# df["PRODUCT"] = (
#     (df["PRODUCT"].str.split("|").str[0])
#     + "（"
#     + df["PRODUCT"].str.split("|").str[1].str[-3:]
#     + "）"
# )
# df["PRODUCT_CORP"] = (
#     df["PRODUCT_CORP"].str.split("（").str[0].str.split("|").str[0]
#     + "\n"
#     + df["PRODUCT_CORP"].str.split("（").str[1].str.split("|").str[0]
# )
mask = df["MOLECULE"] == "氯沙坦钾"
df.loc[mask, "MOLECULE"] = "氯沙坦"
mask = df["MOLECULE"] == "氯沙坦钾氢氯噻嗪"
df.loc[mask, "MOLECULE"] = "氯沙坦氢氯噻嗪"
mask = df["MOLECULE"] == "奥美沙坦酯氢氯噻嗪"
df.loc[mask, "MOLECULE"] = "奥美沙坦氢氯噻嗪"
mask = df["MOLECULE"] == "培哚普利叔丁胺"
df.loc[mask, "MOLECULE"] = "培哚普利"
mask = df["MOLECULE"] == "贝那普利,氨氯地平"
df.loc[mask, "MOLECULE"] = "贝那普利氨氯地平"
mask = df["MOLECULE"].isin(["氨氯地平贝那普利(II)", "氨氯地平贝那普利"])
df.loc[mask, "MOLECULE"] = "贝那普利氨氯地平"
mask = df["MOLECULE"].isin(
    [
        "厄贝沙坦",
        "缬沙坦",
        "氯沙坦",
        "奥美沙坦",
        "坎地沙坦",
        "厄贝沙坦,氢氯噻嗪",
        "福辛普利",
        "卡托普利",
        "赖诺普利",
        "依那普利",
        "培哚普利",
        "替米沙坦",
        "缬沙坦,氨氯地平",
        "缬沙坦,氢氯噻嗪",
    ]
)
df.loc[mask, "VBP"] = "VBP品种"
mask = (
    df["MOLECULE"].isin(
        [
            "厄贝沙坦",
            "缬沙坦",
            "氯沙坦",
            "奥美沙坦",
            "坎地沙坦",
            "厄贝沙坦,氢氯噻嗪",
            "福辛普利",
            "卡托普利",
            "赖诺普利",
            "依那普利",
            "培哚普利",
            "替米沙坦",
            "缬沙坦,氨氯地平",
            "缬沙坦,氢氯噻嗪",
        ]
    )
    == False
)
df.loc[mask, "VBP"] = "非VBP品种"


mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])

df["STRENGTH"] = df["PACKAGE"].apply(lambda x: x.split()[-2])

convert_std_volume(df, "MOLECULE", "氯沙坦", "100MG", 2)
convert_std_volume(df, "MOLECULE", "厄贝沙坦", "75MG", 0.5)
convert_std_volume(df, "MOLECULE", "替米沙坦", "20MG", 0.25)
convert_std_volume(df, "MOLECULE", "替米沙坦", "40MG", 0.5)
convert_std_volume(df, "MOLECULE", "坎地沙坦", "4MG", 0.5)
convert_std_volume(df, "MOLECULE", "缬沙坦", "40MG", 0.5)
convert_std_volume(df, "MOLECULE", "缬沙坦", "160MG", 2)
convert_std_volume(df, "MOLECULE", "培哚普利", "8MG", 2)
convert_std_volume(df, "MOLECULE", "贝那普利", "5MG", 0.5)
convert_std_volume(df, "MOLECULE", "卡托普利", "12.5MG", 0.25)
convert_std_volume(df, "MOLECULE", "卡托普利", "25MG", 0.5)
convert_std_volume(df, "MOLECULE", "依那普利", "5MG", 0.5)
convert_std_volume(df, "MOLECULE", "雷米普利", "2.5MG", 0.5)
convert_std_volume(df, "MOLECULE", "沙库巴曲缬沙坦", "100MG", 0.5)
convert_std_volume(df, "MOLECULE", "沙库巴曲缬沙坦", "50MG", 0.25)

print(df)

a = DfAnalyzer(df, name="ARB单方市场", date_column="DATE")

for index in ["PRODUCT_CORP", "MOLECULE"]:
    for unit in ["销售金额", "病人治疗天数"]:
        query_unit="Value" if unit == "销售金额" else "Volume (Std Counting Unit)"

        df_combined = pd.DataFrame()
        cmap = {}
        years = ["2019", "2020", "2021", "2022"]
        for i, year in enumerate(years):
            mat = a.get_pivot(
                index=index,
                columns="DATE",
                values="AMOUNT",
                query_str=f"UNIT=='{query_unit}' and PERIOD=='MAT'",
            ).iloc[:, i * 4 - 13]
            rank = mat.rank(ascending=False)
            share = mat.div(mat.sum())
            df = pd.concat([rank, mat, share], axis=1)
            df.columns = [f"排名_{year}", f"年{unit}_{year}", f"份额_{year}"]
            df_combined = pd.concat([df_combined, df], axis=1)
            cmap[year] = normed_cmap(df[f"份额_{year}"], cmap=mpl.cm.PiYG, num_stds=2.5)

        col_defs = (
            [
                ColumnDefinition(
                    name=f"排名_{year}",
                    title="排名",
                    textprops={"ha": "center"},
                    formatter="{:,.0f}",
                    group=f"{year}年{unit}",
                    width=0.5,
                    border="left",
                )
                for year in ["2019", "2020", "2021", "2022"]
            ]
            + [
                ColumnDefinition(
                    name=f"年{unit}_{year}",
                    title=f"年{unit}",
                    textprops={"ha": "right"},
                    formatter="{:,.0f}",
                    group=f"{year}年{unit}",
                )
                for year in ["2019", "2020", "2021", "2022"]
            ]
            + [
                ColumnDefinition(
                    name=f"份额_{year}",
                    title="份额",
                    # plot_fn=bar,
                    # plot_kw={
                    #     "cmap": cmap[year],
                    #     "plot_bg_bar": False,
                    #     "annotate": True,
                    #     "height": 0.5,
                    #     "lw": 0.5,
                    #     "formatter": "{:.1%}",
                    #     "xlim": (0, 0.3),
                    # },
                    textprops={
                        "ha": "right",
                        "bbox": {"boxstyle": "round", "pad": 0.3},
                    },
                    formatter="{:.1%}",
                    group=f"{year}年{unit}",
                    cmap=cmap[year],
                )
                for year in ["2019", "2020", "2021", "2022"]
            ]
        )

        plt.rcParams["font.family"] = ["Microsoft YaHei"]
        plt.rcParams["savefig.bbox"] = "tight"

        # for i in range(0, len(df), 20):
        height = 10 if index == "MOLECULE" else 11
        fig, ax = plt.subplots(figsize=(25, height))

        table = Table(
            df_combined.head(20),
            column_definitions=col_defs,
            row_dividers=True,
            footer_divider=True,
            ax=ax,
            textprops={
                "fontsize": 14,
            },
            even_row_color="#eeeeee",
            row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))},
            col_label_divider_kw={"linewidth": 1, "linestyle": "-"},
            col_label_cell_kw={"height": 2},
            column_border_kw={"linewidth": 1, "linestyle": "-"},
        ).autoset_fontcolors(colnames=None)

        fig.savefig(f"plots/table_{index}_{unit}.png", facecolor=ax.get_facecolor(), dpi=400)