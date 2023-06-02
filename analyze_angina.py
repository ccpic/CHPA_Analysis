import time
import pandas as pd
from data_func import get_trend_data, generate_df
from chart_func import *
import re

start = time.clock()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', -1)
desired_width = 320
pd.set_option('display.width', desired_width)

df = pd.read_csv('data_angina.csv', delimiter='\t', encoding='utf-8')

mask = df.TC_II == 'C07 β受体阻断剂|BETA BLOCKING AGENTS'
df.loc[mask,['VALUE', 'CNT_UNIT', 'UNIT']] = df.loc[mask,['VALUE', 'CNT_UNIT', 'UNIT']] * 0.25 #添加BB系数0.25
df.loc[mask,'CLASS'] =  'β受体阻断剂'
mask = (df.TC_II == 'C08 钙离子拮抗剂|CALCIUM ANTAGONISTS')&(df.MOLECULE != '地尔硫卓|DILTIAZEM')&(df.MOLECULE != '维拉帕米|VERAPAMIL')
df.loc[mask,['VALUE', 'CNT_UNIT', 'UNIT']] = df.loc[mask,['VALUE', 'CNT_UNIT', 'UNIT']] * 0.2 #添加二氢吡啶类CCB系数0.25, 保持非二氢吡啶类CCB系数为1
df.loc[mask,'CLASS'] =  '二氢吡啶类CCB'
mask = (df.MOLECULE == '地尔硫卓|DILTIAZEM')|(df.MOLECULE == '维拉帕米|VERAPAMIL')
df.loc[mask,'CLASS'] =  '非二氢吡啶类CCB'
mask = (df.TC_III == 'C01E 亚硝酸盐和硝酸盐|NITRITES & NITRATES')
df.loc[mask,'CLASS'] =  '硝酸甘油和长效硝酸酯'
mask = (df.MOLECULE == '曲美他嗪|TRIMETAZIDINE')
df.loc[mask,'CLASS'] =  '代谢治疗（曲美他嗪）'
mask = (df.MOLECULE == '尼可地尔|NICORANDIL')
df.loc[mask,'CLASS'] =  '钾离子通道开放剂（尼可地尔）'

mask = (df.MOLECULE != '伊伐布雷定|IVABRADINE')&(df.MOLECULE != '薯蓣皂苷|DIOSCOREA BULBIFERA')&\
       (df.MOLECULE != '薯蓣皂苷|SAPONINE')&(df.MOLECULE != '吗多明|MOLSIDOMINE')&\
       (df.MOLECULE != '曲匹地尔|TRAPIDIL')&(df.MOLECULE != '双嘧达莫|DIPYRIDAMOLE')
df = df.loc[mask,:]#去除通用名伊伐布雷定等其他

mask = df.FORMULATION.str.contains('ORAL')
df.loc[mask, 'FORM_CN'] = '口服'
mask = df.FORMULATION.str.contains('PARENTERAL')
df.loc[mask, 'FORM_CN'] = '注射'

mask = (df.MANUF_TYPE == 'I')|(df.MANUF_TYPE == 'J')
df.loc[mask, 'MANUF_TYPE'] = '原研'
mask = (df.MANUF_TYPE == 'L')
df.loc[mask, 'MANUF_TYPE'] = '仿制'

column_order = ['二氢吡啶类CCB',
           '硝酸甘油和长效硝酸酯',
           '代谢治疗（曲美他嗪）',
            'β受体阻断剂',
           '非二氢吡啶类CCB',
           '钾离子通道开放剂（尼可地尔）']

