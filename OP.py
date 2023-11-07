from CHPA2 import CHPA, convert_std_volume, extract_strength
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
# engine = create_engine("mssql+pymssql://sa:Luna1117@49.232.203.83/CHPA_1806") # 远程数据库
table_name = "data"
condition = "([TC IV] in ('M05B3 BISPHOSPH OSTEOPOROSIS|治疗骨质疏松和骨钙失调的二膦酸盐类', \
    'H04A0 CALCITONINS|降钙素', \
    'H04E0 PARATHYROID HORM&ANALOGS|甲状旁腺激素及类似物', \
    'G03J0 SERMS|选择性雌激素受体调节剂') OR PRODUCT in ('PROLIA                   AAI'))"
sql = "SELECT * FROM " + table_name + " WHERE " + condition
df = pd.read_sql(sql=sql, con=engine)

df["TC IV"] = (
    df["TC IV"].str.split("|").str[0].str[:6] + df["TC IV"].str.split("|").str[1]
)
df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
# df["STRENGTH"] = df["PACKAGE"].apply(lambda x: x.split()[-2])
df["STRENGTH"] = df["PACKAGE"].apply(extract_strength)
# df.to_excel("test.xlsx")
# df["PRODUCT"] = (
#     df["PRODUCT"].str.split("|").str[0]
#     + "（"
#     + df["PRODUCT"].str.split("|").str[1].str[-3:]
#     + "）"
# )
# df["PRODUCT_CORP"] = (
#     df["PRODUCT_CORP"].str.split("（").str[0].str.split("|").str[0]
#     + "\n"
#     + df["PRODUCT_CORP"].str.split("（").str[1].str.split("|").str[0]
# )
mask = df["TC IV"] == "M05B3 治疗骨质疏松和骨钙失调的二膦酸盐类"
df.loc[mask, "TC IV"] = "双膦酸盐类"
mask = df["TC IV"] == "H04A0 降钙素"
df.loc[mask, "TC IV"] = "降钙素"
mask = df["TC IV"] == "H04E0 甲状旁腺激素及类似物"
df.loc[mask, "TC IV"] = "PTH"
mask = df["TC IV"] == "G03J0 选择性雌激素受体调节剂"
df.loc[mask, "TC IV"] = "SERM"
mask = df["MOLECULE"] == "鲑鱼降钙素"
df.loc[mask, "MOLECULE"] = "鲑降钙素"
mask = df["MOLECULE"] == "阿仑膦酸"
df.loc[mask, "MOLECULE"] = "阿仑膦酸钠"
mask = df["MOLECULE"] == "注射用重组特立帕肽"
df.loc[mask, "MOLECULE"] = "特立帕肽"
mask = df["MOLECULE"] == "地舒单抗"
df.loc[mask, "TC IV"] = "地舒单抗"

# 折算标准片数
mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "PTD"
df = pd.concat([df, df_std_volume])


# def convert_std_volume(df, dimension, target, strength, ratio):
#     column_unit = "UNIT"
#     column_strength = "STRENGTH"
#     unit_std_volume = "PTD"
#     column_value = "AMOUNT"
#     mask = (
#         (df[dimension] == target)
#         & (df[column_strength] == strength)
#         & (df[column_unit] == unit_std_volume)
#     )
#     df.loc[mask, column_value] = (df.loc[mask, column_value]) * ratio


convert_std_volume(df, "MOLECULE", "阿仑膦酸", "70MG", 7)
convert_std_volume(df, "MOLECULE", "阿仑膦酸钠维生素D3", "2800IU", 7)
convert_std_volume(df, "MOLECULE", "阿仑膦酸钠维生素D3", "5600IU", 7)
convert_std_volume(df, "MOLECULE", "阿仑膦酸钠维生素D3", "70MG", 7)
convert_std_volume(df, "MOLECULE", "利塞膦酸钠", "35MG", 7)
convert_std_volume(df, "MOLECULE", "依替膦酸二钠", "200MG", 0.5)
convert_std_volume(df, "MOLECULE", "唑来膦酸", "5MG", 365)
convert_std_volume(df, "MOLECULE", "唑来膦酸", "4MG", 365 / 12)
convert_std_volume(df, "MOLECULE", "依降钙素", "10IU", 7)
convert_std_volume(df, "MOLECULE", "依降钙素", "20IU", 7)
convert_std_volume(df, "MOLECULE", "地舒单抗", "60MG", 365 / 2)
# convert_std_volume(df, "PRODUCT", "欣复泰", "200IU", 365 / 36)
# convert_std_volume(df, "PRODUCT", "珍固", "200IU", 365 / 36)
convert_std_volume(df, "PRODUCT", "FORSTEO (LLY)", "600Y", 28)
convert_std_volume(df, "PRODUCT", "XIN FU TAI (XIL)", "600Y", 30)
# convert_std_volume(df, "PRODUCT", "ZHEN GU (S60)", "200IU", 365 / 36)

