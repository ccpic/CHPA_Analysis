from CHPA2 import CHPA, convert_std_volume, extract_strength
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from chart.figure import GridFigure
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

molecule_mapping = {
    "奥美沙坦酯氨氯地平片": "奥美沙坦氨氯地平",
    "奥美沙坦酯氨氯地平": "奥美沙坦氨氯地平",
    "舒脈康膜衣錠": "奥美沙坦氨氯地平",
    "奥美沙坦酯,氨氯地平": "奥美沙坦氨氯地平",
    "奥美沙坦酯氢氯噻嗪": "奥美沙坦氢氯噻嗪",
    "氯沙坦钾,氢氯噻嗪": "氯沙坦氢氯噻嗪",
    "氯沙坦钾氢氯噻嗪": "氯沙坦氢氯噻嗪",
    "培哚普利氨氯地平片(III)": "培哚普利氨氯地平",
    "坎地氢噻": "坎地沙坦氢氯噻嗪",
    "复方卡托普利": "卡托普利氢氯噻嗪",
    "氨氯地平贝那普利(II)": "贝那普利氨氯地平",
    "氨氯地平贝那普利": "贝那普利氨氯地平",
    "缬沙坦,氨氯地平": "缬沙坦氨氯地平",
    "阿利沙坦酯氨氯地平": "阿利沙坦氨氯地平",
}

df["MOLECULE"] = df["MOLECULE"].replace(molecule_mapping)

VBP_LIST = [
    "缬沙坦氨氯地平",
    "厄贝沙坦氢氯噻嗪",
    "缬沙坦氢氯噻嗪",
    "氯沙坦氢氯噻嗪",
    "奥美沙坦氢氯噻嗪",
    "奥美沙坦氨氯地平",
    "替米沙坦氢氯噻嗪",
]
mask = df["MOLECULE"].isin(VBP_LIST)
df.loc[mask, "VBP"] = "VBP品种"
mask = ~df["MOLECULE"].isin(VBP_LIST)
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


FOCUS_MOLECULE = "阿利沙坦氨氯地平"
FOCUS_PRODUCT = "FU LI TAN (SI6)"


r = CHPA(df, name="RAAS复方市场", date_column="DATE", period_interval=3)

r.plot_overall_performance_dual(
    index="FDC CLASS",
    unit_change="亿",
    label_threshold=0.01,
    fontsize=11,
    width=15,
    height=6,
    sorter=["A+C", "A+D"],
)

r.plot_overall_performance(index="FDC CLASS", unit_change="亿")
r.plot_overall_performance(index="FDC CLASS", unit="PTD", unit_change="亿")

r.plot_overall_performance(index="FDC CLASS", unit_change="亿", period="QTR")
r.plot_overall_performance(
    index="FDC CLASS", unit="PTD", unit_change="亿", period="QTR"
)

r.plot_overall_performance_dual(
    index="VBP",
    unit_change="亿",
    label_threshold=0.01,
    fontsize=11,
    width=15,
    height=6,
    sorter=["VBP品种", "非VBP品种"],
)

r.plot_size_diff(index="MOLECULE", unit_change="亿", hue="VBP", focus=FOCUS_MOLECULE)
r.plot_size_diff(
    index="MOLECULE", unit="PTD", unit_change="亿", hue="VBP", focus=FOCUS_MOLECULE
)
r.plot_share_gr(
    index="MOLECULE", hue="VBP", label_topy=4, ylim=(-0.5, 1), focus=FOCUS_MOLECULE
)
r.plot_share_gr(
    index="MOLECULE",
    unit="PTD",
    hue="VBP",
    label_topy=4,
    ylim=(-0.5, 1),
    focus=FOCUS_MOLECULE,
)

r.plottable_latest(index="MOLECULE", hue=("FDC CLASS", "VBP"), focus=FOCUS_MOLECULE)
r.plottable_latest(
    index="MOLECULE", unit="PTD", hue=("FDC CLASS", "VBP"), focus=FOCUS_MOLECULE
)

