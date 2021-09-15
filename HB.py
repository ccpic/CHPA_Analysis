from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"
# condition = '1=1'
condition = "[TC III] = 'B01B HEPARINS|肝素' OR MOLECULE = '比伐芦定|BIVALIRUDIN'"
sql = "SELECT * FROM " + table_name + " WHERE " + condition
df = pd.read_sql(sql=sql, con=engine)

mask = df["MOLECULE"] != "比伐芦定|BIVALIRUDIN"
df.loc[mask, "MOLECULE"] = "肝素|HEPARIN"

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[0]
df["PRODUCT"] = df["PRODUCT"].str.split("|").str[0] + "（" + df["PRODUCT"].str.split("|").str[1].str[-3:] + "）"
df["PRODUCT_CORP"] = (
    df["PRODUCT_CORP"].str.split("（").str[0].str.split("|").str[0]
    + "\n"
    + df["PRODUCT_CORP"].str.split("（").str[1].str.split("|").str[0]
)


r = chpa(df, name="肝素和比伐芦定市场")

r.plot_overall_performance(dimension='MOLECULE')

# r.plot_group_size_diff(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column='泰加宁\n深圳信立泰药业股份有限公司', adjust_scale=0.01, series_limit=250, showLabel=True, unit='Value')
# r.plot_group_share_gr(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column='泰加宁\n深圳信立泰药业股份有限公司', adjust_scale=0.01, series_limit=250,
#                       ylim=[-0.5, 1])

# r.plot_share(dimension='PRODUCT', column='泰加宁（SI6）', return_type='份额')
# r.plot_share(dimension='PRODUCT', column='泰加宁（SI6）', return_type='净增长贡献')
# r.plot_share_gr_trend(dimension='PRODUCT', column='泰加宁（SI6）')

# r.plot_share_trend(
#     dimension="PRODUCT",
#     column="泰加宁（SI6）",
#     show_list=["万脉舒（H2C）", "克赛（AVS）", "注射用那屈肝素钙（DG+）", "速避凝（A3N）", "希弗全（A1L）", "立迈青（AHK）", "那屈肝素钙注射液（JJY）", "泰加宁（SI6）"],
# )

# df = df[df['MOLECULE'] == '比伐芦定']
# r = chpa(df, name="比伐芦定市场")

# r.plot_overall_performance(dimension='PRODUCT_CORP')

# r.plot_group_size_diff(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column='泰加宁\n深圳信立泰药业股份有限公司', adjust_scale=0.02, series_limit=250, showLabel=True, unit='Value')
# r.plot_group_share_gr(index='PRODUCT_CORP', date=[r.latest_date()], dimension=None,
#                       column='泰加宁\n深圳信立泰药业股份有限公司', adjust_scale=0.04, series_limit=15)

# r.plot_share(dimension='PRODUCT_CORP', column='泰加宁\n深圳信立泰药业股份有限公司', return_type='份额')
# r.plot_share(dimension='PRODUCT_CORP', column='泰加宁\n深圳信立泰药业股份有限公司', return_type='净增长贡献')
# r.plot_share_gr_trend(dimension='PRODUCT', column='泰加宁')

# r.plot_share_trend(dimension='PRODUCT_CORP', column='泰加宁\n深圳信立泰药业股份有限公司')

# r = chpa(df, name="全国大医院渠道市场")
# r.plot_overall_performance(dimension=None, cycle="Quarterly", period="QTR")