r = CHPA(df, name="骨松治疗市场", date_column="DATE", period_interval=3)

# r.plot_overall_performance(
#     index="TC IV",
#     sorter=["SERM", "降钙素", "双膦酸盐类", "PTH", "地舒单抗"],
#     unit_change="百万",
#     label_threshold=0,
# )
# r.plot_overall_performance(
#     index="TC IV",
#     sorter=["SERM", "降钙素", "双膦酸盐类", "PTH", "地舒单抗"],
#     unit="Volume (Std Counting Unit)",
#     unit_change="百万",
#     label_threshold=0,
# )


# r.plot_size_diff(
#     index="MOLECULE",
#     unit="Value",
#     unit_change="百万",
# )

# r.plot_size_diff(
#     index="MOLECULE",
#     unit="PTD",
#     unit_change="百万",
# )

# r.plot_share_gr(
#     index="MOLECULE",
#     unit="Value",
# )

# r.plot_share_gr(
#     index="MOLECULE",
#     unit="PTD",
# )

# r.plottable_latest(index="MOLECULE", unit="Value", hue="TC IV")
# r.plottable_latest(index="MOLECULE", unit="PTD", hue="TC IV")


# r.plot_share_trend(
#     index="MOLECULE",
#     focus="特立帕肽"
# )
# r.plot_share_trend(
#     index="MOLECULE",
#     focus="特立帕肽",
#     unit="PTD",
# )

# r.plottable_annual(index="MOLECULE", unit="Value")
# r.plottable_annual(index="MOLECULE", unit="PTD")


# r.plot_size_diff(
#     index="PRODUCT",
#     unit="Value",
#     unit_change="百万",
# )

# r.plot_size_diff(
#     index="PRODUCT",
#     unit="PTD",
#     unit_change="百万",
# )

# r.plot_share_gr(index="PRODUCT", unit="Value", ylim=(-0.5, 2), label_topy=3)

# r.plot_share_gr(index="PRODUCT", unit="PTD", ylim=(-0.5, 2), label_topy=3)


# r.plottable_latest(
#     index="PRODUCT", unit="Value", focus="XIN FU TAI (XIL)", hue="CORPORATION"
# )
# r.plottable_latest(
#     index="PRODUCT",
#     unit="PTD",
#     focus="XIN FU TAI (XIL)",
#     hue="CORPORATION",
# )

# r.plot_share_trend(
#     index="PRODUCT",
#     focus="XIN FU TAI (XIL)"
# )
# r.plot_share_trend(
#     index="PRODUCT",
#     focus="XIN FU TAI (XIL)",
#     unit="PTD",
# )

# r.plottable_annual(index="PRODUCT", unit="Value")
# r.plottable_annual(index="PRODUCT", unit="PTD")

df2 = df[df["MOLECULE"] == "特立帕肽"]
r = CHPA(df2, name="特立帕肽市场", date_column="DATE", period_interval=3)


# r.plot_overall_performance(
#     index="PACKAGE",
#     unit_change="百万",
# )
# r.plot_overall_performance(
#     index="PACKAGE",
#     unit="PTD",
#     unit_change="千",
# )


# r.plot_overall_performance(
#     index="PACKAGE",
#     unit_change="百万",
#     period="QTR",
# )
# r.plot_overall_performance(
#     index="PACKAGE",
#     unit="PTD",
#     unit_change="千",
#     period="QTR",
# )

r.plottable_latest(
    index="PACKAGE",
    unit="Value",
    hue="CORPORATION",
    fontsize=18,
)
r.plottable_latest(
    index="PACKAGE",
    unit="PTD",
    hue="CORPORATION",
    fontsize=18,
)
