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

x = get_trend_data(df=df, index='PRODUCT', period='MAT', return_type='ABS').loc['2017-12-01',:]/100000000
x.to_csv('data_product.csv', sep='\t', encoding='utf-8')


#TC I 气泡图
# x = get_trend_data(df=df, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:]/100000000
# y = get_trend_data(df=df, index='TC_I', period='MAT', return_type='GR').loc['2017-12-01',:]
# xy = pd.concat([x, y], axis=1)
# xy.columns = ['Sales', 'GR']
# # xy = xy[xy.Sales.between(30, 400, inclusive=True)]
# xy.sort_values(by='GR', ascending=False, inplace=True)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(xy)
# z = list(map(lambda i: i*5, xy.Sales))
# labels = xy.Sales.index.tolist()
# labels = [re.split('\|', label)[0] for label in labels]
# avggr = get_trend_data(df=df, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:].sum()/\
#         get_trend_data(df=df, index='TC_I', period='MAT', return_type='ABS').loc['2016-12-01',:].sum() - 1
# title_text = 'TC I 2017表现'
# plot_bubble_m(x=xy.Sales, y=xy.GR, z=z,avggr=avggr,width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#               title=title_text, xtitle='2017销售额（亿元）', ytitle='同比增长率', xfmt='{:,.0f}', ymin=-0.05, ymax=0.2)

#TC II气泡图
# x = get_trend_data(df=df, index='TC_II', period='MAT', return_type='ABS').loc['2017-12-01',:]/100000000
# y = get_trend_data(df=df, index='TC_II', period='MAT', return_type='GR').loc['2017-12-01',:]
# xy = pd.concat([x, y], axis=1)
# xy.columns = ['Sales', 'GR']
# xy = xy[xy.Sales.between(30, 400, inclusive=True)]
# xy.sort_values(by='GR', ascending=False, inplace=True)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(xy)
# z = list(map(lambda i: i*5, xy.Sales))
# labels = xy.Sales.index.tolist()
# labels = [re.split('\|', label)[0] for label in labels]
# avggr = get_trend_data(df=df, index='TC_II', period='MAT', return_type='ABS').loc['2017-12-01',:].sum()/\
#         get_trend_data(df=df, index='TC_II', period='MAT', return_type='ABS').loc['2016-12-01',:].sum() - 1
# title_text = 'Top TC II 2017表现'
# plot_bubble_m(x=xy.Sales, y=xy.GR, z=z,avggr=avggr,width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#               title=title_text, xtitle='2017销售额（亿元）', ytitle='同比增长率', xfmt='{:,.0f}', label_fontsize=10)

#TC III气泡图
# x = get_trend_data(df=df, index='TC_III', period='MAT', return_type='ABS').loc['2017-12-01',:]/100000000
# y = get_trend_data(df=df, index='TC_III', period='MAT', return_type='GR').loc['2017-12-01',:]
# xy = pd.concat([x, y], axis=1)
# xy.columns = ['Sales', 'GR']
# xy = xy[xy.Sales.between(30, 400, inclusive=True)]
# xy.sort_values(by='GR', ascending=False, inplace=True)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(xy)
# z = list(map(lambda i: i*5, xy.Sales))
# labels = xy.Sales.index.tolist()
# labels = [re.split('\|', label)[0] for label in labels]
# avggr = get_trend_data(df=df, index='TC_III', period='MAT', return_type='ABS').loc['2017-12-01',:].sum()/\
#         get_trend_data(df=df, index='TC_III', period='MAT', return_type='ABS').loc['2016-12-01',:].sum() - 1
# title_text = 'Top TC III 2017表现'
# plot_bubble_m(x=xy.Sales, y=xy.GR, z=z,avggr=avggr,width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#               title=title_text, xtitle='2017销售额（亿元）', ytitle='同比增长率', xfmt='{:,.0f}', label_fontsize=10)


