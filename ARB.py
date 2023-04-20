from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

# ARB单方
condition_arb = "[TC III] in ('C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药')"

# RAAS单方市场
condition_raasi_plain = (
    "[TC III] in ('C09A ACE INHIBITORS PLAIN|血管紧张素转换酶抑制剂，单一用药' ,"
    # "'C09B ACE INHIBITORS COMBS|血管紧张素转换酶抑制剂，联合用药' ,"
    "'C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药')"
    # "'C09D ANGIOTEN-II ANTAG, COMB|血管紧张素II拮抗剂，联合用药')"
)

# RAAS单方市场+ARNI
condition_raasi_plain_arni = (
    "[TC III] in ('C09A ACE INHIBITORS PLAIN|血管紧张素转换酶抑制剂，单一用药' ,"
    "'C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药')"
    " or MOLECULE = 'SACUBITRIL+VALSARTAN|沙库巴曲缬沙坦'"
)

# RAAS市场除沙库巴曲缬沙坦
condition_arni_excl = (
    "[TC III] in ('C09A ACE INHIBITORS PLAIN|血管紧张素转换酶抑制剂，单一用药' ,"
    "'C09B ACE INHIBITORS COMBS|血管紧张素转换酶抑制剂，联合用药' ,"
    "'C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药' ,"
    "'C09D ANGIOTEN-II ANTAG, COMB|血管紧张素II拮抗剂，联合用药') and MOLECULE != '沙库巴曲缬沙坦|SACUBITRIL+VALSARTAN'"
)

# RAAS市场
condition_raasi = (
    "[TC III] in ('C09A ACE INHIBITORS PLAIN|血管紧张素转换酶抑制剂，单一用药' ,"
    "'C09B ACE INHIBITORS COMBS|血管紧张素转换酶抑制剂，联合用药' ,"
    "'C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药' ,"
    "'C09D ANGIOTEN-II ANTAG, COMB|血管紧张素II拮抗剂，联合用药')"
)

# 诺欣妥+信立坦
# condition = "[MOLECULE] in ('沙库巴曲,缬沙坦|SACUBITRIL+VALSARTAN', '阿利沙坦|ALLISARTAN ISOPROXIL')"

# 所有高血压药
# condition = "[TC II]  in ('C03 DIURETICS|利尿剂', " \
#             "'C07 BETA BLOCKING AGENTS|β受体阻断剂', " \
#             "'C08 CALCIUM ANTAGONISTS|钙离子拮抗剂', " \
#             "'C09 RENIN-ANGIOTEN SYST AGENT|作用于肾素-血管紧张素系统的药物')"

condition = condition_raasi_plain_arni
sql = "SELECT * FROM " + table_name + " WHERE " + condition
df = pd.read_sql(sql=sql, con=engine)
# print(df['MOLECULE'].unique())

# for col in ['TC III', 'MOLECULE']:
#     df[col] = df[col].map(d_rename).fillna('其他')

# df['TC III'] = df['TC III'].str.split('|').str[1]
df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
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
mask = df["MOLECULE"] == "氯沙坦钾"
df.loc[mask, "MOLECULE"] = "氯沙坦"
mask = df["MOLECULE"] == "氯沙坦钾氢氯噻嗪"
df.loc[mask, "MOLECULE"] = "氯沙坦氢氯噻嗪"
mask = df["MOLECULE"] == "奥美沙坦酯氢氯噻嗪"
df.loc[mask, "MOLECULE"] = "奥美沙坦氢氯噻嗪"
mask = df["MOLECULE"] == "培哚普利叔丁胺"
df.loc[mask, "MOLECULE"] = "培哚普利"
mask = df["MOLECULE"] == "贝那普利,氨氯地平"
df.loc[mask, "MOLECULE"] = "贝那普利氨氯地平"
mask = df["MOLECULE"].isin(["氨氯地平贝那普利(II)", "氨氯地平贝那普利"])
df.loc[mask, "MOLECULE"] = "贝那普利氨氯地平"
mask = df["MOLECULE"].isin(
    [
        "厄贝沙坦",
        "缬沙坦",
        "氯沙坦",
        "奥美沙坦",
        "坎地沙坦",
        "厄贝沙坦,氢氯噻嗪",
        "福辛普利",
        "卡托普利",
        "赖诺普利",
        "依那普利",
        "培哚普利",
        "替米沙坦",
        "缬沙坦,氨氯地平",
        "缬沙坦,氢氯噻嗪",
    ]
)
df.loc[mask, "VBP"] = "VBP品种"
mask = (
    df["MOLECULE"].isin(
        [
            "厄贝沙坦",
            "缬沙坦",
            "氯沙坦",
            "奥美沙坦",
            "坎地沙坦",
            "厄贝沙坦,氢氯噻嗪",
            "福辛普利",
            "卡托普利",
            "赖诺普利",
            "依那普利",
            "培哚普利",
            "替米沙坦",
            "缬沙坦,氨氯地平",
            "缬沙坦,氢氯噻嗪",
        ]
    )
    == False
)
df.loc[mask, "VBP"] = "非VBP品种"

