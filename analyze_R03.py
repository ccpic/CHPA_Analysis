import time
import pandas as pd
from data_func import get_trend_data, generate_df
from chart_func import *
import re
import chardet

start = time.clock()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', -1)
desired_width = 320
pd.set_option('display.width', desired_width)

df = pd.read_csv('data_R03.csv', delimiter='\t', encoding='utf-8')

# #市场表现趋势bar_line混合图
# df2 = pd.read_csv('data_2017.csv', delimiter='\t', encoding='utf-8')
#
# data_abs = get_trend_data(df=df, index=None, period='MAT', return_type='ABS', unit = 'VALUE')/1000000000
# # data_abs = data_abs.iloc[[11,23,35,47],:]
# data_gr = get_trend_data(df=df, index=None, period='MAT', return_type='GR', unit = 'VALUE')
# # data_gr = data_gr.iloc[[11,23,35],:]
# data_gr2 = get_trend_data(df=df2, index=None, period='MAT', return_type='GR', unit = 'VALUE')
# # data_gr2 = data_gr2.iloc[[11,23,35],:]
# df = data_abs.merge(data_gr, left_index=True, right_index=True, how='left')
# df = df.merge(data_gr2, left_index=True, right_index=True, how='left')
# df.columns = ['R03滚动年销售额', 'R03市场同比增长率', '处方药整体市场同比增长率']
#
# title_text = 'R03 哮喘和COPD用药定义市场表现趋势（滚动年）'
#
# plot_bar_line(x=df.index, y_bar=df['R03滚动年销售额'], y_line1=df['R03市场同比增长率'], y_line2=df['处方药整体市场同比增长率'],
#               y_bar_label='R03滚动年销售额', y_line1_label='R03市场同比增长率', y_line2_label='处方药整体市场同比增长率',
#               savefile='plots/' + title_text + '.png', title=title_text)


df_class = pd.read_csv('R03_Class.csv', engine='python')
df = df.merge(df_class, on='MOLECULE')
mask = df.MOLECULE == '特布他林|SODIUM,TERBUTALINE'
df.loc[mask, 'MOLECULE'] = '特布他林|TERBUTALINE'
mask = (df.MOLECULE == '多索茶碱葡萄糖|DOXOFYLLINE')|(df.MOLECULE == '多索茶碱葡萄糖|DOXOFYLLINE,GLUCOSE')
df.loc[mask, 'MOLECULE'] = '多索茶碱|DOXOFYLLINE'
mask = (df.MOLECULE == '茶碱(II)|THEOPHYLLINE')|(df.MOLECULE == '甘氨酸茶碱|THEOPHYLLINE')
df.loc[mask, 'MOLECULE'] = '茶碱|THEOPHYLLINE'
df_form = pd.read_csv('R03_FormCN.csv', engine='python')
df = df.merge(df_form, on='FORMULATION')

# #Class气泡图
# x = get_trend_data(df=df, index='CLASS', period='MAT', return_type='SHARE').iloc[-1,:]
# y = get_trend_data(df=df, index='CLASS', period='MAT', return_type='GR').iloc[-1,:]
# xy = pd.concat([x, y], axis=1)
# xy.columns = ['MS', 'GR']
# # xy = xy[xy.Sales.between(30, 400, inclusive=True)]
# xy.sort_values(by='MS', ascending=False, inplace=True)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(xy)
# z = list(map(lambda i: i*30000, xy.MS))
# labels = xy.MS.index.tolist()
# labels = [re.split('\|', label)[0] for label in labels]
# avggr = get_trend_data(df=df, index='CLASS', period='MAT', return_type='ABS').iloc[-1,:].sum()/\
#         get_trend_data(df=df, index='CLASS', period='MAT', return_type='ABS').iloc[-13,:].sum() - 1
# title_text = 'R03 哮喘和COPD用药定义市场各品类表现'
# plot_bubble(x=xy.MS, y=xy.GR, z=z,avggr=avggr,width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#               title=title_text, xtitle='滚动年销售额份额', ytitle='同比增长率', xfmt='{:.0%}')