# #TC IV气泡图
# x = get_trend_data(df=df, index='TC_IV', period='MAT', return_type='ABS').loc['2017-12-01',:]/100000000
# y = get_trend_data(df=df, index='TC_IV', period='MAT', return_type='GR').loc['2017-12-01',:]
# xy = pd.concat([x, y], axis=1)
# xy.columns = ['Sales', 'GR']
# xy = xy[xy.Sales.between(30, 400, inclusive=True)]
# xy.sort_values(by='GR', ascending=False, inplace=True)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(xy)
# z = list(map(lambda i: i*5, xy.Sales))
# labels = xy.Sales.index.tolist()
# labels = [re.split('\|', label)[0] for label in labels]
# avggr = get_trend_data(df=df, index='TC_IV', period='MAT', return_type='ABS').loc['2017-12-01',:].sum()/\
#         get_trend_data(df=df, index='TC_IV', period='MAT', return_type='ABS').loc['2016-12-01',:].sum() - 1
# title_text = 'Top TC IV 2017表现'
# plot_bubble_m(x=xy.Sales, y=xy.GR, z=z,avggr=avggr,width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#               title=title_text, xtitle='2017销售额（亿元）', ytitle='同比增长率', xfmt='{:,.0f}', label_fontsize=10)

# #MOLECULE气泡图
# df['MOLECULE'] = df['MOLECULE'].str.split('\|', 1).str[0]+'('+df['TC_IV'].str[0:4]+')'
# x = get_trend_data(df=df, index='MOLECULE', period='MAT', return_type='ABS').loc['2017-12-01',:]/100000000
# y = get_trend_data(df=df, index='MOLECULE', period='MAT', return_type='GR').loc['2017-12-01',:]
# xy = pd.concat([x, y], axis=1)
# xy.columns = ['Sales', 'GR']
# xy = xy[xy.Sales.between(2, 3, inclusive=True)]
# xy.sort_values(by='GR', ascending=False, inplace=True)
# xy = refine_outlier(xy, 'GR', 0.75)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(xy)
# z = list(map(lambda i: i*5, xy.Sales))
# labels = xy.Sales.index.tolist()
# labels = [re.split('\|', label)[0] for label in labels]
# avggr = get_trend_data(df=df, index='MOLECULE', period='MAT', return_type='ABS').loc['2017-12-01',:].sum()/\
#         get_trend_data(df=df, index='MOLECULE', period='MAT', return_type='ABS').loc['2016-12-01',:].sum() - 1
# title_text = '化合物2017表现 （年销售额2-3亿）'
# plot_bubble_m(x=xy.Sales, y=xy.GR, z=z,avggr=avggr,width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#               title=title_text, xtitle='2017销售额（亿元）', ytitle='同比增长率', xfmt='{:,.1f}', label_fontsize=9)

#净增长和增速气泡图
# df['MOLECULE'] = df['MOLECULE'].str.split('\|', 1).str[0]+'('+df['TC_IV'].str[0:4]+')'
# x = get_trend_data(df=df, index='MOLECULE', period='MAT', return_type='ABS').loc['2017-12-01',:]/100000000 - get_trend_data(df=df, index='MOLECULE', period='MAT', return_type='ABS').loc['2016-12-01',:]/100000000
# y = get_trend_data(df=df, index='MOLECULE', period='MAT', return_type='GR').loc['2017-12-01',:]
# xy = pd.concat([x, y], axis=1)
# xy.columns = ['Uplift', 'GR']
# xy = xy[xy.Uplift.between(0.5,100, inclusive=True)]
# xy = xy[xy.GR.between(0.5,500, inclusive=True)]
# xy.sort_values(by='Uplift', ascending=False, inplace=True)
# xy = refine_outlier(xy, 'GR', 2)
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(xy)
# z = xy.Uplift/xy.GR*100
# labels = xy.Uplift.index.tolist()
# labels = [re.split('\|', label)[0] for label in labels]
# title_text = '优质表现化合物 （2017年净增长大于5000万且增速大于50%）'
# plot_bubble_m(x=xy.Uplift, y=xy.GR, z=z, width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#               title=title_text, xtitle='2017年净增长（亿元）', ytitle='同比增长率', xfmt='{:,.1f}', label_fontsize=8)


