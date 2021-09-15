from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

condition = (
    "[TC III] in ('C09B ACE INHIBITORS COMBS|血管紧张素转换酶抑制剂，联合用药' ,"
    "'C09D ANGIOTEN-II ANTAG, COMB|血管紧张素II拮抗剂，联合用药')"
    " AND MOLECULE not in ('沙库巴曲,缬沙坦|SACUBITRIL+VALSARTAN', '依那普利,叶酸|ENALAPRIL+FOLIC ACID')"
)
sql = "SELECT * FROM " + table_name + " WHERE " + condition
print(sql)
df = pd.read_sql(sql=sql, con=engine)

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[0]
df["PRODUCT"] = df["PRODUCT"].str.split("|").str[0]  # + '（'+ df['PRODUCT'].str.split('|').str[1].str[-3:] +'）'
df["PRODUCT_CORP"] = (
    df["PRODUCT_CORP"].str.split("（").str[0].str.split("|").str[0]
    + "\n"
    + df["PRODUCT_CORP"].str.split("（").str[1].str.split("|").str[0]
)

mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])

mask = df["MOLECULE"].isin(["厄贝沙坦", "缬沙坦", "氯沙坦", "奥美沙坦", "坎地沙坦", "厄贝沙坦,氢氯噻嗪", "福辛普利", "卡托普利", "赖诺普利", "依那普利"])
df.loc[mask, "VBP"] = "带量品种"
mask = df["MOLECULE"].isin(["厄贝沙坦", "缬沙坦", "氯沙坦", "奥美沙坦", "坎地沙坦", "厄贝沙坦,氢氯噻嗪", "福辛普利", "卡托普利", "赖诺普利", "依那普利"]) == False
df.loc[mask, "VBP"] = "非带量品种"

mask = df["MOLECULE"] == "舒脈康膜衣錠"
df.loc[mask, "MOLECULE"] = "奥美沙坦酯,氨氯地平"
mask = df["MOLECULE"] == "氯沙坦钾,氢氯噻嗪"
df.loc[mask, "MOLECULE"] = "氯沙坦,氢氯噻嗪"
mask = df["MOLECULE"] == "培哚普利氨氯地平片(III)"
df.loc[mask, "MOLECULE"] = "培哚普利,氨氯地平"
mask = df["MOLECULE"] == "坎地氢噻"
df.loc[mask, "MOLECULE"] = "坎地沙坦,氢氯噻嗪"
mask = df["MOLECULE"] == "复方卡托普利"
df.loc[mask, "MOLECULE"] = "卡托普利,氢氯噻嗪"
mask = df["MOLECULE"].isin(['氨氯地平贝那普利(II)', '氨氯地平贝那普利'])
df.loc[mask, "MOLECULE"] = "贝那普利,氨氯地平"


mask = df["MOLECULE"].str.contains("地平")
df.loc[mask, "FDC CLASS"] = "A+C"
mask = df["MOLECULE"].str.contains("噻嗪")
df.loc[mask, "FDC CLASS"] = "A+D"

r = chpa(df, name="RAAS复方制剂市场")
r.plot_overall_performance(dimension="TC II")
# r.plot_overall_performance(dimension='FDC CLASS')
# r.plot_overall_performance(dimension='FDC CLASS', unit='Volume (Std Counting Unit)')

# # r.plot_group_size_diff(index='MOLECULE', date=[r.latest_date()], dimension=None,
# #                       column='培哚普利,氨氯地平', adjust_scale=0.03,series_limit=250, labelLimit=8, showLabel=True, unit='Value')
# # r.plot_group_size_diff(index='MOLECULE', date=[r.latest_date()], dimension=None,
# #                       column='培哚普利,氨氯地平', adjust_scale=0.05,series_limit=250, labelLimit=8, showLabel=True, unit='Volume (Std Counting Unit)')
#
# r.plot_group_size_diff(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                        column=None, adjust_scale=0.03,series_limit=250, labelLimit=10, showLabel=True, unit='Value')
# r.plot_group_size_diff(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                        column=None, adjust_scale=0.05,series_limit=250, labelLimit=10, showLabel=True, unit='Volume (Std Counting Unit)')