# #市场表现趋势bar_line混合图
# df2 = pd.read_csv('data_2017.csv', delimiter='\t', encoding='utf-8')
#
# data_abs = get_trend_data(df=df, index=None, period='MAT', return_type='ABS', unit = 'VALUE')/100000000
# # data_abs = data_abs.iloc[[11,23,35,47],:]
# data_gr = get_trend_data(df=df, index=None, period='MAT', return_type='GR', unit = 'VALUE')
# # data_gr = data_gr.iloc[[11,23,35],:]
# data_gr2 = get_trend_data(df=df2, index=None, period='MAT', return_type='GR', unit = 'VALUE')
# # data_gr2 = data_gr2.iloc[[11,23,35],:]
# df = data_abs.merge(data_gr, left_index=True, right_index=True, how='left')
# df = df.merge(data_gr2, left_index=True, right_index=True, how='left')
# df.columns = ['抗心绞痛（症状）定义市场滚动年销售额', '抗心绞痛（症状）定义市场同比增长率', '处方药整体市场同比增长率']
#
# title_text = '抗心绞痛（症状）定义市场表现趋势（滚动年）'
#
# plot_bar_line(x=df.index, y_bar=df['抗心绞痛（症状）定义市场滚动年销售额'], y_line1=df['抗心绞痛（症状）定义市场同比增长率'], y_line2=df['处方药整体市场同比增长率'],
#               y_bar_label='抗心绞痛（症状）定义市场滚动年销售额', y_line1_label='抗心绞痛（症状）定义市场同比增长率', y_line2_label='处方药整体市场同比增长率',
#               savefile='plots/angina/' + title_text + '.png', title=title_text)

# #Class气泡图
# x = get_trend_data(df=df, index='CLASS', period='MAT', return_type='ABS').iloc[-1,:]/100000000
# y = get_trend_data(df=df, index='CLASS', period='MAT', return_type='GR').iloc[-1,:]
# xy = pd.concat([x, y], axis=1)
# xy.columns = ['MS', 'GR']
# # xy = xy[xy.Sales.between(30, 400, inclusive=True)]
# xy.sort_values(by='MS', ascending=False, inplace=True)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(xy)
# z = list(map(lambda i: i*1000, xy.MS))
# labels = xy.MS.index.tolist()
# labels = [re.split('\|', label)[0] for label in labels]
# avggr = get_trend_data(df=df, index='CLASS', period='MAT', return_type='ABS').iloc[-1,:].sum()/\
#         get_trend_data(df=df, index='CLASS', period='MAT', return_type='ABS').iloc[-13,:].sum() - 1
# title_text = '抗心绞痛（症状）定义市场各品类表现'
# plot_bubble(x=xy.MS, y=xy.GR, z=z,avggr=avggr,width=15,height=9, labels=labels, savefile='plots/angina/'+title_text+'.png',
#               title=title_text, xtitle='滚动年销售额（亿元）', ytitle='同比增长率', xfmt='{:,.1f}')
#
#
# # Class销售额份额趋势折线图, 增长率趋势折线图,双图
# column_order = ['二氢吡啶类CCB',
#            '硝酸甘油和长效硝酸酯',
#            '代谢治疗（曲美他嗪）',
#             'β受体阻断剂',
#            '非二氢吡啶类CCB',
#            '钾离子通道开放剂（尼可地尔）']
# df1 = get_trend_data(df=df, index='CLASS', period='MAT', return_type='SHARE')
# df1 = df1[column_order]
# df2 = get_trend_data(df=df, index='CLASS', period='MAT', return_type='GR')
# df2 = df2[column_order]
# plot_dual_line(df1=df1,df2=df2, savefile='plots/Angina/抗心绞痛（症状）定义市场各品类表现趋势（滚动年）.png', xlabelrotation=90,
#                title1='抗心绞痛（症状）定义市场\n各品类销售额份额趋势（滚动年）', ytitle1='',
#                title2='抗心绞痛（症状）定义市场\n各品类销售额增长率趋势（滚动年）', ytitle2='')
#
#
# #各Class表现趋势bar_line混合图
#
#
# for c in column_order:
#     dff = df[df.CLASS == c]
#     data_abs = get_trend_data(df=dff, index=None, period='MAT', return_type='ABS', unit = 'VALUE')
#     if (data_abs.max() > 100000000).bool() == True:
#         unit = '(亿元)'
#         data_abs =data_abs/100000000
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
#     df_chart.columns = [c+'滚动年销售额', c+'同比增长率', '抗心绞痛（症状）定义市场同比增长率']
#
#     title_text = c+'表现趋势（滚动年）'
#
#     plot_bar_line(x=df_chart.index, y_bar=df_chart[c+'滚动年销售额'], y_line1=df_chart[c+'同比增长率'], y_line2=df_chart['抗心绞痛（症状）定义市场同比增长率'],
#                   y_bar_label=c+'滚动年销售额', y_line1_label=c+'同比增长率', y_line2_label='抗心绞痛（症状）定义市场同比增长率',
#                   savefile='plots/Angina/' + title_text + '.png', title=title_text, unit=unit)
#     print(title_text+' finished.')