# ARNI销量打55折
if condition == condition_raasi or condition_raasi_plain_arni:
    mask = df["MOLECULE"] == "沙库巴曲缬沙坦"
    df.loc[mask, "AMOUNT"] = df.loc[mask, "AMOUNT"] * 0.55


mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])

df["STRENGTH"] = df["PACKAGE"].apply(lambda x: x.split()[-2])

convert_std_volume(df, "MOLECULE", "氯沙坦", "100MG", 2)
convert_std_volume(df, "MOLECULE", "厄贝沙坦", "75MG", 0.5)
convert_std_volume(df, "MOLECULE", "替米沙坦", "20MG", 0.25)
convert_std_volume(df, "MOLECULE", "替米沙坦", "40MG", 0.5)
convert_std_volume(df, "MOLECULE", "坎地沙坦", "4MG", 0.5)
convert_std_volume(df, "MOLECULE", "缬沙坦", "40MG", 0.5)
convert_std_volume(df, "MOLECULE", "缬沙坦", "160MG", 2)
convert_std_volume(df, "MOLECULE", "培哚普利", "8MG", 2)
convert_std_volume(df, "MOLECULE", "贝那普利", "5MG", 0.5)
convert_std_volume(df, "MOLECULE", "卡托普利", "12.5MG", 0.25)
convert_std_volume(df, "MOLECULE", "卡托普利", "25MG", 0.5)
convert_std_volume(df, "MOLECULE", "依那普利", "5MG", 0.5)
convert_std_volume(df, "MOLECULE", "雷米普利", "2.5MG", 0.5)
convert_std_volume(df, "MOLECULE", "沙库巴曲缬沙坦", "100MG", 0.5)
convert_std_volume(df, "MOLECULE", "沙库巴曲缬沙坦", "50MG", 0.25)

mask = df["MOLECULE"].str.contains("普利")
df.loc[mask, "TC III"] = "ACEI"
mask = df["MOLECULE"].str.contains("沙坦")
df.loc[mask, "TC III"] = "ARB"
mask = df["MOLECULE"].str.contains("地平")
df.loc[mask, "TC III"] = "A+C"
mask = df["MOLECULE"].str.contains("噻嗪|舒脈康膜衣錠|叶酸|吲达帕胺|氢噻")
df.loc[mask, "TC III"] = "A+D"
mask = df["MOLECULE"].str.contains("沙库巴曲缬沙坦")
df.loc[mask, "TC III"] = "ARNI"


# writer = pd.ExcelWriter('output.xlsx')
# df.to_excel(writer,'Sheet1')
# writer.save()

