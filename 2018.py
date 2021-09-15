from CHPA import *

start = time.clock()


engine = create_engine('mssql+pymssql://(local)/CHPA_1806')
sql = "SELECT * FROM data where unit='Value' and period = 'MAT' and " \
      "[TC III] <> 'V03B KANPO & CHINESE MEDICINES|汉方药和中药' and [TC I] <> 'Z PROMOTIONAL|保健品'"
df = pd.read_sql(sql=sql, con=engine)
# df['MOLECULE'] = df['MOLECULE'].str.split('|').str[0]
# df = pd.pivot_table(data=df, index='MOLECULE', columns='DATE', values='AMOUNT', aggfunc=np.sum)
df_mpn = pd.pivot_table(data=df, index= 'MOLECULE', values='PRODUCT_CORP', aggfunc=pd.Series.nunique)
df_mpn.columns = ['NOP']
df = pd.merge(df, df_mpn, left_on='MOLECULE', right_index=True)
mask = (df['NOP'] == 1) & (df['MANUF_TYPE'].isin(['IMPORT', 'JOINT_VENTURE']))
df = df.loc[mask]
# df = pd.pivot_table(data=df, index='MOLECULE', values='AMOUNT', aggfunc=np.sum)
# df.sort_values('AMOUNT', axis=0, ascending=False, inplace=True)
# df =df[df['AMOUNT'] > 100000000]
print(df)
df.to_csv('df.csv', encoding='utf_8_sig', index=False)
print(time.clock()-start)