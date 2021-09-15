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

df = pd.read_csv('data_2017.csv', delimiter='\t', encoding='utf-8')
df = df[df.TC_III != 'V03B 汉方药和中药|KANPO & CHINESE MEDICINES']

# #TC I 气泡图
# df_local = df[df.MANUF_TYPE == 'L']
# # mask = (df['DATE'] > '2017-2-1') & (df['DATE'] <= '2018-2-1')
# # df_mnc = df[(df.MANUF_TYPE == 'I')|(df.MANUF_TYPE == 'J')]
# x = get_trend_data(df=df, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:]/100000000
# y = get_trend_data(df=df_local, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:]/\
#     get_trend_data(df=df, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:]
#
# # y = get_trend_data(df=df, index='TC_I', period='MAT', return_type='GR').loc['2017-12-01',:]
# xy = pd.concat([x, y], axis=1)
# xy.columns = ['Sales', 'GR']
# # xy = xy[xy.Sales.between(30, 400, inclusive=True)]
# xy.sort_values(by='GR', ascending=False, inplace=True)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(xy)
# z = list(map(lambda i: i*5, xy.Sales))
# labels = xy.Sales.index.tolist()
# labels = [re.split('\|', label)[0] for label in labels]
# avggr = get_trend_data(df=df_local, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:].sum()/\
#     get_trend_data(df=df, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:].sum()
# print(avggr)
# title_text = 'TC I 国产品牌销售额比例'
# plot_bubble_m(x=xy.Sales, y=xy.GR, z=z,avggr=avggr,width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#               title=title_text, xtitle='2017销售额（亿元）', ytitle='国产品牌销售额比例', xfmt='{:,.0f}', yfmt='{:.0%}',
# ylabel='市场平均\n国产品牌\n销售额占比')

# #TC II 气泡图
# df_local = df[df.MANUF_TYPE == 'L']
# # mask = (df['DATE'] > '2017-2-1') & (df['DATE'] <= '2018-2-1')
# # df_mnc = df[(df.MANUF_TYPE == 'I')|(df.MANUF_TYPE == 'J')]
# x = get_trend_data(df=df, index='TC_II', period='MAT', return_type='ABS').loc['2017-12-01',:]/100000000
# y = get_trend_data(df=df_local, index='TC_II', period='MAT', return_type='ABS').loc['2017-12-01',:]/\
#     get_trend_data(df=df, index='TC_II', period='MAT', return_type='ABS').loc['2017-12-01',:]
#
# # y = get_trend_data(df=df, index='TC_I', period='MAT', return_type='GR').loc['2017-12-01',:]
# xy = pd.concat([x, y], axis=1)
# xy.columns = ['Sales', 'GR']
# xy = xy[xy.Sales.between(30, 400, inclusive=True)]
# xy.sort_values(by='GR', ascending=False, inplace=True)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(xy)
# z = list(map(lambda i: i*5, xy.Sales))
# labels = xy.Sales.index.tolist()
# labels = [re.split('\|', label)[0] for label in labels]
# avggr = get_trend_data(df=df_local, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:].sum()/\
#     get_trend_data(df=df, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:].sum()
# print(avggr)
# title_text = 'Top TC II 国产品牌销售额比例'
# plot_bubble_m(x=xy.Sales, y=xy.GR, z=z,avggr=avggr,width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#               title=title_text, xtitle='2017销售额（亿元）', ytitle='国产品牌销售额比例', xfmt='{:,.0f}', yfmt='{:.0%}',
#               ylabel='市场平均\n国产品牌\n销售额占比', label_fontsize=10)

# #TC III 气泡图
# df_local = df[df.MANUF_TYPE == 'L']
# # mask = (df['DATE'] > '2017-2-1') & (df['DATE'] <= '2018-2-1')
# # df_mnc = df[(df.MANUF_TYPE == 'I')|(df.MANUF_TYPE == 'J')]
# x = get_trend_data(df=df, index='TC_III', period='MAT', return_type='ABS').loc['2017-12-01',:]/100000000
# y = get_trend_data(df=df_local, index='TC_III', period='MAT', return_type='ABS').loc['2017-12-01',:]/\
#     get_trend_data(df=df, index='TC_III', period='MAT', return_type='ABS').loc['2017-12-01',:]
#
# # y = get_trend_data(df=df, index='TC_I', period='MAT', return_type='GR').loc['2017-12-01',:]
# xy = pd.concat([x, y], axis=1)
# xy.columns = ['Sales', 'GR']
# xy = xy[xy.Sales.between(30, 400, inclusive=True)]
# xy.sort_values(by='GR', ascending=False, inplace=True)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(xy)
# z = list(map(lambda i: i*5, xy.Sales))
# labels = xy.Sales.index.tolist()
# labels = [re.split('\|', label)[0] for label in labels]
# avggr = get_trend_data(df=df_local, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:].sum()/\
#     get_trend_data(df=df, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:].sum()
# print(avggr)
# title_text = 'Top TC III 国产品牌销售额比例'
# plot_bubble_m(x=xy.Sales, y=xy.GR, z=z,avggr=avggr,width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#               title=title_text, xtitle='2017销售额（亿元）', ytitle='国产品牌销售额比例', xfmt='{:,.0f}', yfmt='{:.0%}',
#               ylabel='市场平均\n国产品牌\n销售额占比', label_fontsize=10)

