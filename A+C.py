from CHPA2 import CHPA, convert_std_volume, extract_strength
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from figure import GridFigure
import matplotlib.pyplot as plt

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

condition = (
    "[TC IV] in ('C09B1 ACE INH COMB+A-HYP/DIURET|血管紧张素转换酶掏抑制剂，与抗高血压药（C02）和/或利尿药（C03）联合用药' ,"
    "'C09B3 ACE INHIB COMB+CALC ANTAG|血管紧张素转换酶抑制剂和钙离子拮抗剂(C08)联合用药' ,"
    "'C09D1 AT2 ANTG COMB C2 &/O DIU|血管紧张素II拮抗剂与抗高血压药（C02）和/利尿剂联合用药（C03）' ,"
    "'C09D3 AT2 ANTG COMB CALC ANTAG|血管紧张素II拮抗剂与钙离子拮抗剂(C08)联合用药') "
    "and MOLECULE != '沙库巴曲缬沙坦|SACUBITRIL+VALSARTAN' and MOLECULE !='ENALAPRIL+FOLIC ACID|马来酸依那普利叶酸片'"
)
sql = "SELECT * FROM " + table_name + " WHERE " + condition
print(sql)
df = pd.read_sql(sql=sql, con=engine)

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
df["STRENGTH"] = df["PACKAGE"].apply(extract_strength)
# + '（'+ df['PRODUCT'].str.split('|').str[1].str[-3:] +'）'
# df["PRODUCT_CORP"] = (
#     df["PRODUCT_CORP"].str.split("（").str[0].str.split("|").str[0]
#     + "\n"
#     + df["PRODUCT_CORP"].str.split("（").str[1].str.split("|").str[0]
# )

mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "PTD"
df = pd.concat([df, df_std_volume])

mask = df["MOLECULE"].isin(["奥美沙坦酯氨氯地平片", "舒脈康膜衣錠"])
df.loc[mask, "MOLECULE"] = "奥美沙坦氨氯地平"
mask = df["MOLECULE"].isin(["奥美沙坦酯氢氯噻嗪"])
df.loc[mask, "MOLECULE"] = "奥美沙坦氢氯噻嗪"
mask = df["MOLECULE"].isin(["氯沙坦钾,氢氯噻嗪", "氯沙坦钾氢氯噻嗪"])
df.loc[mask, "MOLECULE"] = "氯沙坦氢氯噻嗪"
mask = df["MOLECULE"] == "培哚普利氨氯地平片(III)"
df.loc[mask, "MOLECULE"] = "培哚普利氨氯地平"
mask = df["MOLECULE"] == "坎地氢噻"
df.loc[mask, "MOLECULE"] = "坎地沙坦氢氯噻嗪"
mask = df["MOLECULE"] == "复方卡托普利"
df.loc[mask, "MOLECULE"] = "卡托普利氢氯噻嗪"
mask = df["MOLECULE"].isin(["氨氯地平贝那普利(II)", "氨氯地平贝那普利"])
df.loc[mask, "MOLECULE"] = "贝那普利氨氯地平"

VBP_LIST = [
    "缬沙坦氨氯地平",
    "厄贝沙坦氢氯噻嗪",
    "缬沙坦氢氯噻嗪",
    "氯沙坦氢氯噻嗪",
    "奥美沙坦氢氯噻嗪",
    "奥美沙坦氨氯地平",
]
mask = df["MOLECULE"].isin(VBP_LIST)
df.loc[mask, "VBP"] = "VBP品种"
mask = df["MOLECULE"].isin(VBP_LIST) == False
df.loc[mask, "VBP"] = "非VBP品种"

mask = df["TC IV"].isin(
    [
        "C09B3 ACE INHIB COMB+CALC ANTAG|血管紧张素转换酶抑制剂和钙离子拮抗剂(C08)联合用药",
        "C09D3 AT2 ANTG COMB CALC ANTAG|血管紧张素II拮抗剂与钙离子拮抗剂(C08)联合用药",
    ]
)
df.loc[mask, "FDC CLASS"] = "A+C"
mask = df["TC IV"].isin(
    [
        "C09B1 ACE INH COMB+A-HYP/DIURET|血管紧张素转换酶掏抑制剂，与抗高血压药（C02）和/或利尿药（C03）联合用药",
        "C09D1 AT2 ANTG COMB C2 &/O DIU|血管紧张素II拮抗剂与抗高血压药（C02）和/利尿剂联合用药（C03）",
    ]
)
df.loc[mask, "FDC CLASS"] = "A+D"