# dimension = "MOLECULE"
# target = "阿利沙坦"
# filter_list = ["缬沙坦", "厄贝沙坦", "氯沙坦", "奥美沙坦", "坎地沙坦", "阿利沙坦", "缬沙坦,氨氯地平", "厄贝沙坦,氢氯噻嗪", "培哚普利", "贝那普利,氨氯地平"]
# # filter_list = ["缬沙坦", "厄贝沙坦", "氯沙坦", "奥美沙坦", "坎地沙坦", "阿利沙坦", "培哚普利" , '贝那普利', '替米沙坦']
# # dimension = "PRODUCT"
# # target = "信立坦"
# # filter_list = ["代文", "安博维", "雅施达", "倍博特", "科素亚", "傲坦", "信立坦", '百安新']
# # filter_list = ["代文", "安博维", "雅施达", "洛汀新", "科素亚", "傲坦", "信立坦"]
# r.plot_share_trend(dimension=dimension, column=target, show_list=filter_list)
# r.plot_share_trend(dimension=dimension, column=target, period="QTR", show_list=filter_list)
# r.plot_share_trend(dimension=dimension, column=target, unit="Volume (Std Counting Unit)", show_list=filter_list)
# r.plot_share_trend(
#     dimension=dimension, column=target, period="QTR", unit="Volume (Std Counting Unit)", show_list=filter_list
# )
# r.plot_overall_performance(dimension='MOLECULE')
# r.plot_overall_performance(dimension='MOLECULE', unit='Volume (Std Counting Unit)')
# r.plot_annual_performance(dimension='MOLECULE', sorter=['缬沙坦', '厄贝沙坦', '氯沙坦钾', '替米沙坦', '坎地沙坦', '奥美沙坦', '阿利沙坦', '培哚普利', '贝那普利', '其他'])
# r.plot_annual_performance(dimension='MOLECULE', unit='Volume (Counting Unit)', sorter=['缬沙坦', '厄贝沙坦', '氯沙坦钾', '替米沙坦', '坎地沙坦', '奥美沙坦', '阿利沙坦', '培哚普利', '贝那普利', '其他'])


r = chpa(df, name="RAAS+ARNI市场")

# r.plot_overall_performance(
#     dimension="TC III",
#     sorter=["ARB", "ACEI", "A+C", "A+D", "ARNI"],
#     width=15,
#     height=6,
# )
# r.plot_overall_performance(
#     dimension="TC III",
#     unit="Volume (Std Counting Unit)",
#     sorter=["ARB", "ACEI", "A+C", "A+D", "ARNI"],
#     width=15,
#     height=6,
# )
# r.plot_overall_performance(
#     dimension="TC III",
#     sorter=["ARB", "ACEI", "A+C", "A+D", "ARNI"],
#     width=15,
#     height=6,
#     period="QTR",
#     cycle="Quarterly",
# )
# r.plot_overall_performance(
#     dimension="TC III",
#     unit="Volume (Std Counting Unit)",
#     sorter=["ARB", "ACEI", "A+C", "A+D", "ARNI"],
#     width=15,
#     height=6,
#     period="QTR",
#     cycle="Quarterly",
# )

# r.plot_overall_performance(dimension="VBP")
# r.plot_overall_performance(dimension="VBP", unit="Volume (Std Counting Unit)")

# r.plot_group_size_diff(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column="阿利沙坦",
#     adjust_scale=0.01,
#     series_limit=250,
#     showLabel=True,
#     unit="Value",
#     labelLimit=20,
# )
# r.plot_group_size_diff(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column="阿利沙坦",
#     adjust_scale=0.02,
#     series_limit=250,
#     showLabel=True,
#     unit="Volume (Std Counting Unit)",
#     labelLimit=20,
# )

# r.plot_group_share_gr(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column="阿利沙坦",
#     adjust_scale=0.01,
#     series_limit=250,
#     showLabel=True,
#     labelLimit=20,
#     ylim=[-1, 1],
# )
# r.plot_group_share_gr(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column="阿利沙坦",
#     adjust_scale=0.02,
#     series_limit=250,
#     showLabel=True,
#     unit="Volume (Std Counting Unit)",
#     labelLimit=20,
#     ylim=[-1, 2],
# )

# r.plot_share(dimension="MOLECULE", column="阿利沙坦", return_type="份额")
# r.plot_share(dimension="MOLECULE", column="阿利沙坦", return_type="净增长贡献")
# r.plot_share(
#     dimension="MOLECULE",
#     column="阿利沙坦",
#     return_type="份额",
#     unit="Volume (Std Counting Unit)",
# )
# r.plot_share(
#     dimension="MOLECULE",
#     column="阿利沙坦",
#     return_type="净增长贡献",
#     unit="Volume (Std Counting Unit)",
# )

# r.plot_share_trend(
#     dimension="MOLECULE",
#     column="阿利沙坦",
# )
# r.plot_share_trend(
#     dimension="MOLECULE",
#     column="阿利沙坦",
#     unit="Volume (Std Counting Unit)",
#     series_limit=12,
# )

