from msilib.schema import Condition
from CHPA import *

df_index = pd.read_excel("肾性贫血定义市场分子PTD系数.xlsx", engine="openpyxl")
df_index["PRODUCT_STR"] = df_index["PRODUCT"].apply(lambda x: f"'{x}'")
str = ", ".join(df_index["PRODUCT_STR"])

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"
condition = f"[PRODUCT] in ({str})"

# condition = "([TC III] in ('B03A HAEMATINICS,IRON & COMBS|补血药，铁剂和所有联合用药', \
#     'B03C ERYTHROPOIETIN PRODUCTS|红细胞生成素类药物', \
#     'B03D HIF-PH INHIBITORS|HIF-PH抑制剂'))"
sql = "SELECT * FROM " + table_name + " WHERE " + condition

df = pd.read_sql(sql=sql, con=engine)
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

df["PRODUCT_PACKAGE"] = (
    df["PRODUCT"].apply(lambda x: x.split("(")[0].strip()) + " " + df["PACKAGE"]
)

df_index.drop_duplicates(subset="PACKAGE", inplace=True)
for index, value in df_index.iterrows():
    mask = (df["PRODUCT_PACKAGE"] == value[3]) & (df["UNIT"] == "PTD")
    df.loc[mask, "AMOUNT"] = df.loc[mask, "AMOUNT"] * value[4]


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


r = chpa(df, name="肾性贫血市场")

# r.plot_overall_performance(dimension="TC III")
# r.plot_overall_performance(dimension="TC III", unit="PTD")
# r.plot_overall_performance(dimension="TC III", cycle="Quarterly", period="QTR")
# r.plot_overall_performance(
#     dimension="TC III", unit="PTD", cycle="Quarterly", period="QTR"
# )

# r.plot_share(dimension="TC III", column=None, return_type="份额")
# r.plot_share(dimension="TC III", column=None, return_type="净增长贡献")
# r.plot_share(dimension="TC III", column=None, return_type="份额", unit="PTD")
# r.plot_share(dimension="TC III", column=None, return_type="净增长贡献", unit="PTD")


# r.plot_group_size_diff(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.01,
#     series_limit=250,
#     showLabel=True,
#     unit="Value",
#     labelLimit=7,
# )

# r.plot_group_size_diff(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.2,
#     series_limit=250,
#     showLabel=True,
#     unit="PTD",
#     labelLimit=7,
# )

# r.plot_group_share_gr(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.01,
#     series_limit=250,
#     showLabel=True,
#     unit="Value",
# )

# r.plot_group_share_gr(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.2,
#     series_limit=250,
#     showLabel=True,
#     unit="PTD",
# )

# r.plot_share_trend(dimension="MOLECULE", column=None, series_limit=10)

# r.plot_share_trend(
#     dimension="MOLECULE",
#     column=None,
#     series_limit=10,
#     unit="PTD",
# )