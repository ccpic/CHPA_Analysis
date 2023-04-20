from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

D_RENAME = {
    "A10H SULPHONYLUREA A-DIABS|磺脲类降糖药(A10B1)":"磺脲类",
    "A10J BIGUANIDE ANTIDIABETICS|双胍类降糖药":"二甲双胍",
    'A10L A-GLUCOSIDASE INH A-DIAB|α-葡糖苷酶抑制剂(A10B5)':"α糖苷酶抑制剂",
    'A10M GLINIDE ANTIDIABETICS|格列奈类降糖药':"格列奈类",
    'A10K GLITAZONE ANTIDIABETICS|格列酮类降糖药':"TZD & PPAR全激动剂",
    'A10N DPP-IV INHIBITOR A-DIABS|DPP-IV（二肽基肽酶IV）抑制剂': "DPP4",
    'A10S GLP-1 AGONIST A-DIABS|GLP-1激动剂(胰高血糖素样肽-1激动剂类降糖药)(A10B9)': "GLP-1",
    'A10P SGLT2 INHIBITOR A-DIABS|钠-葡萄糖协同转运蛋白2抑制剂': "SGLT2",
}

condition_niad = "[TC III] in ('A10H SULPHONYLUREA A-DIABS|磺脲类降糖药(A10B1)', \
    'A10J BIGUANIDE ANTIDIABETICS|双胍类降糖药', \
    'A10L A-GLUCOSIDASE INH A-DIAB|α-葡糖苷酶抑制剂(A10B5)', \
    'A10M GLINIDE ANTIDIABETICS|格列奈类降糖药', \
    'A10K GLITAZONE ANTIDIABETICS|格列酮类降糖药', \
    'A10N DPP-IV INHIBITOR A-DIABS|DPP-IV（二肽基肽酶IV）抑制剂', \
    'A10S GLP-1 AGONIST A-DIABS|GLP-1激动剂(胰高血糖素样肽-1激动剂类降糖药)(A10B9)', \
    'A10P SGLT2 INHIBITOR A-DIABS|钠-葡萄糖协同转运蛋白2抑制剂')"

condition_oad = "[TC III] in ('A10H SULPHONYLUREA A-DIABS|磺脲类降糖药(A10B1)', \
    'A10J BIGUANIDE ANTIDIABETICS|双胍类降糖药', \
    'A10L A-GLUCOSIDASE INH A-DIAB|α-葡糖苷酶抑制剂(A10B5)', \
    'A10M GLINIDE ANTIDIABETICS|格列奈类降糖药', \
    'A10K GLITAZONE ANTIDIABETICS|格列酮类降糖药', \
    'A10N DPP-IV INHIBITOR A-DIABS|DPP-IV（二肽基肽酶IV）抑制剂', \
    'A10P SGLT2 INHIBITOR A-DIABS|钠-葡萄糖协同转运蛋白2抑制剂')"
    
sql = "SELECT * FROM " + table_name + " WHERE " + condition_niad
df = pd.read_sql(sql=sql, con=engine)
df.to_excel("test.xlsx")

df_index = pd.read_excel("非胰岛素降糖药PTD计算系数.xlsx", engine="openpyxl")
print(df_index)

# 折算标准片数
mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "PTD"
df = pd.concat([df, df_std_volume])

for index, value in df_index.iterrows():
    mask = (df["PACKAGE"] == value[6]) & (df["UNIT"] == "PTD")
    df.loc[mask, "AMOUNT"] = df.loc[mask, "AMOUNT"] / value[8]


df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
df["TC III"] = df["TC III"].map(D_RENAME)



r = chpa(df, name="NIAD(非胰岛素降糖药)市场")
# r = chpa(df, name="口服降糖药市场")

r.plot_overall_performance(dimension="TC III")
r.plot_overall_performance(dimension="TC III", unit="PTD")