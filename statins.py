from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"
condition = "[TC IV] = 'C10A1 STATINS (HMG-COA RED)|他汀类(HMG-COA（羟-甲戊二酰辅酶A）还原酶抑制剂)' and MOLECULE != '洛伐他汀|LOVASTATIN'"
sql = "SELECT * FROM " + table_name + " WHERE " + condition
df = pd.read_sql(sql=sql, con=engine)

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[0]
df["PRODUCT"] = (
    df["PRODUCT"].str.split("|").str[0]
    + "（"
    + df["PRODUCT"].str.split("|").str[1].str[-3:]
    + "）"
)
df["PRODUCT_CORP"] = (
    df["PRODUCT_CORP"].str.split("（").str[0].str.split("|").str[0]
    + "\n"
    + df["PRODUCT_CORP"].str.split("（").str[1].str.split("|").str[0]
)
mask = df["MOLECULE"] == "匹伐他汀钙片"
df.loc[mask, "MOLECULE"] = "匹伐他汀"

mask = df["MOLECULE"].isin(
    [
        "阿托伐他汀",
        "瑞舒伐他汀",
        "辛伐他汀",
        "匹伐他汀",
    ]
)
df.loc[mask, "VBP"] = "带量品种"
mask = (
    df["MOLECULE"].isin(
        [
            "阿托伐他汀",
            "瑞舒伐他汀",
            "辛伐他汀",
            "匹伐他汀",
        ]
    )
    == False
)
df.loc[mask, "VBP"] = "非带量品种"

lst_winner_generic = [
    "京可新（ZXJ）",
    "邦之（JBI）",
    "匹伐他汀（JN.）",
    "信立明（SI6）",
    "优力平（ZLU）",
    "阿托伐他汀（FJ.）",
    "阿托伐他汀（QIL）",
    "瑞舒伐他汀（NVU）",
    "瑞舒伐他汀（C2T）",
    "瑞舒伐他汀钙片（ZHI）",
    "京诺（ZXJ）",
    "阿乐（SDS）",
]
lst_loser_origin = [
    "力清之（KW.）",
    "立普妥（VI/）",
    "可定（A5Z）",
]
mask = df["PRODUCT"].isin(lst_winner_generic)
df.loc[mask, "VBP_STATUS"] = "中标仿制"
mask = df["PRODUCT"].isin(lst_loser_origin)
df.loc[mask, "VBP_STATUS"] = "未中标原研"
mask = (df["PRODUCT"].isin(lst_winner_generic) == False) & (
    df["PRODUCT"].isin(lst_loser_origin) == False
)
df.loc[mask, "VBP_STATUS"] = "未中标仿制"

mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])
convert_std_volume(df, "MOLECULE", "匹伐他汀", "1MG", 0.5)
convert_std_volume(df, "MOLECULE", "阿托伐他汀", "10MG", 0.5)
convert_std_volume(df, "MOLECULE", "阿托伐他汀", "40MG", 2)
convert_std_volume(df, "MOLECULE", "瑞舒伐他汀", "5MG", 0.5)
convert_std_volume(df, "MOLECULE", "瑞舒伐他汀", "20MG", 2)
convert_std_volume(df, "MOLECULE", "辛伐他汀", "5MG", 0.25)
convert_std_volume(df, "MOLECULE", "辛伐他汀", "10MG", 0.5)
convert_std_volume(df, "MOLECULE", "辛伐他汀", "40MG", 2)
convert_std_volume(df, "MOLECULE", "氟伐他汀", "20MG", 0.5)
convert_std_volume(df, "MOLECULE", "氟伐他汀", "80MG", 2)
convert_std_volume(df, "MOLECULE", "普伐他汀", "10MG", 0.5)
convert_std_volume(df, "MOLECULE", "普伐他汀", "40MG", 2)
convert_std_volume(df, "MOLECULE", "洛伐他汀", "10MG", 0.5)

r = chpa(df, name="他汀市场")