# r.plot_share_trend(
#     dimension="MOLECULE",
#     column="阿利沙坦",
#     show_list=[
#         "沙库巴曲缬沙坦",
#         "缬沙坦氨氯地平",
#         "缬沙坦",
#         "阿利沙坦",
#         "贝那普利氨氯地平",
#         "厄贝沙坦氢氯噻嗪",
#         "贝那普利",
#         "厄贝沙坦",
#         "替米沙坦",
#         "氯沙坦氢氯噻嗪",
#         "氯沙坦",
#         "奥美沙坦",
#         "奥美沙坦氢氯噻嗪",
#     ],
# )
# r.plot_share_trend(
#     dimension="MOLECULE",
#     column="阿利沙坦",
#     unit="Volume (Std Counting Unit)",
#     show_list=[
#         "沙库巴曲缬沙坦",
#         "厄贝沙坦",
#         "缬沙坦",
#         "厄贝沙坦氢氯噻嗪",
#         "氯沙坦",
#         "缬沙坦氨氯地平",
#         "贝那普利",
#         "依那普利",
#         "替米沙坦",
#         "坎地沙坦",
#         "培哚普利",
#         "阿利沙坦",
#         "奥美沙坦",
#         "奥美沙坦氢氯噻嗪",
#     ],
# )


# r.plot_group_size_diff(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.015,
#     series_limit=30,
#     showLabel=True,
#     unit="Value",
#     labelLimit=20,
# )
# r.plot_group_size_diff(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.03,
#     series_limit=30,
#     showLabel=True,
#     unit="Volume (Std Counting Unit)",
#     labelLimit=20,
# )
# r.plot_group_share_gr(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.015,
#     series_limit=30,
#     showLabel=True,
#     ylim=[-1, 1],
#     labelLimit=20,
# )
# r.plot_group_share_gr(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.03,
#     series_limit=30,
#     showLabel=True,
#     unit="Volume (Std Counting Unit)",
#     ylim=[-1, 2],
#     labelLimit=20,
# )

# r.plot_share(dimension="PRODUCT", column="XIN LI TAN (SI6)", return_type="份额")
# r.plot_share(dimension="PRODUCT", column="XIN LI TAN (SI6)", return_type="净增长贡献")
# r.plot_share(
#     dimension="PRODUCT",
#     column="XIN LI TAN (SI6)",
#     return_type="份额",
#     unit="Volume (Std Counting Unit)",
# )
# r.plot_share(
#     dimension="PRODUCT",
#     column="XIN LI TAN (SI6)",
#     return_type="净增长贡献",
#     unit="Volume (Std Counting Unit)",
# )

# r.plot_share_trend(
#     dimension="PRODUCT",
#     column="XIN LI TAN (SI6)",
#     series_limit=10,
# )
# r.plot_share_trend(
#     dimension="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     column="XIN LI TAN (SI6)",
#     series_limit=10,
# )

r = chpa(df, name="RAAS平片+ARNI市场")

# r.plot_overall_performance(dimension="TC III")
# r.plot_overall_performance(dimension="TC III", unit="Volume (Std Counting Unit)")
# r.plot_overall_performance(dimension="TC III", period="QTR", cycle="Quarterly")
# r.plot_overall_performance(
#     dimension="TC III",
#     unit="Volume (Std Counting Unit)",
#     period="QTR",
#     cycle="Quarterly",
# )


# r.plot_overall_performance(dimension="VBP")
# r.plot_overall_performance(dimension="VBP", unit="Volume (Std Counting Unit)")


# r.plot_group_size_diff(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column="阿利沙坦",
#     adjust_scale=0.02,
#     series_limit=250,
#     showLabel=True,
#     unit="Value",
# )
# r.plot_group_size_diff(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column="阿利沙坦",
#     adjust_scale=0.04,
#     series_limit=250,
#     showLabel=True,
#     unit="Volume (Std Counting Unit)",
# )

# r.plot_group_share_gr(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column="阿利沙坦",
#     adjust_scale=0.01,
#     series_limit=250,
#     showLabel=True,
#     ylim=[-0.6, 0.4],
#     labelLimit=12,
# )
# r.plot_group_share_gr(
#     index="MOLECULE",
#     date=[r.latest_date()],
#     dimension=None,
#     column="阿利沙坦",
#     adjust_scale=0.01,
#     series_limit=250,
#     showLabel=True,
#     unit="Volume (Std Counting Unit)",
#     ylim=[-1, 2],
#     labelLimit=12,
# )