# #根据通用名下产品数分析
# #气泡图
# df['MOLECULE'] = df['MOLECULE'].str.split('\|', 1).str[0] + '(' + df['TC_IV'].str[0:4] + ')'
# product_n = pd.pivot_table(df, values='PRODUCT', index='MOLECULE', columns='DATE',
#                            aggfunc=lambda x: len(x.dropna().unique())).iloc[:, -14:-2].max(axis=1)
# x = get_trend_data(df=df, index='MOLECULE', period='MAT', return_type='ABS').loc['2017-12-01', :] / 100000000
# y = get_trend_data(df=df, index='MOLECULE', period='MAT', return_type='GR').loc['2017-12-01', :]
# df = pd.concat([x, y, product_n], axis=1)
# df.columns = ['Sales', 'GR', 'Product_n']
# df = df[df.Sales.between(5, 10, inclusive=True)]
# for n in range(3):
#     xy = df[df.Product_n.between(n+1, n+1, inclusive=True)]
#     xy.sort_values(by='GR', ascending=False, inplace=True)
#     xy = refine_outlier(xy, 'GR', 1)
#     z = list(map(lambda i: i*100, xy.Sales))
#     labels = xy.Sales.index.tolist()
#     labels = [re.split('\|', label)[0] for label in labels]
#     title_text = '化合物2017表现 （年销售额5-10亿&通用名下产品数='+str(n+1)+'）'
#     plot_bubble_m(x=xy.Sales, y=xy.GR, z=z, width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#                   title=title_text, xtitle='2017年销售额（亿元）', ytitle='同比增长率', xfmt='{:,.1f}', label_fontsize=10)
#     print(title_text)

#气泡图-通用名下商品名n-净增长
# df['MOLECULE'] = df['MOLECULE'].str.split('\|', 1).str[0]+'('+df['TC_IV'].str[0:4]+')'
# product_n = pd.pivot_table(df, values='PRODUCT', index='MOLECULE', columns='DATE',
#                            aggfunc=lambda x: len(x.dropna().unique())).iloc[:, -14:-2].max(axis=1)
# x = get_trend_data(df=df, index='MOLECULE', period='MAT', return_type='ABS').loc['2017-12-01',:]/100000000 - get_trend_data(df=df, index='MOLECULE', period='MAT', return_type='ABS').loc['2016-12-01',:]/100000000
# y = get_trend_data(df=df, index='MOLECULE', period='MAT', return_type='GR').loc['2017-12-01',:]
# df = pd.concat([x, y, product_n], axis=1)
# df.columns = ['Uplift', 'GR', 'Product_n']
# df = df[df.Uplift.between(1, 100, inclusive=True)]
# for n in range(3):
#     xy = df[df.Product_n.between(n+1, n+1, inclusive=True)]
#     xy.sort_values(by='Uplift', ascending=False, inplace=True)
#     xy = refine_outlier(xy, 'GR', 1)
#     z = list(map(lambda i: i*500, xy.Uplift))
#     labels = xy.Uplift.index.tolist()
#     labels = [re.split('\|', label)[0] for label in labels]
#     title_text = '优质表现化合物 （2017年净增长1亿以上&通用名下产品数='+str(n+1)+'）'
#     plot_bubble_m(x=xy.Uplift, y=xy.GR, z=z, width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#                   title=title_text, xtitle='2017年净增长（亿元）', ytitle='同比增长率', xfmt='{:,.1f}', label_fontsize=10)
#     print(title_text)



# #通用名下商品名数分布饼图
# df['MOLECULE'] = df['MOLECULE'].str.split('\|', 1).str[0]+'('+df['TC_IV'].str[0:4]+')'
# df = df[df.TC_III != 'V03B 汉方药和中药|KANPO & CHINESE MEDICINES']
# dff = df.loc[:,['MOLECULE', 'TC_I']]
# molecule_tc = dff.drop_duplicates()
# molecule_tc.set_index(keys='MOLECULE', inplace=True)
# product_n = pd.pivot_table(df, values='PRODUCT', index='MOLECULE', columns='DATE',
#                            aggfunc=lambda x: len(x.dropna().unique())).iloc[:, -14:-2].max(axis=1)
# xy = pd.concat([molecule_tc, product_n], axis=1)
# xy.columns = ['TC_I', 'Product_n']
# xy.dropna(how='any', inplace=True)
# avg = xy.Product_n.mean()
# table = pd.pivot_table(xy, values='TC_I', index='Product_n', aggfunc='count')
# flattened = pd.DataFrame(table.to_records())
# flattened.columns = ['Product_n', 'Cases']
# sum20 = flattened[flattened.Product_n.between(20, 200, inclusive=True)].Cases.sum()
# sum10 = flattened[flattened.Product_n.between(10, 19, inclusive=True)].Cases.sum()
# flattened = flattened[flattened.Product_n < 10]
# flattened.Product_n = flattened.Product_n.apply(lambda x: 'n='+str(int(x)))
# flattened.loc[len(flattened)] = ['n=10-19', sum10]
# flattened.loc[len(flattened)] = ['n=20+', sum20]
#
# title_text = '2017中国处方药市场\n通用名下商品名数\n不包含中药\n(平均n='+'{:,.1f}'.format(avg)+')'
# plot_pie(flattened.Cases, flattened.Product_n, savefile='plots/2017中国处方药市场通用名下商品名数（不包含中药）.png', title=title_text)


