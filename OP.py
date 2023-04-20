from CHPA import *

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
df["STRENGTH"] = df["PACKAGE"].apply(lambda x: x.split()[-2])
df.to_excel("output.xlsx")  
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


def convert_std_volume(df, dimension, target, strength, ratio):
    column_unit = "UNIT"
    column_strength = "STRENGTH"
    unit_std_volume = "PTD"
    column_value = "AMOUNT"
    mask = (
        (df[dimension] == target)
        & (df[column_strength] == strength)
        & (df[column_unit] == unit_std_volume)
    )
    df.loc[mask, column_value] = (df.loc[mask, column_value]) * ratio


convert_std_volume(df, "MOLECULE", "阿仑膦酸", "70MG", 7)
convert_std_volume(df, "MOLECULE", "阿仑膦酸钠维生素D3", "5600IU", 7)
convert_std_volume(df, "MOLECULE", "阿仑膦酸钠维生素D3", "70MG", 7)
convert_std_volume(df, "MOLECULE", "阿仑膦酸钠维生素D3", "CTD", 7)
convert_std_volume(df, "MOLECULE", "利塞膦酸钠", "35MG", 7)
convert_std_volume(df, "MOLECULE", "依替膦酸二钠", "200MG", 0.5)
convert_std_volume(df, "MOLECULE", "唑来膦酸", "5MG", 365)
convert_std_volume(df, "MOLECULE", "唑来膦酸", "4MG", 365 / 12)
convert_std_volume(df, "MOLECULE", "依降钙素", "1ML", 7)
convert_std_volume(df, "PRODUCT", "DA FEN GAI (SZA)", "/DOS", 1 / 4)
convert_std_volume(df, "PRODUCT", "JIN ER LI (B-Y)", "/DOS", 0.5)
convert_std_volume(df, "PRODUCT", "MIACALCIC  (NVR)", "/DOS", 2)
convert_std_volume(df, "PRODUCT", "达芬盖", "50IU", 1 / 4)
convert_std_volume(df, "PRODUCT", "金尔力", "20Y", 0.5)
convert_std_volume(df, "PRODUCT", "普罗力", "60MG", 365 / 2)
convert_std_volume(df, "PRODUCT", "复泰奥", "20Y", 28)
convert_std_volume(df, "PRODUCT", "达芬盖（SZA）", "50IU", 1 / 4)
convert_std_volume(df, "PRODUCT", "金尔力（B-Y）", "20Y", 0.5)
convert_std_volume(df, "PRODUCT", "普罗力（AAI）", "60MG", 365 / 2)
convert_std_volume(df, "MOLECULE", "地舒单抗", "1ML", 365 / 2)
convert_std_volume(df, "PRODUCT", "复泰奥（LYG）", "20Y", 28)
# convert_std_volume(df, "PRODUCT", "欣复泰", "200IU", 365 / 36)
# convert_std_volume(df, "PRODUCT", "珍固", "200IU", 365 / 36)
convert_std_volume(df, "PRODUCT", "FORSTEO (LLY)", "2.4ML", 28)
convert_std_volume(df, "PRODUCT", "XIN FU TAI (XIL)", "2.4ML", 30)
# convert_std_volume(df, "PRODUCT", "ZHEN GU (S60)", "200IU", 365 / 36)

r = chpa(df, name="骨松治疗市场")

# r.plot_overall_performance(
#     dimension="TC IV", sorter=["SERM", "降钙素", "双膦酸盐类", "PTH", "地舒单抗"]
# )
# # r.plot_overall_performance(dimension="TC IV", unit="Volume (Counting Unit)", yunit="k")
# r.plot_overall_performance(
#     dimension="TC IV",
#     unit="PTD",
#     yunit="k",
#     sorter=["SERM", "降钙素", "双膦酸盐类", "PTH", "地舒单抗"],
# )

# r.plot_group_size_diff(
#     index="TC IV",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.1,
#     series_limit=250,
#     showLabel=True,
#     unit="Value",
# )
# r.plot_group_size_diff(
#     index="TC IV",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.3,
#     series_limit=250,
#     showLabel=True,
#     unit="PTD",
# )

# r.plot_group_share_gr(
#     index="TC IV",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.1,
#     series_limit=15,
# )
# r.plot_group_share_gr(
#     index="TC IV",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.1,
#     series_limit=15,
#     unit="PTD",
# )

