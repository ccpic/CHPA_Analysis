from CHPA2 import CHPA, extract_strength
from sqlalchemy import create_engine
import pandas as pd

df_index = pd.read_excel(
    "肾性贫血定义市场分子PTD系数_0821.xlsx", engine="openpyxl", sheet_name="匹配表"
)
df_index["PACKAGE_STR"] = df_index["PACKAGE"].apply(lambda x: f"'{x}'")
str = ", ".join(df_index["PACKAGE_STR"])
print(df_index)
engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
# engine = create_engine(
#     "mssql+pymssql://sa:Luna1117@49.232.203.83/CHPA_1806"
# )  # 远程数据库

table_name = "data"
condition = f"[PACKAGE] in ({str})"

# condition = "([TC III] in ('B03A HAEMATINICS,IRON & COMBS|补血药，铁剂和所有联合用药', \
#     'B03C ERYTHROPOIETIN PRODUCTS|红细胞生成素类药物', \
#     'B03D HIF-PH INHIBITORS|HIF-PH抑制剂'))"
sql = "SELECT * FROM " + table_name + " WHERE " + condition

df = pd.read_sql(sql=sql, con=engine)
# df.to_excel("test.xlsx")
# print(df)

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
mask = df["MOLECULE"].str.contains("EPOETIN") & ~df["MOLECULE"].str.contains(
    "DARBEPOETIN ALFA|达依泊汀α"
)
df.loc[mask, ["MOLECULE"]] = "重组人促红素|短效EPO"

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

# mask = (df["MOLECULE"] == "多糖铁复合物") & (df["STRENGTH"] == "500MG")
# df.loc[mask, "MOLECULE"] = "二异麦芽糖铁"
# mask = (df["MOLECULE"] == "多糖铁复合物") & (df["CLASS"] == "静脉铁")
# df.loc[mask, "MOLECULE"] = "蔗糖铁"
# mask = df["PRODUCT"] == "IRON PROTEINSUCCIN (JY5)"
# df.loc[mask, "MOLECULE"] = "蛋白琥珀酸铁"
# mask = (df["MOLECULE"] == "富马酸亚铁") & (df["STRENGTH"] == "150MG")
# df.loc[mask, "MOLECULE"] = "多糖铁复合物"

# mask = (df["PRODUCT"].str.contains("SUCCINATE")) | (
#     df["PRODUCT"].isin(["SU LI FEI (JNG)", "LI FEI LONG (H3U)"])
# )
# df.loc[mask, "MOLECULE"] = "琥珀酸亚铁"
# mask = df["PRODUCT"].str.contains("FUMARATE")
# df.loc[mask, "MOLECULE"] = "富马酸亚铁"
# mask = df["PRODUCT"].str.contains("LACTATE") | (
#     df["PRODUCT"].isin(["LA KE FEI (TGD)", "DAN ZHU (TAJ)", "TIE XIN (JFH)"])
# )
# df.loc[mask, "MOLECULE"] = "乳酸亚铁"
# mask = df["PRODUCT"].str.contains("GLUCONATE") | (
#     df["PRODUCT"].isin(["XU TAI (ZJ&)", "XUE YI (HT8)"])
# )
# df.loc[mask, "MOLECULE"] = "葡萄糖酸亚铁"
# mask = (df["MOLECULE"] == "富马酸亚铁") & (df["PRODUCT"].str.contains("SULFATE"))
# df.loc[mask, "MOLECULE"] = "硫酸亚铁"

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


d_TC3 = {
    "B03C 红细胞生成素": "ESA",
    "B03D HIF-PH抑制剂": "HIF-PHI",
    "V03B 中药和中成药": "补血中药",
    "B03A 补血药，铁剂": "铁剂",
}
df["TC III"] = df["TC III"].map(d_TC3).fillna(df["TC III"])
# df.to_excel("test-1.xlsx")
# print(df)

r = CHPA(df, name="肾性贫血市场", date_column="DATE", period_interval=3)


# 肾性贫血分治疗大类滚动年趋势（双图）
r.plot_overall_performance_dual(
    index="TC III",
    unit_change="百万",
    sorter=["HIF-PHI", "ESA", "铁剂", "补血中药"],
    width=15,
    height=6,
)

