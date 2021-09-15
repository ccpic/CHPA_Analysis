import pyodbc as pyodbc
import pandas as pd
import numpy as np


def get_trend_data(df, index, period, return_type, unit='VALUE', filter=None, filter_target=None, target_list=None, incl_others=True):

    #筛选数据
    if filter != None and filter_target != None:
        df = df[df[filter] == filter_target]

    
    df['TC_II'] = df['TC_II'].astype('category')
    df['TC_III'] = df['TC_III'].astype('category')
    df['TC_IV'] = df['TC_IV'].astype('category')
    df['MOLECULE'] = df['MOLECULE'].astype('category')
    df['DATE'] = df['DATE'].astype('category')
    df['PRODUCT'] = df['PRODUCT'].astype('category')
    df['PACKAGE'] = df['PACKAGE'].astype('category')
    df['CORPORATION'] = df['CORPORATION'].astype('category')
    df['MANUF_TYPE'] = df['MANUF_TYPE'].astype('category')
    df['FORMULATION'] = df['FORMULATION'].astype('category')

    #生成数据透视表
    table = pd.pivot_table(df, values=unit, index=index, columns='DATE', aggfunc=np.sum)

    #填充缺失值为0
    table.dropna(axis=0, how='all', inplace=True)
    # if fillna:
    #     table.fillna(0, inplace=True)
    #根据时间段设置rolling数据，rolling后会产生最初的几个月份为新的缺失值，需要重新截取数据
    rolling = 0
    if period != 'MON':
        if period == 'MAT':
            rolling = 12
        elif period == 'MQT':
            rolling = 3

        #Rolling
        for i in range(0, len(table.index)):
            table.iloc[i] = table.iloc[i].rolling(window=rolling, min_periods=1).sum()

        #Rolling后截取数据
        if len(table.columns)>rolling:
            table = table.iloc[:, rolling:]

    #根据返回类型的不同微调数据
    if return_type == 'ABS':
        table = table
    elif return_type == 'SHARE':
        table = table.transform(lambda x: x/x.sum())
    elif return_type == 'GR':
        table = table.pct_change(axis=1, periods=12)#增长率计算会造成最初月份变成缺失值，需要重新截取数据
        if len(table.columns)> 12:
            table = table.iloc[:, 12:]
            # table.fillna('', inplace=True)

    #Index和Columns改为字符串类，跟一些绘图函数更兼容
    table.columns = table.columns.astype('str')
    table.index = table.index.astype('str')

    #只提取targetlist里的核心目标还是包括others
    if target_list != None:
        if incl_others == False:
            table = table.reindex(target_list)
        if incl_others == True:
            table1 = table.reindex(target_list)
            table1.loc['Others'] = table.sum()-table1.sum()
            table = table1

    #剔除可能由于计算增长率产生的新的NA
    # table.dropna(axis=0, how='all', inplace=True)

    #转置
    table = table.transpose()
    table.index = pd.to_datetime(table.index)

    return table


