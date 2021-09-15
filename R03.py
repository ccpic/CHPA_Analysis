from CHPA import *
import pandas as pd

engine = create_engine('mssql+pymssql://(local)/CHPA_1806')
sql = "SELECT * FROM data_city_R03"
df = pd.read_sql(sql=sql, con=engine)

d_class = {
            '布地奈德|BUDESONIDE': '吸入性糖皮质激素(ICS)',
            '多索茶碱|DOXOFYLLINE': '黄嘌呤类',
            '吡嘧司特|PEMIROLAST': '非类固醇类呼吸道消炎药',
            '二羟丙茶碱|DIPROPHYLLINE': '黄嘌呤类',
            '特布他林|TERBUTALINE': '短效β2受体激动剂(SABA)',
            '丙酸倍氯米松|BECLOMETASONE': '吸入性糖皮质激素(ICS)',
            '倍氯米松,福莫特罗|BECLOMETASONE+FORMOTEROL': 'LABA+ICS固定复方制剂',
            '布地奈德,福莫特罗|BUDESONIDE+FORMOTEROL': 'LABA+ICS固定复方制剂',
            '福莫特罗|FORMOTEROL': '长效β2受体激动剂(LABA)',
            '噻托溴铵|TIOTROPIUM BROMIDE': '长效抗胆碱剂(LAMA)',
            '异丙托溴铵|IPRATROPIUM BROMIDE': '短效抗胆碱剂(SAMA)',
            '异丙托溴铵,沙丁胺醇|IPRATROPIUM BROMIDE+SALBUTAMOL': 'SAMA+SABA固定复方制剂',
            '孟鲁司特|MONTELUKAST': '抗白三烯类药物(LTRA)',
            '普仑司特|PRANLUKAST': '抗白三烯类药物(LTRA)',
            '沙美特罗替卡松|FLUTICASONE+SALMETEROL': 'LABA+ICS固定复方制剂',
            '沙丁胺醇|SALBUTAMOL': '短效β2受体激动剂(SABA)',
            '丙酸氟替卡松|FLUTICASONE': '吸入性糖皮质激素(ICS)',
            '茚达特罗|INDACATEROL': '长效β2受体激动剂(LABA)',
            '奥马珠单抗|OMALIZUMAB': 'lgE单抗',
            '多索茶碱葡萄糖|DOXOFYLLINE': '黄嘌呤类',
            '氨茶碱|AMINOPHYLLINE': '黄嘌呤类',
            '丙卡特罗|PROCATEROL': '长效β2受体激动剂(LABA)',
            '茶碱|THEOPHYLLINE': '黄嘌呤类',
            '酮替芬|KETOTIFEN': '非类固醇类呼吸道消炎药',
            '塞曲司特|SERATRODAST': '非类固醇类呼吸道消炎药',
            '多索茶碱葡萄糖|DOXOFYLLINE+GLUCOSE': '黄嘌呤类',
            '妥洛特罗|TULOBUTEROL': '长效β2受体激动剂(LABA)',
            '曲尼司特|TRANILAST': '非类固醇类呼吸道消炎药',
            '细辛脑|ALPHA ASARONE': '其他',
            '甲磺司特|SUPLATAST TOSILATE': '非类固醇类呼吸道消炎药',
            '复方氨茶碱|ATROPA BELLADONNA+CAFFEINE+EPHEDRINE+PHENACETIN+PHENAZONE+PHENOBARBITAL+THEOBROMINE+THEOPHY': '黄嘌呤类',
            '复方芜地溴铵/维兰特罗吸入剂|UMECLIDINIUM BROMIDE+VILANTEROL': 'LAMA+LABA固定复方制剂',
            '特布他林|SODIUM+TERBUTALINE': '短效β2受体激动剂(SABA)',
            '班布特罗|BAMBUTEROL': '长效β2受体激动剂(LABA)',
            '茶碱,麻黄碱|AMOBARBITAL+EPHEDRINE+THEOPHYLLINE': '黄嘌呤类',
            '甘氨酸茶碱|THEOPHYLLINE': '黄嘌呤类',
            '环索奈德|CICLESONIDE': '吸入性糖皮质激素(ICS)',
            '环仑特罗|CLENBUTEROL': '长效β2受体激动剂(LABA)',
            '复方胆氨|AMINOPHYLLINE+EPHEDRINE+SODIUM': '黄嘌呤类',
            '复方妥英麻黄茶碱|ATROPA BELLADONNA+CAFFEINE+CHLORPHENAMINE+EPHEDRINE+PHENYTOIN+THEOBROMINE+THEOPHYLLINE': '黄嘌呤类',
            '二羟丙茶碱氯化钠|DIPROPHYLLINE': '黄嘌呤类',
            '茶碱葡萄糖注射液|GLUCOSE+THEOPHYLLINE': '黄嘌呤类',
            '噻托溴铵/奥达特罗|OLODATEROL+TIOTROPIUM BROMIDE': '黄嘌呤类',
            '曲尼司特,沙丁胺醇|SALBUTAMOL+TRANILAST': '其他',
            '异丙肾上腺素|ISOPRENALINE': '短效β2受体激动剂(SABA)',
            '茶碱,盐酸甲麻黄碱,暴马子浸膏|AMOBARBITAL+CHLORPHENAMINE+METHYLEPHEDRINE+SYRINGA VULGARIS+THEOPHYLLINE': '黄嘌呤类',
            '复方茶碱麻黄碱|ATROPA BELLADONNA+CAFFEINE+EPHEDRINE+THEOBROMINE+THEOPHYLLINE': '黄嘌呤类',
            '复方妥英麻黄茶碱|ANISODAMINE+CAFFEINE+CHLORPHENAMINE+EPHEDRINE+HYOSCYAMINE+PHENYTOIN+THEOPHYLLINE': '黄嘌呤类',
            }

