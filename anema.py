from CHPA2 import CHPA, extract_strength
from sqlalchemy import create_engine
import pandas as pd

df_index = pd.read_excel(
    "肾性贫血定义市场分子PTD系数.xlsx", engine="openpyxl", sheet_name="匹配表"
)
df_index["PACKAGE_STR"] = df_index["PACKAGE"].apply(lambda x: f"'{x}'")
str = ", ".join(df_index["PACKAGE_STR"])
print(df_index)
engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"
condition = f"[PACKAGE] in ({str})"

# condition = "([TC III] in ('B03A HAEMATINICS,IRON & COMBS|补血药，铁剂和所有联合用药', \
#     'B03C ERYTHROPOIETIN PRODUCTS|红细胞生成素类药物', \
#     'B03D HIF-PH INHIBITORS|HIF-PH抑制剂'))"
sql = "SELECT * FROM " + table_name + " WHERE " + condition

df = pd.read_sql(sql=sql, con=engine)
df.to_excel("test.xlsx")
print(df)

# 定义市场简化命名及调整系数
mask = df["TC III"] == "B03A HAEMATINICS,IRON & COMBS|补血药，铁剂和所有联合用药"
df.loc[mask, ["AMOUNT"]] = df.loc[mask, ["AMOUNT"]] * 0.2
df.loc[mask, ["TC III"]] = "B03A HAEMATINICS,IRON & COMBS|补血药，铁剂"
mask = df["TC III"] == "B03C ERYTHROPOIETIN PRODUCTS|红细胞生成素类药物"
df.loc[mask, ["AMOUNT"]] = df.loc[mask, ["AMOUNT"]] * 0.6
df.loc[mask, ["TC III"]] = "B03C ERYTHROPOIETIN PRODUCTS|红细胞生成素"
mask = df["TC III"] == "V03B KANPO & CHINESE MEDICINES|汉方药和中药"
df.loc[mask, ["AMOUNT"]] = df.loc[mask, ["AMOUNT"]] * 0.2
df.loc[mask, ["TC III"]] = "V03B V03B KANPO & CHINESE MEDICINES|中药和中成药"
df.loc[mask, ["MOLECULE"]] = "KANPO & CHINESE MEDICINES|中药和中成药"

# 统一EPO分子名
mask = df["MOLECULE"].str.contains("重组人促红素")
df.loc[mask, ["MOLECULE"]] = "重组人促红素|EPOETIN"

df["TC III"] = (
    df["TC III"].str.split("|").str[0].str[:5] + df["TC III"].str.split("|").str[1]
)
df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
df["STRENGTH"] = df["PACKAGE"].apply(extract_strength)

mask = df["PACKAGE"].str.contains(" AMP | VIAL | DRY | IV | INFUSION ")
df.loc[mask, "CLASS"] = "静脉铁"
df["CLASS"].fillna("口服铁", inplace=True)


# IQVIA原数据通用名只有二价铁/三价铁，并且中文通用名错误，此处进行归类和修正

mask = (df["MOLECULE"] == "多糖铁复合物") & (df["STRENGTH"] == "500MG")
df.loc[mask, "MOLECULE"] = "二异麦芽糖铁"
mask = (df["MOLECULE"] == "多糖铁复合物") & (df["CLASS"] == "静脉铁")
df.loc[mask, "MOLECULE"] = "蔗糖铁"
mask = df["PRODUCT"] == "IRON PROTEINSUCCIN (JY5)"
df.loc[mask, "MOLECULE"] = "蛋白琥珀酸铁"
mask = (df["MOLECULE"] == "富马酸亚铁") & (df["STRENGTH"] == "150MG")
df.loc[mask, "MOLECULE"] = "多糖铁复合物"

mask = (df["PRODUCT"].str.contains("SUCCINATE")) | (
    df["PRODUCT"].isin(["SU LI FEI (JNG)", "LI FEI LONG (H3U)"])
)
df.loc[mask, "MOLECULE"] = "琥珀酸亚铁"
mask = df["PRODUCT"].str.contains("FUMARATE")
df.loc[mask, "MOLECULE"] = "富马酸亚铁"
mask = df["PRODUCT"].str.contains("LACTATE") | (
    df["PRODUCT"].isin(["LA KE FEI (TGD)", "DAN ZHU (TAJ)", "TIE XIN (JFH)"])
)
df.loc[mask, "MOLECULE"] = "乳酸亚铁"
mask = df["PRODUCT"].str.contains("GLUCONATE") | (
    df["PRODUCT"].isin(["XU TAI (ZJ&)", "XUE YI (HT8)"])
)
df.loc[mask, "MOLECULE"] = "葡萄糖酸亚铁"
mask = (df["MOLECULE"] == "富马酸亚铁") & (df["PRODUCT"].str.contains("SULFATE"))
df.loc[mask, "MOLECULE"] = "硫酸亚铁"