# #TC IV 气泡图
# df_local = df[df.MANUF_TYPE == 'L']
# # mask = (df['DATE'] > '2017-2-1') & (df['DATE'] <= '2018-2-1')
# # df_mnc = df[(df.MANUF_TYPE == 'I')|(df.MANUF_TYPE == 'J')]
# x = get_trend_data(df=df, index='TC_IV', period='MAT', return_type='ABS').loc['2017-12-01',:]/100000000
# y = get_trend_data(df=df_local, index='TC_IV', period='MAT', return_type='ABS').loc['2017-12-01',:]/\
#     get_trend_data(df=df, index='TC_IV', period='MAT', return_type='ABS').loc['2017-12-01',:]
#
# # y = get_trend_data(df=df, index='TC_I', period='MAT', return_type='GR').loc['2017-12-01',:]
# xy = pd.concat([x, y], axis=1)
# xy.columns = ['Sales', 'GR']
# xy = xy[xy.Sales.between(30, 400, inclusive=True)]
# xy.sort_values(by='GR', ascending=False, inplace=True)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(xy)
# z = list(map(lambda i: i*5, xy.Sales))
# labels = xy.Sales.index.tolist()
# labels = [re.split('\|', label)[0] for label in labels]
# avggr = get_trend_data(df=df_local, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:].sum()/\
#     get_trend_data(df=df, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:].sum()
# print(avggr)
# title_text = 'Top TC IV 国产品牌销售额比例'
# plot_bubble_m(x=xy.Sales, y=xy.GR, z=z,avggr=avggr,width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#               title=title_text, xtitle='2017销售额（亿元）', ytitle='国产品牌销售额比例', xfmt='{:,.0f}', yfmt='{:.0%}',
#               ylabel='市场平均\n国产品牌\n销售额占比', label_fontsize=10)

#MOLECULE 气泡图
l = [[30, 100], [20, 30], [15, 20], [10, 15], [7, 10], [5, 7], [3, 5]]
df['MOLECULE'] = df['MOLECULE'].str.split('\|', 1).str[0] + '(' + df['TC_IV'].str[0:4] + ')'
df_local = df[df.MANUF_TYPE == 'L']
for i in l:
    # mask = (df['DATE'] > '2017-2-1') & (df['DATE'] <= '2018-2-1')
    # df_mnc = df[(df.MANUF_TYPE == 'I')|(df.MANUF_TYPE == 'J')]
    x = get_trend_data(df=df, index='MOLECULE', period='MAT', return_type='ABS').loc['2017-12-01',:]/100000000
    y = get_trend_data(df=df_local, index='MOLECULE', period='MAT', return_type='ABS').loc['2017-12-01',:]/\
        get_trend_data(df=df, index='MOLECULE', period='MAT', return_type='ABS').loc['2017-12-01',:]

    # y = get_trend_data(df=df, index='TC_I', period='MAT', return_type='GR').loc['2017-12-01',:]
    xy = pd.concat([x, y], axis=1)
    xy.columns = ['Sales', 'GR']
    xy = xy[xy.Sales.between(i[0], i[1], inclusive=True)]
    xy.sort_values(by='GR', ascending=False, inplace=True)
    xy.fillna(0, inplace=True)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(xy)
    z = list(map(lambda i: i*5, xy.Sales))
    labels = xy.Sales.index.tolist()
    labels = [re.split('\|', label)[0] for label in labels]
    avggr = get_trend_data(df=df_local, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:].sum()/\
        get_trend_data(df=df, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:].sum()
    print(avggr)
    title_text = '通用名（'+str(i[0])+'亿-'+str(i[1])+'亿）国产品牌销售额比例'
    plot_bubble_m(x=xy.Sales, y=xy.GR, z=z,avggr=avggr,width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
                  title=title_text, xtitle='2017销售额（亿元）', ytitle='国产品牌销售额比例', xfmt='{:,.0f}', yfmt='{:.0%}',
                  ylabel='市场平均\n国产品牌\n销售额占比', label_fontsize=10)