# for col in ['TC III', 'PRODUCT']:
#     df[col] = df[col].map(d_rename).fillna('其他')

df['REGION1'] = df['CITY'].map(d_region1)
df['REGION2'] = df['CITY'].map(d_region2)
df['TIER'] = df['CITY'].map(d_tier)
df['CLASS'] = df['MOLECULE'].map(d_class)
df['MOLECULE'] = df['MOLECULE'].str.split('|').str[0]
df['PRODUCT'] = df['PRODUCT'].str.split('|').str[0]

market1 = '哮喘和COPD药物市场'
market2 = '吸入性糖皮质激素(ICS)'

#哮喘和COPD药物市场分城市销售和及增长率
r=chpa(df, name=market1)
r.plot_group_size_gr(index='CITY', date=[r.latest_date()], dimension='CLASS', column=market2, comparison_method='EI')


#分城市各维度份额比较
# r =chpa(df, name=market1)
# r.plot_group_share(index='CITY', date=[r.latest_date()], dimension='CLASS', column=market2, method='share', threshold=False)
# df['MOLECULE'] = df['MOLECULE'].str.split('|').str[0]
# r.plot_group_share(index='CITY', date=[r.latest_date()], dimension='MOLECULE', column=None,
#                    method='share', threshold=False, sort_method='Value')
# r.plot_group_share(index='CITY', date=[r.latest_date()], dimension='PRODUCT', column='信立坦',
#                    method='share', threshold=False, sort_method='List', sorter=['信立坦', '代文', '安博维', '科素亚', '美卡素', '傲坦', '必洛斯', '雅施达', '洛汀新', '其他'])

# #吸入性糖皮质激素(ICS)市场分城市销售和及增长率
# mask = df['CLASS'] == market2
# r =chpa(df.loc[mask], name=market2)
# r.plot_group_size_gr(index='CITY', date=[r.latest_date()], dimension=None, column=None, comparison_method='EI')

# # 布地奈德分城市销售额及增长率
# r =chpa(df, name=market1)
# r.plot_group_size_gr(index='CITY', date=[r.latest_date()], dimension='PRODUCT', column='普米克令舒',comparison_method='EI')

# #信立坦分城市潜力 versus 份额气泡图
# r =chpa(df, name='RAAS平片市场')
# r.plot_group_size_share(index='CITY', date=[r.latest_date()],  dimension='PRODUCT', column='信立坦', ylim=[0, 0.11])
# for brand in ['代文', '科素亚', '安博维', '必洛斯']:
#     r.plot_group_size_share(index='CITY', date=[r.latest_date()],  dimension='PRODUCT', column=brand, adjust_scale=0.2)

# #分城市层级及东南西北大区主要产品份额
# r = chpa(df, name=market2)
# r.plot_grid_share_trend(grid_index='TIER', dimension='PRODUCT', column=None,
#                         sort_method='List', sorter=['一线', '二线', '三线'])

# #分大区主要产品份额趋势
# index_list = df['REGION2'].unique()
# print(index_list)
# for region in index_list:
#     mask = (df['REGION2'] == region)
#     r = chpa(df.loc[mask], name='RAAS平片市场')
#     r.plot_grid_share_trend(grid_index='CITY', dimension='PRODUCT', column='信立坦', ignore_list=['美卡素', '必洛斯', '洛汀新'])
#
# r =chpa(df, name=market1)
# r.plot_map('PRODUCT', '舒利迭')

# #分城市数据表
# r =chpa(df, name='哮喘和COPD市场')
# # print(r.agg_table(index='CITY', dimension='PRODUCT', column=None))



# engine = create_engine('mssql+pymssql://(local)/CHPA_1806')
# sql = "SELECT * FROM data_RAAS_Plain"
# df = pd.read_sql(sql=sql, con=engine)
#
# for col in ['TC III', 'PRODUCT']:
#     df[col] = df[col].map(d_rename).fillna('其他')
#
# r = chpa(df, name='RAAS平片市场')
# # r.plot_annual_performance(dimension='TC III')
# # r.plot_annual_performance(dimension='PRODUCT', sorter= ['信立坦', '代文', '安博维', '科素亚', '美卡素', '傲坦', '必洛斯', '雅施达', '洛汀新', '其他'])
# r.plot_share('PRODUCT', '信立坦', '份额')
# r.plot_share('PRODUCT', '信立坦', '净增长贡献')