r = CHPA(df, name="RAAS复方市场", date_column="DATE", period_interval=3)

# r.plot_overall_performance(index="FDC CLASS",unit_change="百万")
# r.plot_overall_performance(index="FDC CLASS", unit="PTD",unit_change="百万")

# r.plot_overall_performance(index="FDC CLASS",unit_change="百万", period="QTR")
# r.plot_overall_performance(index="FDC CLASS", unit="PTD",unit_change="百万", period="QTR")

# r.plot_overall_performance(index="VBP",unit_change="百万")
# r.plot_overall_performance(index="VBP", unit="PTD",unit_change="百万")

# r.plot_size_diff(index="MOLECULE", unit_change="百万", hue="VBP")
# r.plot_size_diff(
#     index="MOLECULE",
#     unit="PTD",
#     unit_change="百万",
#     hue="VBP",
# )
# r.plot_share_gr(index="MOLECULE", hue="VBP")
# r.plot_share_gr(
#     index="MOLECULE",
#     unit="PTD",
#     hue="VBP",
# )

# r.plottable_latest(index="MOLECULE", hue=("FDC CLASS", "VBP"))
# r.plottable_latest(index="MOLECULE", unit="PTD", hue=("FDC CLASS", "VBP"))

# r.plot_share_trend(index="MOLECULE")
# r.plot_share_trend(index="MOLECULE", unit="PTD")

# r.plottable_annual(index="MOLECULE")
# r.plottable_annual(index="MOLECULE", unit="PTD")

# r.plot_size_diff(
#     index="PRODUCT",
#     unit_change="百万",
#     label_limit=20,
#     hue="FDC CLASS",
# )
# r.plot_size_diff(
#     index="PRODUCT",
#     unit="PTD",
#     unit_change="百万",
#     label_limit=20,
#     hue="FDC CLASS",
# )

# r.plot_share_gr(index="PRODUCT", ylim=(-0.5, 1), hue="FDC CLASS", label_topy=4)
# r.plot_share_gr(
#     index="PRODUCT", unit="PTD", ylim=(-0.5, 1), hue="FDC CLASS", label_topy=4
# )

# r.plottable_latest(index="PRODUCT", hue=("MOLECULE", "CORPORATION", "VBP"))
# r.plottable_latest(index="PRODUCT", unit="PTD", hue=("MOLECULE", "CORPORATION", "VBP"))

# r.plot_share_trend(index="PRODUCT")
# r.plot_share_trend(index="PRODUCT", unit="PTD")

# r.plottable_annual(index="PRODUCT")
# r.plottable_annual(index="PRODUCT", unit="PTD")

df2 = df[
    df["TC IV"].isin(
        [
            "C09B3 ACE INHIB COMB+CALC ANTAG|血管紧张素转换酶抑制剂和钙离子拮抗剂(C08)联合用药",
            "C09D3 AT2 ANTG COMB CALC ANTAG|血管紧张素II拮抗剂与钙离子拮抗剂(C08)联合用药",
        ]
    )
]
mask = (
    df2["TC IV"]
    == "C09B3 ACE INHIB COMB+CALC ANTAG|血管紧张素转换酶抑制剂和钙离子拮抗剂(C08)联合用药"
)
df2.loc[mask, "FDC CLASS"] = "ACEI+C"
mask = (
    df2["TC IV"]
    == "C09D3 AT2 ANTG COMB CALC ANTAG|血管紧张素II拮抗剂与钙离子拮抗剂(C08)联合用药"
)
df2.loc[mask, "FDC CLASS"] = "ARB+C"

r = CHPA(df2, name="A+C复方市场", date_column="DATE", period_interval=3)

# r.plot_overall_performance(index="FDC CLASS", unit_change="百万")
# r.plot_overall_performance(index="FDC CLASS", unit="PTD", unit_change="百万")
# r.plot_overall_performance(index="FDC CLASS", unit_change="百万", period="QTR")
# r.plot_overall_performance(
#     index="FDC CLASS", unit="PTD", unit_change="百万", period="QTR"
# )

# r.plot_overall_performance(index="MOLECULE", unit_change="百万")
# r.plot_overall_performance(index="MOLECULE", unit="PTD", unit_change="百万")

# r.plot_overall_performance(index="VBP",unit_change="百万")
# r.plot_overall_performance(index="VBP", unit="PTD",unit_change="百万")

