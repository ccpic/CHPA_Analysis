from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"
condition = "([TC III] in ('B03A HAEMATINICS,IRON & COMBS|补血药，铁剂和所有联合用药', \
    'B03C ERYTHROPOIETIN PRODUCTS|红细胞生成素类药物', \
    'B03D HIF-PH INHIBITORS|HIF-PH抑制剂'))"
sql = "SELECT * FROM " + table_name + " WHERE " + condition
df = pd.read_sql(sql=sql, con=engine)

# 定义市场简化命名及调整系数
mask = df["TC III"] == 'B03A HAEMATINICS,IRON & COMBS|补血药，铁剂和所有联合用药'
df.loc[mask,['AMOUNT']] = df.loc[mask,['AMOUNT']] * 0.2
df.loc[mask,["TC III"]] = 'B03A HAEMATINICS,IRON & COMBS|补血药，铁剂'
mask = df["TC III"] == 'B03C ERYTHROPOIETIN PRODUCTS|红细胞生成素类药物'
df.loc[mask,['AMOUNT']] = df.loc[mask,['AMOUNT']] * 0.6
df.loc[mask,["TC III"]] = 'B03C ERYTHROPOIETIN PRODUCTS|红细胞生成素'

# 统一EPO分子名
mask = df['MOLECULE'].str.contains("重组人促红素")
df.loc[mask,['MOLECULE']] = "重组人促红素|EPOETIN"

df["TC III"] = (
    df["TC III"].str.split("|").str[0].str[:5] + df["TC III"].str.split("|").str[1]
)
df["MOLECULE"] = df["MOLECULE"].str.split("|").str[0]
df["PRODUCT"] = (
    (df["PRODUCT"].str.split("|").str[0])
    # + "（"
    # + df["PRODUCT"].str.split("|").str[1].str[-3:]
    # + "）"
)
df["PRODUCT_CORP"] = (
    df["PRODUCT_CORP"].str.split("（").str[0].str.split("|").str[0]
    + "\n"
    + df["PRODUCT_CORP"].str.split("（").str[1].str.split("|").str[0]
)

r = chpa(df, name="肾性贫血市场")

# r.plot_overall_performance(dimension="TC III")

# r.plot_share(dimension="TC III", column=None, return_type="份额")
# r.plot_share(dimension="TC III", column=None, return_type="净增长贡献")

# r.plot_group_size_diff(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.05,
#     series_limit=250,
#     showLabel=True,
#     unit="Value",
#     labelLimit=7,
# )

# r.plot_group_size_diff(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.05,
#     series_limit=250,
#     showLabel=True,
#     unit="Value",
#     labelLimit=7,
# )

r.plot_share_trend(
    dimension="PRODUCT",
    column=None,
    show_list=["爱瑞卓", "益比奥", "依普定", "怡宝", "赛博尔", "济脉欣"],
)

# r.plot_share_trend(dimension="TC IV", column=None)

# Select * from data Where PERIOD = 'MAT' And UNIT = 'Value' AND ([TC IV] in ('M05B3 BISPHOSPH OSTEOPOROSIS|治疗骨质疏松和骨钙失调的二膦酸盐类', 'H04A0 CALCITONINS|降钙素', 'H04E0 PARATHYROID HORM&ANALOGS|甲状旁腺激素及类似物', 'G03J0 SERMS|选择性雌激素受体调节剂') OR MOLECULE in ('地舒单抗|DENOSUMAB'))

# r.plot_group_size_diff(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.1,
#     series_limit=250,
#     showLabel=True,
#     unit="Value",
# )
# r.plot_group_share_gr(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.1,
#     series_limit=15,
# )

# r.plot_share(dimension="MOLECULE", column="特立帕肽", return_type="份额")
# r.plot_share(dimension="MOLECULE", column="特立帕肽", return_type="净增长贡献")

# r.plot_share_trend(dimension="MOLECULE", column="特立帕肽")

# r.plot_group_size_diff(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.05,
#     series_limit=250,
#     showLabel=True,
#     unit="Value",
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

# r.plot_share(dimension="PRODUCT", column="欣复泰（XIL）", return_type="份额")
# r.plot_share(dimension="PRODUCT", column="欣复泰（XIL）", return_type="净增长贡献")

# r.plot_share_trend(
#     dimension="PRODUCT",
#     column=None,
#     show_list=["密固达", "依固", "密盖息", "福美加", "福善美", "金尔力", "复泰奥", "欣复泰"],
# )