# #TC I 气泡图-通用名下商品名数
# df['MOLECULE'] = df['MOLECULE'].str.split('\|', 1).str[0]+'('+df['TC_IV'].str[0:4]+')'
# dff = df.loc[:,['MOLECULE', 'TC_I']]
# molecule_tc = dff.drop_duplicates()
# molecule_tc.set_index(keys='MOLECULE', inplace=True)
# product_n = pd.pivot_table(df, values='PRODUCT', index='MOLECULE', columns='DATE',
#                            aggfunc=lambda x: len(x.dropna().unique())).iloc[:, -14:-2].max(axis=1)
# xy = pd.concat([molecule_tc, product_n], axis=1)
# xy.columns = ['TC_I', 'Product_n']
# xy.dropna(how='any', inplace=True)
# avg = xy.Product_n.mean()
# table = pd.pivot_table(xy, values='Product_n', index='TC_I', aggfunc=np.mean)
# flattened = pd.DataFrame(table.to_records())
# flattened.columns = ['TC_I', 'Product_n']
# flattened.set_index(keys='TC_I', inplace=True)
# x = get_trend_data(df=df, index='TC_I', period='MAT', return_type='ABS').loc['2017-12-01',:]/100000000
# xy = pd.concat([x, flattened.Product_n], axis=1)
# xy.columns = ['Sales', 'Product_n']
# xy.sort_values(by='Product_n', ascending=False, inplace=True)
# z = list(map(lambda i: i*5, xy.Sales))
# labels = xy.Sales.index.tolist()
# labels = [re.split('\|', label)[0] for label in labels]
# title_text = 'TC I 2017通用名下产品名数'
# print(xy)
# plot_bubble_m(x=xy.Sales, y=xy.Product_n, z=z,avggr=avg,width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#               title=title_text, xtitle='2017销售额（亿元）', ytitle='该TC通用名下平均商品数', xfmt='{:,.0f}', yfmt='{:.1f}')


# #TC IV 气泡图-通用名下商品名数
# df['MOLECULE'] = df['MOLECULE'].str.split('\|', 1).str[0]+'('+df['TC_IV'].str[0:4]+')'
# df['TC_IV'] = df['TC_IV'].str.split('\|', 1).str[0]
# dff = df.loc[:,['MOLECULE', 'TC_IV']]
# molecule_tc = dff.drop_duplicates()
# molecule_tc.set_index(keys='MOLECULE', inplace=True)
# product_n = pd.pivot_table(df, values='PRODUCT', index='MOLECULE', columns='DATE',
#                            aggfunc=lambda x: len(x.dropna().unique())).iloc[:, -14:-2].max(axis=1)
# product_n = product_n.to_frame()
# xy = molecule_tc.merge(product_n, left_index=True, right_index=True, how='left')
# xy.columns = ['TC_IV', 'Product_n']
# xy.dropna(how='any', inplace=True)
# avg = xy.Product_n.mean()
# table = pd.pivot_table(xy, values='Product_n', index='TC_IV', aggfunc=np.mean)
# flattened = pd.DataFrame(table.to_records())
# flattened.columns = ['TC_IV', 'Product_n']
# flattened.set_index(keys='TC_IV', inplace=True)
# x = get_trend_data(df=df, index='TC_IV', period='MAT', return_type='ABS').loc['2017-12-01',:]/100000000
# xy = pd.concat([x, flattened.Product_n], axis=1)
# xy.columns = ['Sales', 'Product_n']
# xy = xy[xy.Sales.between(30, 400, inclusive=True)]
# xy = refine_outlier(xy, 'Product_n', 10)
# xy.sort_values(by='Product_n', ascending=True, inplace=True)
# z = list(map(lambda i: i*5, xy.Sales))
# labels = xy.Sales.index.tolist()
# labels = [re.split('\|', label)[0] for label in labels]
# title_text = 'Top TC IV 2017通用名下产品名数'
# print(xy)
# plot_bubble_m(x=xy.Sales, y=xy.Product_n, z=z,avggr=avg,width=15,height=9, labels=labels, savefile='plots/'+title_text+'.png',
#               title=title_text, xtitle='2017销售额（亿元）', ytitle='该TC通用名下平均商品数', ylabel = '市场平均\nn=',
#               xfmt='{:,.0f}', yfmt='{:.1f}',label_fontsize=10)