# df["PRODUCT"] = (
#     df["PRODUCT"]
#     .str.split("|")
#     .str[0]
#     # + "（"
#     # + df["PRODUCT"].str.split("|").str[1].str[-3:]
#     # + "）"
# )
# df["PRODUCT_CORP"] = (
#     df["PRODUCT_CORP"].str.split("（").str[0].str.split("|").str[0]
#     + "\n"
#     + df["PRODUCT_CORP"].str.split("（").str[1].str.split("|").str[0]
# )

# 折算标准片数
mask = df["UNIT"] == "Volume"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "PTD"
df = pd.concat([df, df_std_volume])

# df["PRODUCT_PACKAGE"] = (
#     df["PRODUCT"].apply(lambda x: x.split("(")[0].strip()) + " " + df["PACKAGE"]
# )

df_index.drop_duplicates(subset="PACKAGE", inplace=True)

for index, value in df_index.iterrows():
    mask = (df["PACKAGE"] == value["PACKAGE"]) & (df["UNIT"] == "PTD")
    df.loc[mask, "AMOUNT"] = df.loc[mask, "AMOUNT"] * value["盒数换算系数(乘)"]


# df.to_excel("test.xlsx")

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


# convert_std_volume(df, "MOLECULE", "罗沙司他胶囊", "50MG", 5 / 3)
# convert_std_volume(df, "MOLECULE", "罗沙司他胶囊", "20MG", 2 / 3)
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "10K", 10000 / (9000 / 7))
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "3000IU", 3000 / (9000 / 7))
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "4000IU", 4000 / (9000 / 7))
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "6000IU", 6000 / (9000 / 7))
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "5000IU", 5000 / (9000 / 7))
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "2000IU", 2000 / (9000 / 7))
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "5K", 5000 / (9000 / 7))
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "6K", 6000 / (9000 / 7))
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "3K", 3000 / (9000 / 7))
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "2500IU", 2500 / (9000 / 7))
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "12K", 12000 / (9000 / 7))
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "4K", 4000 / (9000 / 7))
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "9000IU", 9000 / (9000 / 7))
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "36K", 36000 / (9000 / 7))
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "2K", 2000 / (9000 / 7))
# convert_std_volume(df, "TC III", "B03C 红细胞生成素", "0.01M", 10000 / (9000 / 7))
# convert_std_volume(df, "MOLECULE", "蔗糖铁", "200MG", 2)
# convert_std_volume(df, "MOLECULE", "琥珀酸亚铁", "100MG", 0.5)
# convert_std_volume(df, "MOLECULE", "右旋糖酐铁", "25MG", 0.25)
# convert_std_volume(df, "MOLECULE", "右旋糖酐铁", "50MG", 0.5)
# convert_std_volume(df, "MOLECULE", "乳酸亚铁", "150MG", 1 / 3)
# convert_std_volume(df, "MOLECULE", "乳酸亚铁", "100MG", 1 / 4.5)
# convert_std_volume(df, "MOLECULE", "乳酸亚铁", "0.1G", 1 / 4.5)
# convert_std_volume(df, "MOLECULE", "乳酸亚铁", "900MG", 2)
# convert_std_volume(df, "MOLECULE", "乳酸亚铁", "1.8G", 4)
# convert_std_volume(df, "MOLECULE", "硫酸亚铁", "450MG", 0.5)
# convert_std_volume(df, "MOLECULE", "硫酸亚铁", "300MG", 1 / 3)
# convert_std_volume(df, "MOLECULE", "硫酸亚铁", "0.3G", 1 / 3)

d_TC3 = {"B03C 红细胞生成素": "ESA", "B03D HIF-PH抑制剂": "HIF-PHI"}
df["TC III"] = df["TC III"].map(d_TC3).fillna(df["TC III"])

r = CHPA(df, name="肾性贫血市场", date_column="DATE", period_interval=3)

# r.plot_overall_performance(index="TC III", unit_change="百万")
# r.plot_overall_performance(index="TC III", unit="PTD", unit_change="百万")
# r.plot_overall_performance(index="TC III", period="QTR", unit_change="百万")
# r.plot_overall_performance(index="TC III", period="QTR", unit="PTD", unit_change="百万")


# r.plot_size_diff(index="MOLECULE", unit_change="百万", hue="TC III", focus="恩那度司他")
# r.plot_size_diff(
#     index="MOLECULE", unit="PTD", unit_change="百万", hue="TC III", focus="恩那度司他"
# )
# r.plot_share_gr(
#     index="MOLECULE", ylim=(-0.2, 0.4), label_topy=0, hue="TC III", focus="恩那度司他",
# )
# r.plot_share_gr(
#     index="MOLECULE",
#     ylim=(-0.2, 0.4),
#     unit="PTD",
#     label_topy=0,
#     hue="TC III",
#     focus="恩那度司他",
# )

# r.plottable_latest(index="MOLECULE", hue="TC III", focus="恩那度司他")
# r.plottable_latest(index="MOLECULE", unit="PTD", hue="TC III", focus="恩那度司他")
# r.plot_share_trend(index="MOLECULE", focus="恩那度司他")
# r.plot_share_trend(index="MOLECULE", unit="PTD", focus="恩那度司他")
# r.plottable_annual(index="MOLECULE")
# r.plottable_annual(index="MOLECULE", unit="PTD")

