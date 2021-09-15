from CHPA import *

engine = create_engine('mssql+pymssql://(local)/CHPA_1806')
table_name = 'data'
condition = "'培哚普利,吲达帕胺|INDAPAMIDE+PERINDOPRIL', " \
            "'雷沙吉兰|RASAGILINE', " \
            "'戈利木单抗|GOLIMUMAB', " \
            "'托珠单抗|TOCILIZUMAB', " \
            ""
sql = "SELECT * FROM " + table_name + " WHERE MOLECULE in (" + condition + ")"
df = pd.read_sql(sql=sql, con=engine)

df['MOLECULE'] = df['MOLECULE'].str.split('|').str[0]
df['PRODUCT'] = df['PRODUCT'].str.split('|').str[0] + '（'+ df['PRODUCT'].str.split('|').str[1].str[-3:] +'）'
df['PRODUCT_CORP'] = df['PRODUCT_CORP'].str.split('（').str[0].str.split('|').str[0] + '\n' + \
                       df['PRODUCT_CORP'].str.split('（').str[1].str.split('|').str[0]

r = chpa(df, name='19医保新纳入品种（非谈判）')
r.plot_group_size_diff(index='MOLECULE', date=[r.latest_date()], dimension=None,
                      column=None, adjust_scale=0.01, series_limit=250, showLabel=True, labelLimit=5)