# # Class销售额份额趋势折线图, 增长率趋势折线图,双图
# column_order = ['吸入性糖皮质激素(ICS)',
#            '短效β2受体激动剂(SABA)',
#            '长效β2受体激动剂(LABA)',
#            '抗白三烯类药物(LTRA)',
#            '黄嘌呤类',
#            '长效抗胆碱剂(LAMA)',
#            '短效抗胆碱剂(SAMA)',
#            'LABA+ICS固定复方制剂',
#            'SAMA+SABA固定复方制剂',
#            '非类固醇类呼吸道消炎药',
#            '其他']
# df1 = get_trend_data(df=df, index='CLASS', period='MAT', return_type='SHARE')
# df1 = df1[column_order]
# df2 = get_trend_data(df=df, index='CLASS', period='MAT', return_type='GR')
# df2 = df2[column_order]
# plot_dual_line(df1=df1,df2=df2, savefile='plots/R03 哮喘和COPD用药定义市场各品类表现趋势（滚动年）.png', xlabelrotation=90,
#                title1='R03 哮喘和COPD用药定义市场\n各品类销售额份额趋势（滚动年）', ytitle1='',
#                title2='R03 哮喘和COPD用药定义市场\n各品类销售额增长率趋势（滚动年）', ytitle2='')


# #各Class表现趋势bar_line混合图
#
# column_order = ['吸入性糖皮质激素(ICS)',
#            '短效β2受体激动剂(SABA)',
#            '长效β2受体激动剂(LABA)',
#            '抗白三烯类药物(LTRA)',
#            '黄嘌呤类',
#            '长效抗胆碱剂(LAMA)',
#            '短效抗胆碱剂(SAMA)',
#            'LABA+ICS固定复方制剂',
#            'SAMA+SABA固定复方制剂',
#            '非类固醇类呼吸道消炎药',
#            '其他']
#
# for c in column_order:
#     dff = df[df.CLASS == c]
#     data_abs = get_trend_data(df=dff, index=None, period='MAT', return_type='ABS', unit = 'VALUE')
#     if (data_abs.max() > 1000000000).bool() == True:
#         unit = '(十亿元)'
#         data_abs =data_abs/1000000000
#     else:
#         unit = '(百万元)'
#         data_abs = data_abs / 1000000
#
#     # data_abs = data_abs.iloc[[11,23,35,47],:]
#     data_gr = get_trend_data(df=dff, index=None, period='MAT', return_type='GR', unit = 'VALUE')
#     # data_gr = data_gr.iloc[[11,23,35],:]
#     data_gr2 = get_trend_data(df=df, index=None, period='MAT', return_type='GR', unit = 'VALUE')
#     # data_gr2 = data_gr2.iloc[[11,23,35],:]
#     df_chart = data_abs.merge(data_gr, left_index=True, right_index=True, how='left')
#     df_chart = df_chart.merge(data_gr2, left_index=True, right_index=True, how='left')
#     df_chart.columns = [c+'滚动年销售额', c+'同比增长率', 'R03 哮喘和COPD用药定义市场同比增长率']
#
#     title_text = c+'表现趋势（滚动年）'
#
#     plot_bar_line(x=df_chart.index, y_bar=df_chart[c+'滚动年销售额'], y_line1=df_chart[c+'同比增长率'], y_line2=df_chart['R03 哮喘和COPD用药定义市场同比增长率'],
#                   y_bar_label=c+'滚动年销售额', y_line1_label=c+'同比增长率', y_line2_label='R03 哮喘和COPD用药定义市场同比增长率',
#                   savefile='plots/' + title_text + '.png', title=title_text, unit=unit)
#     print(title_text+' finished.')