# r.plot_size_diff(index="MOLECULE", unit_change="百万", hue="VBP")
# r.plot_size_diff(index="MOLECULE", unit="PTD", unit_change="百万", hue="VBP")
# r.plot_share_gr(index="MOLECULE", label_topy=4, hue="VBP")
# r.plot_share_gr(index="MOLECULE", unit="PTD", label_topy=4, hue="VBP")

# r.plottable_latest(index="MOLECULE", hue="VBP", fontsize=18)
# r.plottable_latest(index="MOLECULE", unit="PTD", hue="VBP", fontsize=18)

# r.plot_share_trend(index="MOLECULE")
# r.plot_share_trend(index="MOLECULE", unit="PTD")

# r.plottable_annual(index="MOLECULE", fontsize=18)
# r.plottable_annual(index="MOLECULE", unit="PTD", fontsize=18)

# r.plot_size_diff(index="PRODUCT", unit_change="百万", label_limit=9, hue="MOLECULE")
# r.plot_size_diff(
#     index="PRODUCT", unit="PTD", unit_change="百万", label_limit=9, hue="MOLECULE"
# )
# r.plot_share_gr(index="PRODUCT", ylim=(-0.5, 1), label_topy=4, hue="MOLECULE")
# r.plot_share_gr(
#     index="PRODUCT", unit="PTD", ylim=(-0.5, 1), label_topy=4, hue="MOLECULE"
# )

# r.plottable_latest(index="PRODUCT", hue=("MOLECULE", "CORPORATION", "VBP"))
# r.plottable_latest(index="PRODUCT", unit="PTD", hue=("MOLECULE", "CORPORATION", "VBP"))

# r.plot_share_trend(index="PRODUCT")
# r.plot_share_trend(index="PRODUCT", unit="PTD")

# r.plottable_annual(index="PRODUCT")
# r.plottable_annual(index="PRODUCT", unit="PTD")

D_MAP_PRODUCT = {
    "AMLODIPINE&BENAZEP (S5O)": "贝那普利氨氯地平（地奥）",
    "BAI AN XIN (GRU)": "百安新",
    "COVERAM (SVR)": "开素达",
    "EXFORGE (NVR)": "倍博特",
    "TIAN SHU PING (NJ2)": "天舒平",
    "XIE AN ZHI (ZHU)": "协安之",
    "RUI XIN AN (JSH)": "瑞心安",
    "SEVIKAR (DSC)": "思卫卡",
    "VALSARTAN&AMLODIPI (BB4)": "缬沙坦氨氯地平（百奥）",
    "XIE AN YUE (ZJ5)": "缬氨悦",
    "VALSARTAN&AMLODIPI (HZ6)": "缬沙坦氨氯地平（华新）",
}

r.data["PRODUCT"] = r.data["PRODUCT"].map(D_MAP_PRODUCT).fillna(r.data["PRODUCT"])
r.data["PRODUCT_MOLECULE"] = r.data.apply(
    lambda x: (
        f"{x['PRODUCT']}\n{x['MOLECULE']}"
        if x["PRODUCT"]
        not in [
            "贝那普利氨氯地平（地奥）",
            "缬沙坦氨氯地平（百奥）",
            "缬沙坦氨氯地平（华新）",
        ]
        else x["PRODUCT"]
    ),
    axis=1,
)

f = plt.figure(
    FigureClass=GridFigure,
    ncols=2,
    width=15,
    height=6,
    style={
        "title": f"{r.name}市场Top产品滚动年份额趋势",
    },
    fontsize=11,
    color_dict={
        "贝那普利氨氯地平（地奥）": "navy",
        "百安新\n贝那普利氨氯地平": "crimson",
        "开素达\n培哚普利氨氯地平": "darkgreen",
        "倍博特\n缬沙坦氨氯地平": "saddlebrown",
        "天舒平\n奥美沙坦氨氯地平": "olivedrab",
        "协安之\n缬沙坦氨氯地平": "purple",
        "瑞心安\n缬沙坦氨氯地平": "teal",
        "思卫卡\n奥美沙坦氨氯地平": "deepskyblue",
        "缬沙坦氨氯地平（百奥）": "gold",
        "缬氨悦\n缬沙坦氨氯地平": "darkorange",
        "缬沙坦氨氯地平（华新）": "violet",
    },
)

