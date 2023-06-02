from CHPA2 import CHPA, convert_std_volume, extract_strength
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

condition = (
    "[TC IV] in ('C09B1 ACE INH COMB+A-HYP/DIURET|血管紧张素转换酶掏抑制剂，与抗高血压药（C02）和/或利尿药（C03）联合用药' ,"
    "'C09B3 ACE INHIB COMB+CALC ANTAG|血管紧张素转换酶抑制剂和钙离子拮抗剂(C08)联合用药' ,"
    "'C09D1 AT2 ANTG COMB C2 &/O DIU|血管紧张素II拮抗剂与抗高血压药（C02）和/利尿剂联合用药（C03）' ,"
    "'C09D3 AT2 ANTG COMB CALC ANTAG|血管紧张素II拮抗剂与钙离子拮抗剂(C08)联合用药') "
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
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])

mask = df["MOLECULE"].isin(["奥美沙坦酯氨氯地平片", "舒脈康膜衣錠"])
df.loc[mask, "MOLECULE"] = "奥美沙坦氨氯地平"
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

VBP_LIST = ["缬沙坦氨氯地平", "厄贝沙坦氢氯噻嗪", "缬沙坦氢氯噻嗪", "氯沙坦氢氯噻嗪"]
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


r = CHPA(df, name="RAAS复方制剂市场", date_column="DATE", period_interval=3)

# r.plot_overall_performance(index="FDC CLASS",unit_change="百万")
# r.plot_overall_performance(index="FDC CLASS", unit="Volume (Std Counting Unit)",unit_change="百万")

# r.plot_overall_performance(index="VBP",unit_change="百万")
# r.plot_overall_performance(index="VBP", unit="Volume (Std Counting Unit)",unit_change="百万")

# r.plot_size_diff(index="MOLECULE", unit_change="百万", label_limit=12)
# r.plot_size_diff(
#     index="MOLECULE",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
#     label_limit=12,
# )
# r.plot_share_gr(index="MOLECULE")
# r.plot_share_gr(
#     index="MOLECULE",
#     unit="Volume (Std Counting Unit)",
# )
# r.plottable_latest(index="MOLECULE", hue="FDC CLASS")
# r.plottable_latest(index="MOLECULE", unit="Volume (Std Counting Unit)", hue="FDC CLASS")

# r.plot_share_trend(index="MOLECULE")
# r.plot_share_trend(index="MOLECULE", unit="Volume (Std Counting Unit)")

# r.plottable_annual(index="MOLECULE")
# r.plottable_annual(index="MOLECULE", unit="Volume (Std Counting Unit)")

# r.plot_size_diff(
#     index="PRODUCT",
#     unit_change="百万",
#     label_limit=20,
# )
# r.plot_size_diff(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
#     label_limit=20,
# )
# r.plot_share_gr(index="PRODUCT", ylim=(-0.5, 1), label_topy=4)
# r.plot_share_gr(
#     index="PRODUCT", unit="Volume (Std Counting Unit)", ylim=(-0.5, 1), label_topy=4
# )
r.plottable_latest(index="PRODUCT", hue="CORPORATION")
r.plottable_latest(
    index="PRODUCT", unit="Volume (Std Counting Unit)", hue="CORPORATION"
)

# r.plot_share_trend(index="PRODUCT")
# r.plot_share_trend(index="PRODUCT", unit="Volume (Std Counting Unit)")

# r.plottable_annual(index="PRODUCT")
# r.plottable_annual(index="PRODUCT", unit="Volume (Std Counting Unit)")

df2 = df[
    df["TC IV"].isin(
        [
            "C09B3 ACE INHIB COMB+CALC ANTAG|血管紧张素转换酶抑制剂和钙离子拮抗剂(C08)联合用药",
            "C09D3 AT2 ANTG COMB CALC ANTAG|血管紧张素II拮抗剂与钙离子拮抗剂(C08)联合用药",
        ]
    )
]
mask = df2["TC IV"] == "C09B3 ACE INHIB COMB+CALC ANTAG|血管紧张素转换酶抑制剂和钙离子拮抗剂(C08)联合用药"
df2.loc[mask, "FDC CLASS"] = "ACEI+C"
mask = df2["TC IV"] == "C09D3 AT2 ANTG COMB CALC ANTAG|血管紧张素II拮抗剂与钙离子拮抗剂(C08)联合用药"
df2.loc[mask, "FDC CLASS"] = "ARB+C"

r = CHPA(df2, name="A+C复方制剂市场", date_column="DATE", period_interval=3)

