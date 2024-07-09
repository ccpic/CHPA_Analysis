from CHPA2 import CHPA, extract_strength
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

D_RENAME = {
    "A10H SULPHONYLUREA A-DIABS|磺脲类降糖药(A10B1)": "磺脲类",
    "A10J BIGUANIDE ANTIDIABETICS|双胍类降糖药": "二甲双胍",
    "A10L A-GLUCOSIDASE INH A-DIAB|α-葡糖苷酶抑制剂(A10B5)": "α糖苷酶抑制剂",
    "A10M GLINIDE ANTIDIABETICS|格列奈类降糖药": "格列奈类",
    "A10K GLITAZONE ANTIDIABETICS|格列酮类降糖药": "TZD & PPAR全激动剂",
    "A10N DPP-IV INHIBITOR A-DIABS|DPP-IV（二肽基肽酶IV）抑制剂": "DPP4",
    "A10S GLP-1 AGONIST A-DIABS|GLP-1激动剂(胰高血糖素样肽-1激动剂类降糖药)(A10B9)": "GLP-1",
    "A10P SGLT2 INHIBITOR A-DIABS|钠-葡萄糖协同转运蛋白2抑制剂": "SGLT2",
    "A10X OTHER DRUGS FOR DIABETES|用于糖尿病的其他药物": "GKA",
}

D_CLASS = {
    "A10H SULPHONYLUREA A-DIABS|磺脲类降糖药(A10B1)": "口服降糖药",
    "A10D ANIMAL INSULINS|动物胰岛素": "胰岛素",
    "A10J BIGUANIDE ANTIDIABETICS|双胍类降糖药": "口服降糖药",
    "A10C HUMAN INSULIN+ANALOGUES|人胰岛素和类似物": "胰岛素",
    "A10L A-GLUCOSIDASE INH A-DIAB|α-葡糖苷酶抑制剂(A10B5)": "口服降糖药",
    "A10M GLINIDE ANTIDIABETICS|格列奈类降糖药": "口服降糖药",
    "A10K GLITAZONE ANTIDIABETICS|格列酮类降糖药": "口服降糖药",
    "A10X OTHER DRUGS FOR DIABETES|用于糖尿病的其他药物": "口服降糖药",
    "A10N DPP-IV INHIBITOR A-DIABS|DPP-IV（二肽基肽酶IV）抑制剂": "口服降糖药",
    "A10S GLP-1 AGONIST A-DIABS|GLP-1激动剂(胰高血糖素样肽-1激动剂类降糖药)(A10B9)": "GLP-1",
    "A10P SGLT2 INHIBITOR A-DIABS|钠-葡萄糖协同转运蛋白2抑制剂": "口服降糖药",
    "A10E INSULIN DEVICES|胰岛素设备": "胰岛素",
}

condition_all = "[TC II] in ('A10 DRUGS USED IN DIABETES|糖尿病用药')"

condition_niad = "[TC III] in ('A10H SULPHONYLUREA A-DIABS|磺脲类降糖药(A10B1)', \
    'A10J BIGUANIDE ANTIDIABETICS|双胍类降糖药', \
    'A10L A-GLUCOSIDASE INH A-DIAB|α-葡糖苷酶抑制剂(A10B5)', \
    'A10M GLINIDE ANTIDIABETICS|格列奈类降糖药', \
    'A10K GLITAZONE ANTIDIABETICS|格列酮类降糖药', \
    'A10N DPP-IV INHIBITOR A-DIABS|DPP-IV（二肽基肽酶IV）抑制剂', \
    'A10S GLP-1 AGONIST A-DIABS|GLP-1激动剂(胰高血糖素样肽-1激动剂类降糖药)(A10B9)', \
    'A10P SGLT2 INHIBITOR A-DIABS|钠-葡萄糖协同转运蛋白2抑制剂') or MOLECULE='DORZAGLIATIN|多格列艾汀'"

condition_oad = "[TC III] in ('A10H SULPHONYLUREA A-DIABS|磺脲类降糖药(A10B1)', \
    'A10J BIGUANIDE ANTIDIABETICS|双胍类降糖药', \
    'A10L A-GLUCOSIDASE INH A-DIAB|α-葡糖苷酶抑制剂(A10B5)', \
    'A10M GLINIDE ANTIDIABETICS|格列奈类降糖药', \
    'A10K GLITAZONE ANTIDIABETICS|格列酮类降糖药', \
    'A10N DPP-IV INHIBITOR A-DIABS|DPP-IV（二肽基肽酶IV）抑制剂', \
    'A10P SGLT2 INHIBITOR A-DIABS|钠-葡萄糖协同转运蛋白2抑制剂') or MOLECULE='DORZAGLIATIN|多格列艾汀'"

sql = "SELECT * FROM " + table_name + " WHERE " + condition_all
df = pd.read_sql(sql=sql, con=engine)
df = df[~df["TC III"].isin(["A10E INSULIN DEVICES|胰岛素设备"])]
df = df[
    ~df["MOLECULE"].isin(
        [
            "EPALRESTAT|依帕司他",
            "THIOCTIC ACID|硫辛酸",
            "ACETYL-L-CARNITINE|乙酰左旋肉碱",
        ]
    )
]

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
df["CLASS"] = df["TC III"].map(D_CLASS)
df["TC III"] = df["TC III"].map(D_RENAME)
df["STRENGTH"] = df["PACKAGE"].apply(extract_strength)

# 折算标准片数
mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "PTD"
df = pd.concat([df, df_std_volume])

df_index = pd.read_excel("降糖药PTD系数.xlsx", engine="openpyxl", sheet_name="匹配表")
df_index.drop_duplicates(subset="PACKAGE", inplace=True)

for index, value in df_index.iterrows():
    mask = (df["PACKAGE"] == value["PACKAGE"]) & (df["UNIT"] == "PTD")
    df.loc[mask, "AMOUNT"] = df.loc[mask, "AMOUNT"] / value["一天吃几片"]

df2 = df[~df["TC III"].isin(["GLP-1"])]
r = CHPA(df2, name="口服降糖药+胰岛素市场", date_column="DATE", period_interval=3)
r.plot_overall_performance_dual(index="CLASS", unit_change="亿", width=15, height=6)

r.plot_size_diff(index="MOLECULE", unit="Value", unit_change="百万", hue="CLASS", label_limit=25)
r.plot_size_diff(
    index="MOLECULE", unit="PTD", unit_change="百万", hue="CLASS", label_limit=25
)
# r.plottable_latest(index="PRODUCT", unit="Value", hue="CORPORATION")


# df3 = df[df["CLASS"] == "胰岛素"]
# r = CHPA(df3, name="胰岛素", date_column="DATE", period_interval=3)
# r.plot_share_trend(index="PRODUCT")
# r.plot_share_trend(index="MOLECULE", unit="Value", width=8, height=7)
# r.plot_share_trend(index="PACKAGE", unit="Value", width=8, height=7)