#通用名下商品名数和销售份额的关系
# df = df[df.TC_I == 'B 血液和血液形成器官|BLOOD + B.FORMING ORGANS']
# df = df[df.LAUNCHDATE != '1900-01-01']
# df['MOLECULE'] = df['MOLECULE'].str.split('\|', 1).str[0]+'('+df['TC_IV'].str[0:4]+')'
# mask_date = (df['DATE'] > '2016-12-01') & (df['DATE'] <= '2017-12-01')
# df = df.loc[mask_date]
# # mask_launchdate = (df['LAUNCHDATE'] > '2012-12-01') & (df['LAUNCHDATE'] <= '2017-12-01')
# # df =df.loc[mask_launchdate]
# product_n = pd.pivot_table(df, values='PRODUCT', index='MOLECULE', aggfunc=lambda x: len(x.dropna().unique()))
# df['Product_n'] = df.MOLECULE.map(product_n.PRODUCT)
# print(df)
# summary = pd.DataFrame()
# for i in range(10):
#     dist = pd.DataFrame()
#     molecule_list = df[df.Product_n == i+1].MOLECULE.unique().tolist()
#     print(len(molecule_list)/len(product_n.PRODUCT))
#     for molecule in molecule_list:
#         table = pd.pivot_table(df[df.MOLECULE==molecule], values='VALUE', index= ['MOLECULE', 'PRODUCT'], aggfunc=np.sum, dropna=True).transform(lambda x: x/x.sum())
#         table.sort_values(by='VALUE',ascending=False, inplace=True)
#         flattened = pd.DataFrame(table.to_records())
#         for j in range(i+1):
#             if j >=1:
#                 dist.loc[len(dist) -1, j] = flattened.iloc[j, -1]
#             else:
#                 dist.loc[len(dist), j] = flattened.iloc[j, -1]
#
#     for j in range(i+1):
#         try:
#             summary.loc[j, i + 1] = dist.iloc[:,j].mean()
#         except:
#             summary.loc[j, i + 1] = np.NaN
#             pass
#         continue
#
#
# summary.index = ['第一大产品', '第二大产品', '第三大产品', '第四大产品', '第五大产品',
#                  '第六大产品', '第七大产品', '第八大产品', '第九大产品', '第十大产品']
# summary.columns = ['n='+str(x+1) for x in range(10)]
# title_text = '通用名下不同商品数的销售分布(B 血液和血液形成器官)'
# plot_stackbar(df=summary.T, savefile='plots/'+title_text+'.png', title=title_text, width=7.5, height=4.5,
#                 xtitle='通用名下商品数n', ytitle='2017销售额份额')