# r.plot_overall_performance(index="FDC CLASS",unit_change="百万")
# r.plot_overall_performance(index="FDC CLASS", unit="Volume (Std Counting Unit)",unit_change="百万")

# r.plot_overall_performance(index="MOLECULE",unit_change="百万")
# r.plot_overall_performance(index="MOLECULE", unit="Volume (Std Counting Unit)",unit_change="百万")

# r.plot_overall_performance(index="VBP",unit_change="百万")
# r.plot_overall_performance(index="VBP", unit="Volume (Std Counting Unit)",unit_change="百万")

# r.plot_size_diff(
#     index="MOLECULE",
#     unit_change="百万",
# )
# r.plot_size_diff(
#     index="MOLECULE",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
# )
# r.plot_share_gr(index="MOLECULE", label_topy=4)
# r.plot_share_gr(index="MOLECULE", unit="Volume (Std Counting Unit)", label_topy=4)
# r.plottable_latest(index="MOLECULE", hue="FDC CLASS", fontsize=20)
# r.plottable_latest(index="MOLECULE", unit="Volume (Std Counting Unit)", hue="FDC CLASS", fontsize=20)


# r.plot_size_diff(
#     index="PRODUCT",
#     unit_change="百万",
#     label_limit=9,
# )
# r.plot_size_diff(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
#     label_limit=9,
# )
# r.plot_share_gr(index="PRODUCT", ylim=(-0.5, 0.5), label_topy=4)
# r.plot_share_gr(
#     index="PRODUCT", unit="Volume (Std Counting Unit)", ylim=(-0.5, 0.5), label_topy=4
# )
# r.plottable_latest(index="PRODUCT", hue="CORPORATION")
# r.plottable_latest(index="PRODUCT", unit="Volume (Std Counting Unit)", hue="CORPORATION")

# r.plot_share_trend(index="PRODUCT")
# r.plot_share_trend(index="PRODUCT", unit="Volume (Std Counting Unit)")

# r.plottable_annual(index="PRODUCT")
# r.plottable_annual(index="PRODUCT", unit="Volume (Std Counting Unit)")


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
    df3["TC IV"] == "C09D1 AT2 ANTG COMB C2 &/O DIU|血管紧张素II拮抗剂与抗高血压药（C02）和/利尿剂联合用药（C03）"
)
df3.loc[mask, "FDC CLASS"] = "ARB+D"

r = CHPA(df3, name="A+D复方制剂市场", date_column="DATE", period_interval=3)


# r.plot_overall_performance(index="FDC CLASS", unit_change="百万")
# r.plot_overall_performance(
#     index="FDC CLASS", unit="Volume (Std Counting Unit)", unit_change="百万"
# )

# r.plot_overall_performance(index="VBP", unit_change="百万")
# r.plot_overall_performance(
#     index="VBP", unit="Volume (Std Counting Unit)", unit_change="百万"
# )


# r.plot_size_diff(
#     index="MOLECULE",
#     unit_change="百万",
# )
# r.plot_size_diff(
#     index="MOLECULE",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
# )
# r.plot_share_gr(index="MOLECULE", label_topy=4)
# r.plot_share_gr(index="MOLECULE", unit="Volume (Std Counting Unit)", label_topy=4)
# r.plottable_latest(index="MOLECULE", hue="FDC CLASS")
# r.plottable_latest(index="MOLECULE", unit="Volume (Std Counting Unit)", hue="FDC CLASS")

# r.plot_share_trend(index="MOLECULE")
# r.plot_share_trend(index="MOLECULE", unit="Volume (Std Counting Unit)")

# r.plottable_annual(index="MOLECULE")
# r.plottable_annual(index="MOLECULE", unit="Volume (Std Counting Unit)")

# r.plot_size_diff(
#     index="PRODUCT",
#     unit_change="百万",
# )
# r.plot_size_diff(
#     index="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
# )
# r.plot_share_gr(index="PRODUCT", ylim=(-0.5,1), label_topy=0)
# r.plot_share_gr(index="PRODUCT", unit="Volume (Std Counting Unit)",ylim=(-0.5,1), label_topy=0)
# r.plottable_latest(index="PRODUCT", hue="CORPORATION")
# r.plottable_latest(
#     index="PRODUCT", unit="Volume (Std Counting Unit)", hue="CORPORATION"
# )

# r.plot_share_trend(index="PRODUCT")
# r.plot_share_trend(index="PRODUCT", unit="Volume (Std Counting Unit)")

# r.plottable_annual(index="PRODUCT")
# r.plottable_annual(index="PRODUCT", unit="Volume (Std Counting Unit)")