# r.plot_share(dimension="MOLECULE", column="阿利沙坦", return_type="份额")
# r.plot_share(dimension="MOLECULE", column="阿利沙坦", return_type="净增长贡献")
# r.plot_share(
#     dimension="MOLECULE",
#     column="阿利沙坦",
#     return_type="份额",
#     unit="Volume (Std Counting Unit)",
# )
# r.plot_share(
#     dimension="MOLECULE",
#     column="阿利沙坦",
#     return_type="净增长贡献",
#     unit="Volume (Std Counting Unit)",
# )

# r.plot_share_trend(
#     dimension="MOLECULE",
#     column="阿利沙坦",
#     show_list=[
#         "沙库巴曲缬沙坦",
#         "缬沙坦",
#         "厄贝沙坦",
#         "氯沙坦",
#         "替米沙坦",
#         "坎地沙坦",
#         "奥美沙坦",
#         "阿利沙坦",
#         "培哚普利",
#         "贝那普利",
#     ],
# )
# r.plot_share_trend(
#     dimension="MOLECULE",
#     column="阿利沙坦",
#     unit="Volume (Std Counting Unit)",
#     show_list=[
#         "沙库巴曲缬沙坦",
#         "缬沙坦",
#         "厄贝沙坦",
#         "氯沙坦",
#         "替米沙坦",
#         "坎地沙坦",
#         "奥美沙坦",
#         "阿利沙坦",
#         "培哚普利",
#         "贝那普利",
#     ],
# )

# r.plot_group_size_diff(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.015,
#     series_limit=30,
#     showLabel=True,
#     unit="Value",
# )
# r.plot_group_size_diff(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.03,
#     series_limit=30,
#     showLabel=True,
#     unit="Volume (Std Counting Unit)",
# )

# r.plot_group_share_gr(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.015,
#     series_limit=30,
#     showLabel=True,
#     ylim=[-1, 1],
# )
# r.plot_group_share_gr(
#     index="PRODUCT",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.03,
#     series_limit=30,
#     showLabel=True,
#     labelLimit=20,
#     unit="Volume (Std Counting Unit)",
#     ylim=[-1, 2],
# )

# r.plot_share(dimension="PRODUCT", column="XIN LI TAN (SI6)", return_type="份额")
# r.plot_share(dimension="PRODUCT", column="XIN LI TAN (SI6)", return_type="净增长贡献")
# r.plot_share(
#     dimension="PRODUCT",
#     column="XIN LI TAN (SI6)",
#     return_type="份额",
#     unit="Volume (Std Counting Unit)",
# )
# r.plot_share(
#     dimension="PRODUCT",
#     column="XIN LI TAN (SI6)",
#     return_type="净增长贡献",
#     unit="Volume (Std Counting Unit)",
# )

# r.plot_share_trend(
#     dimension="PRODUCT",
#     column="XIN LI TAN (SI6)",
#     series_limit=10,
# )
# r.plot_share_trend(
#     dimension="PRODUCT",
#     column="XIN LI TAN (SI6)",
#     unit="Volume (Std Counting Unit)",
#     series_limit=10,
# )

df = df[df["TC III"] == "ARB"]
r = chpa(df, name="ARB平片市场")
r.plot_overall_performance(dimension="MOLECULE", width=15, height=6)
# r.plot_annual_performance(dimension='MOLECULE', sorter=['缬沙坦', '厄贝沙坦', '氯沙坦钾', '替米沙坦', '坎地沙坦', '奥美沙坦', '阿利沙坦'])
# r.plot_annual_performance(dimension='MOLECULE', unit='Volume (Counting Unit)', sorter=['缬沙坦', '厄贝沙坦', '氯沙坦钾', '替米沙坦', '坎地沙坦', '奥美沙坦', '阿利沙坦'])
# r.plot_group_share_gr(index='MOLECULE', date=[r.latest_date()], dimension=None,
#                       column='阿利沙坦', adjust_scale=0.02, series_limit=250)
# r.plot_group_share_gr(index='MOLECULE', date=[r.latest_date()], dimension=None,
#                       column='阿利沙坦', adjust_scale=0.08, unit='Volume (Counting Unit)', series_limit=250)
# r.plot_group_share_gr(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column='信立坦\n深圳信立泰药业股份有限公司', adjust_scale=0.02, series_limit=15)
# r.plot_group_share_gr(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column='信立坦\n深圳信立泰药业股份有限公司', adjust_scale=0.08, unit='Volume (Counting Unit)', series_limit=15)