def generate_df():

    CONN_MSSQL = pyodbc.connect('DRIVER={SQL Server};SERVER=AMIDNOJQ-PC;Database=CHPA;Trusted_Connection=yes;')


    SQL_FULL = 'Select Left(Dim_Pack.[Therapeutic_Code],1) + \' \' + TC_I_CN.namec + \'|\' + RTRIM(TC_I.Therapeutic_Name) As TC_I, ' \
          'Left(Dim_Pack.[Therapeutic_Code],3) + \' \' + TC_II_CN.namec + \'|\' + RTRIM(TC_II.Therapeutic_Name) As TC_II, ' \
          'Left(Dim_Pack.[Therapeutic_Code],4) + \' \' + TC_III_CN.namec + \'|\' + RTRIM(TC_III.Therapeutic_Name) As TC_III, ' \
          'Dim_Pack.[Therapeutic_Code] + \' \' + TC_IV_CN.namec + \'|\' + RTRIM(TC_IV.Therapeutic_Name) As TC_IV, ' \
          'RTRIM(PROD_CN.namec)+ \'|\' + RTRIM(Product_Name) + REPLICATE(\' \',19-LEN(Product_Name)) + Manufacturer_Abbr AS PRODUCT, ' \
          'RTRIM(PROD_CN.namec)+ \'|\' + RTRIM(Product_Name) + \' \'+ Pack_Description AS PACKAGE, ' \
          'RTRIM(PROD_CN.gene_name)+ \'|\' + s.Molecule_Name as MOLECULE, ' \
          'RTRIM(MANU_CN.namec)+ \'|\' + RTRIM(Manufacturer_Name) as CORPORATION, ManufacturerType_Code as MANUF_TYPE, ' \
          'NewFormClass_Name as FORMULATION, ' \
          'Amount_IC as VALUE, Quantity_ST as CNT_UNIT, Quantity_UN as UNIT, ' \
          'Year as YEAR, period as MONTH, ' \
          'CAST(CAST(year AS VARCHAR(4)) + RIGHT(\'0\' + CAST(period AS VARCHAR(2)), 2) + \'01\' AS DATETIME) as DATE, ' \
          'CAST(CAST(LEFT(Dim_Pack.LaunchTime, 4) AS VARCHAR(4)) + CAST(RIGHT(Dim_Pack.LaunchTime, 2) AS VARCHAR(2)) + \'01\' AS DATETIME) as LAUNCHDATE ' \
          'FROM ((((((((((((((Dim_Pack INNER JOIN Dim_Product ON Dim_Pack.Product_ID = Dim_Product.Product_ID) INNER JOIN ' \
          'Dim_Manufacturer ON Dim_Product.Manufacturer_ID = Dim_Manufacturer.Manufacturer_ID) '\
          'INNER JOIN Dim_New_Form_Class ON Dim_Pack.NewFormClass_ID = Dim_New_Form_Class.NewFormClass_ID) INNER JOIN ' \
          'Fact_Sales ON Dim_Pack.Pack_ID = Fact_Sales.Pack_ID) INNER JOIN ' \
          'TC_I ON Left(Dim_Pack.[Therapeutic_Code],1) = TC_I.[Therapeutic_Code]) INNER JOIN ' \
          'TC_II ON Left(Dim_Pack.[Therapeutic_Code],3) = TC_II.[Therapeutic_Code]) INNER JOIN ' \
          'TC_III ON Left(Dim_Pack.[Therapeutic_Code],4) = TC_III.[Therapeutic_Code]) INNER JOIN ' \
          'TC_IV ON Dim_Pack.[Therapeutic_Code] = TC_IV.[Therapeutic_Code]) INNER JOIN ' \
          'PROD_CN ON PROD_CN.prodcode = Dim_Product.Product_Code) INNER JOIN ' \
          'MANU_CN ON MANU_CN.abbrev = Dim_Manufacturer.Manufacturer_Abbr) INNER JOIN ' \
          'TC_I_CN on TC_I.[Therapeutic_Code] = TC_I_CN.TC_CODE) INNER JOIN ' \
          'TC_II_CN on TC_II.[Therapeutic_Code] = TC_II_CN.TC_CODE) INNER JOIN ' \
          'TC_III_CN on TC_III.[Therapeutic_Code] = TC_III_CN.TC_CODE) INNER JOIN ' \
          'TC_IV_CN on TC_IV.[Therapeutic_Code] = TC_IV_CN.TC_CODE) INNER JOIN ' \
          '(SELECT Product_ID, Molecule_Name = STUFF((SELECT DISTINCT \',\' + RTRIM(cast(Molecule_Name as varchar)) ' \
          'FROM Dim_Product_Molecule b WHERE b.Product_ID = a.Product_ID FOR XML PATH(\'\')), 1, 1, \'\') ' \
          'FROM Dim_Product_Molecule a GROUP BY Product_ID) s ON Dim_Pack.Product_ID=s.Product_ID '


    df = pd.DataFrame()
    for chunk in pd.read_sql(sql=SQL_FULL, con=CONN_MSSQL, chunksize=2000000):  # 分chunk导入，提高效率
        df = df.append(chunk)
        print(1)
    CONN_MSSQL.close()

    return df

if __name__ == '__main__':
    df = generate_df()
    mask = (df.TC_II == 'C07 β受体阻断剂|BETA BLOCKING AGENTS')|(df.TC_II == 'C08 钙离子拮抗剂|CALCIUM ANTAGONISTS')|(df.TC_III == 'C01E 亚硝酸盐和硝酸盐|NITRITES & NITRATES')|(df.TC_III == 'C01D 冠脉治疗，钙离子拮抗剂和亚硝酸盐除外|CORONARY THERAPY')
    df = df.loc[mask,:]
    df.to_csv('data_angina.csv', sep='\t', encoding='utf-8')