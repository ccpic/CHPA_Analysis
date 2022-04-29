from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

condition = "[TC III] in ('C08A CALCIUM ANTAGONISTS PLAIN|钙离子拮抗剂，单一用药') AND FORMULATION in ('ORAL SOLID ORDINARY', 'ORAL SOLID LONG-ACTING') AND MOLECULE not in ('地尔硫卓|DILTIAZEM','维拉帕米|VERAPAMIL')"
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
mask = df["MOLECULE"] == "硝苯地平(II)"
df.loc[mask, "MOLECULE"] = "硝苯地平"

vbp_list = ["氨氯地平"]
mask = df["MOLECULE"].isin(vbp_list)
df.loc[mask, "VBP"] = "带量品种"
mask = df["MOLECULE"].isin(vbp_list) == False
df.loc[mask, "VBP"] = "非带量品种"

show_list = ["氨氯地平", "左旋氨氯地平", "硝苯地平", "非洛地平", "贝尼地平"]
mask = df["MOLECULE"].isin(show_list) == False
df.loc[mask, "MOLECULE"] = "其他品种"

mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])

convert_std_volume(df, "MOLECULE", "硝苯地平", "20MG", 0.5)
convert_std_volume(df, "MOLECULE", "硝苯地平", "10MG", 1 / 3)
convert_std_volume(df, "MOLECULE", "硝苯地平", "60MG", 2)
convert_std_volume(df, "MOLECULE", "氨氯地平", "10MG", 2)
convert_std_volume(df, "MOLECULE", "氨氯地平", "2.5MG", 0.5)
convert_std_volume(df, "MOLECULE", "乐卡地平", "20MG", 2)
convert_std_volume(df, "MOLECULE", "非洛地平", "2.5MG", 0.5)
convert_std_volume(df, "MOLECULE", "非洛地平", "10MG", 2)
convert_std_volume(df, "MOLECULE", "左旋氨氯地平", "5MG", 2)
convert_std_volume(df, "MOLECULE", "贝尼地平", "4MG", 0.5)
convert_std_volume(df, "MOLECULE", "贝尼地平", "2MG", 0.25)

r = chpa(df, name="二氢吡啶类CCB市场")
r.plot_overall_performance(dimension="MOLECULE")
r.plot_overall_performance(
    dimension="MOLECULE",
    unit="Volume (Std Counting Unit)",
)