#

# # 各Class下PRODUCT销售额份额趋势折线图, 增长率趋势折线图,双图
# df['PRODUCT'] = df['PRODUCT'].str.split('\|', 1).str[0] + '|'+ df['MOLECULE'].str.split('\|', 1).str[0] + '\n' + df['CORPORATION'].str.split('\|', 1).str[0]
#
# for c in column_order:
#     dff = df[df.CLASS == c]
#     df1 = get_trend_data(df=dff, index='PRODUCT', period='MAT', return_type='SHARE')
#     df1 = df1.T.sort_values('2018-02-01 ', ascending=False).head(10).T
#     df2 = get_trend_data(df=dff, index='PRODUCT', period='MAT', return_type='GR')
#     df2 = df2[df1.columns]
#     title_text = c+'Top10产品表现趋势'
#     plot_dual_line(df1=df1,df2=df2, savefile='plots/Angina/'+title_text+'.png', xlabelrotation=90,
#                    title1=c+'\nTop10产品销售额份额趋势（滚动年）', ytitle1='',
#                    title2=c+'\nTop10产品销售额增长率趋势（滚动年）', ytitle2='')
#     print(title_text + ' finished.')

# #各Class下PRODUCT剂型比例
#
# df['PRODUCT'] = df['PRODUCT'].str.split('\|', 1).str[0] + '|'+ df['MOLECULE'].str.split('\|', 1).str[0] + '\n' + df['CORPORATION'].str.split('\|', 1).str[0]
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
#     plot_bar(df2,'plots/Angina/'+title_text+'.png',width=14, height=7, title=title_text, ytitle='剂型占比', xtitle='')
#     print(c)

# # 各Class剂型比例
#
# df['PRODUCT'] = df['PRODUCT'].str.split('\|', 1).str[0] + '|' + df['MOLECULE'].str.split('\|', 1).str[0] + '\n' + \
#                 df['CORPORATION'].str.split('\|', 1).str[0]
#
# mask = (df['DATE'] > '2017-2-1') & (df['DATE'] <= '2018-2-1')
# df = df.loc[mask, :]
#
# df1 = get_trend_data(df=df, index='CLASS', period='MAT', return_type='SHARE')
# df1 = df1.T.sort_values('2018-02-01 ', ascending=False).head(10).T
# table = pd.pivot_table(df, index='FORM_CN', columns='CLASS', values='VALUE', aggfunc=np.sum).transform(
#     lambda x: x / x.sum())
# df2 = table.loc[:, df1.columns].T
# title_text = '抗心绞痛（症状）定义市场各品类剂型分布'
# plot_bar(df2, 'plots/Angina/' + title_text + '.png', width=14, height=7, title=title_text, ytitle='剂型占比',
#          xtitle='')


# 各Class本地/MNC比例

df['PRODUCT'] = df['PRODUCT'].str.split('\|', 1).str[0] + '|' + df['MOLECULE'].str.split('\|', 1).str[0] + '\n' + \
                df['CORPORATION'].str.split('\|', 1).str[0]

mask = (df['DATE'] > '2017-2-1') & (df['DATE'] <= '2018-2-1')
df = df.loc[mask, :]

df1 = get_trend_data(df=df, index='CLASS', period='MAT', return_type='SHARE')
df1 = df1.T.sort_values('2018-02-01 ', ascending=False).head(10).T
table = pd.pivot_table(df, index='MANUF_TYPE', columns='CLASS', values='VALUE', aggfunc=np.sum).transform(
    lambda x: x / x.sum())
df2 = table.loc[:, df1.columns].T
title_text = '抗心绞痛（症状）定义市场各品类原研仿制比例'
plot_bar(df2, 'plots/Angina/' + title_text + '.png', width=14, height=7, title=title_text, ytitle='原研/仿制占比',
         xtitle='')