r.plot_share_trend(index="MOLECULE", focus=FOCUS_MOLECULE)
r.plot_share_trend(index="MOLECULE", unit="PTD", focus=FOCUS_MOLECULE)

r.plottable_annual(index="MOLECULE")
r.plottable_annual(index="MOLECULE", unit="PTD")

r.plot_size_diff(
    index="PRODUCT",
    unit_change="亿",
    label_limit=20,
    hue="FDC CLASS",
    focus=FOCUS_PRODUCT
)
r.plot_size_diff(
    index="PRODUCT",
    unit="PTD",
    unit_change="亿",
    label_limit=20,
    hue="FDC CLASS",
    focus=FOCUS_PRODUCT,
)

r.plot_share_gr(
    index="PRODUCT",
    ylim=(-0.4, 0.6),
    hue="FDC CLASS",
    label_topy=4,
    focus=FOCUS_PRODUCT,
)
r.plot_share_gr(
    index="PRODUCT",
    unit="PTD",
    ylim=(-0.4, 0.8),
    hue="FDC CLASS",
    label_topy=4,
    focus=FOCUS_PRODUCT,
)

r.plottable_latest(
    index="PRODUCT", hue=("MOLECULE", "CORPORATION", "VBP"), focus=FOCUS_PRODUCT
)
r.plottable_latest(
    index="PRODUCT",
    unit="PTD",
    hue=("MOLECULE", "CORPORATION", "VBP"),
    focus=FOCUS_PRODUCT,
)

r.plot_share_trend(index="PRODUCT", focus=FOCUS_PRODUCT)
r.plot_share_trend(index="PRODUCT", unit="PTD", focus=FOCUS_PRODUCT)

r.plottable_annual(index="PRODUCT")
r.plottable_annual(index="PRODUCT", unit="PTD")

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

r.plot_overall_performance_dual(
    index="FDC CLASS",
    unit_change="亿",
    label_threshold=0.01,
    fontsize=11,
    width=15,
    height=6,
    sorter=["ACEI+C", "ARB+C"],
)

r.plot_overall_performance(index="FDC CLASS", unit_change="亿")
r.plot_overall_performance(index="FDC CLASS", unit="PTD", unit_change="亿")
r.plot_overall_performance(index="FDC CLASS", unit_change="亿", period="QTR")
r.plot_overall_performance(
    index="FDC CLASS", unit="PTD", unit_change="亿", period="QTR"
)

r.plot_overall_performance(index="MOLECULE", unit_change="亿")
r.plot_overall_performance(index="MOLECULE", unit="PTD", unit_change="亿")

r.plot_overall_performance_dual(
    index="VBP",
    unit_change="亿",
    label_threshold=0.01,
    fontsize=11,
    width=15,
    height=6,
    sorter=["VBP品种", "非VBP品种"],
)

r.plot_size_diff_dual(
    index="MOLECULE",
    unit_change=("亿", "亿"),
    hue="VBP",
    fontsize=11,
    width=15,
    height=6,
    focus=FOCUS_MOLECULE,
)

r.plot_size_diff(
    index="MOLECULE",
    unit_change="亿",
    hue="VBP",
    focus=FOCUS_MOLECULE,
)
r.plot_size_diff(
    index="MOLECULE",
    unit="PTD",
    unit_change="亿",
    hue="VBP",
    focus=FOCUS_MOLECULE,
)
r.plot_share_gr(
    index="MOLECULE",
    label_topy=4,
    hue="VBP",
    focus=FOCUS_MOLECULE,
)
r.plot_share_gr(
    index="MOLECULE",
    unit="PTD",
    label_topy=4,
    hue="VBP",
    focus=FOCUS_MOLECULE,
)

r.plottable_latest(
    index="MOLECULE",
    hue="VBP",
    fontsize=18,
    focus=FOCUS_MOLECULE,
)
r.plottable_latest(
    index="MOLECULE",
    unit="PTD",
    hue="VBP",
    fontsize=18,
    focus=FOCUS_MOLECULE,
)

r.plot_share_trend(
    index="MOLECULE",
    focus=FOCUS_MOLECULE,
)
r.plot_share_trend(
    index="MOLECULE",
    unit="PTD",
    focus=FOCUS_MOLECULE,
)