# r.plot_share(dimension='MOLECULE', column='阿利沙坦', return_type='份额')
# r.plot_share(dimension='MOLECULE', column='阿利沙坦', return_type='净增长贡献')
# r.plot_share(dimension='MOLECULE', column='阿利沙坦', return_type='份额', unit='Volume (Counting Unit)')
# r.plot_share(dimension='MOLECULE', column='阿利沙坦', return_type='净增长贡献', unit='Volume (Counting Unit)')


# df = df[df['TC III'] == 'ACEI']
#
# mask = df['MOLECULE'].isin(['贝那普利', '培哚普利叔丁胺', '依那普利', '福辛普利'])
# df.loc[-mask, 'MOLECULE'] = '其他'
#
#
#
# r = chpa(df, name='ACEI平片市场')
# r.plot_annual_performance(dimension='MOLECULE', sorter=['贝那普利', '培哚普利叔丁胺', '依那普利', '福辛普利', '其他'])
# r.plot_annual_performance(dimension='MOLECULE', unit='Volume (Counting Unit)', sorter=['贝那普利', '培哚普利叔丁胺', '依那普利', '福辛普利', '其他'])
# r.plot_group_share_gr(index='MOLECULE', date=[r.latest_date()], dimension=None,
#                       column=None, adjust_scale=0.05, series_limit=15)
# r.plot_group_share_gr(index='MOLECULE', date=[r.latest_date()], dimension=None,
#                       column=None, adjust_scale=0.08, unit='Volume (Counting Unit)', series_limit=15)
# r.plot_share(dimension='MOLECULE', column='贝那普利', return_type='份额')
# r.plot_share(dimension='MOLECULE', column='贝那普利', return_type='净增长贡献')
# r.plot_share(dimension='MOLECULE', column='贝那普利', return_type='份额', unit='Volume (Counting Unit)')
# r.plot_share(dimension='MOLECULE', column='贝那普利', return_type='净增长贡献', unit='Volume (Counting Unit)')
# r.plot_group_share_gr(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column='信达怡\n深圳信立泰药业股份有限公司', adjust_scale=0.05, series_limit=15)
# r.plot_group_share_gr(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column='信达怡\n深圳信立泰药业股份有限公司', adjust_scale=0.08, unit='Volume (Counting Unit)', series_limit=15)
# r.plot_share_gr_trend(dimension='MOLECULE', column='贝那普利')
# r.plot_share_gr_trend(dimension='MOLECULE', column='贝那普利', unit='Volume (Counting Unit)')
# r.plot_share_gr_trend(dimension='PRODUCT', column='信达怡')
# r.plot_share_gr_trend(dimension='PRODUCT', column='信达怡', unit='Volume (Counting Unit)')


# df = df[df['MOLECULE']=='贝那普利']
# r = chpa(df, name='贝那普利市场')
# r.plot_group_share_gr(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column='信达怡\n深圳信立泰药业股份有限公司', adjust_scale=0.05, series_limit=15)
# r.plot_group_share_gr(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column='信达怡\n深圳信立泰药业股份有限公司', adjust_scale=0.08, unit='Volume (Counting Unit)', series_limit=15)
# r.plot_share_gr_trend(dimension='PRODUCT', column='信达怡')
# r.plot_share_gr_trend(dimension='PRODUCT', column='信达怡', unit='Volume (Counting Unit)')


# df = df[df['MOLECULE']=='奥美沙坦']
# r = chpa(df, name='奥美沙坦市场')