# r.plot_size_diff(
#     index="PRODUCT", unit_change="百万", hue="TC III", focus="EN NA LUO (SI6)"
# )
# r.plot_size_diff(
#     index="PRODUCT",
#     unit="PTD",
#     unit_change="百万",
#     hue="TC III",
#     focus="EN NA LUO (SI6)",
# )
# r.plot_share_gr(
#     index="PRODUCT",
#     ylim=(-0.2, 0.4),
#     label_topy=0,
#     hue="TC III",
#     focus="EN NA LUO (SI6)",
# )
# r.plot_share_gr(
#     index="PRODUCT",
#     ylim=(-0.2, 0.4),
#     unit="PTD",
#     label_topy=0,
#     hue="TC III",
#     focus="EN NA LUO (SI6)",
# )

# r.plottable_latest(
#     index="PRODUCT",
#     hue=("MOLECULE", "CORPORATION"),
#     focus="EN NA LUO (SI6)",
# )
# r.plottable_latest(
#     index="PRODUCT",
#     unit="PTD",
#     hue=("MOLECULE", "CORPORATION"),
#     focus="EN NA LUO (SI6)",
# )

# r.plot_share_trend(
#     index="PRODUCT",
#     focus="EN NA LUO (SI6)",
# )
# r.plot_share_trend(
#     index="PRODUCT",
#     unit="PTD",
#     focus="EN NA LUO (SI6)",
# )

# r.plottable_annual(index="PRODUCT")
# r.plottable_annual(index="PRODUCT", unit="PTD")

df2 = df[df["TC III"].isin(["ESA", "HIF-PHI"])]
r = CHPA(df2, name="ESA+HIF市场", date_column="DATE", period_interval=3)

r.plot_overall_performance_dual(index="TC III", unit_change="百万", sorter=["HIF-PHI", "ESA"])
# r.plot_overall_performance_dual(index="TC III", unit_change="百万", period="QTR")

# r.plot_overall_performance(index="TC III", unit_change="百万")
# r.plot_overall_performance(index="TC III", unit="PTD", unit_change="百万")
# r.plot_overall_performance(index="TC III", period="QTR", unit_change="百万")
# r.plot_overall_performance(index="TC III", period="QTR", unit="PTD", unit_change="百万")


# r.plot_size_diff(index="MOLECULE", unit_change="百万", hue="TC III", focus="恩那度司他")
# r.plot_size_diff(
#     index="MOLECULE", unit="PTD", unit_change="百万", hue="TC III", focus="恩那度司他"
# )
# r.plot_share_gr(
#     index="MOLECULE", ylim=(-0.2, 0.4), label_topy=0, hue="TC III", focus="恩那度司他",
# )
# r.plot_share_gr(
#     index="MOLECULE",
#     ylim=(-0.2, 0.4),
#     unit="PTD",
#     label_topy=0,
#     hue="TC III",
#     focus="恩那度司他",
# )

# r.plottable_latest(index="MOLECULE", hue="TC III", focus="恩那度司他", fontsize=18)
# r.plottable_latest(
#     index="MOLECULE", unit="PTD", hue="TC III", focus="恩那度司他", fontsize=18
# )
# r.plot_share_trend(index="MOLECULE", focus="恩那度司他")
# r.plot_share_trend(index="MOLECULE", unit="PTD", focus="恩那度司他")
# r.plottable_annual(index="MOLECULE", fontsize=18)
# r.plottable_annual(index="MOLECULE", unit="PTD", fontsize=18)

# r.plot_size_diff(
#     index="PRODUCT", unit_change="百万", hue="TC III", focus="EN NA LUO (SI6)"
# )
# r.plot_size_diff(
#     index="PRODUCT",
#     unit="PTD",
#     unit_change="百万",
#     hue="TC III",
#     focus="EN NA LUO (SI6)",
# )
# r.plot_share_gr(
#     index="PRODUCT",
#     ylim=(-0.2, 0.4),
#     label_topy=0,
#     hue="TC III",
#     focus="EN NA LUO (SI6)",
# )
# r.plot_share_gr(
#     index="PRODUCT",
#     ylim=(-0.2, 0.4),
#     unit="PTD",
#     label_topy=0,
#     hue="TC III",
#     focus="EN NA LUO (SI6)",
# )

# r.plottable_latest(
#     index="PRODUCT",
#     hue=("MOLECULE", "CORPORATION"),
#     focus="EN NA LUO (SI6)",
# )
# r.plottable_latest(
#     index="PRODUCT",
#     unit="PTD",
#     hue=("MOLECULE", "CORPORATION"),
#     focus="EN NA LUO (SI6)",
# )

# r.plot_share_trend(
#     index="PRODUCT",
#     focus="EN NA LUO (SI6)",
# )
# r.plot_share_trend(
#     index="PRODUCT",
#     unit="PTD",
#     focus="EN NA LUO (SI6)",
# )

# r.plottable_annual(index="PRODUCT")
# r.plottable_annual(index="PRODUCT", unit="PTD")
