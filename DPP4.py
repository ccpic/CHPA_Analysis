from CHPA2 import CHPA, convert_std_volume, extract_strength
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

condition = "[TC IV] in ('A10N1 DPP-IV INH A-DIAB PLAIN|DPP-IV（二肽基肽酶IV）抑制剂，单用(A10B6)')"
sql = "SELECT * FROM " + table_name + " WHERE " + condition
df = pd.read_sql(sql=sql, con=engine)


df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
df["STRENGTH"] = df["PACKAGE"].apply(extract_strength)
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

# mask = df["MOLECULE"] == "阿卡波糖"
# df.loc[mask, "MOLECULE"] = "阿卡波糖片剂"

vbp_list = ["维格列汀", "沙格列汀"]
mask = df["MOLECULE"].isin(vbp_list)
df.loc[mask, "VBP"] = "VBP品种"
mask = df["MOLECULE"].isin(vbp_list) == False
df.loc[mask, "VBP"] = "非VBP品种"


mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "PTD"
df = pd.concat([df, df_std_volume])

convert_std_volume(df, "MOLECULE", "沙格列汀", "2.5MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "维格列汀", "50MG", 1 / 2)


r = CHPA(df, name="DPP4抑制剂单方市场", date_column="DATE", period_interval=3)

# r.plot_overall_performance(
#     index="MOLECULE", sorter=["西格列汀", "利格列汀", "沙格列汀", "维格列汀", "阿格列汀"], unit_change="百万"
# )

# r.plot_overall_performance(
#     index="MOLECULE",
#     unit="PTD",
#     unit_change="百万",
#     sorter=["西格列汀", "利格列汀", "沙格列汀", "维格列汀", "阿格列汀"],
# )

# r.plot_overall_performance(
#     index="MOLECULE",
#     sorter=["西格列汀", "利格列汀", "沙格列汀", "维格列汀", "阿格列汀"],
#     unit_change="百万",
#     period="QTR",
# )

# r.plot_overall_performance(
#     index="MOLECULE",
#     unit="PTD",
#     unit_change="百万",
#     sorter=["西格列汀", "利格列汀", "沙格列汀", "维格列汀", "阿格列汀"],
#     period="QTR",
# )


# r.plot_overall_performance(index="VBP", unit_change="百万")

# r.plot_overall_performance(
#     index="VBP",
#     unit_change="百万",
#     unit="PTD",
# )

# r.plottable_latest(index="MOLECULE", unit="Value", fontsize=18)
# r.plottable_latest(index="MOLECULE", unit="PTD", fontsize=18)

# r.plottable_annual(index="MOLECULE", unit="Value", fontsize=18)
# r.plottable_annual(index="MOLECULE", unit="PTD", fontsize=18)

# r.plot_size_diff(
#     index="PRODUCT", unit="Value", unit_change="百万", label_limit=5, hue="MOLECULE"
# )

# r.plot_size_diff(
#     index="PRODUCT", unit="PTD", unit_change="百万", label_limit=5, hue="MOLECULE"
# )
# r.plot_share_gr(
#     index="PRODUCT",
#     unit="Value",
#     label_limit=7,
#     hue="MOLECULE",
#     ylim=(-0.2, 0.4),
#     label_topy=0,
# )

# r.plot_share_gr(
#     index="PRODUCT",
#     unit="PTD",
#     label_limit=7,
#     hue="MOLECULE",
#     ylim=(-0.2, 0.4),
#     label_topy=0,
# )

# r.plottable_latest(index="PRODUCT", unit="Value", hue="CORPORATION")
# r.plottable_latest(index="PRODUCT", unit="PTD", hue="CORPORATION")

# r.plot_share_trend(
#     index="PRODUCT",
# )
# r.plot_share_trend(
#     index="PRODUCT",
#     unit="PTD",
# )

# r.plottable_annual(index="PRODUCT")
# r.plottable_annual(index="PRODUCT", unit="PTD")