# r.plot_share(dimension="TC IV", column=None, return_type="份额")
# r.plot_share(dimension="TC IV", column=None, return_type="净增长贡献")
# r.plot_share(dimension="TC IV", column=None, return_type="份额", unit="PTD")
# r.plot_share(dimension="TC IV", column=None, return_type="净增长贡献", unit="PTD")

# r.plot_share_trend(dimension="TC IV", column=None)
# r.plot_share_trend(dimension="TC IV", column=None, unit="PTD")

# Select * from data Where PERIOD = 'MAT' And UNIT = 'Value' AND ([TC IV] in ('M05B3 BISPHOSPH OSTEOPOROSIS|治疗骨质疏松和骨钙失调的二膦酸盐类', 'H04A0 CALCITONINS|降钙素', 'H04E0 PARATHYROID HORM&ANALOGS|甲状旁腺激素及类似物', 'G03J0 SERMS|选择性雌激素受体调节剂') OR MOLECULE in ('地舒单抗|DENOSUMAB'))

# r.plot_group_size_diff(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.05,
#     series_limit=250,
#     showLabel=True,
#     unit="Value",
# )
# r.plot_group_size_diff(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.3,
#     series_limit=250,
#     showLabel=True,
#     unit="PTD",
# )

# r.plot_group_share_gr(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.1,
#     series_limit=15,
# )
# r.plot_group_share_gr(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.1,
#     series_limit=15,
#     unit="PTD",
#     ylim=[-0.3, 0.4],
# )

# r.plot_share(dimension="MOLECULE", column="特立帕肽", series_limit=7, return_type="份额")
# r.plot_share(dimension="MOLECULE", column="特立帕肽", series_limit=7, return_type="净增长贡献")
# r.plot_share(
#     dimension="MOLECULE", column="特立帕肽", series_limit=7, return_type="份额", unit="PTD"
# )
# r.plot_share(
#     dimension="MOLECULE", column="特立帕肽", series_limit=7, return_type="净增长贡献", unit="PTD"
# )

# r.plot_share_trend(dimension="MOLECULE", column="特立帕肽")
# r.plot_share_trend(dimension="MOLECULE", column="特立帕肽", unit="PTD")

# r.plot_group_size_diff(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.05,
#     series_limit=250,
#     showLabel=True,
#     unit="Value",
# )
# r.plot_group_size_diff(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.2,
#     series_limit=250,
#     showLabel=True,
#     unit="PTD",
# )

# r.plot_group_share_gr(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.1,
#     series_limit=250,
#     ylim=[-0.5, 4],
# )
# r.plot_group_share_gr(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.1,
#     series_limit=250,
#     ylim=[-0.5, 4],
#     unit="PTD"
# )

# r.plot_share(dimension="PRODUCT", column="XIN FU TAI (XIL)", series_limit=8, return_type="份额")
# r.plot_share(
#     dimension="PRODUCT", column="XIN FU TAI (XIL)", series_limit=8, return_type="净增长贡献"
# )
# r.plot_share(
#     dimension="PRODUCT", column="XIN FU TAI (XIL)", series_limit=8, return_type="份额", unit="PTD"
# )
# r.plot_share(
#     dimension="PRODUCT", column="XIN FU TAI (XIL)", series_limit=8, return_type="净增长贡献", unit="PTD"
# )

# r.plot_share_trend(
#     dimension="PRODUCT",
#     column="XIN FU TAI (XIL)",
#     series_limit=10,
# )

# r.plot_share_trend(
#     dimension="PRODUCT",
#     column="XIN FU TAI (XIL)",
#     series_limit=10,
#     unit="PTD",
# )

df = df[df["MOLECULE"] == "特立帕肽"]

r = chpa(df, name="特立帕肽市场")
r.plot_overall_performance(dimension="PRODUCT")
# r.plot_overall_performance(
#     dimension="PRODUCT", unit="Volume (Counting Unit)", yunit="k"
# )
r.plot_overall_performance(dimension="PRODUCT", unit="PTD", yunit="k")
r.plot_overall_performance(dimension="PRODUCT", cycle="Quarterly", period="QTR")
r.plot_overall_performance(
    dimension="PRODUCT", unit="PTD", yunit="k", cycle="Quarterly",period="QTR"
)