# r.plot_group_share_gr(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column=None, adjust_scale=0.05, series_limit=15)
# r.plot_group_share_gr(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column=None, adjust_scale=0.08, unit='Volume (Counting Unit)', series_limit=15)
# r.plot_share_gr_trend(dimension='PRODUCT', column=None)
# r.plot_share_gr_trend(dimension='PRODUCT', column=None, unit='Volume (Counting Unit)')
# r.plot_share(dimension='PRODUCT', column=None, return_type='份额')
# r.plot_share(dimension='PRODUCT', column=None, return_type='净增长贡献')
# r.plot_share(dimension='PRODUCT', column=None, return_type='份额', unit='Volume (Counting Unit)')
# r.plot_share(dimension='PRODUCT', column=None, return_type='净增长贡献', unit='Volume (Counting Unit)')

# r = chpa(df, name="信立坦 versus 诺欣妥")
# r.plot_share_trend(dimension='PRODUCT', column='信立坦')
# r.plot_group_size_diff(index='PRODUCT', date=[r.latest_date()], dimension=None,
#                       column='信立坦', adjust_scale=0.03, series_limit=250, showLabel=True, unit='Value')
# r.plot_group_size_diff(index='PRODUCT', date=[r.latest_date()], dimension=None,
#                       column='信立坦', adjust_scale=0.03, series_limit=250, showLabel=True, unit='Value', period='QTR')
# r.plot_share(dimension="PRODUCT", column=None, return_type="份额")
# r.plot_share(dimension="PRODUCT", column=None, return_type="净增长贡献")
# r.plot_share(dimension="PRODUCT", column=None, return_type="份额", period="QTR")
# r.plot_share(dimension="PRODUCT", column=None, return_type="净增长贡献", period="QTR")

# df = df[df["MOLECULE"] == "奥美沙坦"]

# print(df.PRODUCT.unique())

# lst_winner_generic = [
#     "兰沙（BW.）",
#     "欧美利（GY0）",
#     "信达悦（SI6）",
#     "希佳（C2T）",
# ]
# lst_loser_origin = ["傲坦（DCG）"]
# mask = df["PRODUCT"].isin(lst_winner_generic)
# df.loc[mask, "VBP_STATUS"] = "中标仿制"
# mask = df["PRODUCT"].isin(lst_loser_origin)
# df.loc[mask, "VBP_STATUS"] = "未中标原研"
# mask = (df["PRODUCT"].isin(lst_winner_generic) == False) & (
#     df["PRODUCT"].isin(lst_loser_origin) == False
# )
# df.loc[mask, "VBP_STATUS"] = "未中标仿制"

# mask = (
#     df["PRODUCT"].isin(["兰沙（BW.）", "欧美利（GY0）", "信达悦（SI6）", "希佳（C2T）", "傲坦（DCG）"])
#     == False
# )
# df.loc[mask, "PRODUCT"] = "其他"

# r = chpa(df, name="奥美沙坦市场")

# r.plot_overall_performance(
#     dimension="VBP_STATUS",
#     sorter=["中标仿制", "未中标原研", "未中标仿制"],
# )
# r.plot_overall_performance(
#     dimension="VBP_STATUS",
#     unit="Volume (Std Counting Unit)",
#     sorter=["中标仿制", "未中标原研", "未中标仿制"],
# )

# r.plot_overall_performance(
#     dimension="PRODUCT",
#     sorter=["傲坦（DCG）", "兰沙（BW.）", "希佳（C2T）", "欧美利（GY0）", "信达悦（SI6）", "其他"],
# )
# r.plot_overall_performance(
#     dimension="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     sorter=["傲坦（DCG）", "兰沙（BW.）", "希佳（C2T）", "欧美利（GY0）", "信达悦（SI6）", "其他"],
# )

# r.plot_group_size_diff(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column="信立明",
#     adjust_scale=0.3,
#     series_limit=250,
#     showLabel=True,
# )
# r.plot_group_size_diff(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column="信立明",
#     unit="Volume (Std Counting Unit)",
#     adjust_scale=0.3,
#     series_limit=250,
#     showLabel=True,
# )
# r.plot_group_share_gr(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.3,
#     series_limit=15,
# )
# r.plot_group_share_gr(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     unit="Volume (Std Counting Unit)",
#     adjust_scale=0.3,
#     series_limit=15,
# )

# r = chpa(df, name="ARB单方市场")

# r.plot_overall_performance(dimension="VBP")
# r.plot_overall_performance(dimension="VBP", unit="Volume (Std Counting Unit)")