# #各Class下MOLECULE气泡图
#
# column_order = ['吸入性糖皮质激素(ICS)',
#            '短效β2受体激动剂(SABA)',
#            '长效β2受体激动剂(LABA)',
#            '抗白三烯类药物(LTRA)',
#            '黄嘌呤类',
#            '长效抗胆碱剂(LAMA)',
#            '短效抗胆碱剂(SAMA)',
#            'LABA+ICS固定复方制剂',
#            'SAMA+SABA固定复方制剂',
#            '非类固醇类呼吸道消炎药',
#            '其他']
#
# for c in column_order:
#     dff = df[df.CLASS == c]
#     x = get_trend_data(df=dff, index='MOLECULE', period='MAT', return_type='SHARE').iloc[-1,:]
#     y = get_trend_data(df=dff, index='MOLECULE', period='MAT', return_type='GR').iloc[-1,:]
#     xy = pd.concat([x, y], axis=1)
#     xy.columns = ['MS', 'GR']
#     # xy = xy[xy.Sales.between(30, 400, inclusive=True)]
#     xy.sort_values(by='MS', ascending=False, inplace=True)
#     xy.dropna(how='any', inplace=True)
#     with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#         print(xy)
#     z = list(map(lambda i: i*30000, xy.MS))
#     labels = xy.MS.index.tolist()
#     labels = [re.split('\|', label)[0] for label in labels]
#     avggr = get_trend_data(df=dff, index='MOLECULE', period='MAT', return_type='ABS').iloc[-1,:].sum()/\
#             get_trend_data(df=dff, index='MOLECULE', period='MAT', return_type='ABS').iloc[-13,:].sum() - 1
#     title_text = c+'各通用名表现'
#     plot_bubble(x=xy.MS, y=xy.GR, z=z,avggr=avggr,width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#                   title=title_text, xtitle='滚动年销售额份额', ytitle='同比增长率', xfmt='{:.0%}')

# # 各Class下通用名销售额份额趋势折线图, 增长率趋势折线图,双图
# df['MOLECULE'] = df['MOLECULE'].str.split('\|', 1).str[0]
#
# column_order = ['吸入性糖皮质激素(ICS)',
#            '短效β2受体激动剂(SABA)',
#            '长效β2受体激动剂(LABA)',
#            '抗白三烯类药物(LTRA)',
#            '黄嘌呤类',
#            '长效抗胆碱剂(LAMA)',
#            '短效抗胆碱剂(SAMA)',
#            'LABA+ICS固定复方制剂',
#            'SAMA+SABA固定复方制剂',
#            '非类固醇类呼吸道消炎药',
#            '其他']
#
# for c in column_order:
#     dff = df[df.CLASS == c]
#     df1 = get_trend_data(df=dff, index='MOLECULE', period='MAT', return_type='SHARE')
#     df1 = df1.T.sort_values('2018-02-01 ', ascending=False).T
#     df2 = get_trend_data(df=dff, index='MOLECULE', period='MAT', return_type='GR')
#     df2 = df2[df1.columns]
#     title_text = c+'各通用名表现趋势'
#     plot_dual_line(df1=df1,df2=df2, savefile='plots/'+title_text+'.png', xlabelrotation=90,
#                    title1=c+'\n各通用名销售额份额趋势（滚动年）', ytitle1='',
#                    title2=c+'\n各通用名销售额增长率趋势（滚动年）', ytitle2='')
#     print(title_text + ' finished.')

# #各Class下PRODUCT气泡图
# df['PRODUCT'] = df['PRODUCT'].str.split('\|', 1).str[0] + '\n'+ df['MOLECULE'].str.split('\|', 1).str[0] + '\n' + df['CORPORATION'].str.split('\|', 1).str[0]
#
# column_order = ['吸入性糖皮质激素(ICS)',
#            '短效β2受体激动剂(SABA)',
#            '长效β2受体激动剂(LABA)',
#            '抗白三烯类药物(LTRA)',
#            '黄嘌呤类',
#            '长效抗胆碱剂(LAMA)',
#            '短效抗胆碱剂(SAMA)',
#            'LABA+ICS固定复方制剂',
#            'SAMA+SABA固定复方制剂',
#            '非类固醇类呼吸道消炎药',
#            '其他']
#
# for c in column_order:
#     dff = df[df.CLASS == c]
#     x = get_trend_data(df=dff, index='PRODUCT', period='MAT', return_type='ABS').iloc[-1,:]/1000000
#     y = get_trend_data(df=dff, index='PRODUCT', period='MAT', return_type='GR').iloc[-1,:]
#     xy = pd.concat([x, y], axis=1)
#     xy.columns = ['MS', 'GR']
#     # xy = xy[xy.Sales.between(30, 400, inclusive=True)]
#     xy.sort_values(by='MS', ascending=False, inplace=True)
#     xy.dropna(how='any', inplace=True)
#     xy = xy.head(10)
#     with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#         print(xy)
#     z = list(map(lambda i: i*10, xy.MS))
#     labels = xy.MS.index.tolist()
#     # labels = [re.split('\|', label)[0] for label in labels]
#     avggr = get_trend_data(df=dff, index='PRODUCT', period='MAT', return_type='ABS').iloc[-1,:].sum()/\
#             get_trend_data(df=dff, index='PRODUCT', period='MAT', return_type='ABS').iloc[-13,:].sum() - 1
#     title_text = c+'Top10产品表现'
#     plot_bubble(x=xy.MS, y=xy.GR, z=z,avggr=avggr,width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#                   title=title_text, xtitle='滚动年销售额（百万）', ytitle='同比增长率', xfmt='{:,.0f}', fontsize=12)

