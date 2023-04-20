from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"
# condition = "MOLECULE in ('氢氯吡格雷|CLOPIDOGREL', '氯吡格雷|CLOPIDOGREL')"

condition = "MOLECULE in ('CLOPIDOGREL|氯吡格雷', 'TICAGRELOR|替格瑞洛') OR PRODUCT='BAYASPIRIN               BAY'"
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


# df = df[df['MOLECULE']=='氯吡格雷']
# r = chpa(df, name='氯吡格雷市场')
# r.plot_overall_performance(dimension='PRODUCT')
# r.plot_overall_performance(dimension='PRODUCT', unit='Volume (Std Counting Unit)')

r = chpa(df, name="抗血小板市场")

# r.plot_overall_performance(
#     dimension="MOLECULE", sorter=["替格瑞洛", "氯吡格雷", "阿司匹林"]
# )
# r.plot_overall_performance(
#     dimension="MOLECULE",
#     unit="Volume (Std Counting Unit)",
#     sorter=["替格瑞洛", "氯吡格雷", "阿司匹林"],
# )

# r.plot_group_size_diff(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.01,
#     series_limit=250,
#     showLabel=True,
#     unit="Value",
# )
# r.plot_group_size_diff(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.03,
#     series_limit=250,
#     showLabel=True,
#     unit="Volume (Std Counting Unit)",
# )

# r.plot_group_share_gr(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     series_limit=250,
#     adjust_scale=0.01,
# )
# r.plot_group_share_gr(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     series_limit=250,
#     adjust_scale=0.02,
#     unit="Volume (Std Counting Unit)",
# )

# r.plot_share("PRODUCT", "TALCOM (SI6)", "份额", series_limit=7)
# r.plot_share("PRODUCT", "TALCOM (SI6)", "净增长贡献", series_limit=7)
# r.plot_share(
#     "PRODUCT", "TALCOM (SI6)", "份额", unit="Volume (Std Counting Unit)", series_limit=7
# )
# r.plot_share(
#     "PRODUCT",
#     "TALCOM (SI6)",
#     "净增长贡献",
#     unit="Volume (Std Counting Unit)",
#     series_limit=7,
# )

# Select * from data Where PERIOD = 'MAT' And UNIT = 'Value' AND (MOLECULE in ('替格瑞洛|TICAGRELOR', '氯吡格雷|CLOPIDOGREL', '氢氯吡格雷|CLOPIDOGREL') OR PRODUCT in ('拜阿司匹灵|BAYASPIRIN         BAY'))

# r.plot_share_trend(
#     dimension="PRODUCT",
#     column=None,
#     series_limit=10,
# )
# r.plot_share_trend(
#     dimension="PRODUCT",
#     column=None,
#     unit="Volume (Std Counting Unit)",
#     series_limit=10,
# )

# D_MAP = {
#     "PLAVIX (SG9)": "PLAVIX (SG9)",
#     "EN CUN (S1H)": "EN CUN (S1H)",
#     "TALCOM (SI6)": "TALCOM (SI6)",
#     "SHUAI XIN (LUU)": "SHUAI XIN/SHUAI TAI (LUU)",
#     "SHUAI TAI (LUU)": "SHUAI XIN/SHUAI TAI (LUU)",
#     "YOU LI WEI (NJ2)": "Others",
#     "CLOPIDOGREL BISULF (HDO)": "Others",
#     "PLAGRIL (DRL)": "Others",
#     "DE LUN (ZGZ)": "Others",
#     "XIN LAI LE (S-N)": "Others",
#     "RUI WEI SHENG (JBM)": "Others",
#     "DU QING (JYG)": "Others",
# }
# df["PRODUCT"] = df["PRODUCT"].map(D_MAP)
# r = chpa(df, name="氯吡格雷市场")

# r.plot_overall_performance(
#     dimension="PRODUCT",
# )
# r.plot_overall_performance(
#     dimension="PRODUCT",
#     unit="Volume (Std Counting Unit)",
# )


# r = chpa(df, name="抗血小板市场")

# r.plot_overall_performance(dimension="PRODUCT")
# r.plot_overall_performance(
#     dimension="PRODUCT",
#     unit="Volume (Std Counting Unit)",
# )

# print(r.agg_table(index=None, dimension='PRODUCT', column='泰嘉'))