# 肾性贫血市场分治疗大类销售额/PTD滚动年趋势
r.plot_overall_performance(index="TC III", unit_change="百万")
r.plot_overall_performance(index="TC III", unit="PTD", unit_change="百万")

# 肾性贫血市场分治疗大类销售额/PTD季度趋势
r.plot_overall_performance(index="TC III", period="QTR", unit_change="百万")
r.plot_overall_performance(index="TC III", period="QTR", unit="PTD", unit_change="百万")


# 以下为通用名维度分析

# 肾性贫血市场通用名滚动年销售额/PTD绝对值 vs. 净增长
r.plot_size_diff(index="MOLECULE", unit_change="百万", hue="TC III", focus="恩那度司他")
r.plot_size_diff(
    index="MOLECULE", unit="PTD", unit_change="百万", hue="TC III", focus="恩那度司他"
)

# 肾性贫血市场通用名滚动年销售额/PTD份额 vs. 同比增长率
r.plot_share_gr(
    index="MOLECULE", ylim=(-0.2, 0.6), label_topy=0, hue="TC III", focus="恩那度司他",
)
r.plot_share_gr(
    index="MOLECULE",
    ylim=(-0.2, 0.6),
    unit="PTD",
    label_topy=0,
    hue="TC III",
    focus="恩那度司他",
)

# 滚动年TOP20通用名销售额/PTD明细
r.plottable_latest(index="MOLECULE", hue="TC III", focus="恩那度司他")
r.plottable_latest(index="MOLECULE", unit="PTD", hue="TC III", focus="恩那度司他")

# TOP10通用码滚动年销售额/PTD份额趋势
r.plot_share_trend(index="MOLECULE", focus="恩那度司他")
r.plot_share_trend(index="MOLECULE", unit="PTD", focus="恩那度司他")

# 肾性贫血定义市场历年通用名销售额/PTD排名
r.plottable_annual(index="MOLECULE")
r.plottable_annual(index="MOLECULE", unit="PTD")


# 以下为品牌维度分析

# 肾性贫血市场产品滚动年销售额/PTD绝对值 vs. 净增长
r.plot_size_diff(
    index="PRODUCT", unit_change="百万", hue="TC III", focus="EN NA LUO (SI6)"
)
r.plot_size_diff(
    index="PRODUCT",
    unit="PTD",
    unit_change="百万",
    hue="TC III",
    focus="EN NA LUO (SI6)",
)

# 肾性贫血市场产品滚动年销售额/PTD份额 vs. 同比增长率
r.plot_share_gr(
    index="PRODUCT",
    ylim=(-0.2, 0.6),
    label_topy=0,
    hue="TC III",
    focus="EN NA LUO (SI6)",
)
r.plot_share_gr(
    index="PRODUCT",
    ylim=(-0.2, 0.6),
    unit="PTD",
    label_topy=0,
    hue="TC III",
    focus="EN NA LUO (SI6)",
)

# 滚动年TOP20产品销售额/PTD明细
r.plottable_latest(
    index="PRODUCT",
    hue=("MOLECULE", "CORPORATION"),
    focus="EN NA LUO (SI6)",
)
r.plottable_latest(
    index="PRODUCT",
    unit="PTD",
    hue=("MOLECULE", "CORPORATION"),
    focus="EN NA LUO (SI6)",
)

# TOP10产品滚动年销售额/PTD份额趋势
r.plot_share_trend(
    index="PRODUCT",
    focus="EN NA LUO (SI6)",
)
r.plot_share_trend(
    index="PRODUCT",
    unit="PTD",
    focus="EN NA LUO (SI6)",
)

# 肾性贫血定义市场历年产品销售额/PTD排名
r.plottable_annual(index="PRODUCT")
r.plottable_annual(index="PRODUCT", unit="PTD")


# # ESA+HIF定义市场
df2 = df[df["TC III"].isin(["ESA", "HIF-PHI"])]
r = CHPA(df2, name="ESA+HIF市场", date_column="DATE", period_interval=3)


r.plot_overall_performance_dual(index="TC III", unit_change="百万", sorter=["HIF-PHI", "ESA"],width=15,height=6)

r.plot_overall_performance(index="TC III", unit_change="百万")
r.plot_overall_performance(index="TC III", unit="PTD", unit_change="百万")
r.plot_overall_performance(index="TC III", period="QTR", unit_change="百万")
r.plot_overall_performance(index="TC III", period="QTR", unit="PTD", unit_change="百万")