# # 各Class下PRODUCT销售额份额趋势折线图, 增长率趋势折线图,双图
# df['PRODUCT'] = df['PRODUCT'].str.split('\|', 1).str[0] + '|'+ df['MOLECULE'].str.split('\|', 1).str[0] + '\n' + df['CORPORATION'].str.split('\|', 1).str[0]
#
# column_order = ['吸入性糖皮质激素(ICS)',
#            '短效β2受体激动剂(SABA)',
#            '长效β2受体激动剂(LABA)',
#            '抗白三烯类药物(LTRA)',
#            '黄嘌呤类',
#            '长效抗胆碱剂(LAMA)',
#            '短效抗胆碱剂(SAMA)',
#            'LABA+ICS固定复方制剂',
#            'SAMA+SABA固定复方制剂',
#            '非类固醇类呼吸道消炎药',
#            '其他']
#
# for c in column_order:
#     dff = df[df.CLASS == c]
#     df1 = get_trend_data(df=dff, index='PRODUCT', period='MAT', return_type='SHARE')
#     df1 = df1.T.sort_values('2018-02-01 ', ascending=False).head(10).T
#     df2 = get_trend_data(df=dff, index='PRODUCT', period='MAT', return_type='GR')
#     df2 = df2[df1.columns]
#     title_text = c+'Top10产品表现趋势'
#     plot_dual_line(df1=df1,df2=df2, savefile='plots/'+title_text+'.png', xlabelrotation=90,
#                    title1=c+'\nTop10产品销售额份额趋势（滚动年）', ytitle1='',
#                    title2=c+'\nTop10产品销售额增长率趋势（滚动年）', ytitle2='')
#     print(title_text + ' finished.')

##各Class下PRODUCT剂型比例

# df['PRODUCT'] = df['PRODUCT'].str.split('\|', 1).str[0] + '|'+ df['MOLECULE'].str.split('\|', 1).str[0] + '\n' + df['CORPORATION'].str.split('\|', 1).str[0]
# column_order = ['吸入性糖皮质激素(ICS)',
#            '短效β2受体激动剂(SABA)',
#            '长效β2受体激动剂(LABA)',
#            '抗白三烯类药物(LTRA)',
#            '黄嘌呤类',
#            '长效抗胆碱剂(LAMA)',
#            '短效抗胆碱剂(SAMA)',
#            'LABA+ICS固定复方制剂',
#            'SAMA+SABA固定复方制剂',
#            '非类固醇类呼吸道消炎药',
#            '其他']
#
# mask = (df['DATE'] > '2017-2-1') & (df['DATE'] <= '2018-2-1')
# df = df.loc[mask,:]
# for c in column_order:
#     dff = df[df.CLASS == c]
#     df1 = get_trend_data(df=dff, index='PRODUCT', period='MAT', return_type='SHARE')
#     df1 = df1.T.sort_values('2018-02-01 ', ascending=False).head(10).T
#     table = pd.pivot_table(dff, index='FORM_CN', columns='PRODUCT', values ='VALUE', aggfunc=np.sum).transform(lambda x: x/x.sum())
#     df2 = table.loc[:,df1.columns].T
#     title_text = c+'Top产品剂型分布'
#     plot_bar(df2,'plots/'+title_text+'.png',width=14, height=7, title=title_text, ytitle='剂型占比', xtitle='')
#     print(c)