# r.plot_overall_performance(
#     dimension="MOLECULE", sorter=["阿托伐他汀", "瑞舒伐他汀", "匹伐他汀", "辛伐他汀", "氟伐他汀", "普伐他汀"]
# )
# r.plot_overall_performance(
#     dimension="MOLECULE",
#     unit="Volume (Std Counting Unit)",
#     sorter=["阿托伐他汀", "瑞舒伐他汀", "匹伐他汀", "辛伐他汀", "氟伐他汀", "普伐他汀"],
# )

# r.plot_overall_performance(dimension="VBP")
# r.plot_overall_performance(dimension="VBP", unit="Volume (Std Counting Unit)")

# r.plot_group_size_diff(index='MOLECULE', date=[r.latest_date()], dimension=None,
#                       column='匹伐他汀', adjust_scale=0.01, series_limit=250, showLabel=True)
# r.plot_group_size_diff(index='MOLECULE', date=[r.latest_date()], dimension=None,
#                       column='匹伐他汀', unit='Volume (Std Counting Unit)', adjust_scale=0.03, series_limit=250, showLabel=True)
# r.plot_group_share_gr(index='MOLECULE', date=[r.latest_date()], dimension=None,
#                       column=None, adjust_scale=0.01, series_limit=15)
# r.plot_group_share_gr(index='MOLECULE', date=[r.latest_date()], dimension=None,
#                       column=None,unit='Volume (Std Counting Unit)', adjust_scale=0.05, series_limit=15)

# r.plot_share(dimension='MOLECULE', column=None, return_type='份额')
# r.plot_share(dimension='MOLECULE', column=None, return_type='净增长贡献')
# r.plot_share(dimension='MOLECULE', column=None, unit='Volume (Std Counting Unit)', return_type='份额')
# r.plot_share(dimension='MOLECULE', column=None, unit='Volume (Std Counting Unit)', return_type='净增长贡献')

# r.plot_group_size_diff(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column=None, adjust_scale=0.01, series_limit=250, showLabel=True)
# r.plot_group_size_diff(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column=None, unit='Volume (Std Counting Unit)', adjust_scale=0.03, series_limit=250, showLabel=True)
# r.plot_group_share_gr(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column=None, adjust_scale=0.01, series_limit=250, ylim=[-1, 0.8])
# r.plot_group_share_gr(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column=None,unit='Volume (Std Counting Unit)', adjust_scale=0.03, series_limit=250, ylim=[-1, 0.8])

# r.plot_share(dimension="PRODUCT", column="信立明（SI6）", return_type="份额", series_limit=7)
# r.plot_share(dimension="PRODUCT", column="信立明（SI6）", return_type="净增长贡献", series_limit=7)
# r.plot_share(
#     dimension="PRODUCT",
#     column="信立明（SI6）",
#     unit="Volume (Std Counting Unit)",
#     return_type="份额",
#     series_limit=7
# )
# r.plot_share(
#     dimension="PRODUCT",
#     column="信立明（SI6）",
#     unit="Volume (Std Counting Unit)",
#     return_type="净增长贡献",
#     series_limit=7
# )

# r.plot_share_trend(
#     dimension="PRODUCT",
#     column="信立明（SI6）",
#     show_list=[
#         "立普妥（VI/）",
#         "可定（A5Z）",
#         "优力平（ZLU）",
#         "美百乐镇（DCG）",
#         "来适可XL（NVU）",
#         "阿托伐他汀（QIL）",
#         "瑞旨（S7O）",
#         "信立明（SI6）",
#     ],
# )
# r.plot_share_trend(
#     dimension="PRODUCT",
#     column="信立明（SI6）",
#     unit="Volume (Std Counting Unit)",
#     show_list=[
#         "阿托伐他汀（QIL）",
#         "优力平（ZLU）",
#         "阿托伐他汀（FJ.）",
#         "立普妥（VI/）",
#         "瑞舒伐他汀钙片（ZHI）",
#         "瑞舒伐他汀（C2T）",
#         "京诺（ZXJ）",
#         "信立明（SI6）",
#     ],
# )

# df = df[df["MOLECULE"] == "匹伐他汀"]

