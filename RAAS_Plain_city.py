from CHPA import *

engine = create_engine('mssql+pymssql://(local)/CHPA_1806')
sql = "SELECT * FROM data_city_RAAS_Plain"
df = pd.read_sql(sql=sql, con=engine)

for col in ['TC III', 'PRODUCT']:
    df[col] = df[col].map(d_rename).fillna('其他')

df['REGION1'] = df['CITY'].map(d_region1)
df['REGION2'] = df['CITY'].map(d_region2)
df['TIER'] = df['CITY'].map(d_tier)

df['MOLECULE'] = df['MOLECULE'].str.split('|').str[0]
df['PRODUCT'] = df['PRODUCT'].str.split('|').str[0]
#
# #4+7带量采购城市采购品种份额
# df = df[df['CITY'].isin(['北京','天津','上海','重庆','沈阳','大连','褔厦泉','广州','深圳','成都','西安'])]
# r =chpa(df, name='RAAS平片市场')
# r.plot_group_share(index='CITY', date=[r.latest_date()], dimension='MOLECULE', column=None, method='share', threshold=False, sort_method='Value')


#r =chpa(df, name='RAAS平片市场')
# #RAAS平片市场分城市销售和及增长率
# r =chpa(df, name='RAAS平片市场')
# r.plot_group_size_gr(index='CITY', date=[r.latest_date()], dimension=None, column=None, comparison_method='增长率')
# r.plot_group_size_gr(index='TIER', date=[r.latest_date()], dimension=None, column=None, comparison_method='增长率')


#分城市各维度份额比较
df = df[df['CITY'].isin(['哈尔滨', '长春', '沈阳', '大连', '石家庄', '郑州', '呼和浩特', '南昌', '南宁', '兰州', '乌鲁木齐'])]
r =chpa(df, name='RAAS平片市场')
# r.plot_group_share(index='CITY', date=[r.latest_date()], dimension='TC III', column='ARB', method='share', threshold=True)
# r.plot_group_share(index='CITY', date=[r.latest_date()], dimension='MOLECULE', column=None,
#                    method='share', threshold=False, sort_method='Value')
r.plot_group_share(index='CITY', date=[r.latest_date()], dimension='PRODUCT', column='信立坦',
                   method='share', threshold=False, sort_method='List', sorter=['信立坦', '代文', '安博维', '科素亚', '美卡素', '傲坦', '必洛斯', '雅施达', '洛汀新', '其他'])

# #ARB平片市场分城市销售和及增长率
# mask = df['TC III'] == 'ARB'
# r =chpa(df.loc[mask], name='ARB平片市场')
# r.plot_group_size_gr(index='CITY', date=[r.latest_date()], dimension=None, column=None, comparison_method='增长率')

# # 信立坦分城市销售额及增长率
# r =chpa(df, name='RAAS平片市场')
# r.plot_group_size_gr(index='CITY', date=[r.latest_date()], dimension='PRODUCT', column='信立坦',comparison_method='EI', y2lim=[0, 2000])
#
#信立坦分城市潜力 versus 份额气泡图
# r =chpa(df, name='RAAS平片市场')
# r.plot_group_size_share(index='CITY', date=[r.latest_date()],  dimension='PRODUCT', column='信立坦', ylim=[0, 0.11])
# for brand in ['信立坦', '代文', '科素亚', '傲坦', '安博维', '缓宁', '吉加', '依苏', '倍怡', '平欣']:
#     r.plot_group_size_share(index='CITY', date=[r.latest_date()],  dimension='PRODUCT', column=brand, adjust_scale=0.2, labelLimit=99)

#分城市层级及东南西北大区主要产品份额
# r = chpa(df, name='RAAS平片市场')
# r.plot_grid_share_trend(grid_index='TIER', dimension='PRODUCT', column='信立坦',
#                         sort_method='List', sorter=['一线', '二线', '三线'], ignore_list=['其他','兰沙', '迪之雅', '平欣', '依苏', '吉加'])


#分城市层级及东南西北大区主要产品份额
# r = chpa(df, name='RAAS平片市场')
# r.plot_grid_share_trend(grid_index='REGION1', dimension='PRODUCT', column='信立坦',
#                         sort_method='List', sorter=['北区', '东区', '中区', '南区'], ignore_list=['其他'])


# #分大区主要产品份额趋势
# index_list = df['CITY'].unique()
# print(index_list)
# for city in index_list:
#     mask = (df['CITY'] == city)
#     r = chpa(df.loc[mask], name='RAAS平片市场')
#     df_city = r.matrix_by_timeseries(None, None, 'PRODUCT', '份额')
#     df_city.sort_values(by='2018-12-1', axis=1, ascending=False, inplace=True)
#
#     df1 = df_city.loc[:, df_city.columns[df_city.iloc[-1] >= 0.05]]
#     df2 = df_city.loc[:, df_city.columns[df_city.iloc[-1].between(0.02, 0.05)]]
#     xlt = df_city.loc['2018-12-01', '信立坦']
#     if xlt < 0.02:
#         df2 =pd.concat([df2, df_city.loc[:,'信立坦']], axis=1)
#     print(df1, df2)
#     r.plot_line_twin(df1, df2, '信立坦', city+'RAAS市场竞争品牌表现', '市场份额领先品牌(MS>=5%)', '市场份额追赶品牌(MS>=2%)', '滚动年销售额份额',
#                      ylim1 = [0,df1.max().max()], ylim2 = [0, df2.max().max()])

#
# r =chpa(df, name='RAAS平片市场')
# df1 = r.matrix_by_timeseries(None, None,'PRODUCT', '绝对值')
# df1.sort_values(by='2018-12-01', ascending=False, axis=1, inplace=True)
# df1 = df1.iloc[-1,:]
# #
# #
# engine = create_engine('mssql+pymssql://(local)/CHPA_1806')
# sql = "SELECT * FROM data_RAAS_Plain"
# df_chpa = pd.read_sql(sql=sql, con=engine)
#
# for col in ['TC III', 'PRODUCT']:
#     df_chpa[col] = df_chpa[col].map(d_rename).fillna('其他')
# df_chpa['PRODUCT'] = df_chpa['PRODUCT'].str.split('|').str[0]
# r =chpa(df_chpa, name='RAAS平片市场')
# # df2 = r.matrix_by_timeseries(None, None,'PRODUCT', '绝对值')
# # df2.sort_values(by='2018-12-01', ascending=False, axis=1, inplace=True)
# # df2 = df2.iloc[-1,:]
# # df3 = pd.concat([df1,df2, df1/df2], axis=1)
# # df3.columns = ['34+2城市','CHPA','占比']
# # df3.sort_values(by='CHPA', ascending=False, inplace=True)
# # print(df3)
# #
#
# #
# r = chpa(df, name='RAAS平片市场')
# r.plot_annual_performance(dimension='TC III', unit='Volume')
# # # r.plot_annual_performance(dimension='PRODUCT', sorter= ['信立坦', '代文', '安博维', '科素亚', '美卡素', '傲坦', '必洛斯', '雅施达', '洛汀新', '其他'])
# r.plot_share('PRODUCT', '信立坦', '份额')
# r.plot_share('PRODUCT', '信立坦', '净增长贡献')