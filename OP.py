from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"
condition = "([TC IV] in ('M05B3 BISPHOSPH OSTEOPOROSIS|治疗骨质疏松和骨钙失调的二膦酸盐类', \
    'H04A0 CALCITONINS|降钙素', \
    'H04E0 PARATHYROID HORM&ANALOGS|甲状旁腺激素及类似物', \
    'G03J0 SERMS|选择性雌激素受体调节剂') OR MOLECULE in ('地舒单抗|DENOSUMAB'))"
sql = "SELECT * FROM " + table_name + " WHERE " + condition
df = pd.read_sql(sql=sql, con=engine)

df["TC IV"] = (
    df["TC IV"].str.split("|").str[0].str[:6] + df["TC IV"].str.split("|").str[1]
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
mask = df["TC IV"] == "M05B3 治疗骨质疏松和骨钙失调的二膦酸盐类"
df.loc[mask, "TC IV"] = "M05B3\n治疗骨质疏松\n和骨钙失调\n的二膦酸盐类"
mask = df["TC IV"] == "H04A0 降钙素"
df.loc[mask, "TC IV"] = "H04A0\n降钙素"
mask = df["TC IV"] == "H04E0 甲状旁腺激素及类似物"
df.loc[mask, "TC IV"] = "H04E0\n甲状旁腺激素\n及类似物"
mask = df["TC IV"] == "G03J0 选择性雌激素受体调节剂"
df.loc[mask, "TC IV"] = "G03J0\n选择性雌激素\n受体调节剂"
mask = df["MOLECULE"] == "鲑鱼降钙素"
df.loc[mask, "MOLECULE"] = "鲑降钙素"
mask = df["MOLECULE"] == "阿仑膦酸"
df.loc[mask, "MOLECULE"] = "阿仑膦酸钠"
mask = df["MOLECULE"] == "注射用重组特立帕肽"
df.loc[mask, "MOLECULE"] = "特立帕肽"
mask = df["MOLECULE"] == "地舒单抗"
df.loc[mask, "TC IV"] = "地舒单抗"

# r = chpa(df, name="骨松治疗市场")

# r.plot_overall_performance(dimension="TC IV")

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
# r.plot_group_share_gr(
#     index="TC IV",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.1,
#     series_limit=15,
# )

# r.plot_share(dimension="TC IV", column=None, return_type="份额")
# r.plot_share(dimension="TC IV", column=None, return_type="净增长贡献")

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

df = df[df["MOLECULE"] == "特立帕肽"]

r = chpa(df, name="特立帕肽市场")
r.plot_overall_performance(dimension="PRODUCT")