# r = chpa(df, name="匹伐他汀市场")

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
#     sorter=[
#         "京可新（ZXJ）",
#         "邦之（SFO）",
#         "冠爽（SHN）",
#         "匹伐他汀钙片（S1Q）",
#         "匹伐他汀（JN.）",
#         "力清之（KW.）",
#         "信立明（SI6）",
#     ],
# )
# r.plot_overall_performance(
#     dimension="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     sorter=[
#         "京可新（ZXJ）",
#         "冠爽（SHN）",
#         "邦之（SFO）",
#         "匹伐他汀钙片（S1Q）",
#         "匹伐他汀（JN.）",
#         "力清之（KW.）",
#         "信立明（SI6）",
#     ],
# )


# r.plot_group_size_diff(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column='信立明', adjust_scale=0.05, series_limit=250, showLabel=True)
# r.plot_group_size_diff(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column='信立明', unit='Volume (Std Counting Unit)', adjust_scale=0.2, series_limit=250, showLabel=True)
# r.plot_group_share_gr(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column=None, adjust_scale=0.1, series_limit=15)
# r.plot_group_share_gr(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column=None,unit='Volume (Std Counting Unit)', adjust_scale=0.5, series_limit=15)

# df = df[df["MOLECULE"] == "阿托伐他汀"]

# mask = (
#     df["PRODUCT"].isin(["优力平（ZLU）", "立普妥（VI/）", "阿乐（SDS）", "阿托伐他汀（FJ.）", "阿托伐他汀（QIL）"])
#     == False
# )
# df.loc[mask, "PRODUCT"] = "其他"

# r = chpa(df, name="阿托伐他汀市场")

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
#     sorter=["立普妥（VI/）", "阿乐（SDS）", "优力平（ZLU）", "阿托伐他汀（FJ.）", "阿托伐他汀（QIL）", "其他"],
# )

# r.plot_overall_performance(
#     dimension="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     sorter=["立普妥（VI/）", "阿乐（SDS）", "优力平（ZLU）", "阿托伐他汀（FJ.）", "阿托伐他汀（QIL）", "其他"],
# )


# r.plot_group_size_diff(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column="信立明",
#     adjust_scale=0.01,
#     series_limit=250,
#     showLabel=True,
# )
# r.plot_group_size_diff(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column="信立明",
#     unit="Volume (Std Counting Unit)",
#     adjust_scale=0.04,
#     series_limit=250,
#     showLabel=True,
# )
# r.plot_group_share_gr(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.02,
#     series_limit=15,
# )
# r.plot_group_share_gr(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     unit="Volume (Std Counting Unit)",
#     adjust_scale=0.04,
#     series_limit=15,
# )


df = df[df["MOLECULE"] == "瑞舒伐他汀"]

mask = (
    df["PRODUCT"].isin(
        ["瑞舒伐他汀（NVU）", "瑞舒伐他汀钙片（ZHI）", "瑞舒伐他汀（C2T）", "可定（A5Z）", "京诺（ZXJ）"]
    )
    == False
)

df.loc[mask, "PRODUCT"] = "其他"

r = chpa(df, name="瑞舒伐他汀市场")

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
#     sorter=["可定（A5Z）", "瑞舒伐他汀（NVU）", "瑞舒伐他汀钙片（ZHI）", "瑞舒伐他汀（C2T）", "京诺（ZXJ）", "其他"],
# )

# r.plot_overall_performance(
#     dimension="PRODUCT",
#     unit="Volume (Std Counting Unit)",
#     sorter=["可定（A5Z）", "瑞舒伐他汀（NVU）", "瑞舒伐他汀钙片（ZHI）", "瑞舒伐他汀（C2T）", "京诺（ZXJ）", "其他"],
# )

# r.plot_group_size_diff(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column="信立明",
#     adjust_scale=0.03,
#     series_limit=250,
#     showLabel=True,
# )
# r.plot_group_size_diff(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column="信立明",
#     unit="Volume (Std Counting Unit)",
#     adjust_scale=0.04,
#     series_limit=250,
#     showLabel=True,
# )
# r.plot_group_share_gr(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     adjust_scale=0.02,
#     series_limit=15,
# )
# r.plot_group_share_gr(
#     index="PRODUCT_CORP",
#     date=[r.latest_date()],
#     dimension=None,
#     column=None,
#     unit="Volume (Std Counting Unit)",
#     adjust_scale=0.05,
#     series_limit=15,
# )
