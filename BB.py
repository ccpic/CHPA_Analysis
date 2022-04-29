from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

condition = "[TC III] in ('C07A BETA BLOCKING AGENT PLN|β受体阻断剂，单用') AND FORMULATION in ('ORAL SOLID ORDINARY', 'ORAL SOLID LONG-ACTING')"
sql = "SELECT * FROM " + table_name + " WHERE " + condition
df = pd.read_sql(sql=sql, con=engine)

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[0]
df["PRODUCT"] = (
    (df["PRODUCT"].str.split("|").str[0])
    + "（"
    + df["PRODUCT"].str.split("|").str[1].str[-3:]
    + "）"
)
df["PRODUCT_CORP"] = (
    df["PRODUCT_CORP"].str.split("（").str[0].str.split("|").str[0]
    + "\n"
    + df["PRODUCT_CORP"].str.split("（").str[1].str.split("|").str[0]
)

mask = ((df["MOLECULE"] == "美托洛尔") & (df["PRODUCT"] != "倍他乐克ZOK（AZN）"))
df.loc[mask, "MOLECULE"] = "美托洛尔常释剂型"
mask = df["PRODUCT"] == "倍他乐克ZOK（AZN）"
df.loc[mask, "MOLECULE"] = "美托洛尔缓释剂型"

vbp_list = ["美托洛尔常释剂型", "比索洛尔"]
mask = df["MOLECULE"].isin(vbp_list)
df.loc[mask, "VBP"] = "带量品种"
mask = df["MOLECULE"].isin(vbp_list) == False
df.loc[mask, "VBP"] = "非带量品种"

show_list = ["美托洛尔常释剂型", "美托洛尔缓释剂型", "阿罗洛尔", "比索洛尔"]
mask = df["MOLECULE"].isin(show_list) == False
df.loc[mask, "MOLECULE"] = "其他品种"

mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])

convert_std_volume(df, "MOLECULE", "美托洛尔常释剂型", "25MG", 0.5)
convert_std_volume(df, "MOLECULE", "美托洛尔常释剂型", "100MG", 2)
convert_std_volume(df, "MOLECULE", "美托洛尔缓释剂型", "100MG", 2)
convert_std_volume(df, "MOLECULE", "比索洛尔", "100MG", 0.5)

r = chpa(df, name="β受体阻滞剂市场")
r.plot_overall_performance(dimension="VBP")
r.plot_overall_performance(
    dimension="VBP",
    unit="Volume (Std Counting Unit)",
)