r.plot_overall_performance_dual(
    index="MOLECULE", unit_change="百万", width=15, height=6, label_threshold=0.01
)
r.plot_overall_performance(index="MOLECULE", unit_change="百万")
r.plot_overall_performance(
    index="MOLECULE", unit="PTD", unit_change="百万", label_threshold=0.01
)


r.plot_size_diff(index="MOLECULE", unit_change="百万", hue="TC III", focus="恩那度司他")
r.plot_size_diff(
    index="MOLECULE", unit="PTD", unit_change="百万", hue="TC III", focus="恩那度司他"
)
r.plot_share_gr(
    index="MOLECULE", ylim=(-0.2, 0.6), label_topy=0, hue="TC III", focus="恩那度司他",
)
r.plot_share_gr(
    index="MOLECULE",
    ylim=(-0.2, 0.6),
    unit="PTD",
    label_topy=0,
    hue="TC III",
    focus="恩那度司他",
)

r.plottable_latest(index="MOLECULE", hue="TC III", focus="恩那度司他", fontsize=18)
r.plottable_latest(
    index="MOLECULE", unit="PTD", hue="TC III", focus="恩那度司他", fontsize=18
)
r.plot_share_trend(index="MOLECULE", focus="恩那度司他")
r.plot_share_trend(index="MOLECULE", unit="PTD", focus="恩那度司他")
r.plottable_annual(index="MOLECULE", fontsize=18)
r.plottable_annual(index="MOLECULE", unit="PTD", fontsize=18)

r.plot_size_diff(
    index="PRODUCT", unit_change="百万", hue="TC III", focus="EN NA LUO (SI6)"
)
r.plot_size_diff(
    index="PRODUCT",
    unit="PTD",
    unit_change="百万",
    hue="TC III",
    focus="EN NA LUO (SI6)",
)
r.plot_share_gr(
    index="PRODUCT",
    ylim=(-0.2, 0.6),
    label_topy=0,
    hue="TC III",
    focus="EN NA LUO (SI6)",
)
r.plot_share_gr(
    index="PRODUCT",
    ylim=(-0.2, 0.6),
    unit="PTD",
    label_topy=0,
    hue="TC III",
    focus="EN NA LUO (SI6)",
)

r.plottable_latest(
    index="PRODUCT",
    hue=("MOLECULE", "CORPORATION"),
    focus="EN NA LUO (SI6)",
)
r.plottable_latest(
    index="PRODUCT",
    unit="PTD",
    hue=("MOLECULE", "CORPORATION"),
    focus="EN NA LUO (SI6)",
)

r.plot_share_trend(
    index="PRODUCT",
    focus="EN NA LUO (SI6)",
)
r.plot_share_trend(
    index="PRODUCT",
    unit="PTD",
    focus="EN NA LUO (SI6)",
)

r.plottable_annual(index="PRODUCT")
r.plottable_annual(index="PRODUCT", unit="PTD")


# HIF定义市场------------

df3 = df[df["TC III"].isin(["HIF-PHI"])]
r = CHPA(df3, name="HIF-PHI市场", date_column="DATE", period_interval=3)

r.plot_overall_performance_dual(index="MOLECULE", unit_change="百万", width=15,height=6)

r.plot_overall_performance(index="MOLECULE", unit_change="百万")
r.plot_overall_performance(index="MOLECULE", unit="PTD", unit_change="百万")
r.plot_overall_performance(index="MOLECULE", period="QTR", unit_change="百万")
r.plot_overall_performance(
    index="MOLECULE", period="QTR", unit="PTD", unit_change="百万"
)

r.plottable_latest(
    index="MOLECULE", focus="恩那度司他", fontsize=18)
r.plottable_latest(
    index="MOLECULE", unit="PTD", focus="恩那度司他", fontsize=18)

r.plottable_latest(
    index="PRODUCT",
    hue=("MOLECULE", "CORPORATION"),
    focus="EN NA LUO (SI6)",
    fontsize=18
)
r.plottable_latest(
    index="PRODUCT",
    unit="PTD",
    hue=("MOLECULE", "CORPORATION"),
    focus="EN NA LUO (SI6)",
    fontsize=18
)