r.plottable_annual(index="MOLECULE", fontsize=18)
r.plottable_annual(index="MOLECULE", unit="PTD", fontsize=18)

r.plot_size_diff(
    index="PRODUCT",
    unit_change="亿",
    label_limit=9,
    hue="MOLECULE",
    focus=FOCUS_PRODUCT,
)
r.plot_size_diff(
    index="PRODUCT",
    unit="PTD",
    unit_change="亿",
    label_limit=9,
    hue="MOLECULE",
    focus=FOCUS_PRODUCT,
)
r.plot_share_gr(
    index="PRODUCT",
    ylim=(-0.5, 1),
    label_topy=4,
    hue="MOLECULE",
    focus=FOCUS_PRODUCT,
)
r.plot_share_gr(
    index="PRODUCT",
    unit="PTD",
    ylim=(-0.5, 1),
    label_topy=4,
    hue="MOLECULE",
    focus=FOCUS_PRODUCT,
)

r.plottable_latest(
    index="PRODUCT",
    hue=("MOLECULE", "CORPORATION", "VBP"),
    topn=20,
    focus=FOCUS_PRODUCT,
)
r.plottable_latest(
    index="PRODUCT",
    unit="PTD",
    hue=("MOLECULE", "CORPORATION", "VBP"),
    topn=20,
    focus=FOCUS_PRODUCT,
)

r.plot_share_trend(
    index="PRODUCT",
    focus=FOCUS_PRODUCT,
)
r.plot_share_trend(
    index="PRODUCT",
    unit="PTD",
    focus=FOCUS_PRODUCT,
)

r.plottable_annual(index="PRODUCT")
r.plottable_annual(index="PRODUCT", unit="PTD")

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


r.plot_overall_performance(index="FDC CLASS", unit_change="亿")
r.plot_overall_performance(index="FDC CLASS", unit="PTD", unit_change="亿")

r.plot_overall_performance(index="FDC CLASS", unit_change="亿", period="QTR")
r.plot_overall_performance(
    index="FDC CLASS", unit="PTD", unit_change="亿", period="QTR"
)

r.plot_overall_performance(index="VBP", unit_change="亿")
r.plot_overall_performance(index="VBP", unit="PTD", unit_change="亿")


r.plot_size_diff(index="MOLECULE", unit_change="亿", hue="VBP")
r.plot_size_diff(index="MOLECULE", unit="PTD", unit_change="亿", hue="VBP")
r.plot_share_gr(index="MOLECULE", label_topy=4, hue="VBP", ylim=(-0.5, 1))
r.plot_share_gr(index="MOLECULE", unit="PTD", label_topy=4, hue="VBP", ylim=(-0.5, 1))

r.plottable_latest(index="MOLECULE", hue="VBP")
r.plottable_latest(index="MOLECULE", unit="PTD", hue="VBP")

r.plot_share_trend(index="MOLECULE")
r.plot_share_trend(index="MOLECULE", unit="PTD")

r.plottable_annual(index="MOLECULE")
r.plottable_annual(index="MOLECULE", unit="PTD")

r.plot_size_diff(
    index="PRODUCT",
    unit_change="亿",
    hue="MOLECULE",
)
r.plot_size_diff(
    index="PRODUCT",
    unit="PTD",
    unit_change="亿",
    hue="MOLECULE",
)
r.plot_share_gr(
    index="PRODUCT",
    ylim=(-0.4, 0.4),
    label_topy=0,
    hue="MOLECULE",
)
r.plot_share_gr(
    index="PRODUCT",
    unit="PTD",
    ylim=(-0.4, 0.4),
    label_topy=0,
    hue="MOLECULE",
)

r.plottable_latest(index="PRODUCT", hue="CORPORATION")
r.plottable_latest(index="PRODUCT", unit="PTD", hue="CORPORATION")

r.plot_share_trend(index="PRODUCT")
r.plot_share_trend(index="PRODUCT", unit="PTD")

r.plottable_annual(index="PRODUCT")
r.plottable_annual(index="PRODUCT", unit="PTD")
