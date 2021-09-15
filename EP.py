from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"
condition = "[TC IV] = 'N03A0 ANTI-EPILEPTICS|抗癫痫药物'"
sql = "SELECT * FROM " + table_name + " WHERE " + condition
df = pd.read_sql(sql=sql, con=engine)


df["TC IV"] = df["TC IV"].str.split("|").str[0].str[:6] + df["TC IV"].str.split("|").str[1]
df["MOLECULE"] = df["MOLECULE"].str.split("|").str[0]
df["PRODUCT"] = df["PRODUCT"].str.split("|").str[0] + "（" + df["PRODUCT"].str.split("|").str[1].str[-3:] + "）"
df["PRODUCT_CORP"] = (
    df["PRODUCT_CORP"].str.split("（").str[0].str.split("|").str[0]
    + "\n"
    + df["PRODUCT_CORP"].str.split("（").str[1].str.split("|").str[0]
)

mask = df["MOLECULE"].isin(["丙戊酸钠", "左乙拉西坦", "奥卡西平", "硫酸镁", "普瑞巴林", "拉莫三嗪", "苯巴比妥"])
df.loc[-mask, "MOLECULE"] = "其他"

# r = chpa(df, name='抗癫痫药物市场')
# r.plot_overall_performance(dimension='MOLECULE',sorter= ['丙戊酸钠','左乙拉西坦','奥卡西平', '硫酸镁', '普瑞巴林', '拉莫三嗪','苯巴比妥','其他'])
# r.plot_group_size_diff(index='MOLECULE', date=[r.latest_date()], dimension=None,
#                       column=None, adjust_scale=0.03, series_limit=250, showLabel=True, unit='Value')
# r.plot_group_share_gr(index='MOLECULE', date=[r.latest_date()], dimension=None,
#                       column=None, adjust_scale=0.05, series_limit=250, ylim=[-0.5, 1])
# r.plot_share(dimension='MOLECULE', column='左乙拉西坦', return_type='份额')
# r.plot_share(dimension='MOLECULE', column='左乙拉西坦', return_type='净增长贡献')
# r.plot_share_gr_trend(dimension='MOLECULE', column='左乙拉西坦')

# df = df[df['MOLECULE'] == '左乙拉西坦']
# r = chpa(df, name='左乙拉西坦市场')
# r.plot_group_size_diff(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column=None, adjust_scale=0.03, series_limit=250, showLabel=True, unit='Value')
# r.plot_group_share_gr(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column=None, adjust_scale=0.05, series_limit=15)
# r.plot_share(dimension='PRODUCT', column='左乙拉西坦片（SI6）', return_type='份额')
# r.plot_share(dimension='PRODUCT', column='左乙拉西坦片（SI6）', return_type='净增长贡献')
# r.plot_share_gr_trend(dimension='PRODUCT', column='左乙拉西坦片（SI6）')


mask = df["FORMULATION"] == "ORAL SOLID ORDINARY"
df.loc[mask, "FORMULATION"] = "口服片剂"
mask = df["FORMULATION"] == "ORAL SOLID LONG-ACTING"
df.loc[mask, "FORMULATION"] = "口服片剂"
mask = df["FORMULATION"] == "ORAL LIQUID ORDINARY"
df.loc[mask, "FORMULATION"] = "口服溶液"
mask = df["FORMULATION"] == "PARENTERAL ORDINARY"
df.loc[mask, "FORMULATION"] = "注射剂"

df = df[df["MOLECULE"] == "左乙拉西坦"]
# r = chpa(df, name='左乙拉西坦市场')
# r.plot_overall_performance(dimension='FORMULATION')

df = df[df["FORMULATION"] == "口服片剂"]
mask = df["STRENGTH"] == "0.5G"
df.loc[mask, "STRENGTH"] = "500MG"
mask = df["STRENGTH"] == "0.25G"
df.loc[mask, "STRENGTH"] = "250MG"

mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])
convert_std_volume(df, "MOLECULE", "左乙拉西坦", "250MG", 0.5)

r = chpa(df, name="左乙拉西坦口服片剂市场")
# r.plot_overall_performance(dimension='STRENGTH')
# r.plot_overall_performance(dimension='STRENGTH', unit='Volume (Std Counting Unit)')

# r.plot_share(dimension='STRENGTH', column=None, return_type='份额')
# r.plot_share(dimension='STRENGTH', column=None, return_type='净增长贡献')
# r.plot_share(dimension='STRENGTH', column=None, return_type='份额', unit='Volume (Std Counting Unit)')
# r.plot_share(dimension='STRENGTH', column=None, return_type='净增长贡献', unit='Volume (Std Counting Unit)')

# r.plot_share_trend(dimension='STRENGTH', column=None)
# r.plot_share_trend(dimension='STRENGTH', column=None, unit='Volume (Std Counting Unit)')


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
# r.plot_group_size_diff(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.1,
#     series_limit=250,
#     showLabel=True,
#     unit="Volume (Std Counting Unit)",
# )

# r.plot_group_share_gr(
#     index="PRODUCT_CORP", date=[r.latest_date()], dimension=None, column=None, adjust_scale=0.05, series_limit=15
# )
# r.plot_group_share_gr(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.1,
#     series_limit=15,
#     unit="Volume (Std Counting Unit)",
# )

r.plot_share(dimension='PRODUCT', column='左乙拉西坦片（SI6）', return_type='份额')
r.plot_share(dimension='PRODUCT', column='左乙拉西坦片（SI6）', return_type='净增长贡献')
r.plot_share(dimension='PRODUCT', column='左乙拉西坦片（SI6）', return_type='份额', unit='Volume (Std Counting Unit)')
r.plot_share(dimension='PRODUCT', column='左乙拉西坦片（SI6）', return_type='净增长贡献', unit='Volume (Std Counting Unit)')
r.plot_share_trend(dimension='PRODUCT_CORP', column='左乙拉西坦\n深圳信立泰药业股份有限公司')
r.plot_share_trend(dimension='PRODUCT_CORP', column='左乙拉西坦\n深圳信立泰药业股份有限公司', unit='Volume (Std Counting Unit)')



# r.plot_share_gr_trend(dimension='STRENGTH', column=None)
# r.plot_share_gr_trend(dimension='STRENGTH', column=None, unit='Volume (Std Counting Unit)')


