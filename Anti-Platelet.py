from CHPA2 import CHPA, convert_std_volume
from sqlalchemy import create_engine
import pandas as pd

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


r.plottable_latest(
    index="PRODUCT", unit="Value", focus="TALCOM (SI6)", hue="CORPORATION"
)
r.plottable_latest(
    index="PRODUCT",
    unit="Volume (Std Counting Unit)",
    focus="TALCOM (SI6)",
    hue="CORPORATION",
)

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

# df3 = df[df["MOLECULE"]=="氯吡格雷"]
# r = CHPA(df3, name="氯吡格雷市场", date_column="DATE", period_interval=3)

r.plottable_latest(
    index="PRODUCT", unit="Value", focus="TALCOM (SI6)", hue="CORPORATION"
)
r.plottable_latest(
    index="PRODUCT",
    unit="Volume (Std Counting Unit)",
    focus="TALCOM (SI6)",
    hue="CORPORATION",
)

# r.plottable_annual(index="PRODUCT", unit="Value")
# r.plottable_annual(index="PRODUCT", unit="Volume (Std Counting Unit)")