#新品分析 - 2017上市
# df['MOLECULE'] = df['MOLECULE'].str.split('\|', 1).str[0]+'('+df['TC_IV'].str[0:4]+')'
# molecule_sales = pd.pivot_table(df, values='VALUE', index='MOLECULE',columns='DATE', aggfunc=np.sum)
#
# molecule_mthsales_2017 = molecule_sales.iloc[:,-14:-2]
# molecule_sales_2017 = molecule_sales.iloc[:,-14:-2].sum(axis=1).to_frame()
# molecule_sales_2017.columns = ['2017']
#
# molecule_sales_before = molecule_sales.iloc[:,:-14].sum(axis=1).to_frame()
# molecule_sales_before.columns = ['Before2017']
#
# df['TC_I'] = df['TC_I'].str.split('\|', 1).str[0]
# dff = df.loc[:,['MOLECULE', 'TC_I']]
# molecule_tc = dff.drop_duplicates()
# molecule_tc.set_index(keys='MOLECULE', inplace=True)
# molecule_tc.columns = ['TC_I']
#
# molecule_sales_merged = molecule_sales_before.merge(molecule_sales_2017, left_index=True, right_index=True, how='left')
# molecule_sales_merged = molecule_sales_merged.merge(molecule_tc, left_index=True, right_index=True, how='left')
# molecule_sales_merged = molecule_sales_merged.merge(molecule_mthsales_2017, left_index=True, right_index=True, how='left')
# new_molecule_sales = molecule_sales_merged[(molecule_sales_merged['Before2017'] == 0) & (molecule_sales_merged['2017'] > 0)]
# top_new = new_molecule_sales.iloc[:,3:].sort_values(by='2017-12-01', ascending=False).head(12)
#
# title_text = '2017新产品 Top表现'
#
# plot_line_simple(df=top_new.T, savefile='plots/'+title_text+'.png', yfmt= '{:,.0f}', xlabelrotation=90,
#                  title=title_text, ytitle='单月销售额(元)')


# tc_count = pd.pivot_table(new_molecule_sales, index='TC_I', values='2017', aggfunc='count')
# tc_count.columns = ['产品数量']
# title_text = 'IMS CHPA 2017新上市或再上市产品各TC数量'
# plot_bar(tc_count,savefile='plots/'+title_text+'.png', width=9, height=5, stacked=False , title= title_text, haslegend=False,
#          xtitle='' ,ytitle='2017新上市或再上市产品数量#', yfmt='{:.0f}', labelfmt='{:.0f}')


# #新品分析 - 2016上市
# df['MOLECULE'] = df['MOLECULE'].str.split('\|', 1).str[0]+'('+df['TC_IV'].str[0:4]+')'
# molecule_sales = pd.pivot_table(df, values='VALUE', index='MOLECULE',columns='DATE', aggfunc=np.sum)
#
# molecule_mthsales_1617 = molecule_sales.iloc[:,-26:-2]
# molecule_sales_1617 = molecule_sales.iloc[:,-26:-2].sum(axis=1).to_frame()
# molecule_sales_1617.columns = ['1617']
#
# molecule_sales_before = molecule_sales.iloc[:,:-26].sum(axis=1).to_frame()
# molecule_sales_before.columns = ['Before2016']
#
# df['TC_I'] = df['TC_I'].str.split('\|', 1).str[0]
# dff = df.loc[:,['MOLECULE', 'TC_I']]
# molecule_tc = dff.drop_duplicates()
# molecule_tc.set_index(keys='MOLECULE', inplace=True)
# molecule_tc.columns = ['TC_I']
#
# molecule_sales_merged = molecule_sales_before.merge(molecule_sales_1617, left_index=True, right_index=True, how='left')
# molecule_sales_merged = molecule_sales_merged.merge(molecule_tc, left_index=True, right_index=True, how='left')
# molecule_sales_merged = molecule_sales_merged.merge(molecule_mthsales_1617, left_index=True, right_index=True, how='left')
# new_molecule_sales = molecule_sales_merged[(molecule_sales_merged['Before2016'] == 0) & (molecule_sales_merged['1617'] > 0)]
# top_new = new_molecule_sales.iloc[:,3:].sort_values(by='2017-12-01', ascending=False)
#
# print(top_new)

# title_text = '2017新产品 Top表现'
#
# plot_line_simple(df=top_new.T, savefile='plots/'+title_text+'.png', yfmt= '{:,.0f}', xlabelrotation=90,
#                  title=title_text, ytitle='单月销售额(元)')


# tc_count = pd.pivot_table(new_molecule_sales, index='TC_I', values='2017', aggfunc='count')
# tc_count.columns = ['产品数量']
# title_text = 'IMS CHPA 2017新上市或再上市产品各TC数量'
# plot_bar(tc_count,savefile='plots/'+title_text+'.png', width=9, height=5, stacked=False , title= title_text, haslegend=False,
#          xtitle='' ,ytitle='2017新上市或再上市产品数量#', yfmt='{:.0f}', labelfmt='{:.0f}')

elapsed = (time.clock() - start)
print('Time used:', elapsed)