for i, unit in enumerate(["Value", "PTD"]):
    plot_data = r.get_pivot(
        index="PRODUCT_MOLECULE",
        columns=r.date_column,
        values="AMOUNT",
        query_str=f"UNIT=='{unit}' and PERIOD=='MAT'",
    ).sort_values("2024-03", ascending=False)
    plot_data = (
        plot_data.div(plot_data.sum(axis=0), axis=1)
        .head(10)
        .loc[:, ["2022-03", "2023-03", "2024-03"]]
    )
    print(plot_data)

    f.plot(
        data=plot_data.transpose(),
        kind="line",
        ax_index=i,
        fmt="{:.1%}",
        style={
            "title": "滚动年金额" if unit == "Value" else "滚动年PTD",
            "ylabel": "金额份额（%）" if unit == "Value" else "PTD份额（%）",
            "remove_yticks": True,
        },
        show_label=plot_data.index,
        linewidth=1,
    )

f.save()

df3 = df[
    df["TC IV"].isin(
        [
            "C09B1 ACE INH COMB+A-HYP/DIURET|血管紧张素转换酶掏抑制剂，与抗高血压药（C02）和/或利尿药（C03）联合用药",
            "C09D1 AT2 ANTG COMB C2 &/O DIU|血管紧张素II拮抗剂与抗高血压药（C02）和/利尿剂联合用药（C03）",
        ]
    )
]
mask = (
    df3["TC IV"]
    == "C09B1 ACE INH COMB+A-HYP/DIURET|血管紧张素转换酶掏抑制剂，与抗高血压药（C02）和/或利尿药（C03）联合用药"
)
df3.loc[mask, "FDC CLASS"] = "ACEI+D"
mask = (
    df3["TC IV"]
    == "C09D1 AT2 ANTG COMB C2 &/O DIU|血管紧张素II拮抗剂与抗高血压药（C02）和/利尿剂联合用药（C03）"
)
df3.loc[mask, "FDC CLASS"] = "ARB+D"

r = CHPA(df3, name="A+D复方制剂市场", date_column="DATE", period_interval=3)


# r.plot_overall_performance(index="FDC CLASS", unit_change="百万")
# r.plot_overall_performance(index="FDC CLASS", unit="PTD", unit_change="百万")

# r.plot_overall_performance(index="FDC CLASS", unit_change="百万", period="QTR")
# r.plot_overall_performance(
#     index="FDC CLASS", unit="PTD", unit_change="百万", period="QTR"
# )

# r.plot_overall_performance(index="VBP", unit_change="百万")
# r.plot_overall_performance(index="VBP", unit="PTD", unit_change="百万")


# r.plot_size_diff(index="MOLECULE", unit_change="百万", hue="VBP")
# r.plot_size_diff(index="MOLECULE", unit="PTD", unit_change="百万", hue="VBP")
# r.plot_share_gr(index="MOLECULE", label_topy=4, hue="VBP")
# r.plot_share_gr(index="MOLECULE", unit="PTD", label_topy=4, hue="VBP")

# r.plottable_latest(index="MOLECULE", hue="VBP")
# r.plottable_latest(index="MOLECULE", unit="PTD", hue="VBP")

# r.plot_share_trend(index="MOLECULE")
# r.plot_share_trend(index="MOLECULE", unit="PTD")

# r.plottable_annual(index="MOLECULE")
# r.plottable_annual(index="MOLECULE", unit="PTD")

# r.plot_size_diff(
#     index="PRODUCT",
#     unit_change="百万",
#     hue="MOLECULE",
# )
# r.plot_size_diff(
#     index="PRODUCT",
#     unit="PTD",
#     unit_change="百万",
#     hue="MOLECULE",
# )
# r.plot_share_gr(
#     index="PRODUCT",
#     ylim=(-0.4, 0.4),
#     label_topy=0,
#     hue="MOLECULE",
# )
# r.plot_share_gr(
#     index="PRODUCT",
#     unit="PTD",
#     ylim=(-0.4, 0.4),
#     label_topy=0,
#     hue="MOLECULE",
# )

# r.plottable_latest(index="PRODUCT", hue="CORPORATION")
# r.plottable_latest(
#     index="PRODUCT", unit="PTD", hue="CORPORATION"
# )

# r.plot_share_trend(index="PRODUCT")
# r.plot_share_trend(index="PRODUCT", unit="PTD")

# r.plottable_annual(index="PRODUCT")
# r.plottable_annual(index="PRODUCT", unit="PTD")
